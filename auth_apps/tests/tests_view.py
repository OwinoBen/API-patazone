from .test_setup import TestSetup


class TestViews(TestSetup):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.user_data, format='json')
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.data['error'], False)
        self.assertEqual(res.status_code, 200)

    def test_user_login(self):
        self.client.post(self.register_url, self.user_data, format='json')
        res = self.client.post(self.login_url, self.user_data, format='json')

        self.assertEqual(res.status_code, 200)
