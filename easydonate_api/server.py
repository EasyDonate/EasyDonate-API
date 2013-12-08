from .APICore import cached_property, api
from .item import Item

class Server(object):
	def __init__(self, sid):
		self._sid = sid
	
	@cached_property(ttl=3600)
	def _summary(self):
		return api().call('IServers', 'GetServerSummaries', servers=self._sid)['servers'][0]
	
	@property
	def address(self):
		return self._summary['address']
		
	@property
	def id(self):
		return self._sid
		
	@property
	def name(self):
		return self._summary['name']
	
	@cached_property(ttl=600)
	def items(self):
		return [Item(item['itemid']) for item in api().call('IServers', 'GetServerItems', sid=self._sid)['items']]