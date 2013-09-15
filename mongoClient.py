#encoding = utf-8
import pymongo

class MongoClient:
	def __init__(self):
		self.conn = pymongo.Connection('localhost',27017)
		self.db = self.conn.simpleChecker
		self.tasks = self.db.tasks

	def find_tasks(self,filters):
		cursor = self.tasks.find(filters).sort('priority')
		return list(cursor)

	def insert_task(self,task):
		self.tasks.insert(task)

	def update_task(self,filter,update):
		self.tasks.update(filter,{"$set":{'priority':update}})

	def delete_task(self,task):
		self.tasks.remove(task)
