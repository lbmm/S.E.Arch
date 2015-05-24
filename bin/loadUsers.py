__author__ = 'federicamoscato'

import csv
import re
from datetime import datetime
import pymongo

import pubblicazioniASI.userDAO as userDAO

FILE_TO_LOAD = ''

connection_string = ""
connection = pymongo.MongoClient(connection_string)
database = connection.publicationASI
users = userDAO.UserDAO(database)

repls = {" ": "", "'": ""}

class AuthorException(ValueError):
    pass


class InsertError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Author(object):

    def __init__(self, name, lastname, start_date):
        self.name = name
        self.lastname = lastname
        self.start_date = datetime.strptime(start_date, "%d/%m/%Y")


def insertIntoDB(author):

     return users.add_user(name=author.name, lastname=author.lastname,
                           start_date=author.start_date, password=author.name,
                           username='%s%s' % (
                               reduce(lambda a, kv: a.replace(*kv), repls.iteritems(), author.lastname.lower())
                               , author.name[0].lower()),
                           email='moscato@asdc.asi.it')


def main():

    print 'starting to load authors in DB'

    with open(FILE_TO_LOAD) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            lastname_name = row[2].strip()
            name = row[3].strip()
            lastname = lastname_name[:-len(name)]
            try:
               new_author = Author(name, lastname.strip(), row[1])
               if not insertIntoDB(new_author):
                raise InsertError("error inserting author %s  " % row[2])
            except AuthorException, e:
                print e.message
            except InsertError as e:
                print e.value

    print "end of load all the authors"



if __name__ == '__main__':

    main()
