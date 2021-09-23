from django_redis import get_redis_connection

conn = get_redis_connection()

# class CacheHandle():
#
#     def check_code(self, key, code):
#         value = conn.get(key).decode()
#         if value != code:
#             return False
#         return True

def check_code(key, code):
    value = conn.get(key).decode()
    if value != code:
        return False
    return True
