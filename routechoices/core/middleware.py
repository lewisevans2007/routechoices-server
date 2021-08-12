''' XFF Middleware '''
import logging
from re import compile

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.urls import NoReverseMatch, set_urlconf, get_urlconf

from django_hosts.middleware import HostsBaseMiddleware

from routechoices.core.models import Club


XFF_EXEMPT_URLS = []
if hasattr(settings, 'XFF_EXEMPT_URLS'):
    XFF_EXEMPT_URLS = [compile(expr) for expr in settings.XFF_EXEMPT_URLS]

logger = logging.getLogger(__name__)


class XForwardedForMiddleware:
    '''
    Fix HTTP_REMOTE_ADDR header to show client IP in a proxied environment.
    WARNING: If you are going to trust the address, you need to know how
    many proxies you have in chain. Nothing stops a malicious client from
    sending one and your reverse proxies adding one.
    You can set the exact number of reverse proxies by adding the
    XFF_TRUSTED_PROXY_DEPTH setting. Without it, the header will remain
    insecure even with this middleware. Setting XFF_STRICT = True will
    cause a bad request to be sent on spoofed or wrongly routed requests.
    XFF_ALWAYS_PROXY will drop all requests with too little depth.
    XFF_NO_SPOOFING will drop connections with too many headers.
    This middleware will automatically clean the X-Forwarded-For header
    unless XFF_CLEAN = False is set.
    XFF_LOOSE_UNSAFE = True will simply shut up and set the last in the
    stack.
    XFF_EXEMPT_URLS can be an iterable (eg. list) that defines URLs as
    regexps that will not be checked. XFF_EXEMPT_STEALTH = True will
    return a 404 when all proxies are present. This is nice for a
    healtcheck URL that is not for the public eye.
    XFF_HEADER_REQUIRED = True will return a bad request when the header
    is not set. By default it takes the same value as XFF_ALWAYS_PROXY.
    '''
    def __init__(self, get_response=None):
        self.get_response = get_response

        self.depth = getattr(settings, 'XFF_TRUSTED_PROXY_DEPTH', 0)
        self.stealth = getattr(settings, 'XFF_EXEMPT_STEALTH', False)
        self.loose = getattr(settings, 'XFF_LOOSE_UNSAFE', False)
        self.strict = getattr(settings, 'XFF_STRICT', False)
        self.always_proxy = getattr(settings, 'XFF_ALWAYS_PROXY', False)
        self.no_spoofing = getattr(settings, 'XFF_NO_SPOOFING', False)
        self.header_required = getattr(settings, 'XFF_HEADER_REQUIRED',
                                       (self.always_proxy or self.strict))
        self.clean = getattr(settings, 'XFF_CLEAN', True)

    def __call__(self, request):
        response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        return response

    def process_request(self, request):
        '''
        The beef.
        '''
        path = request.path_info.lstrip('/')
        depth = self.depth
        exempt = any(m.match(path) for m in XFF_EXEMPT_URLS)

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            header = request.META['HTTP_X_FORWARDED_FOR']
            levels = [x.strip() for x in header.split(',')]

            if len(levels) >= depth and exempt and self.stealth:
                return HttpResponseNotFound()

            if self.loose or exempt:
                request.META['REMOTE_ADDR'] = levels[0]
                return None

            if len(levels) != depth and self.strict:
                logger.warning((
                    "Incorrect proxy depth in incoming request.\n" +
                    'Expected {} and got {} remote addresses in ' +
                    'X-Forwarded-For header.')
                    .format(
                        depth, len(levels)))
                return HttpResponseBadRequest()

            if len(levels) < depth or depth == 0:
                logger.warning(
                    'Not running behind as many reverse proxies as expected.' +
                    "\nThe right value for XFF_TRUSTED_PROXY_DEPTH for this " +
                    'request is {} and {} is configured.'.format(
                        len(levels), depth)
                )
                if self.always_proxy:
                    return HttpResponseBadRequest()

                depth = len(levels)
            elif len(levels) > depth:
                logger.info(
                    ('X-Forwarded-For spoof attempt with {} addresses when ' +
                     '{} expected. Full header: {}').format(
                         len(levels), depth, header))
                if self.no_spoofing:
                    return HttpResponseBadRequest()

            request.META['REMOTE_ADDR'] = levels[-1 * depth]

            if self.clean:
                cleaned = ','.join(levels[-1 * depth:])
                request.META['HTTP_X_FORWARDED_FOR'] = cleaned

        elif self.header_required and not (exempt or self.loose):
            logger.error(
                'No X-Forwarded-For header set, not behind a reverse proxy.')
            return HttpResponseBadRequest()

        return None



class HostsRequestMiddleware(HostsBaseMiddleware):
    def process_request(self, request):
        # Find best match, falling back to settings.DEFAULT_HOST
        default_domain = settings.PARENT_HOST
        if ':' in settings.PARENT_HOST:
            default_domain = settings.PARENT_HOST[:settings.PARENT_HOST.rfind(':')]
        raw_host = request.get_host()
        if ':' in raw_host:
            raw_host = raw_host[:raw_host.rfind(':')]
        request.use_cname = False
        if not raw_host.endswith(default_domain) and not raw_host in ('localhost', '127.0.0.1'):
            club = Club.objects.filter(domain=raw_host).first()
            if not club:
                return HttpResponse(status=204)
            raw_host = f'{club.slug.lower()}.{default_domain}'
            request.use_cname = True
        host, kwargs = self.get_host(raw_host)
        # This is the main part of this middleware
        request.urlconf = host.urlconf
        request.host = host
        # But we have to temporarily override the URLconf
        # already to allow correctly reversing host URLs in
        # the host callback, if needed.
        current_urlconf = get_urlconf()
        try:
            set_urlconf(host.urlconf)
            return host.callback(request, **kwargs)
        finally:
            # Reset URLconf for this thread on the way out for complete
            # isolation of request.urlconf
            set_urlconf(current_urlconf)


class HostsResponseMiddleware(HostsBaseMiddleware):
    def process_response(self, request, response):
        # Django resets the base urlconf when it starts to process
        # the response, so we need to set this again, in case
        # any of our middleware makes use of host, etc URLs.

        # Find best match, falling back to settings.DEFAULT_HOST
        default_domain = settings.PARENT_HOST
        if ':' in settings.PARENT_HOST:
            default_domain = settings.PARENT_HOST[:settings.PARENT_HOST.rfind(':')]
        raw_host = request.get_host()
        if ':' in raw_host:
            raw_host = raw_host[:raw_host.rfind(':')]
        if not raw_host.endswith(default_domain) and not raw_host in ('localhost', '127.0.0.1'):
            club = Club.objects.filter(domain=raw_host).first()
            if not club:
                return HttpResponse(status=204)
            raw_host = f'{club.slug.lower()}.{default_domain}'
            request.use_cname = True
        host, kwargs = self.get_host(raw_host)
        # This is the main part of this middleware
        request.urlconf = host.urlconf
        request.host = host

        set_urlconf(host.urlconf)
        return response