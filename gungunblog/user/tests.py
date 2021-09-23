from django.test import TestCase

# Create your tests here.
from django_redis import get_redis_connection

conn = get_redis_connection()


class CacheTest(TestCase):

    def setUp(self):
        conn.set('1', '3', 300)

    def test_set_cache(self):
        print(conn.get('1'))


if __name__ == '__main__':
    test = CacheTest()
    test.test_set_cache()
