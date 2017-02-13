from django.test import TestCase
from django.core.urlresolvers import resolve

class HomePageTest(TestCase):
    def test_root_url_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'landingpage/index.html')
        
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>\n<html'))
        self.assertIn('<title>Clutch',html)
        self.assertTrue(html.endswith('</html>'))