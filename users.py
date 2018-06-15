"""
THis module creates a user class that carters for all users attributes and properties
"""
class User(object):
	"""docstring for User with every user's common methods"""
	admin = False
	def __init__(self, UserFirstName, UserSecondName, UserEmail, UserAddress, UserTown, UserPassword):
		self.UserFirstName = UserFirstName
		self.UserSecondName = UserSecondName
		self.UserEmail = UserEmail
		self.UserAddress = UserAddress
		self.UserTown = UserTown
		self.UserPassword = UserPassword
	def login(self, UserEmail, UserPassword):
		Login = False
		if (self.UserEmail == UserEmail) and (self.UserPassword == UserPassword):
			Login = True
		return Login
	def logout(self):
		login = False
		return login

class Landloard(User):
	"""docstring for Landloard with admin priviledges

	"""
	admin = True
	def __init__(self):
		pass
	def addUser(self, userFirstName):
		pass
	def deleteUser(self, UserObject):
		del UserObject

class Tenant(User):
	"""docstring for Tenant"""
	def __init__(self, userLevel, savingsAccount):
		super(Tenant, self).__init__()
		self.userLevel = userLevel
		self.savingsAccount = savingsAccount
	def bookHouse(self, HouseID, price):
		booked = False
		if self.savingsAccount > price:
			self.savingsAccount -= price
			booked = True
		else:

			return 
	def vacateHouse(self):
		pass
		


class Appartment(object):
		"""docstring for Appartment"""
		def __init__(self, occupantID, type, roomNumber, price, deposit, ):
			self.type = type
			self.roomNumber = roomNumber


				