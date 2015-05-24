__author__ = 'fmoscato'

"""
The Publication DAO  handles interactions with the publication collection
The DAO provides 3 levels interface (da scrivere meglio)
1 - ADMIN can add publications + validate
2- search publications
3- users level
"""

import sys
import re
from datetime import datetime
import json
import ast


import pymongo
import bson

import constants as c



class PublicationDAO(object):

    def __init__(self, database):
        self.db = database
        self.publications = database.publications

    def add_publication(self, **kwargs):
        """
        insert publication.
        param: **kwargs
        return : true || false
        """

        #this piece is done for the not refeered publications, that some times can have 00 instead
        #of a valid month
        error = {'general': ''}

        if 'publication_obj' in kwargs.keys():
            publication = kwargs['publication_obj'].__dict__

        else:
            pub_date = datetime.strptime(kwargs["pub_date"], c.SHORT_DATE_FORMAT)
            # Build a new publication
            publication = { "title": unicode(kwargs["title"], 'utf-8', 'ignore'),
                            "author": kwargs["author"].decode('utf8', 'ignore'),
                            "authors_to_show": kwargs["authors_to_show"],
                            "ASI_authors": kwargs["ASI_authors"],

                            "project_mission": kwargs["project_mission"],
                            "project": kwargs.get("project", ""),
                            "contracts": kwargs.get("contracts", []),

                            "pub_date": pub_date,
                            "abstract": unicode(kwargs["abstract"], 'utf-8', 'ignore'),
                            "keyword": kwargs["keyword"],
                            "link": [kwargs["link"]],
                            "journal": kwargs["journal"],

                            "number": kwargs.get("number", ""),
                            "volume": kwargs.get("volume", ""),
                            "pages": kwargs.get("pages", ""),
                            "series": kwargs.get("series", ""),
                            "type": kwargs.get("type", 'Article Journal'),

                            "doi": kwargs.get("doi"),
                            "issn": kwargs.get("issn"),
                            "isbn": kwargs.get("isbn"),

                            "publisher": kwargs.get("publisher"),
                            "booktitle": kwargs.get("booktitle"),
                            "eventname": kwargs.get("eventname"),

                            'academic_year': kwargs.get("academic_year"),
                            'university': kwargs.get("university"),

                            'code': kwargs.get("code"),

                            "note": kwargs.get("note", "")
                       }


        publication = self.clean_publication_dictionary(publication)
        # now insert the publication
        try:
            self.publications.insert(publication)
        except pymongo.errors.DuplicateKeyError:
            error['general'] = "Publication %s already in the DB" % publication["title"]
        except pymongo.errors.OperationFailure:
            error['general'] = "Error inserting publication %s: %s" % (publication["title"], sys.exc_info()[0])

        return True, error

    def remove_publication(self, _id):

        try:

            print "removing publication %s" % _id

            self.publications.remove({'_id': bson.ObjectId(_id)})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    # return an array of publications still open sorting descending for pub_date, in short format
    def get_publications(self, **kwargs):

        pub, cursor = [], None
        query = {}
        sort_score = False
        options = {}

        kwargs_keys = kwargs.keys()
        if set(['type']).issubset(kwargs_keys):

            query['type'] = kwargs['type']

        if set(['start_date', 'end_date']).issubset(kwargs_keys):

            query['pub_date'] = {'$gte': kwargs['start_date'], '$lte': kwargs['end_date']}

        if set(['authors', 'condition_authors']).issubset(kwargs_keys):

            condition = kwargs['condition_authors']

            if condition == 'OR':
                query['author'] = {'$in': [re.compile(aut, re.IGNORECASE) for aut in kwargs['authors']]}

            elif condition == 'AND':
                query['$and'] = [dict(author={'$regex': auth, '$options': 'i'})for auth in kwargs['authors']]

        #search for single author
        if set(['author']).issubset(kwargs_keys):

            query['ASI_authors'] = kwargs['author']

        if set(['title']).issubset(kwargs_keys) and kwargs['title'].strip():

            # title has the text index on it
            query['$text'] = {'$search': kwargs['title']}
            options['score'] = {'$meta': "textScore"}
            sort_score = True

        if set(['projects_missions', 'condition_category']).issubset(kwargs_keys):

            condition = kwargs['condition_category']

            if condition == 'OR':
                query['project_mission'] = {'$in': [re.compile(p_m, re.IGNORECASE)for p_m in kwargs['projects_missions']]}

            elif condition == 'AND':
                query['$and'] = [dict(project_mission={'$regex': p_m, '$options': 'i'})for p_m in kwargs['projects_missions']]

        if set(['projects', 'condition_projects']).issubset(kwargs_keys):

            condition = kwargs['condition_projects']

            if condition == 'OR':
                query['project'] = {'$in': [re.compile(p, re.IGNORECASE) for p in kwargs['projects']]}

            elif condition == 'AND':
                query['$and'] = [dict(project={'$regex': p, '$options': 'i'})for p in kwargs['projects']]


        if set(['type', 'condition_type']).issubset(kwargs_keys):

            condition = kwargs['condition_type']

            if condition == 'OR':
                query['type'] = {'$in': [re.compile(t, re.IGNORECASE) for t in kwargs['type']]}

            elif condition == 'AND':
                query['$and'] = [dict(type={'$regex': t, '$options': 'i'})for t in kwargs['type']]


        if set(['doi']).issubset(kwargs_keys):

            query['doi'] = {'$regex': kwargs['doi'], '$options': 'i'}

        if set(['issn']).issubset(kwargs_keys):

            query['issn'] = {'$regex': kwargs['issn'], '$options': 'i'}

        if set(['isbn']).issubset(kwargs_keys):

            query['isbn'] = {'$regex': kwargs['isbn'], '$options': 'i'}

        if set(['keywords', 'condition_keywords']).issubset(kwargs_keys):

            condition = kwargs['condition_keywords']

            if condition == 'OR':
                query['keyword'] = {'$in': [re.compile(k, re.IGNORECASE) for k in kwargs['keywords']]}

            elif condition == 'AND':
                query['$and'] = [dict(keyword={'$regex': k, '$options': 'i'})for k in kwargs['keywords']]

        try:

            if sort_score:
                cursor = self.publications.find(query, options)
                cursor.sort([('score', {'$meta': 'textScore'})])

            else:
                cursor = self.publications.find(query).sort("pub_date", pymongo.DESCENDING)

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        for publication in cursor:
             pub.append({'id': publication['_id'],
                         'title': publication['title'],
                         'authors': publication['authors_to_show'],
                         'pub_date': publication['pub_date'].strftime(c.SHORT_DATE_FORMAT),
                         'type': publication["type"],
                         'ASI_authors': publication.get('ASI_authors', ''),
                         'project_mission': publication.get('project_mission', ''),
                         'project': publication.get('project', '')
                         })

        return pub


    def update_categories(self, _id, categories_list):

        try:
            self.publications.update({'_id': bson.ObjectId(_id)},
                                     {'$set': {'category': categories_list}})

        except pymongo.errors.OperationFailure:
            print "Mongo error, updating category in publication %s" % _id
            return False
        return True

    def update_projects(self, _id, projects_list):

        try:
            self.publications.update({'_id': bson.ObjectId(_id)},
                                     {'$set': {'project': projects_list}})

        except pymongo.errors.OperationFailure:
            print "Mongo error, updating project in publication %s" % _id
            return False
        return True

    def update_contracts(self, _id, contract_list):

        try:
            self.publications.update({'_id': bson.ObjectId(_id)},
                                     {'$set': {'contract': contract_list}})

        except pymongo.errors.OperationFailure:
            print "Mongo error, updating contracts in publication %s" % _id
            return False
        return True


    def update_publication(self, publication):

        try:
            _id = publication['_id']
            #then i have to remove, otherwhise it will not update
            del publication['_id']
            publication = self.clean_publication_dictionary(publication)
            self.publications.update({'_id': bson.ObjectId(_id)},
                                     publication)

        except pymongo.errors.OperationFailure:
            print "Mongo error, updating the whole publication %s" % _id
            return False
        return True


    def get_publication_id(self, id):

        return self.publications.find_one({'_id': bson.ObjectId(id)})


    def get_publications_type(self):

        r = self.publications.distinct('type')
        #to convert in a quick and dirty way unicode to str
        return ast.literal_eval(json.dumps(r))

    def clean_publication_dictionary(self, pub_to_save):
        """
        remove all empty fields from the dictionary before to save in DB
        :param pub_to_save:
        :return: dictionary clean
        """

        return (dict((k, v) for k, v in pub_to_save.items() if v))



