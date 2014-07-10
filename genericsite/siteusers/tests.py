import json
from django.test import TestCase
from django.core.exceptions import ValidationError
from siteusers.models import SiteUser
from django.test.client import Client
from django.core.serializers.json import DjangoJSONEncoder

class SiteUserTest(TestCase):
    """Tests for siteuser api calls and supporting functions"""
    uuid = ''

    def test_validation(self):
        """Tests if model validation triggers a ValidationError"""
        with self.assertRaises(ValidationError):
            SiteUser(first_name='Bob', email='this.is.not.an.email').clean_fields()

    def test_add(self):
        """Test adding of new record"""
        c = Client()
        result = c.post('/siteusers/add',content_type='application/json', data=json.dumps({'key': 'access', 'first_name':'First Name 1','last_name': 'Last Name 2','email': 'test@test4.com', 'password': 'password4' }, cls=DjangoJSONEncoder))
        data = json.loads(result.content.decode())
        self.assertEqual("uuid" in data,True)
        self.assertEqual(data['result'], 'success')
        self.assertEqual(data['email'],'test@test4.com')
        self.uuid = data['uuid']

    def test_view(self):
        """Test add of new record"""
        self.test_add()
        c = Client()
        result = c.post('/siteusers/view',content_type='application/json', data=json.dumps({'key': 'access', 'uuid': self.uuid}, cls=DjangoJSONEncoder))
        data = json.loads(result.content.decode())
        self.assertEqual("uuid" in data,True)
        self.assertEqual(data['uuid'], self.uuid)
        self.assertEqual(data['email'],'test@test4.com')

    def test_update(self):
        """Test update of new record"""
        self.test_add()
        c = Client()
        result = c.post('/siteusers/update',content_type='application/json', data=json.dumps({'key': 'access', 'uuid': self.uuid, 'first_name':'First Name 11','last_name': 'Last Name 12','email': 'test@test14.com', 'password': 'password14' }, cls=DjangoJSONEncoder))
        data = json.loads(result.content.decode())
        self.assertEqual("uuid" in data,True)
        self.assertEqual(data['uuid'], self.uuid)
        self.assertEqual(data['result'], 'success')
        result = c.post('/siteusers/view',content_type='application/json', data=json.dumps({'key': 'access', 'uuid': self.uuid}, cls=DjangoJSONEncoder))
        data = json.loads(result.content.decode())
        self.assertEqual("uuid" in data,True)
        self.assertEqual(data['uuid'], self.uuid)
#        print("authenticate result = " + result.content.decode())
        self.assertEqual(data['email'],'test@test14.com')

    def test_delete(self):
        """Test delete of record"""
        self.test_add()
        c = Client()
        result = c.post('/siteusers/delete',content_type='application/json', data=json.dumps({'key': 'access', 'uuid': self.uuid}, cls=DjangoJSONEncoder))
        data = json.loads(result.content.decode())
        self.assertEqual("uuid" in data,True)
        self.assertEqual(data['uuid'], self.uuid)
        self.assertEqual(data['result'], 'success')

    def test_authenticate(self):
        """Test authenticate of email / password """
        self.test_add()
        c = Client()
        result = c.post('/siteusers/authenticate',content_type='application/json', data=json.dumps({'email': 'test@test4.com', 'password': 'password4'}, cls=DjangoJSONEncoder))
        data = json.loads(result.content.decode())
        self.assertEqual("uuid" in data,True)
        self.assertEqual(data['uuid'], self.uuid)
        self.assertEqual(data['result'], 'success')

    def test_apikey(self):
        """Test add of new record"""
        self.test_add()
        c = Client()
        result = c.post('/siteusers/view', content_type='application/json', data=json.dumps({'key': 'accessdenied', 'uuid': self.uuid}, cls=DjangoJSONEncoder))
        data = json.loads(result.content.decode())
        self.assertEqual("uuid" in data,False)
        self.assertEqual(data['result'], 'failure')
