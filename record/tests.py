from django.test import TestCase


# Create your tests here.
class TestRecord(TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_index(self):
        resp = self.client.get("")
        self.assertEqual(resp.status_code, 200)

    def test_add_record(self): ...
