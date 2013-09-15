#encoding = utf-8

"""
	change color of CLI
"""
import sys
class ColorCLI:
	def __init__(self):
		self.colortype = {
			'Bold' : '1',
			'Underline' : '4',
			'Blink' : '5',
			'Normal' : '0',
			'Nondisplay' : '8'
		}
		self.foreground = {
			'black' : 30,
			'red' : 31,
			'green' : 32,
			'yellow' : 33,
			'blue' : 34,
			'white' :37,
			'magenta' : 35,
			'cyan' : 36,
			'default' :39
		}
		self.background = {
			'black' : 40,
			'red' : 41,
			'green' : 42,
			'yellow' : 43,
			'blue' : 44,
			'white' :47,
			'magenta' : 45,
			'cyan' : 46,
			'default' :49
		}
		self.end = '\033[0m'
		self.start = '\033['

	def get_type(self,type):
		try:
			return self.colortype[type]
		except KeyError:
			return self.colortype['Normal']

	def get_fore_color(self,color):
		try:
			return self.foreground[color]
		except KeyError:
			return self.foreground['default']

	def get_back_color(self,color):
		try:
			return self.background[color]
		except KeyError:
			return self.background['default']


	def decorate_text(self,typelist,bkcolor,color,text):
		try:
			typecode = ";".join([self.get_type(v) for v in typelist])
			fore_colorcode = self.get_fore_color(color)
			back_colorcode = self.get_back_color(bkcolor)
			pretext = "%s%s;%d;%dm%s%s" % (self.start,typecode,back_colorcode,fore_colorcode,text,self.end)
			return pretext
		except:
			print sys.exc_info()
			return text

	def decorate_text_from_schema(self,schema_list,text):
		if len(schema_list) == 0:
			return text
		fore_color = schema_list[-1]
		bk_color = schema_list[-2]
		typelist = schema_list[0:-2]
		pretext = self.decorate_text(typelist,bk_color,fore_color,text)
		return pretext
	

