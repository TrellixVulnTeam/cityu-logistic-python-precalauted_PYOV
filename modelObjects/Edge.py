class Edge:
	def __init__(self):
		self.v_id=0
		self.osm_id =''
		self.type =''
		self.oneway=''
		self.maxspeed=50
		self.o_lat=0
		self.o_lng=0
		self.d_lat=0
		self.d_lng=0
		self.o_node=None
		self.d_node=None
		self.length=''
		self.amap_length =0
		self.google_length =0
		self.static_duration =0
		self.name=""
		self.lengthRate=0.2



	def __repr__(self):

		s = "v_id : {} , osm_id : {} , type : {} , maxspeed : {}, length : {}, amap_length : {} , google_length : {} , static_duration : {}".format(self.v_id,self.osm_id,self.type,self.maxspeed,self.length,self.amap_length,self.google_length,self.static_duration)
		return s

		# return "{},{} | {},{} | length : {}".format(self.o_lat,self.o_lng,self.d_lat,self.d_lng, self.length)