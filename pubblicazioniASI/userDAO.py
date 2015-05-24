_author_ = 'fmoscato'


import random
import string
import hashlib
from datetime import datetime

import pymongo

import constants as c
import pubUtilities

# The User Data Access Object handles all interactions with the User collection.


class UserDAO:

    def __init__(self, db):
        self.db = db
        self.users = self.db.users
        self.secret = 'verysecret'

    @staticmethod
    def make_salt():
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt

    def make_pw_hash(self, pw, salt=None):
        if not salt:
            salt = self.make_salt()
        return hashlib.sha256(pw + salt).hexdigest()+"," + salt

    # Validates a user login. Returns user record or None
    def validate_login(self, username, password):

        user = None
        try:
            user = self.users.find_one({'_id': username})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        if not user:
            print "User not in database"
            return None

        salt = user['password'].split(',')[1]

        if user['password'] != self.make_pw_hash(password, salt):
            print "user password is not a match"
            return None

        # Looks good
        return user

    def get_admin_email(self):

        cursor = self.users.find_one({'admin': True})

        return cursor['email']


    def get_users(self, date_format=None):
      
        cursor = self.users.find({'admin': False}).sort('lastname', direction=1)
        date_format_str = c.SHORT_DATE_FORMAT
        if date_format:
            date_format_str = date_format

        l = []

        for user in cursor:

            usr = {'username': user['_id'], 'name': user['name'], 'lastname': user['lastname'],
                   'email': user['email'],
                   'start_date': user['start_date'].strftime(date_format_str),
                   'end_date': user['end_date'].strftime(date_format_str),
                   'contracts': user.get('contracts', []),
                   'projects': user['projects'],
                   'missions_projects': user['missions_projects']}

            l.append(usr)

        return l

    def get_user(self, _id):

        cursor = self.users.find_one({'_id': _id})

        user = None

        if cursor:

            user = {'username': cursor['_id'], 'name': cursor['name'], 'lastname': cursor['lastname'],
                    'email': cursor['email'],
                    'start_date': cursor['start_date'].strftime(c.DATE_FORMAT),
                    'end_date': cursor['end_date'].strftime(c.DATE_FORMAT),
                    'contracts': cursor.get('contracts', []),
                    'projects': cursor.get('projects', []),
                    'missions_projects': cursor.get('missions_projects', '')
                    }
        return user


    def remove_user(self, _id):

        try:

            print "removing user %s" % _id
 
            self.users.remove({'_id': _id})
  
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
    
        return True 
      
    def close_validity_user(self, _id):

        today = datetime.now()

        try:
            self.users.update({'_id': _id}, {'$set': {"end_date": today}})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
         
        return True

    def update_email(self, _id, email):

        try:
            self.users.update({'_id': _id}, {'$set': {'email': email}})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    def update_contracts(self, _id, contracts_list):

        try:
            self.users.update({'_id': _id}, {'$set': {'contracts': contracts_list}})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    def update_projects_missions(self, _id, projects_missions_list):

        try:
            self.users.update({'_id': _id}, {'$set': {'missions_projects': projects_missions_list}})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    def update_projects(self, _id, projects_list):

        try:
            self.users.update({'_id': _id}, {'$set': {'projects': projects_list}})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True


    # creates a new user in the users collection
    def add_user(self, **kwargs):

        pwd = kwargs['password']
        password_hash = self.make_pw_hash(pwd)

        user = {'_id': kwargs['username'], 'password': password_hash, 
                'name': kwargs['name'], 'lastname': kwargs['lastname'],
                'email': kwargs['email'],
                'admin': kwargs.get('admin', False),
                'start_date': kwargs['start_date'],
                'contracts': kwargs.get('contracts', []),
                'projects': kwargs.get('projects', []),
                'missions_projects': kwargs.get('missions_projects', [])}

        if 'end_date'in kwargs and kwargs['end_date'] != '':
            user['end_date'] = kwargs['end_date']
        else:
            date1 = datetime.strptime(c.END_DATE, c.DATE_FORMAT)
            user['end_date'] = date1
        try:
            self.users.insert(user)
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError:
            print "oops, username is already taken"
            return False

        return True

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def create_tmp_password(self, _id):
        """
        creates a new password and updating the DB with the new pwd
        sent email to the user telling the new password
        @param: user
        @return: true || false
        """

        new_pwd = self.id_generator()
        new_pwd_hash = self.make_pw_hash(new_pwd)
        user = self.get_user(_id)

        if not pubUtilities.sendMail(user['email'], c.SUBJECT_FORGOT_PASSWORD, c.BODY_FORGOT_PASSWORD % new_pwd):
            print "error sending email user: %" % user['email']
            return False
        try:
            self.users.update({'_id': _id}, {'$set': {'password': new_pwd_hash}})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True




