__author__ = 'fmoscato'

import cgi
from datetime import datetime
import time
import os.path
import argparse

import pymongo
import bottle


import publicationDAO
import sessionDAO
import userDAO
import project_missionDAO
import projectDAO
from admin import admin_app
from metrics import metric_app
from temporaryPublications import temporary_app
import constants as c
import pubUtilities as utilities
import PDF
import validatePublications
import authentication as auth


#app = bottle.default_app()
app = bottle.app()

app.mount('/admin/', admin_app)
app.mount('/metrics', metric_app)
#app.mount('/tmp_publications', temporary_app)

connection_string = ""
connection = pymongo.MongoClient(connection_string)
database = connection.publicationASI

publication = publicationDAO.PublicationDAO(database)
users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)
projects_missions = project_missionDAO.ProjectMissionDAO(database)
projects = projectDAO.ProjectDAO(database)

valide_user = auth.authenticator_user(sessions)
DOC_ROOT, TMP_DIR = '', ''


#this route the static files
@bottle.route('/static/:filename#.*#')
def server_static(filename):

    path_static = '%s/static' % DOC_ROOT
    try:
        if not os.path.exists(path_static+"/"+filename):
            return bottle.template("not_found")
    except Exception as e:
        return bottle.redirect("/internal_error")

    return bottle.static_file(filename, root=path_static)


