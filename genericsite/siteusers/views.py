import os
import binascii
import json
import hashlib
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse
from siteusers.models import SiteUser
from django.core.serializers.json import DjangoJSONEncoder


def index(request):
    """Send a blank page when visiting api url"""
    context = {}
    return render(request,'siteusers/index.html',context)

def view(request):
    """View user minus password field for security"""
    request_data = json.loads(request.body.decode())
    uuid = request_data.get('uuid','')
    if validate_access(request_data) == False:
        return access_error()
    try:
        siteuser = SiteUser.objects.get(pk=uuid)
        response_data = {}
        for field in SiteUser._meta.fields:
            # don't allow the password to be viewed
            if field.name != 'password':
                response_data[field.name] = str(getattr(siteuser,field.name))
        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")
    except SiteUser.DoesNotExist:
        return general_exception('view error: uuid does not exist ' + uuid)
    except Exception as e:
        return general_exception(e)

def all(request):
    """Lists users minus password field for security, very much
    not scalable with out proper filters"""
    request_data = json.loads(request.body.decode())
    if validate_access(request_data) == False:
        return access_error()
    try:
        user_list = []
        for siteuser in SiteUser.objects.all():
            response_data = {}
            for field in SiteUser._meta.fields:
                # don't allow the password to be viewed
                if field.name != 'password':
                    response_data[field.name] = str(getattr(siteuser,field.name))
            user_list.append(response_data)
        return HttpResponse(json.dumps(user_list, cls=DjangoJSONEncoder), content_type="application/json")
    except SiteUser.DoesNotExist:
        return general_exception('view error: uuid does not exist ' + uuid)
    except Exception as e:
        return general_exception(e)

def add(request):
    """Add user and return uuid on success"""
    request_data = json.loads(request.body.decode())
    response_data = {}
    siteuser = SiteUser()
    for field in SiteUser._meta.fields:
        if field.name != 'uuid' and field.name != 'created':
            value = request_data.get(field.name,'')
            if field.name == 'password' and value != '':
                #encode password md5
                value = encrypt_password(value)
            setattr(siteuser, field.name, value)
    response_data = {}
    try:
        if validate_access(request_data) == False:
            return access_error()
        siteuser.clean_fields()
        siteuser.save()
        response_data['result'] = 'success'
        for field in siteuser._meta.fields:
            # don't allow the password to be viewed
            if field.name == 'uuid':
                response_data[field.name] = getattr(siteuser,field.name).hex
            elif field.name != 'password':
                response_data[field.name] = str(getattr(siteuser,field.name))
        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")
    except ValidationError as e:
        response_data['result'] = 'failure'
        response_data['type'] = 'validation'
        response_data['message'] = str(e)
        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")
    except Exception as e:
        return general_exception(e)

def update(request):
    """update a user, on success user record is returned minus password field
    for security"""
    request_data = json.loads(request.body.decode())
    response_data = {}
    siteuser = SiteUser()
    try:
        if validate_access(request_data) == False:
            return access_error()
        uuid = request_data.get('uuid', '')
        siteuser = SiteUser.objects.get(pk=uuid)
    except SiteUser.DoesNotExist:
        return general_exception('update error: uuid does not exist ' + uuid)
    for field in SiteUser._meta.fields:
        if field.name != 'created' and field.name != 'key' and field.name != 'created':
            value = request_data.get(field.name,'')
            if field.name == 'password' and value != '':
                #encode password md5
                value = encrypt_password(value)
            if value == '':
                #if the value of the request is blank assume that field is not being updated and use previous value.
                value = getattr(siteuser,field.name)
            setattr(siteuser, field.name, request_data.get(field.name,value))
    if not siteuser.uuid:
        return general_exception('uuid is required')
    response_data = {}
    try:
        if validate_access(request_data) == False:
            return access_error()
        siteuser.clean_fields()
        siteuser.save()
        response_data['result'] = 'success'
        for field in siteuser._meta.fields:
            # don't allow the password to be viewed
            if field.name != 'password':
                response_data[field.name] = str(getattr(siteuser,field.name))
        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")
    except ValidationError as e:
        response_data['result'] = 'failure'
        response_data['type'] = 'validation'
        response_data['message'] = str(e)
        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")
    except Exception as e:
        return general_exception(e)

def delete(request):
    """delete a user, returns a failure if user does not exist and on success the uuid of user"""
    request_data = json.loads(request.body.decode())
    try:
        if validate_access(request_data) == False:
            return access_error()
        try:
            uuid = request_data.get('uuid', '')
            siteuser = SiteUser.objects.get(pk=uuid)
            siteuser.delete()
        except SiteUser.DoesNotExist:
            return general_exception('delete error: uuid does not exist ' + uuid)
        response_data = {}
        response_data['result'] = 'success'
        response_data['uuid'] = uuid
        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")
    except Exception as e:
        return general_exception(e)

def authenticate(request):
    """Validate password and email combination. Upon success send uuid"""
    request_data = json.loads(request.body.decode())
    email = request_data.get('email', '')
    password = encrypt_password(request_data.get('password', ''))
    dpassword = ''
    duuid = ''
    try:
        for t in SiteUser.objects.filter(email__exact=email):
            dpassword = t.password
            duuid = t.uuid
    except SiteUser.DoesNotExist:
            return general_exception('validate_password: no match found')
    if dpassword != password:
        return general_exception('validate_password: no match found')
    response_data = {}
    response_data['result'] = 'success'
    response_data['uuid'] = duuid
    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")

def validate_access(request_data):
    """Validate access to the api by checking api key passed by key parameter"""
    if request_data.get('key','') == 'access':
        return True
    return False

def access_error():
    """Return error message indicating api key is incorrect"""
    return general_exception('Api key incorrect')

def general_exception(e):
    """Send a general exception to the api caller in json format"""
    response_data = {}
    response_data['result'] = 'failure'
    response_data['type'] = 'general'
    response_data['message'] = str(e)
    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")

def encrypt_password(value):
   """Encrypt password with md5 + salt to reduce security leaks"""
   value = value + "sa"
   return hashlib.md5(value.encode('utf-8')).hexdigest()


