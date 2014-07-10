import json
from django.test import TestCase
from django.test.client import Client

class FizzBuzzTest(TestCase):

    def test_calculate(self):
        """Spot test FizzBuzz calculation"""
        c = Client()
        test_data = { 1: 1 , 3: 'Fizz', 5: 'Buzz', 10: 'Buzz', 15: 'FizzBuzz', 97: 97}
        for number, result_string in test_data.items():
            result = c.post('/fizzbuzz/calculate',{ 'number': number} )
            data = json.loads(result.content.decode())
            self.assertEqual(data['result'], result_string)
