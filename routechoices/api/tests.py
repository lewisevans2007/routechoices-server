import time

import arrow
from django.conf import settings
from django.contrib.auth.models import User
from django_hosts.resolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, override_settings

from routechoices.core.models import Club, Device, Event


class EssentialApiBase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def reverse_and_check(self, path, expected):
        url = reverse(path, host="api")
        self.assertEqual(url, "//api.localhost:8000" + expected)
        return url

    def get_device_id(self):
        d = Device.objects.create()
        return d.aid


@override_settings(PARENT_HOST="localhost:8000")
class EssentialApiTestCase1(EssentialApiBase):
    def test_api_root(self):
        url = self.reverse_and_check("api_doc", "/")
        res = self.client.get(url, SERVER_NAME="api.localhost:8000")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_time(self):
        url = self.reverse_and_check("time_api", "/time")
        t1 = time.time()
        res = self.client.get(url, SERVER_NAME="api.localhost:8000")
        t2 = time.time()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(t1 < res.data.get("time") < t2)

    def test_get_device_id(self):
        url = self.reverse_and_check("device_id_api", "/device_id")
        res = self.client.post(url, SERVER_NAME="api.localhost:8000")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data.get("device_id")) == 8)
        self.assertTrue(res.data.get("device_id") != self.get_device_id())


@override_settings(PARENT_HOST="localhost:8000")
class ImeiApiTestCase(EssentialApiBase):
    def test_get_imei_no_data(self):
        url = self.reverse_and_check("device_imei_api", "/imei")
        res = self.client.post(url, SERVER_NAME="api.localhost:8000")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_imei_invalid(self):
        url = self.reverse_and_check("device_imei_api", "/imei")
        res = self.client.post(url, {"imei": "abcd"}, SERVER_NAME="api.localhost:8000")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_imei_valid(self):
        url = self.reverse_and_check("device_imei_api", "/imei")
        res = self.client.post(
            url, {"imei": "123456789123458"}, SERVER_NAME="api.localhost:8000"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data.get("device_id")) == 8)
        self.assertTrue(res.data.get("device_id") != self.get_device_id())


@override_settings(PARENT_HOST="localhost:8000")
class LocationApiTestCase(EssentialApiBase):
    def test_locations_api_gw_valid(self):
        url = self.reverse_and_check("locations_api_gw", "/locations")
        dev_id = self.get_device_id()
        t = time.time()
        res = self.client.post(
            url,
            {
                "device_id": dev_id,
                "latitudes": "1.1,1.2",
                "longitudes": "3.1,3.2",
                "timestamps": f"{t},{t+1}",
                "secret": settings.POST_LOCATION_SECRETS[0],
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        nb_points = len(Device.objects.get(aid=dev_id).locations["timestamps"])
        self.assertEqual(nb_points, 2)

    def test_locations_api_gw_invalid(self):
        url = self.reverse_and_check("locations_api_gw", "/locations")
        dev_id = self.get_device_id()
        t = time.time()
        res = self.client.post(
            url,
            {
                "device_id": dev_id,
                "latitudes": "1.1,1.2",
                "longitudes": "3.1,",
                "timestamps": f"{t},{t+1}",
                "secret": settings.POST_LOCATION_SECRETS[0],
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_locations_api_gw_bad_secret(self):
        url = self.reverse_and_check("locations_api_gw", "/locations")
        dev_id = self.get_device_id()
        t = time.time()
        res = self.client.post(
            url,
            {
                "device_id": dev_id,
                "latitudes": "1.1,1.2",
                "longitudes": "3.1,3.2",
                "timestamps": f"{t},{t+1}",
                "secret": "bad secret",
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_locations_api_gw_old_dev_id_valid(self):
        url = self.reverse_and_check("locations_api_gw", "/locations")
        d = Device.objects.create(aid="abcd1234")
        dev_id = d.aid
        t = time.time()
        res = self.client.post(
            url,
            {
                "device_id": dev_id,
                "latitudes": "1.1,1.2",
                "longitudes": "3.1,3.2",
                "timestamps": f"{t},{t+1}",
                "secret": "bad secret",
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_locations_api_gw_old_no_device(self):
        url = self.reverse_and_check("locations_api_gw", "/locations")
        t = time.time()
        res = self.client.post(
            url,
            {
                "device_id": "doesnotexist",
                "latitudes": "1.1,1.2",
                "longitudes": "3.1,3.2",
                "timestamps": f"{t},{t+1}",
                "secret": "bad secret",
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(PARENT_HOST="localhost:8000")
class RegistrationApiTestCase(EssentialApiBase):
    def test_registration(self):
        device_id = self.get_device_id()
        user = User.objects.create_user("alice", "alice@example.com", "pa$$word123")
        club = Club.objects.create(name="Test club", slug="club")
        club.admins.set([user])
        event = Event.objects.create(
            club=club,
            name="Test event",
            open_registration=True,
            start_date=arrow.get().datetime,
            end_date=arrow.get().shift(hours=1).datetime,
        )
        url = reverse("event_register", host="api", kwargs={"event_id": event.aid})
        self.assertEqual(url, f"//api.localhost:8000/events/{event.aid}/register")
        res = self.client.post(
            url,
            {
                "device_id": device_id,
                "name": "Alice",
                "short_name": "🇺🇸 A",
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # name exists
        res = self.client.post(
            url,
            {
                "device_id": device_id,
                "name": "Alice",
                "short_name": "🇺🇸 AB",
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # short_name exists
        res = self.client.post(
            url,
            {
                "device_id": device_id,
                "name": "Albert",
                "short_name": "🇺🇸 A",
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # bad start_time
        res = self.client.post(
            url,
            {
                "device_id": device_id,
                "name": "Albert",
                "short_name": "🇺🇸 A",
                "start_time": arrow.get().shift(hours=-1).datetime,
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # invalid start_time
        res = self.client.post(
            url,
            {
                "device_id": device_id,
                "name": "Bob",
                "short_name": "🇺🇸 B",
                "start_time": "unreadable",
            },
            SERVER_NAME="api.localhost:8000",
        )
        # no name
        res = self.client.post(
            url,
            {
                "device_id": device_id,
                "name": "",
                "short_name": "🇺🇸 B",
            },
            SERVER_NAME="api.localhost:8000",
        )
        # no device
        res = self.client.post(
            url,
            {
                "device_id": "does not exists",
                "name": "",
                "short_name": "🇺🇸 B",
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # ok
        res = self.client.post(
            url,
            {
                "device_id": device_id,
                "name": "Bob",
                "short_name": "🇺🇸 B",
                "start_time": arrow.get().shift(minutes=+1).datetime,
            },
            SERVER_NAME="api.localhost:8000",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
