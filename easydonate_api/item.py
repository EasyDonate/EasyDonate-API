from .APICore import cached_property, api

class Item(object):
	def __init__(self, itemid):
		self._id = itemid
		
	@cached_property(ttl=3600)
	def _summary(self):
		return api().call('IItems', 'GetItemSummaries', items=self._id)['items'][0]
		
	@property
	def duration(self):
		return self._summary['duration']
	
	@cached_property(ttl=3600)
	def group(self):
		return ItemGroup(self._summary['group'])
		
	@property
	def name(self):
		return self._summary['name']
		
	@property
	def shortdesc(self):
		return self._summary['shortdesc']
		
	@property
	def arguments(self):
		return self._summary['arguments']
		
	@property
	def price(self):
		return self._summary['price']
		
	@property
	def description(self):
		return self._summary['description']
		
	@property
	def id(self):
		return self._id
		
class ItemGroup(object):
	def __init__(self, groupid):
		self._id = groupid
		
	@cached_property(ttl=3600)
	def _summary(self):
		return api().call('IItems', 'GetGroupSummaries', groups=self._id)['groups'][0]
		
	@property
	def fields(self):
		return self._summary['fields']
		
	@property
	def id(self):
		return self._id
		
	@property
	def name(self):
		return self._summary['name']