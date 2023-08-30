from unittest import TestCase
from app import db, app
from models import Subject, Course, Grade, WaecSubject

with app.app_context() as ctx:
	ctx.push()

class TestDatabaseModel(TestCase):
	def setUp(self):
		self.subject = Subject(name="Reboot")
		db.session.add(self.subject)
		print(f"Creating database {self.subject}")
		db.session.commit()
	def tearDown(self):
		db.session.delete(self.subject)
		print(f"Deleting database {self.subject}")
		db.session.commit()

	def test_value_added(self):
		sub = self.subject
		self.assertEqual(self.subject.name, "Reboot")

