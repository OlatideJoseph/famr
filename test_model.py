import models
import unittest
from app import db, app

with app.app_context() as ctx:
	ctx.push()

class TestDatabaseModel(unittest.TestCase):
	def setUp(self) -> None:
		self.subject = models.Subject(name="Reboot")
		db.session.add(self.subject)
		print(f"Creating database {self.subject}")
		db.session.commit()

	def tearDown(self) -> None:
		db.session.delete(self.subject)
		print(f"Deleting database {self.subject}")
		db.session.commit()

	def test_value_added(self) -> None:
		sub = self.subject
		self.assertEqual(self.subject.name, "Reboot")



class TestUserModel(unittest.TestCase):
	"""\
		A model to test the user database model
	"""
	def setUp(self) -> None:
		self.user = models.User.query.get(1)
		self.model = models.User

	def tearDown(self) -> None:
		pass

	def test_user(self) -> None:
		self.assertEqual(self.user.username, 'webcrawler001')
		self.isInstance(self.user, self.model)
		
	def test_can_create(self):
		pass