@bottle.route('/pdf/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root=TMP_DIR)

#this route the js files
@bottle.route('/js/:filename#.*#')
def server_js(filename):

    path_js = '%s/js' % DOC_ROOT
    try:
        if not os.path.exists(path_js+"/"+filename):
            return bottle.template("not_found")
    except Exception as e:
        return bottle.redirect("/internal_error")

    return bottle.static_file(filename, root=path_js)


@bottle.error(404)
def error404(error):
    return bottle.template("not_found")

@bottle.error(500)
def error500(error):
    return bottle.template("error_template")

@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    return {'error': "System has encountered a DB error"}


# This route is the main page
@bottle.route('/')
def publication_index():

    #moved overview into metrics
    return bottle.redirect('overview')

# displays the initial login form
@bottle.get('/login')
def present_login():
    return bottle.template("login",
                           dict(username="", password="",
                                login_error=""))


# handles a login request
@bottle.post('/login')
def process_login():
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    user_record = users.validate_login(username, password)
    if user_record:
        # username is stored in the user collection in the _id key
        session_id = sessions.start_session(user_record['_id'], user_record['admin'])

        if not session_id:
            bottle.redirect("/internal_error")

        cookie = session_id
        bottle.response.set_cookie("session", cookie)

        if user_record['admin']:
            bottle.redirect("/admin")

        bottle.redirect("/welcome")

    else:
        return bottle.template("login",
                               dict(username=cgi.escape(username), password="",
                                    login_error="Invalid Login"))


@bottle.post('/forgot_password')
def forgot_password():
    return bottle.template('forgot_password')


@bottle.post('/recover_password')
def process_forgot_password():

    username = bottle.request.forms.get("username", "")
    user = users.get_user(username)

    if not user:
        return bottle.template("forgot_password", error="user not in DB. Please contact admin")

    if not users.create_tmp_password(user['username']):
        return bottle.template("forgot_password", error="error processing your request. Please contact admin")

    return bottle.template("message_template", msg="Password sent to your email address")

@bottle.get('/user_info')
def present_user_info():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    user_info = users.get_user(username)

    return bottle.template("user_info", user=user_info, username=username)


######################
### Publication part#
#####################


@bottle.get('/list_publications')
def present_publications_list():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    l = publication.get_publications()

    return bottle.template("publications_list", dict(publications=l, username=username,
                                                     is_admin=is_admin))


# Displays a particular publication selected by biblicode
@bottle.get("/pub_detail/<id>")
def show_publication(id="notfound"):
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    pub = publication.get_publication_id(id)

    if not pub:
        bottle.redirect("/publication_not_found")

    return bottle.template("publication_detail", dict(publication=pub,
                                                      username=username,
                                                      is_admin=is_admin,
                                                      errors=""))

@bottle.get("/publication_not_found")
def publication_not_found():
    return "Sorry, publication not found"


@bottle.post("/export_as_pdf")
def process_PDF():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    if not username: username = 'guest'

    filename = c.pdf_file_name + '_' + username + '_' + str(time.time())

    id_to_export = bottle.request.forms.getall("id")

    list_of_publication = [publication.get_publication_id(id)
                              for id in id_to_export]


    PDF.generatePDF(list_of_publication, filename, DOC_ROOT, TMP_DIR)

    return bottle.redirect("/pdf/%s.pdf" % filename)



@bottle.get("/query_details")
def process_search():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    year = bottle.request.query.get("year", None)
    type_publication = bottle.request.query.get("type", None)
    author = bottle.request.query.get("author", None)
    validate = validatePublications.ValidatePublications()
    options = {}

    if year:
        try:
            validate.validate_year(year)
            start_date = ('01/01/%s' % year)
            end_date = ('31/12/%s' % year)
        except validatePublications.ValidationException as e:
            return bottle.redirect("metrics_authors")

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        options.update(start_date=date_start, end_date=date_end)

    if type_publication:

        options.update(type=type_publication)

    if author:

        options.update(author=author)

    p = publication.get_publications(**options)

    return bottle.template("publications_list",
                            dict(publications=p, username=username, is_admin=is_admin))



#### search publications#############
### voglio mettere box autori - tips
#### voglio mettere  box missioni - tips + tendina
### ricerca su comtratto - tendina
### ricerca su progetti - tips + regex
### ricerca per giornale  - tips ??
#### ricerca per tipo -  tendina
### ricerca per titolo - con regex

@bottle.get("/search_publications")
def present_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    validate = validatePublications.ValidatePublications()

    #for authors tips { value: "one", label: "Einz" }
    authors = [dict(value=str(u['lastname']), label="%s - %s" % (str(u['lastname']).title(), str(u['name']).title()))
                for u in users.get_users()]
    # for project_missions tips
    projects_missions_list = [str(p['name']) for p in projects_missions.get_projects_missions()]
    # for projects tips
    projects_list = [str(p['name']) for p in projects.get_projects()]

    #publications types
    types = publication.get_publications_type()

    return bottle.template("search_publications", dict(username=username, authors=authors, projects=projects_list,
                                                       projects_missions=projects_missions_list, types=types,
                                                       is_admin=is_admin, errors=validate.errors,
                                                       mission="", start_date="", end_date=""))


@bottle.post("/search_publications")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    form_fields = {}

    ### form fields#########
    authors_string = bottle.request.forms.get("authors", "").strip()
    authors_array = []
    if authors_string:
        authors_array = authors_string.split(",")
        authors_array = [author.strip() for author in authors_array]
    condition_authors = bottle.request.forms.get("radio_authors")

    form_fields['authors'] = authors_array
    form_fields['condition_authors'] = condition_authors

    form_fields['title'] = bottle.request.forms.get("title", "").strip()

    start_date = bottle.request.forms.get("start_date", None)
    end_date = bottle.request.forms.get("end_date", c.END_DATE)

    ###### data control  for dates###################

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_dates(start_date, end_date)
    except validatePublications.ValidationException as e:
            #for authors tips { value: "one", label: "Einz" }
            authors = [dict(value=str(u['lastname']), label="%s - %s" % (str(u['lastname']).title(), str(u['name']).title()))
                       for u in users.get_users()]
            return bottle.template("search_publications", dict(username=username, authors=authors,
                                                               projects=[str(p['name']) for p in projects.get_projects()],
                                                               projects_missions=[str(p['name']) for p in
                                                                                  projects_missions.get_projects_missions()],
                                                               types=publication.get_publications_type(),
                                                               is_admin=is_admin, errors=validate.errors,
                                                               mission="", start_date=start_date, end_date=end_date))


    ################################################################


    if start_date:
        form_fields['start_date'] = datetime.strptime(start_date, c.DATE_FORMAT)
    if not end_date:
        end_date = c.END_DATE

    form_fields['end_date'] = datetime.strptime(end_date, c.DATE_FORMAT)

    project_missions_strig = bottle.request.forms.get("projects_missions", "")
    projects_missions_array = []
    if project_missions_strig:
        projects_missions_array = project_missions_strig.split(",")
    form_fields['projects_missions'] = projects_missions_array
    form_fields['condition_category'] = bottle.request.forms.get("radio_category")

    ######
    projects_string = bottle.request.forms.get("projects", "")
    projects_array = []
    if projects_string:
        projects_array = projects_string.split(",")
    form_fields['projects'] = projects_array
    form_fields['condition_projects'] = bottle.request.forms.get("radio_projects")

    types_string = bottle.request.forms.get("type", "")
    types_array = []
    if types_string:
        types_array = types_string.split(",")
    form_fields['type'] = types_array
    form_fields['condition_type'] = bottle.request.forms.get("radio_type")


    form_fields['doi'] = bottle.request.forms.get("doi", "").strip()
    form_fields['issn'] = bottle.request.forms.get("issn", "").strip()
    form_fields['isbn'] = bottle.request.forms.get("isbn", "").strip()

    keywords_string = bottle.request.forms.get("keywords", "")
    keywords_array = []
    if keywords_string:
        keywords_array = keywords_string.split(",")
        keywords_array = [k.strip() for k in keywords_array]
    form_fields['keywords'] = keywords_array
    form_fields['condition_keywords'] = bottle.request.forms.get("radio_keywords")

    ###### end of the form fields ###########

    p = publication.get_publications(**dict((k, v) for k, v in form_fields.items() if v))

    return bottle.template("publications_list",
                            dict(publications=p, username=username, is_admin=is_admin))





@bottle.get('/logout')
def process_logout():
    cookie = bottle.request.get_cookie("session")
    sessions.end_session(cookie)
    bottle.response.set_cookie("session", "")
    bottle.redirect("/login")


@bottle.get("/welcome")
def present_welcome():
    # check for a cookie, if present, then extract value

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        print "welcome: can't identify user...contact administrator to obtain user and pwd"
        bottle.redirect("/login")

    return bottle.template("welcome", {'username': username})


def run_server():
    #bottle.run(host='localhost', port=8084, reloader=True) #Start the webserver running and wait for requests
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8084')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='python publication.py will start the publications service')
    parser.add_argument('-d', '--dir', help='where to find the statics files', required=True)
    parser.add_argument('-t', '--tmp', help='tmp dir where to create pdf files', required=True)
    args = vars(parser.parse_args())

    DOC_ROOT = args['dir']
    TMP_DIR = args['tmp']

    bottle.debug(True)
    run_server()





