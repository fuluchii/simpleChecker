#encoding = utf-8

from colorcli import ColorCLI
from checkGlobal import color_schema_list

class Response:
	def __init__(self,text_priority_list):
		self.colorcli = ColorCLI()
		self.response_text_list = []
		for t_p in text_priority_list:
			t = t_p[0]
			p = t_p[1]
			self.response_text_list.append(self.decorate_response(t, p))

	def decorate_response(self,text,priority):
		color_schema = color_schema_list[priority]
		return self.colorcli.decorate_text_from_schema(color_schema,text)


