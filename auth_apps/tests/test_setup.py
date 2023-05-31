from rest_framework.test import APITestCase
from django.urls import reverse

from faker import Faker


class TestSetup(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse('base:auth_apps:register', args=())
        self.login_url = reverse('base:auth_apps:login', args=())

        self.fake = Faker()
        self.psw = self.fake.email().split('@')[0]

        self.user_data = {
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "firstname": self.fake.first_name(),
            "lastname": self.fake.last_name(),
            "password": self.psw,
            "confirm_psd": self.psw,
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
