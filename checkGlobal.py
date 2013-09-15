#endoding = utf-8

color_schema_list = {
	'high': ['Bold','default','red'],
	'normal': ['Bold','default','yellow'],
	'simple': ['Normal','default','yellow'],
	'done': ['Bold','Underline','black','white'],
	'enmergency': ['Bold','Blink','red','white'],
	'default': ['Normal','default','default'],
	'highlight':['Normal','default','red'],
	'daily':['Normal','default','green'],
	'none':[]
}

priority_schema = ['enmergency','highlight','high','done','daily','simple']

priority_emoji_map = {
	'enmergency':'\xF0\x9F\x94\xA5',
	'daily':'\xE2\x98\x95',
	'high':'\xF0\x9F\x94\x94',
	'normal': '\xF0\x9F\x95\x95',
	'simple': '\xF0\x9F\x92\x9B',
	'done': '\xF0\x9F\x9A\xA9',
	'highlight':'\xF0\x9F\x8C\x9F'
}
