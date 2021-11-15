from django.test import TestCase
# User imports
from django.urls import resolve
from bullseye.views import dashboard

# Create your tests here.
class DashboardTest(TestCase):
    
    def test_root_url_resolves_to_dashboard_view(self):
        found = resolve('/')
        self.assertEqual(found.func, dashboard)
