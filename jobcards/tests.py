from django.test import TestCase
from django.contrib.auth import get_user_model
from clients.models import ClientProfile
from .models import Jobcard, JobcardTemplate, LineItem
import datetime

User = get_user_model()

class JobcardModelTest(TestCase):
    def setUp(self):
        self.technician = User.objects.create_user(username='tech', password='password')
        self.client = ClientProfile.objects.create(name='John Doe', email='john@example.com')
        self.template = JobcardTemplate.objects.create(name='Standard Service', layout_schema={})

    def test_jobcard_creation(self):
        jobcard = Jobcard.objects.create(
            template=self.template,
            technician=self.technician,
            client=self.client
        )
        self.assertEqual(jobcard.client.name, 'John Doe')
        self.assertEqual(jobcard.status, 'DRAFT')
        # Check ID format
        year = datetime.datetime.now().year
        self.assertTrue(jobcard.jobcard_id.startswith(f"JC-{year}-"))

    def test_line_item_creation(self):
        jobcard = Jobcard.objects.create(
            template=self.template,
            technician=self.technician,
            client=self.client
        )
        line_item = LineItem.objects.create(
            jobcard=jobcard,
            who_helped='Jane Smith',
            hardware_used='Laptop',
            quantity=1
        )
        self.assertEqual(line_item.who_helped, 'Jane Smith')
        self.assertEqual(line_item.hardware_used, 'Laptop')
        self.assertEqual(line_item.jobcard, jobcard)
