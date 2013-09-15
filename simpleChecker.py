#encoding = utf-8
import readline
from checker import Checker

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def start_loop():
	check_robot = Checker()
	while True:
		line = raw_input("simpleChecker>")
		if line == "quit":
			break
		else:
			for response_text in check_robot.respond_to(line):
				print response_text 

start_loop()