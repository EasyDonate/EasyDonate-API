from .APICore import api, cached_property
from .item import Item
from .server import Server

class Subscriber(object):
	def __init__(self, subid):
		self._id = subid
	
	@cached_property(ttl=3600)
	def _summary(self):
		return api().call('ISubscribers', 'GetSubscriberSummaries', subscribers=self._id)['subscribers'][0]
	
	@cached_property(ttl=3600)
	def server(self):
		return Server(self._summary['server'])
		
	@cached_property(ttl=3600)
	def item(self):
		return Item(self._summary['item'])
		
	@property
	def expires(self):
		return self._summary['expires']
		
	@property
	def steamid(self):
		return self._summary['steamid']
		
def lookup_subscriber(sid, steamid):
	return [Subscriber(sub[id]) for sub in api().call('ISubscribers', 'SubscriberLookup', steamid=steamid, sid=sid)['subscribers']]