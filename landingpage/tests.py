from django.test import TestCase
from django.core.urlresolvers import resolve

class HomePageTest(TestCase):
    def test_root_url_uses_correct_template(self):
        response = self.client.get('/')
        
        self.assertTemplateUsed(response,'landingpage/index.html')