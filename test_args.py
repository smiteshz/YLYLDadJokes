class newClass:
	def __init__(self, *args, **kwargs):
		self.name = kwargs["name"]
		if len(args) != 0:
			for i in args:
				print (i)
		if len(kwargs) != 0:
			for i in kwargs:
				print (kwargs[i])
	def __repr__(self):
		return "Object of "+self.name

cl = newClass(1,2,3,3,name = newClass(name = "Smitesh"))