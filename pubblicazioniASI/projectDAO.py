_author_ = 'fmoscato'

from datetime import datetime

import pymongo
import bson

import constants as c
'''
 The Project Data Access Object handles all interactions with the Project collection.

 Missions and Project = main scientific project
 Project =sub-projects
 URL = url where possible to find more informations regarding the project (point to the ASI web page)
'''



class ProjectDAO:

    def __init__(self, db):
        self.db = db
        self.projects = self.db.projects

    # creates a new project in the projects collection
    def add_project(self, **kwargs):

        project = {'name': kwargs['project_name'],
                   'project_mission': kwargs['project_mission'],
                   'URL': kwargs['URL']}

        try:
            self.projects.insert(project)
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError:
            print "oops, project name is already taken"
            return False

        return True

    def get_projects(self):
      
        cursor = self.projects.find().sort('_id', direction=1)
        l = []

        for project in cursor:

            l.append({'project': project['_id'],
                      'name': project['name'],
                      'project_mission': project['project_mission'],
                      'URL': project['URL']})

        return l

    def remove_project(self, _id):
        try:
            self.projects.remove({'_id':  bson.ObjectId(oid=str(_id))})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
    
        return True 
      




