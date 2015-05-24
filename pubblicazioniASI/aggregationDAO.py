__author__ = 'fmoscato'

from datetime import datetime
from collections import OrderedDict
from itertools import groupby
from operator import itemgetter

import pymongo

import constants as c




# The Aggregation DAO  handles interactions with the publication collection,
# and aggregate the results.

class AggregationDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.publications = database.publications
        self.missions = database.missions
        self.users = database.users



    def aggregatePublicationsTimeline(self):

        pipe = [{'$project': {'year': {'$year': "$pub_date"},
                              'type': '$type'}},
                {'$group': {'_id': {'year': '$year',  'type': '$type'},
                            'count': {'$sum': 1}}},
                {'$sort': {'_id.year': 1}}]

        res = self.publications.aggregate(pipeline=pipe)
        types = self.publications.distinct('type')

        result = OrderedDict()
        old_year = None
        for r in res['result']:
            year = r['_id']['year']

            # we ended the cycle of the year
            if old_year != year:
                if not result:
                    result[year] = {t: 0 for t in types}

                else:
                    result[year] = {t_data: (result[old_year][t_data]) for t_data in result[old_year]}
                old_year = year

            result[year][r['_id']['type']] = result[year][r['_id']['type']] + r['count']

        return result


    """
    Aggregation of Author/type.
    Could be for year or overall
    :param
    :return
    """

    def aggregateAuthor(self, **kwargs):

        authors = []
        pipe = None

        try:
            if set(['year', 'pub_type']).issubset(kwargs.keys()):

                date_start = datetime.strptime('01/01/%s' % kwargs['year'], c.DATE_FORMAT)
                date_end = datetime.strptime('31/12/%s' % kwargs['year'], c.DATE_FORMAT)

                pipe = [{'$unwind': '$ASI_authors'},
                        {'$match': {'type': kwargs['pub_type'],
                                    'pub_date': {'$gte': date_start, '$lte': date_end}}},
                        {'$project': {'ASI_authors': 1}},
                        {'$group': {'_id': '$ASI_authors', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]

            elif 'pub_type' in kwargs:

                pipe = [{'$unwind': '$ASI_authors'},
                        {'$match': {'type': kwargs['pub_type']}},
                        {'$project': {'ASI_authors': 1}},
                        {'$group': {'_id': '$ASI_authors', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]
            elif 'year' in kwargs:

                date_start = datetime.strptime('01/01/%s' % kwargs['year'], c.DATE_FORMAT)
                date_end = datetime.strptime('31/12/%s' % kwargs['year'], c.DATE_FORMAT)

                pipe = [{'$unwind': '$ASI_authors'},
                        {'$match': {'pub_date': {'$gte': date_start, '$lte': date_end}}},
                        {'$project': {'ASI_authors': 1}},
                        {'$group': {'_id': '$ASI_authors', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]
            else:

                pipe = [{'$unwind': '$ASI_authors'},
                        {'$project': {'ASI_authors': 1}},
                        {'$group': {'_id': '$ASI_authors', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]


            res = self.publications.aggregate(pipeline=pipe)

            for j in res['result']:

                authors.append({"author": j["_id"], "count": j["count"]})

        except pymongo.errors.OperationFailure:
            print "Mongo error, aggregating publications"

        return authors



    def aggregateMission(self, is_refeered=True, year=None):

        missions = []
        pipe = None

        try:

            if year:

                date_start = datetime.strptime('01/01/%s' % year, c.DATE_FORMAT)
                date_end = datetime.strptime('31/12/%s' % year, c.DATE_FORMAT)

                pipe = [{'$unwind': '$mission'},
                        {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                    'asdc_auth.validate': True,
                                    'pub_date': {'$gte': date_start, '$lte': date_end}}},
                        {'$project': {'mission': 1}},
                        {'$group': {'_id': '$mission', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]

            else:

                pipe = [{'$unwind': '$mission'},
                        {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                    'asdc_auth.validate': True}},
                        {'$project': {'mission': 1}},
                        {'$group': {'_id': '$mission', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]

            res = self.publications.aggregate(pipeline=pipe)

            for j in res['result']:

                missions.append({"mission": j["_id"], "count": j["count"]})

        except pymongo.errors.OperationFailure:
            print "Mongo error, aggregating publications"

        return missions

    def aggregateMissionsAuthor(self, mission, is_refeered=True):

        author_per_mission = []

        pipe = [{'$unwind': '$asdc_auth'},
                {'$match': {'is_refeered': is_refeered, 'is_open': False, 'asdc_auth.validate': True,
                            'mission': mission}},
                {'$project': {'asdc_auth.author': 1}},
                {'$group': {'_id': '$asdc_auth.author', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}]

        try:

            res = self.publications.aggregate(pipeline=pipe)

            for j in res['result']:

                author_per_mission.append({"author": j["_id"], "count": j["count"]})

        except pymongo.errors.OperationFailure:
            print "Mongo error, aggregating publications"

        return author_per_mission


    def get_publications_type(self):

        return self.publications.distinct('type')

    def aggregateYearHistogram(self, author=None):


        publications_per_year = []
        pipe = None

        types = self.get_publications_type()

        if not author:

            pipe = [{'$project': {'year': {'$year': '$pub_date'}, 'type': 1}},
                    {"$group": {"_id": {'year': '$year', 'type': "$type"},
                                "typecount": {'$sum': 1}}},
                    {"$group": {"_id": "$_id.year",
                                "type": {"$push": {"type": "$_id.type",
                                                   "count": "$typecount"}}}},
                    {'$sort': {'_id': 1}}]


        else:
             pipe = [{'$unwind': '$ASI_authors'},
                     {'$match': {'ASI_authors': author}},
                     {'$project': {'year': {'$year': '$pub_date'}, 'type': 1}},
                     {"$group": {"_id": {'year': '$year', 'type': "$type"},
                                 "typecount": {'$sum': 1}}},
                     {"$group": {"_id": "$_id.year",
                                 "type": {"$push": {"type": "$_id.type",
                                                    "count": "$typecount"}}}},
                     {'$sort': {'_id': 1}}]


        res = self.publications.aggregate(pipeline=pipe)

        for r in res['result']:
            not_present_types = [item for item in types if item not in
                                 [types_db['type'] for types_db in r['type']]]
            year = r['_id']

            types_count = {t: 0 for t in not_present_types}
            types_count.update({types_db['type']: types_db['count'] for types_db in r['type']})
            types_count.update({'year': year})

            publications_per_year.append(types_count)

        return publications_per_year

    def aggregateCountAuthors(self):

        authors_count = OrderedDict()

        for y in reversed(c.years):

            if y == 2000 : continue

            start_date = datetime.strptime("01/01/%s" % y, c.DATE_FORMAT)
            end_date = datetime.strptime("31/12/%s" % y, c.DATE_FORMAT)

            pipeline = [{'$match': {'start_date': {'$lte': start_date}, 'end_date': {'$gte': end_date}}},
                        {'$project': {'_id': 1}}, {'$group': {'_id': '_id', 'count': {'$sum': 1}}}]

            res = self.users.aggregate(pipeline=pipeline)

            results = res['result']

            if results:
               authors_count[y] = results[0]['count']
            else:
                authors_count[y] = 0

        return authors_count



















