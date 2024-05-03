#Code generated from claude on feeding Flask Integration Latest->app.py

import unittest
from unittest.mock import patch, Mock
from flask import Flask, session
import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        self.app.secret_key = 'testing'

    def test_landing_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_route(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['state'] = 'test_state'
            response = client.get('/login')
            self.assertEqual(response.status_code, 302)  # Redirect

    def test_callback_route(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['state'] = 'test_state'
            response = client.get('/callback?state=test_state')
            self.assertEqual(response.status_code, 302)  # Redirect
            self.assertIn('google_id', session)

    def test_logout_route(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['google_id'] = 'test_id'
            response = client.get('/logout')
            self.assertEqual(response.status_code, 302)  # Redirect
            self.assertNotIn('google_id', session)

    @patch('app.get_user_data')
    @patch('app.get_age_gender')
    @patch('app.get_sleep_data')
    def test_data_acquisition(self, mock_sleep_data, mock_age_gender, mock_user_data):
        mock_age_gender.return_value = {'birthdays': [{'date': {'year': 1990, 'month': 1, 'day': 1}}], 'genders': [{'value': 'male'}]}
        mock_user_data.side_effect = [
            {'bucket': [{'dataset': [{'point': [{'value': [{'intVal': 1000}]}]}]}]},  # Steps
            {'bucket': [{'dataset': [{'point': [{'value': [{'fpVal': 80}, {'fpVal': 100}]}]}]}]},  # Heart rate
            {'bucket': [{'dataset': [{'point': [{'value': [{'fpVal': 120}, {'fpVal': 80}]}]}]}]}  # Blood pressure
        ]
        mock_sleep_data.return_value = {'session': [{'startTimeMillis': 1000, 'endTimeMillis': 10000}]}

        with self.app as client:
            with client.session_transaction() as session:
                session['google_access_token'] = 'test_token'
            response = client.get('/data')
            self.assertEqual(response.status_code, 302)  # Redirect
            self.assertEqual(session['age'], 34)
            self.assertEqual(session['gender'], 'male')
            self.assertEqual(session['avgsteps'], 1000)
            self.assertEqual(session['max_heart'], 100)
            self.assertEqual(session['systolic'], 120)
            self.assertEqual(session['diastolic'], 80)
            self.assertEqual(session['sleep_hours'], 2.5)

    def test_homepage_route(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['google_access_token'] = 'test_token'
                session['name'] = 'Test User'
                session['pfp'] = 'https://example.com/profile.jpg'
            response = client.get('/homepage')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)
            self.assertIn(b'https://example.com/profile.jpg', response.data)

    def test_heart_route(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['google_access_token'] = 'test_token'
                session['age'] = 30
                session['gender'] = 'male'
                session['systolic'] = 120
                session['max_heart'] = 100
            response = client.get('/heart')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'30', response.data)
            self.assertIn(b'male', response.data)
            self.assertIn(b'120', response.data)
            self.assertIn(b'100', response.data)

    def test_sleep_route(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['google_access_token'] = 'test_token'
                session['age'] = 30
                session['systolic'] = 120
                session['diastolic'] = 80
                session['avgsteps'] = 5000
                session['avg_heart'] = 70
                session['sleep_hours'] = 7
            response = client.get('/sleep')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'30', response.data)
            self.assertIn(b'120', response.data)
            self.assertIn(b'80', response.data)
            self.assertIn(b'5000', response.data)
            self.assertIn(b'70', response.data)
            self.assertIn(b'7', response.data)

    @patch('app.predict_disease')
    def test_hrisk_route(self, mock_predict_disease):
        mock_predict_disease.return_value = [0]
        data = {
            'age': '30',
            'gender': 'male',
            'rbp': '120',
            'chol': '200',
            'sugar': '100',
            'ecg': '1',
            'rate': '80',
            'ang': '1',
            'thal': '2'
        }
        response = self.app.post('/hrisk', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have a healthy heart!', response.data)

    @patch('app.predict_disease')
    def test_srisk_route(self, mock_predict_disease):
        mock_predict_disease.return_value = [1]
        data = {
            'gender': 'male',
            'age': '30',
            'sleepdura': '7.0',
            'phys': '1',
            'stress': '2',
            'bmi': '25',
            'rate': '70',
            'step': '5000',
            'sys': '120',
            'dia': '80'
        }
        response = self.app.post('/srisk', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Risk of Sleep Apnea', response.data)

    @patch('app.calculate_age')
    def test_calculate_age(self, mock_calculate_age):
        mock_calculate_age.return_value = 30
        birthday = Mock()
        birthday.year = 1990
        birthday.month = 1
        birthday.day = 1
        age = app.calculate_age(birthday)
        self.assertEqual(age, 30)

    def test_current_milli_time(self):
        current_time = app.current_milli_time()
        self.assertIsInstance(current_time, int)
        self.assertGreater(current_time, 1000000000000)  # Reasonable value

    def test_login_is_required(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['google_id'] = 'test_id'
                response = client.get('/data')
                self.assertEqual(response.status_code, 302)  # Redirect

            del session