import requests, os, time

class APIConn(object):
	def __init__(self, base_url, api_key):
		self.base_url = base_url
		self.api_key = api_key
	
	def call(self, interface, method, **params):
		for k in params:
			if type(params[k]) is list:
				params[k] = ','.join(params[k])
			elif type(params[k]) is bool:
				params[k] = 1 if params[k] else 0
		params['key'] = self.api_key
		
		query = "{base_url}/api/{interface}/{method}".format(base_url=self.base_url, interface=interface, method=method)
		
		response = requests.get(query, params=params)
		if response.status_code == 403:
			raise APIKeyInvalidException()
		elif response.status_code == 400:
			raise APIRequestInvalidException()
		elif response.status_code == 404:
			raise APIRequestNotFoundException()
		elif response.status_code != 200:
			raise APIErrorException()
		return response.json()

class APIException(Exception):
	pass
		
class APIErrorException(APIException):
	pass

class APIKeyInvalidException(APIException):
	pass

class APIRequestInvalidException(APIException):
	pass
	
class APIRequestNotFoundException(APIException):
	pass

__api__ = None

def api():
	global __api__
	if not __api__:
		__api__ = APIConn(base_url=os.environ.get('ED_URL', None), api_key=os.environ.get('ED_KEY', None))
	return __api__
	
def configure(api_key, base_url):
	global __api__
	__api__ = APIConn(base_url=base_url, api_key=api_key)
	return __api__
	
class cached_property(object):
    '''Decorator for read-only properties evaluated only once within TTL period.

    It can be used to created a cached property like this::

        import random

        # the class containing the property must be a new-style class
        class MyClass(object):
            # create property whose value is cached for ten minutes
            @cached_property(ttl=600)
            def randint(self):
                # will only be evaluated every 10 min. at maximum.
                return random.randint(0, 100)

    The value is cached  in the '_cache' attribute of the object instance that
    has the property getter method wrapped by this decorator. The '_cache'
    attribute value is a dictionary which has a key for every property of the
    object which is wrapped by this decorator. Each entry in the cache is
    created only when the property is accessed for the first time and is a
    two-element tuple with the last computed property value and the last time
    it was updated in seconds since the epoch.

    The default time-to-live (TTL) is 300 seconds (5 minutes). Set the TTL to
    zero for the cached value to never expire.

    To expire a cached property value manually just do::

        del instance._cache[<property name>]

    '''
    def __init__(self, ttl=300):
        self.ttl = ttl

    def __call__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__
        return self

    def __get__(self, inst, owner):
        now = time.time()
        try:
            value, last_update = inst._cache[self.__name__]
            if self.ttl > 0 and now - last_update > self.ttl:
                raise AttributeError
        except (KeyError, AttributeError):
            value = self.fget(inst)
            try:
                cache = inst._cache
            except AttributeError:
                cache = inst._cache = {}
            cache[self.__name__] = (value, now)
        return value