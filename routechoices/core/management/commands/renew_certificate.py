import os
import os.path
import subprocess
from typing import cast

import arrow
import sewer.client
from cryptography import x509
from django.conf import settings
from django.core.management.base import BaseCommand
from sewer.auth import ProviderBase
from sewer.crypto import AcmeAccount, AcmeKey

from routechoices.core.models import Club
from routechoices.lib.helpers import check_cname_record


def is_expirying(domain):
    cert_path = os.path.join(settings.BASE_DIR, "nginx", "certs", f"{domain}.crt")
    if not os.path.exists(cert_path):
        return True
    with open(cert_path, "rb") as fp:
        data = fp.read()
    cert = x509.load_pem_x509_certificate(data)
    return arrow.utcnow().shift(days=30) > arrow.get(cert.not_valid_after)


def read_account_key(cls, filename: str):
    with open(filename, "rb") as f:
        data = f.read()
    prefix = b""
    n = data.find(b"-----BEGIN")
    if 0 < n:
        prefix = data[:n]
        data = data[n:]
    acct = cast("AcmeAccount", cls.from_pem(data))
    if prefix:
        parts = prefix.split(b"\n")
        for p in parts:
            if p.startswith(b"KID: "):
                acct.__kid = p[5:].decode()
            elif p.startswith(b"Timestamp: "):
                acct._timestamp = float(p[11:])
    return acct


def write_account_key(self, filename):
    with open(filename, "wb") as f:
        if hasattr(self, "__kid") and self.__kid:
            f.write(f"KID: {self.__kid}\n".encode())
            if self._timestamp:
                f.write(f"Timestamp: {self._timestamp}\n".encode())
        f.write(self.to_pem())


class ClubProvider(ProviderBase):
    def __init__(self, club, **kwargs):
        kwargs["chal_types"] = ["http-01"]
        self.club = club
        super().__init__(**kwargs)
        self.chal_type = "http-01"

    def setup(self, challenges):
        self.club.acme_challenge = challenges[0]["key_auth"]
        self.club.save()
        return []

    def unpropagated(self, challenges):
        # could add confirmation here, but it's just a demo
        return []

    def clear(self, challenges):
        self.club.acme_challenge = ""
        self.club.save()
        return []


class Command(BaseCommand):
    help = "Renew letsencrypt certificate for club custom domain"

    def add_arguments(self, parser):
        parser.add_argument("domains", nargs="*", type=str)
        parser.add_argument("--post-hook", dest="post-hook", type=str, default=None)

    def handle(self, *args, **options):
        nginx_need_restart = False

        domains = options["domains"]

        if not domains:
            domains = Club.objects.exclude(domain="").values_list("domain", flat=True)

        for domain in domains:
            self.stdout.write(f"Processing {domain} ...")
            club = Club.objects.filter(domain=domain).first()
            if not club:
                self.stderr.write("No club with this domain")
                continue

            if not os.path.exists(
                os.path.join(settings.BASE_DIR, "nginx", "certs", f"{domain}.key")
            ):
                self.stderr.write(
                    "SSL not setup for this domain, no key/certificate found"
                )
                continue

            if not is_expirying(domain):
                self.stderr.write("Domain is not yet expiring")
                continue

            if not check_cname_record(domain):
                self.stderr.write("Domain is not pointing to routechoices.com anymore")
                club.domain = ""
                club.save()
                continue

            account_exists = os.path.exists(
                os.path.join(
                    settings.BASE_DIR, "nginx", "certs", "accounts", f"{domain}.key"
                )
            )
            if account_exists:
                acct_key = read_account_key(
                    AcmeAccount,
                    os.path.join(
                        settings.BASE_DIR, "nginx", "certs", "accounts", f"{domain}.key"
                    ),
                )
            else:
                acct_key = AcmeAccount.create("secp256r1")
                write_account_key(
                    acct_key,
                    os.path.join(
                        settings.BASE_DIR, "nginx", "certs", "accounts", f"{domain}.key"
                    ),
                )

            cert_key = AcmeKey.read_pem(
                os.path.join(settings.BASE_DIR, "nginx", "certs", f"{domain}.key")
            )

            client = sewer.client.Client(
                domain_name=domain,
                provider=ClubProvider(club),
                account=acct_key,
                cert_key=cert_key,
                is_new_acct=(not account_exists),
                contact_email="raphael@routechoices.com",
            )
            try:
                certificate = client.get_certificate()
            except Exception:
                self.stderr.write("Failed to create certificate...")
                continue
            cert_key = client.cert_key

            with open(
                os.path.join(settings.BASE_DIR, "nginx", "certs", f"{domain}.crt"),
                "w",
                encoding="utf_8",
            ) as fp:
                fp.write(certificate)
            cert_key.write_pem(
                os.path.join(settings.BASE_DIR, "nginx", "certs", f"{domain}.key")
            )
            nginx_need_restart = True
            self.stdout.write("Certificate renewed.")
        if nginx_need_restart:
            print("Reload nginx for changes to take effect...")
            if options["post-hook"]:
                subprocess.run(
                    options["post-hook"],
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    check=False,
                )
