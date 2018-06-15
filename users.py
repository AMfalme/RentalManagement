"""
THis module creates a user class that carters for all users attributes and properties
"""
class User(object):
	"""docstring for User with every user's common methods"""
	def __init__(self, UserFirstName, UserSecondName, UserEmail, UserAddress, UserTown, UserPassword):
		self.UserFirstName = UserFirstName
		self.UserSecondName = UserSecondName
		self.UserEmail = UserEmail
		self.UserAddress = UserAddress
		self.UserTown = UserTown
		self.UserPassword = UserPassword
	def Login(self, UserEmail, UserPassword):
		Login = False
		if (self.UserEmail == UserEmail) and (self.UserPassword == UserPassword):
			Login = True
		return Login
	def logout(self):
		login = False
		return login

class Landloard(object):
	"""docstring for Landloard with admin priviledges

	"""
	def __init__(self, arg):
		super(Landloard, self).__init__()
		self.arg = arg
		
		