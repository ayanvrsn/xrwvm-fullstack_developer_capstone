import json
from unittest.mock import patch
import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import CarMake, CarModel

class PortalTests(TestCase):
    def test_public_pages(self):
        for url,text in [('/about/','About Us'),('/contact/','Contact Us')]:
            self.assertContains(self.client.get(url),text)

    def test_csrf_required_for_registration(self):
        client=Client(enforce_csrf_checks=True)
        response=client.get('/djangoapp/session')
        self.assertEqual(response.status_code,200)
        payload={'userName':'new-user','password':'Test-only-password29!'}
        self.assertEqual(client.post('/djangoapp/register',json.dumps(payload),content_type='application/json').status_code,403)
        token=client.cookies['csrftoken'].value
        self.assertEqual(client.post('/djangoapp/register',json.dumps(payload),content_type='application/json',HTTP_X_CSRFTOKEN=token).status_code,201)
        self.assertEqual(client.get('/djangoapp/session').json()['userName'],'new-user')

    def test_login_and_logout(self):
        User.objects.create_user('tester',password='Test-only-password29!')
        response=self.client.post('/djangoapp/login',json.dumps({'userName':'tester','password':'Test-only-password29!'}),content_type='application/json')
        self.assertEqual(response.json()['status'],'Authenticated')
        self.assertEqual(self.client.post('/djangoapp/logout').status_code,200)
        self.assertIsNone(self.client.get('/djangoapp/session').json()['userName'])

    def test_review_requires_real_authenticated_session(self):
        self.assertEqual(self.client.post('/djangoapp/add_review','{}',content_type='application/json').status_code,401)

    @patch('djangoapp.views.post_review',return_value={'id':101})
    def test_review_author_comes_from_session(self,post):
        user=User.objects.create_user('tester',first_name='Test',last_name='User')
        self.client.force_login(user)
        response=self.client.post('/djangoapp/add_review',json.dumps({'review':'Excellent service','name':'spoofed','dealership':1}),content_type='application/json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(post.call_args.args[0]['name'],'Test User')

    @patch('djangoapp.views.get_request',side_effect=requests.ConnectionError())
    def test_backend_outage_is_502(self,get):
        self.assertEqual(self.client.get('/djangoapp/get_dealers').status_code,502)

    @patch('djangoapp.views.get_request',return_value=[{'id':1,'state':'Kansas'}])
    def test_state_filter_uses_backend_endpoint(self,get):
        self.assertEqual(self.client.get('/djangoapp/get_dealers/Kansas').json()['dealers'][0]['state'],'Kansas')
        get.assert_called_once_with('fetchDealers/Kansas')

    def test_catalog_year_bounds(self):
        make=CarMake.objects.create(name='Toyota')
        car=CarModel(car_make=make,name='Camry',type='Sedan',year=2014)
        with self.assertRaises(ValidationError):car.full_clean()
        car.year=2023
        car.full_clean()
