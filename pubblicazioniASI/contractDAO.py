_author_ = 'fmoscato'

from datetime import datetime

import pymongo

import constants as c
'''
 The Contract  Data Access Object handles all interactions with the Project collection.
 The Contract DAO handle the project object that can have the following field

 Project = project of the contract (the project is a child of project_mission)
 contract_name = contract name
 contract_id = id of the contract
 contract type = if the contract was signed with industry or is a scientific contract
 institution = institution whit who the contract was signed
 start date = when the contract was signed
 end_date = if present, end_date of the contract
 active = if the contract is still active

'''



class ContractDAO:

    def __init__(self, db):
        self.db = db
        self.contracts = self.db.contracts

    # creates a new project in the projects collection
    def add_contract(self, **kwargs):

        date_format = kwargs.get('date_format', c.DATE_FORMAT)
        contract = {'_id': kwargs['contract_id'],
                    'project': kwargs.get('project', ''), 'contract_name': unicode(kwargs["contract_name"], 'utf-8', 'ignore'),
                    'contract_type': kwargs['contract_type'],
                    'institution': unicode(kwargs['institution'], 'utf-8', 'ignore'),
                    'start_date': datetime.strptime(kwargs['start_date'].rstrip(), date_format),
                    'is_active': kwargs['is_active']}

        try:
            self.contracts.insert(contract)
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError:
            print "oops, project name is already taken"
            return False

        return True

    def get_contracts(self):
      
        cursor = self.contracts.find().sort('_id', direction=1)
        l = []

        date_format_str = c.SHORT_DATE_FORMAT

        for contract in cursor:

            l.append({'project': contract['project'],
                      'contract_name': contract['contract_name'],
                      'contract_id': contract['_id'],
                      'start_date': contract['start_date'].strftime(date_format_str),
                      'contrat_type': contract['contract_type'],
                      'institution': contract['institution'],
                      'is_active': contract['is_active']})

        return l

    def remove_contract(self, _id):

        try:
 
            self.contracts.remove({'_id': _id})
  
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
    
        return True


    def update_projects(self, _id, project):

        try:

            self.contracts.update({'_id': _id[1:-1]}, {'$set': {'project': str(project)}})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

      




