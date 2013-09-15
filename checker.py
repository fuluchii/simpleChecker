#encoding = utf-8
from response import Response
from mongoClient import MongoClient
from datetime import date
from checkGlobal import priority_schema,priority_emoji_map
import sys
def _clear_res(func):
	def new_func(self,*args):
		res = func(self,*args)
		self.clear_response_list()
		return res
	return new_func

def _reset(func):
	def new_func(self,*args):
		self.reset(*args)
		res = func(self,*args)
		return res
	return new_func

class Checker:
	def __init__(self):
		self.status = Status()
		self.tasks = []
		self.new_task = None
		self.current_task = None
		self.client = MongoClient()
		self.reset({})

	@_clear_res
	def respond_to(self,msg):
		commands = msg.split()
		output = self.status.get_output(commands)
		self.call_func(self._command_map[output],commands)
		return self.response_list

	def show_tasks(self,commands):
		def parse_filter(filters):
			if len(filters) != 2:
				return None
			else:
				return dict((k,v) for k,v in {'date':filters[0],'priority':filters[1]}.items() if v!='all')
		query_filter = parse_filter(commands[1:])
		if(query_filter is not None):
			self.tasks = self.client.find_tasks(query_filter)
		res_list = self.format_task_list_to_res(self.tasks)
		self.response_list = [" ".join(text for text in res.response_text_list) for res in res_list]

	def format_task_to_res(self,task,index):
		return Response([
			['%d:' % index,'default'],
			['%s ' % priority_emoji_map[task['priority']],'none'],
			[task['content'],task['priority']],
			[task['date'],'none']]
			)

	def format_task_list_to_res(self,tasklist):
		return [self.format_task_to_res(task,tasklist.index(task)) for task in tasklist]


	def add_task(self,commands):
		self.new_task = {}
		add_res = Response([['Plz input content of task:','normal']])
		self.response_list = ["".join(r for r in add_res.response_text_list)]

	def add_task_content(self,commands):
		content = commands[0]
		if content == '':
			self.bad_input('task content')
		else:
			self.new_task['content'] = content
			add_res = Response([['Plz input priority of task (%s) :' % ",".join(priority_schema),'normal']])
			self.response_list = ["".join(r for r in add_res.response_text_list)]

	def add_task_priority(self,commands):
		priority = commands[0]
		if not priority in priority_schema:
			self.bad_input('priority')
		else:
			self.new_task['priority'] = priority
			self.new_task['date'] = str(date.today())
			add_res = self.format_task_to_res(self.new_task, 0)
			self.client.insert_task(self.new_task)
			self.response_list = ["".join(r for r in add_res.response_text_list)]

	def get_chosen_task(self,commands):
		try:
			self.current_task = self.tasks[int(commands[1])]
			chosen_res = self.format_task_to_res(self.current_task,int(commands[1]))
			self.response_list = ["".join(r for r in chosen_res.response_text_list)]
		except:
			print sys.exc_info()
			self.bad_input('index of tasks')

	def deal_with_task(self,commands):
		if commands[0] == 'delete':
			self.client.delete_task(self.current_task)
			self.tasklist.remove(self.current_task)
			badinput_res = Response([['task %s has been deleted.' % self.current_task,'daily']])
			self.current_task = None
			self.response_list = ["".join(r for r in badinput_res.response_text_list)]
			self.print_tasks()
			return
		if not commands[0] in priority_schema:
			self.bad_input('status.(%s)' % ",".join(priority_schema))
		else:
			self.client.update_task(self.current_task, commands[0])
			self.current_task['priority'] = commands[0]
			update_res = Response([['task %s has been update to %s' % (self.current_task,commands[0]),'daily']])
			self.current_task = None
			self.response_list = ["".join(r for r in update_res.response_text_list)]
			self.print_tasks()

	def print_tasks(self):
		res_list = self.format_task_list_to_res(self.tasks)
		self.response_list = [" ".join(text for text in res.response_text_list) for res in res_list]

	def bad_input(self,msg):
		self.status.step_back()
		badinput_res = Response([['Plz input a correct %s.' % msg,'highlight']])
		self.response_list = ["".join(r for r in badinput_res.response_text_list)]

	def do_nothing(self,commands):
		return


	@_reset
	def no_such_cmd(self,cmd):
		cmd = " ".join(cmd)
		error_res = Response([['command not found','default'],[cmd,'high']])
		self.response_list = [":".join([r for r in error_res.response_text_list])]


	def clear_response_list(self):
		self.response_list = []

	def clear_checktask_list(self):
		self.checktask_list = []

	def reset(self,commands):
		self.clear_response_list()
		self.clear_checktask_list()
		self.status.update_status('reset');

	def call_func(o,name,*args):
		getattr(o, name)(*args)

	_command_map = {
		'show': 'show_tasks',
		'unknown': 'no_such_cmd',
		'choose': 'get_chosen_task',
		'reset': 'reset',
		'deal': 'deal_with_task',
		'add': 'add_task',
		'content':'add_task_content',
		'priority': 'add_task_priority',
		'stay': 'do_nothing'
	}

class Status:
	def __init__(self):
		self.status = 0
		self.last_stauts = 0

	_status_cmd_map={
		'show': 0,
		'choose': 1,
		'reset': 0,
		'deal': 0,
		'add':2,
		'content':3,
		'priority':0,
		'unknown':0
	}
	_last_status_map = {
		1:0,
		2:0,
		3:2,
		0:0
	}

	def update_status(self,cmd):
		self.status = self._status_cmd_map[cmd]

	def get_output(self,input_cmds):
		if len(input_cmds) == 0:
			self.output_cmd = 'stay'
			return self.output_cmd

		if self.status == 0:
			if input_cmds[0] == 'show':
				self.output_cmd = 'show'
			elif input_cmds[0] == 'add':
				self.output_cmd = 'add'
			elif input_cmds[0] == 'choose':
				self.output_cmd = 'choose'
			else:
				self.output_cmd = 'unknown'
		elif self.status == 1:
			self.output_cmd = 'deal'
		elif self.status == 2:
			self.output_cmd = 'content'
		elif self.status == 3:
			self.output_cmd = 'priority'
		if input_cmds[0] == 'reset':
			self.output_cmd = 'reset'
		self.last_stauts = self.status
		self.update_status(self.output_cmd)
		return self.output_cmd

	#this method is JUST for a bad input
	def step_back(self):
		self.status = self.last_stauts
		self.last_status = self._last_status_map[self.status]



