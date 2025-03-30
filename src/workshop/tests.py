from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Workshop

class WorkshopModelTests(TestCase):
    def workshop_is_in_the_future(self):
        future_date = timezone.now().date() + timedelta(days=1)
        self.assertTrue(workshop.date > timezone.now().date(), "Workshop date should be in the future.")

class WorkshopIndexViewTests(TestCase):
    def test_no_workshop(self):
        response = self.client.get(reverse("workshop:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No workshops are available.")
        self.assertQuerySetEqual(response.context["workshop_list"], [])
# Create your tests here.
