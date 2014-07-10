Users Admin and API sample
==========================

A basic User Admin and API sample demostrating a basic python, django, angularjs web application utilizing AJAX json calls to an API

Usage
---

To use the app goto the following url for the web interface
{yourserver}/app/userapp/index.html

Install 
---
The django-uuidfield module is needed for django and depending on your version of python you will need to replace the /dist-packages/uuidfield/fields.py file with the supporting/fields.py file

To install uuidfield
pip install django-uuidfield

To start the application create the databases
python3 manage.py syncdb

Run the web server
python3 manage.py runserver {yourserverip}:8000


API
---

All api requests take raw json as the input and require an api key

{server}/siteusers/view - View user
{server}/siteusers/all - List all users
{server}/siteusers/add - Add user
{server}/siteusers/update - Update user
{server}/siteusers/delete - Delete user
{server}/siteusers/authenticate - Authenticate email and password combination


Todo
---

API
Document api parameters

Web interface
Add better error reporting to edit
Warn before deleting

Notes
---

For uuid field it is currently handled by django-uuidfield
pip install django-uuidfield

I'd rather use a id generation method that instagram uses or something along the lines of simpleflake
http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram
http://engineering.custommade.com/simpleflake-distributed-id-generation-for-the-lazy/
