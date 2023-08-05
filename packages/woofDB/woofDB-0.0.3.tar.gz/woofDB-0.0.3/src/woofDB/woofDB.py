import json
import os

class MongoDatabase():
	os.system('pip install --upgrade pymongo; pip install --upgrade dnspython')
	import pymongo
	import dns
	def __init__(self, token):
		client = pymongo.MongoClient(token)
		self.database = client['database']['woof']
	
	def set_file(self, filename, filedata, overwrite=True):
		try:
			t = self.database.find_one({'filename' : filename})
			if not t:
				self.database.insert_one({'filename' : filename, 'data' : filedata})
			else:
				if overwrite:
					self.database.replace_one({'filename' : filename}, {'filename' : filename, 'data' : filedata})
				else:
					raise WoofErrors("Error in set_file: attempted to overwrite file")
		except:
			raise WoofErrors("Error in set_file!")
	
	def get_file(self, filename):
		try:
			full = self.database.find_one({'filename' : filename})
			if full['data']:
				return full['data']
			else:
				raise WoofErrors(f"Error in get_file: file with filename {filename} does not exist")
		except:
			raise WoofErrors(f"Error in get_file: file with filename {filename} does not exist")
	
	def delete_file(self, filename):
		try:
			callback = self.database.delete_one({'filename' : filename})
		except:
			raise WoofErrors(f"Error in delete_file: filename {filename} does not exist")
		

class Database():
	def __init__(self, name):
		self.name = name
		self.setup()
	
	def setup(self):
		if not os.path.isdir('woof'):
			os.system('mkdir woof; cd woof; mkdir databases')
		if not os.path.isfile(f'woof/databases/{self.name}.txt'):
			with open(f'woof/databases/{self.name}.txt', 'x') as file:
				pass
			with open(f"woof/databases/{self.name}.txt", 'w') as file:
				config = {
					'files' : {

					}
				}
				file.write(json.dumps(config))
	
	def set_file(self, filename, filedata, overwrite=True):
		with open(f"woof/databases/{self.name}.txt", 'r') as file:
			current = json.loads(file.read())
		
		if not overwrite:
			if filename in current['files'].keys():
				raise WoofErrors("Error in set_file: attempted to overwrite file")
			else:
				current['files'][filename] = filedata;
		else:
			current['files'][filename] = filedata
		
		with open(f"woof/databases/{self.name}.txt", 'w') as file:
			file.write(json.dumps(current))
	
	def get_file(self, filename):
		with open(f'woof/databases/{self.name}.txt', 'r') as file:
			current = json.loads(file.read())
		if filename not in current['files'].keys():
			raise WoofErrors(f"Error in get_file: file with filename {filename} does not exist")
		else:
			return current['files'][filename]
	
	def delete_file(self, filename):
		with open(f"woof/databases/{self.name}.txt", 'r') as file:
			current = json.loads(file.read())
		
		if filename not in current['files'].keys():
			raise WoofErrors(f"Error in delete_file: filename {filename} does not exist")
		else:
			del current['files'][filename]
			with open(f"woof/databases/{self.name}.txt", 'w') as file:
				file.write(json.dumps(current))

		
	
		



class WoofErrors(Exception):
	pass