import redis

r = redis.Redis(
    host='localhost',
    port=6379)

# This is to test your local connection works. 
# Should return 'bar' when you run this program.
# Your redis server must be running.

r.set('foo', 'bar')
value = r.get('foo')
print(value)
