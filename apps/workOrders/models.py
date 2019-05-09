from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z- ]+$')

class UserManager(models.Manager):
    def initialize(self, session):
        if 'fname' not in session:
            session['fname'] = ""
        if 'lname' not in session:
            session['lname'] = ""
        if 'email' not in session:
            session['email'] = ""
        if 'id' not in session:
            session['id'] = ""

    def validation(self, postData, session):
        errors = {}
        emails = User.objects.filter(email=postData['email']).all()
        if len(postData['fname']) < 2:
            errors['fname'] = "First name must be atleast 2 characters and only consist of letters." 
        elif not NAME_REGEX.match(postData['fname']):
            errors['fname_chars'] = "Name can only contain letters, spaces, or hyphens."
        else:
            session['fname'] = postData['fname']
        if len(postData['lname']) < 2:
            errors['lname'] = "Last name must be atleast 2 characters and only consist of letters."
        elif not NAME_REGEX.match(postData['lname']):
            errors['lname_chars'] = "Name can only contain letters, spaces, or hyphens."
        else:
            session['lname'] = postData['lname']
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        elif len(emails) > 0:
            errors['used'] = "Email has already been registered."
        else:
            session['email'] = postData['email']
        if len(postData['password']) < 8:
            errors['pass_length'] = "Password must be atleast 8 characters."
        elif re.search('[0-9]', postData['password']) is None:
            errors['pass_digit'] = "Password must contain atleast one digit (0-9)."
        elif re.search('[A-Z]', postData['password']) is None:
            errors['pass_cap'] = "Password must contain atleast one capital letter."   
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pw'] = "Does not match password."
        return errors
    
    def login(self, postData):
        errors = {}
        user_length = User.objects.filter(email=postData['email'])
        if len(user_length) < 1:
            errors['login'] = "Check email/password."
            return errors
        user = User.objects.get(email=postData['email'])
        if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors['login'] = "Check email/password."
            return errors

    def info(self, session):
        info = User.objects.get(id=session['id'])
        return info


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Worker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    commission = models.CharField(max_length = 5)
    job_types = models.CharField(max_length=255)
    max_jobs = models.CharField(max_length = 2)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Client(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Job(models.Model):
    prop = models.ForeignKey(Client, related_name="client", on_delete=models.PROTECT)
    employee = models.ForeignKey(Worker, related_name="worker", on_delete=models.PROTECT, null=True, blank=True)
    assigned_by = models.ForeignKey(User, related_name="user", on_delete=models.PROTECT, null=True, blank=True)
    request_by = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    add_info = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="unassigned")
    date_assigned = models.DateField(null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    PO_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)