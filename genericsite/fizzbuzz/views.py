import json
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse


def calculate(request,number=5):
    """calculate fiizbuzz number, pass by parmeter number"""
    number = int(number)
    response_data = {'result': ''}
    if number % 3 == 0:
        response_data['result'] = "Fizz"
    if number % 5 == 0:
        response_data['result'] += "Buzz"
    if not (number % 3 == 0 or number % 5 == 0):
        response_data['result'] = number
    response_data['number'] = number
    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")

