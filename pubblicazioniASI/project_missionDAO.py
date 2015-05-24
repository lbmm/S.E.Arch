_author_ = 'fmoscato'


import pymongo
import bson


'''
 The Project_Mission Data Access Object handles all interactions with the project_mission collection.

 Name = name of the mission_projects
 URL = url where possible to find more informations regarding the mission_project (point to the ASI web page)


'''


class ProjectMissionDAO:

    def __init__(self, db):
        self.db = db
        self.projects_missions = self.db.projects_missions

    def get_projects_missions(self):
      
        cursor = self.projects_missions.find().sort('name', direction=1)
        l = []

        for project_mission in cursor:

            l.append({'id': str(project_mission['_id']), 'name': project_mission['name'], 'URL': project_mission['URL']})

        return l

    def remove_project_mission(self, _id):

        try:
 
            self.projects_missions.remove({'_id': bson.ObjectId(oid=str(_id))})
  
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
    
        return True 
      

    # creates a new project_mission in the projects_missions collection
    def add_project_mission(self, **kwargs):

        project_mission = {'name': kwargs['name'], 'URL': kwargs['URL']}

        try:
            self.projects_missions.insert(project_mission)
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError:
            print "oops, mission name is already taken"
            return False

        return True


