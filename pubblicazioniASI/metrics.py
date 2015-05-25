__author__ = 'fmoscato'

#Router for the metrics pages

from datetime import datetime

import pymongo
import bottle

import config
import aggregationDAO
import sessionDAO
import userDAO
import publicationDAO
import constants as c
import validatePublications



#create the app for the metrics interface

metric_app = bottle.Bottle()

@bottle.get('/metrics_authors')
def process_journal():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    year = bottle.request.query.get("year", None)
    author = bottle.request.query.get("author", None)
    ptype = bottle.request.query.get("ptype", None)

    if year:
        validate = validatePublications.ValidatePublications()
        try:
            validate.validate_year(year)
        except validatePublications.ValidationException as e:
            print "guffy year for metrics authors: resetting to null"
            year = None

    options1 = {}
    options = {'pub_type': ptype}
    aggregation_year_type = None
    if year:
        options1 = {'year': year}
        options.update({'year': year})


    #aggregation per year
    aggregation_year = metrics.aggregateAuthor(**options1)

    if ptype:
       #aggregatio per year and type
       aggregation_year_type = metrics.aggregateAuthor(**options)

    # i need information regarding authors: this information is
    #already stored in the aggregate author method

    authors = sorted([f['author'] for f in aggregation_year])
    complete_authors = users.get_users("%B %d, %Y")
    histogram_year = metrics.aggregateYearHistogram(author)
    types = publications.get_publications_type()


    return bottle.template('authors_metrics', dict(aggregation_year=aggregation_year,
                                                   aggregation_year_type=aggregation_year_type,
                                                   histogram_year=histogram_year,
                                                   types=types, ptype=ptype,
                                                   username=username, years=c.years,
                                                   year=year, complete_authors=complete_authors,
                                                   today=(datetime.today().date()).strftime("%B %d, %Y"),
                                                   authors=authors, author=author, is_admin=is_admin))


@bottle.get('/metrics_missions')
def process_journal():
    cookie = bottle.request.get_cookie("session")
    pass


@bottle.get('/ASI_overview')
def process_ASI_overview():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    overview = metrics.aggregatePublicationsTimeline()

    return bottle.template('asi_overview', dict(overview=overview, username=username, is_admin=is_admin))


@bottle.get('/overview')
def present_overview():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    histogram_year = metrics.aggregateYearHistogram()
    types = metrics.get_publications_type()

    return bottle.template('overview', dict(histogram_year=histogram_year,
                                            types=types, username=username, is_admin=is_admin))





connection_string = config.MONGODB_URI
connection = pymongo.MongoClient(connection_string)
database = connection.publicationASI


sessions = sessionDAO.SessionDAO(database)
metrics = aggregationDAO.AggregationDAO(database)
publications = publicationDAO.PublicationDAO(database)
users = userDAO.UserDAO(database)


