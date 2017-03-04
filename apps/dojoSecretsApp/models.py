from __future__ import unicode_literals
import re
from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):

    def validator(self, first_name, last_name, email, password, password2):
        errorlist = []
        errordict = {"enterfirst": "Please enter a first name (which is at least 2 characters long).",
        "lettersfirst": "Please only include letters in your first name.",
        "enterlast": "Please enter a last name (which is at least 2 characters long).",
        "letterslast": "Please only include letters in your last name.",
        "enteremail": "Please enter an email address.", "entervalid": "Please enter a valid email address.",
        "unique": "That email is already in use.  Please enter a unique email.",
        "enterpassword": "Please enter a password that is at least 8 characters in length.",
        "mismatch": "Please make sure that your confirmation password matches your original password."}

        LETTERS_ONLY_REGEX = re.compile(r'^[a-zA-Z]+$')

        if len(first_name) < 2:
            errorlist.append("enterfirst")
        elif not LETTERS_ONLY_REGEX.match(first_name):
            errorlist.append("lettersfirst")

        if len(last_name) < 2:
            errorlist.append("enterlast")
        elif not LETTERS_ONLY_REGEX.match(last_name):
            errorlist.append("letterslast")

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(email) == 0:
            errorlist.append("enteremail")
        elif not EMAIL_REGEX.match(email):
            errorlist.append("entervalid")
        elif len(self.filter(email = email)) > 0:
            errorlist.append("unique")

        if len(password) < 8:
            errorlist.append("enterpassword")
        elif password != password2:
            errorlist.append("mismatch")

        if len(errorlist) > 0:
            return False, errorlist, errordict
        last = self.create(first_name = first_name, last_name = last_name, email = email, password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
        choice_id = last.id
        return True, choice_id



    def login(self, email, password):
        errorlist = []
        errordict = {"enteremail": "Please enter an email address.",
        "emismatch": "Your email address does not appear in our database.  If you do not have an account, please register below.",
        "pmismatch": "Your password does not match our records.  Please try again or create a new account below."}
        if len(email) == 0:
            errorlist.append("enteremail")
        else:
            try:
                selection = registration.objects.get(email = email)
                if bcrypt.hashpw(password.encode(), selection.password.encode()) == selection.password:
                    choice_id = selection.id
                    return True, choice_id
                else:
                    errorlist.append("pmismatch")
            except:
                errorlist.append("emismatch")

        return False, errorlist,errordict

    def create_secret(self, content, passedcreator):
        if len(content) == 0:
            return False
        else:
            recentPost = secret.objects.create(content = content, creator = passedcreator)
            return True

class registration(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.EmailField()
    password = models.CharField(max_length = 200)
    objects = UserManager()

class secret(models.Model):
    content = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(registration, related_name="creation")
    liker = models.ManyToManyField(registration, related_name="liked")
    objects = UserManager()
