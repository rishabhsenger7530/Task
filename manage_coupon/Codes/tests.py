from django.test import TestCase

from .models import User, Code,CodeType
# Create your tests here.

class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='rishabh',password='root',email='rishabh2@gmail.com',contact="8182027530")
        

    def test_text_content(self):
        user = User.objects.get(id=1)
        expected_object_name = f'{user.username}'
        self.assertEquals(expected_object_name, 'rishabh')
    
    def test_index_loads_properly(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    
   



