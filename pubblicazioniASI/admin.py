__author__ = 'fmoscato'

from datetime import datetime
import json
from collections import OrderedDict
from collections import defaultdict
import ast

import pymongo
import bottle

import authentication as auth
import publicationDAO
import sessionDAO
import userDAO

import config
import project_missionDAO
import projectDAO
import contractDAO
import pubUtilities as pU
import constants as c
import validatePublications
import ASI_authors



# create the app for the admin interface

admin_app = bottle.Bottle()

connection_string = config.MONGODB_URI
connection = pymongo.MongoClient(connection_string)
database = connection.publicationASI

publication = publicationDAO.PublicationDAO(database)
users = userDAO.UserDAO(database)
#####
projects_missions = project_missionDAO.ProjectMissionDAO(database)
projects = projectDAO.ProjectDAO(database)
contracts = contractDAO.ContractDAO(database)
######
sessions = sessionDAO.SessionDAO(database)
valid_admin = auth.authenticator(sessions)

"""
H1 -- Admin application
************************
Admin user is able to :


1- handle users
  - add user
  - change validity of the user
  - remove a user
  - list users

2-handle project_missions
  - add project_mission
  - remove a project_mission
  - list the project_missions

3 - handle a project
  - add project
  - remove a project
  - list the projects

4 - handle a contract
  - add contract
  - remove a contract
  - list the contract


5- handle publications
  - list valide publications for a period
  - search (for biblicode, DOI, author, mission, magazine)

6- add a publication

.. module:: admin.py
   :synopsis: application for the admin

"""


@bottle.get("/admin")
@valid_admin()
def present_admin():
    # check for a cookie, if present, then extract value

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    return bottle.template("admin", dict(username=username, msg='', errors=''))


########################
#                      #
#  admin user part     #
#                      #
########################

@bottle.get('/add_user')
@valid_admin()
def present_add_user():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    m_p = projects_missions.get_projects_missions()
    p = projects.get_projects()
    c = contracts.get_contracts()

    validate = validatePublications.ValidatePublications()

    return bottle.template("add_user",
                           dict(username=username, username_to_add="", password="",
                                password_error="", name="", lastname="",
                                start_date="", end_date="",
                                projects_missions=m_p, projects=p, contracts=c,
                                email="", errors=validate.errors, projects_selected="", missions_projects_selected=""))


@bottle.post('/add_user')
@valid_admin()
def process_add_user():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    username_to_add = bottle.request.forms.get("username")
    name = bottle.request.forms.get("name")
    lastname = bottle.request.forms.get("lastname")
    password = bottle.request.forms.get("password")
    verify = bottle.request.forms.get("verify")
    email = bottle.request.forms.get("email")
    m_p_selected = bottle.request.forms.getall("projects_missions")
    p_selected = bottle.request.forms.get("projects")
    c_selected = bottle.request.forms.get("contract", [])

    start_date = bottle.request.forms.get("start_date")
    end_date = bottle.request.forms.get("end_date", None)

    if not end_date:
        end_date = c.END_DATE

    m_p = projects_missions.get_projects_missions()
    p = projects.get_projects()
    con = contracts.get_contracts()

    # set these up in case we have an error case

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_signup(username_to_add, password, verify, email, start_date, end_date)
    except validatePublications.ValidationException as e:
        return bottle.template("add_user", dict(username=username,
                                                username_to_add=username_to_add, name=name, lastname=lastname,
                                                password=password, email=email, errors=validate.errors,
                                                start_date=start_date, end_date=end_date,
                                                projects_missions=m_p, projects=p, contracts=con,
                                                projects_selected=p_selected,
                                                missions_projects_selected=m_p_selected))

    if not users.add_user(username=username_to_add, name=name, lastname=lastname,
                          password=password, email=email,
                          start_date=datetime.strptime(start_date, c.DATE_FORMAT),
                          end_date=datetime.strptime(end_date, c.DATE_FORMAT),
                          contracts=c_selected, projects=p_selected, missions_projects=m_p_selected):
        # this was a duplicate
        validate.errors['username_error'] = 'username already taken'
        return bottle.template("add_user", dict(username=username,
                                                username_to_add=username_to_add, name=name, lastname=lastname,
                                                password=password, email=email,
                                                start_date=start_date, end_date=end_date, projects_missions=m_p,
                                                projects=p, contracts=con, projects_selected=p_selected,
                                                missions_projects_selected=m_p_selected))

    msg = "user <b>%s</b> added" % username_to_add
    return bottle.template("admin", dict(username=username, msg=msg, errors=''))


@bottle.get('/list_users')
@valid_admin()
def present_list():
    return bottle.template('users_list')


@bottle.get('/list_users')
@valid_admin()
def process_list():
    cookie = bottle.request.get_cookie("session")

    username = sessions.get_username(cookie)

    l = users.get_users()

    return bottle.template('users_list', dict(users=l,
                                              username=username))


@bottle.get('/json_projects_missions')
def present_json():
    only_categories = bottle.request.query.get('onlycategories', '')
    if only_categories:
        keys = OrderedDict((str(p_m['name']), p_m['name']) for p_m in projects_missions.get_projects_missions())
    else:
        keys = OrderedDict((str(p_m['id']), p_m['name']) for p_m in projects_missions.get_projects_missions())
    return json.dumps(keys)


@bottle.get('/json_projects')
def present_json():
    keys = OrderedDict(('%s|%s' % (p['project'], p['name']), p['name']) for p in projects.get_projects())
    return json.dumps(keys)


@bottle.get('/json_contracts')
def present_json():
    keys = OrderedDict((str(c['contract_id']), c['contract_name']) for c in contracts.get_contracts())
    return json.dumps(keys)


@bottle.get('/json_authors')
def present_json_authors():
    keys = OrderedDict((u['username'], u['name'] + " " + u['lastname']) for u in users.get_users())
    return json.dumps(keys)


#update is done by ajax
@bottle.post('/users_update_email')
def process_update():
    id = bottle.request.forms.get("user_id")
    user_id = id.split('-')[1]
    email = bottle.request.forms.get("email")

    if not users.update_email(user_id, email):
        return "error updating email"
    else:
        return email


@bottle.post('/users_update_projects_missions')
def process_missions_update():
    id = bottle.request.forms.get("user_id")
    user_id = id.split("-")[1]
    value = bottle.request.forms.get("projects_missions")

    projects_missions_list = value.split(",")

    if not users.update_projects_missions(user_id, projects_missions_list):
        return "error updating projects missions"
    else:
        return '<br>'.join(projects_missions_list)


@bottle.post('/users_update_projects')
def process_missions_update():
    id = bottle.request.forms.get("user_id")
    user_id = id.split("-")[1]
    value = bottle.request.forms.get("projects")

    projects_list = value.split(",")

    if not users.update_projects(user_id, projects_list):
        return "error updating projects "
    else:
        return '<br>'.join(projects_list)


@bottle.post('/users_update_contracts')
def process_missions_update():
    id = bottle.request.forms.get("user_id")
    user_id = id.split("-")[1]
    value = bottle.request.forms.get("contracts")

    contracts_list = value.split(",")

    if not users.update_contracts(user_id, contracts_list):
        return "error updating contract "
    else:
        return '<br>'.join(contracts_list)


@bottle.post('/close_users_validity')
@valid_admin()
def process_close_users_validity():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    users_to_close = bottle.request.forms.getlist("username")

    errors, msg = [], []
    msg_str, err_str = None, None

    for usr in users_to_close:

        if not users.close_validity_user(usr):
            errors.append(usr)
        else:
            msg.append(usr)

    if msg:
        msg_str = "closed the validity of the following users: %s " % '<br> '.join(msg)
    if errors:
        err_str = "error closing users validity for the following users: %s" % '<br>'.join(errors)

    return bottle.template("admin", dict(username=username, msg=msg_str, errors=err_str))


#remove is done by ajax
@bottle.post('/remove_user')
def process_remove():
    cookie = bottle.request.get_cookie("session")

    user_id = bottle.request.forms.get("user")

    if not users.remove_user(user_id):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body="success")


########################
#                      #
# Project_Mission part #
#                      #
########################


@bottle.get('/add_project_mission')
@valid_admin()
def present_add_project():
    username = bottle.request.forms.get("username")
    cookie = bottle.request.get_cookie("session")

    validate = validatePublications.ValidatePublications()

    return bottle.template("add_project_mission",
                           dict(username=username, project_mission="",
                                URL="",
                                error=validate.errors))


@bottle.post('/add_project_mission')
@valid_admin()
def process_add_mission():
    username = bottle.request.forms.get("username")

    project_mission = bottle.request.forms.get("project_mission")
    URL = bottle.request.forms.get("URL")

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_add_generic_form('project_mission', project_mission)
    except validatePublications.ValidationException as e:
        return bottle.template("add_project_mission", dict(username=username,
                                                           project_mission=project_mission,
                                                           URL=URL,
                                                           error=validate.errors))
    if not projects_missions.add_project_mission(name=project_mission, URL=URL):
        # this was a duplicate
        validate.errors['name_error'] = "Project Name already in use. Please choose another"
        return bottle.template("add_project_mission", dict(username=username,
                                                           project_mission=project_mission, URL=URL,
                                                           error=validate.errors))
    msg = "category/area <b>%s</b> added " \
          "<br> add new <a href='/add_project_mission'>category/area </a>" % project_mission
    return bottle.template("admin", dict(username=username, msg=msg, errors=''))


@bottle.get('/list_mission_projects')
@bottle.post('/list_mission_projects')
@valid_admin()
def present_list():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in

    p_m = projects_missions.get_projects_missions()

    return bottle.template('list_mission_projects', dict(projects_missions=p_m, username=username, msg=""))


@bottle.post('/remove_missions_project')
@valid_admin()
def process_remove():
    project_mission = bottle.request.forms.get("project_mission")

    if not projects_missions.remove_project_mission(project_mission):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body='success')


########################
#                      #
#   Projects part      #
#                      #
########################


@bottle.get('/add_project')
@valid_admin()
def present_add_mission():
    username = bottle.request.forms.get("username")

    validate = validatePublications.ValidatePublications()
    project_missions_lists = projects_missions.get_projects_missions()

    return bottle.template("add_project",
                           dict(username=username, project="", URL="",
                                projects_missions=project_missions_lists,
                                error=validate.errors))


@bottle.post('/add_project')
@valid_admin()
def process_add_project():
    username = bottle.request.forms.get("username")

    project = bottle.request.forms.get("project")
    URL = bottle.request.forms.get("URL")
    project_mission = bottle.request.forms.get("project_mission")
    project_missions_lists = projects_missions.get_projects_missions()

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_add_generic_form('project', project)
    except validatePublications.ValidationException as e:
        return bottle.template("add_project", dict(username=username,
                                                   project=project,
                                                   URL=URL,
                                                   project_mission=project_mission,
                                                   projects_missions=project_missions_lists,
                                                   error=validate.errors))
    if not projects.add_project(project_name=project, URL=URL, project_mission=project_mission):
        # this was a duplicate
        validate.errors['name_error'] = "Project Name already in use. Please choose another"
        return bottle.template("add_mission", dict(username=username,
                                                   project=project, URL=URL,
                                                   project_mission=project_mission,
                                                   projects_missions=project_missions_lists,
                                                   error=validate.errors))
    msg = "project/mission <b>%s</b> added" \
          "<br> add new <a href='/add_project'> project/mission </a>" % project
    return bottle.template("admin", dict(username=username, msg=msg, errors=''))


@bottle.get('/list_projects')
@bottle.post('/list_projects')
@valid_admin()
def present_list():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in

    p = projects.get_projects()
    p_m = projects_missions.get_projects_missions()

    return bottle.template('projects_list', dict(projects=p, projects_missions=p_m, username=username, msg=""))


@bottle.post('/remove_project')
@valid_admin()
def process_remove():
    project = bottle.request.forms.get("project")

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    if not projects.remove_project(project):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body='success')


########################
#                      #
#   Contract part      #
#                      #
########################


@bottle.get('/add_contract')
@valid_admin()
def present_add_project():
    username = bottle.request.forms.get("username")

    validate = validatePublications.ValidatePublications()

    return bottle.template("add_contract",
                           dict(username=username, contract_id="",
                                contract_name="",
                                contract_type="", institution="",
                                projects=projects.get_projects(),
                                start_date="", end_date="",
                                error=validate.errors))


@bottle.post('/add_contract')
@valid_admin()
def process_add_project():
    username = bottle.request.forms.get("username")

    project = bottle.request.forms.get("project")

    contract_id = bottle.request.forms.get("contract_id")
    contract_name = bottle.request.forms.get("contract_name")

    contract_type = bottle.request.forms.get("contract_type")
    institution = bottle.request.forms.get("institution")

    start_date = bottle.request.forms.get("start_date")
    end_date = bottle.request.forms.get("end_date", None)
    is_active = pU.str2bool(bottle.request.forms.get("is_active"))
    projects_list = projects.get_projects()

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_add_contract(contract_id, contract_name, start_date, end_date)
    except validatePublications.ValidationException as e:
        return bottle.template("add_contract", dict(username=username,
                                                    contract_id=contract_id,
                                                    contract_name=contract_name, contract_type=contract_type,
                                                    project=project,
                                                    projects=projects_list,
                                                    institution=institution,
                                                    start_date=start_date, end_date=end_date,
                                                    error=validate.errors))

    if not contracts.add_contract(contract_id=contract_id, project=project, contract_name=contract_name,
                                  contract_type=contract_type, institution=institution,
                                  start_date=start_date, is_active=is_active, end_date=end_date):
        # this was a duplicate
        validate.errors['name_error'] = "Contract id already in use. Please choose another"
        return bottle.template("add_contract", dict(username=username,
                                                    contract_id=contract_id,
                                                    contract_name=contract_name, contract_type=contract_type,
                                                    project=project,
                                                    projects=projects_list,
                                                    institution=institution,
                                                    start_date=start_date, end_date=end_date,
                                                    error=validate.errors))

    msg = "Contract  <b>%s</b> added" % contract_name
    return bottle.template("admin", dict(username=username, msg=msg, errors=''))


@bottle.get('/list_contracts')
@bottle.post('/list_contracts')
@valid_admin()
def process_list():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    c = contracts.get_contracts()
    p = projects.get_projects()

    return bottle.template('contracts_list', dict(contracts=c, projects=p, username=username, msg=""))


@bottle.post('/remove_contract')
@valid_admin()
def process_remove():
    contract = bottle.request.forms.get("contract").replace("_", "/")

    if not contracts.remove_contract(contract):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body='success')


@bottle.post('/contracts_update_projects')
def process_missions_update():
    id = bottle.request.forms.get("contract_id")
    contract_id = id.split("|")[1]
    value = bottle.request.forms.get("project")
    id_project, project_name = value.split("|")

    if not contracts.update_projects(contract_id, id_project):
        return "error updating projects "
    else:
        return project_name


########################
#                      # 
#   Publications part  #
#                      #
########################

def set_default_values_publication():

     default_values = {'title': '',
                      'author': '',
                      'pub_date': '',
                      'journal': '',
                      'link': [],
                      'abstract': '',
                      'keyword': '',
                      'doi': '',
                      'issn': '',
                      'isbn': '',
                      'type': '',
                      'number': '',
                      'volume': '',
                      'note': '',
                      'booktitle': '',
                      'eventname': '',
                      'publisher': '',
                      'academic_year': '',
                      'university': '',
                      'code': ''}

     return default_values


def fill_form_values(forms):

    return {'title': pU.clean_string(forms.get("title")),
                   'author': pU.clean_string(forms.get("author")),
                   'pub_date': forms.get("pub_date"),
                   'journal': forms.get("journal"),
                   'link': pU.clean_string(forms.get("link")),
                   'abstract': pU.clean_string(forms.get("abstract", "")),
                   'keyword': pU.clean_string(forms.get("keyword", "")),
                   'contracts': forms.getall("contracts"),
                   'project_mission': forms.getall('project_mission'),
                   'project': forms.getall('project'),
                   'type': forms.get('type'),
                   'doi': forms.get('doi'),
                   'issn': forms.get('issn'),
                   'isbn': forms.get('isbn'),
                   'number': forms.get('number'),
                   'volume': forms.get('volume'),
                   'note': pU.clean_string(forms.get('note', '')),
                   'booktitle': forms.get('booktitle'),
                   'eventname': forms.get('eventname'),
                   'publisher':  forms.get('publisher'),
                   'academic_year': forms.get('academic_year'),
                   'university': forms.get('university'),
                   'code': forms.get('code')
    }


def set_utilities_values_publication():

    """

    :rtype : dict
    """
    c_list = contracts.get_contracts()
    p_m_list = projects_missions.get_projects_missions()
    area_convertor = {p_m['id']: p_m['name'] for p_m in p_m_list}
    p_list = projects.get_projects()

    projects_per_category = defaultdict(list)
    for p in p_list:
        projects_per_category[area_convertor[p['project_mission']]].append(p['name'])


    return dict(projects_missions=p_m_list,  projects=projects_per_category,
                contracts=c_list)



@bottle.get('/add_publication')
@valid_admin()
def present_add_publication():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    ptypes = publication.get_publications_type()
    validate = validatePublications.ValidatePublications()

    utilities_values = set_utilities_values_publication()
    utilities_values.update({'errors': validate.errors})


    return bottle.template("add_publication", dict(username=username,
                                                   utilities_values=utilities_values,
                                                   ptypes=ptypes,
                                                   publication=set_default_values_publication()))


@bottle.post('/add_publication')
@valid_admin()
def process_add_publication():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    ptypes = publication.get_publications_type()

    form_values = fill_form_values(bottle.request.forms)

    form_values['authors_to_show'], form_values['ASI_authors'] = ASI_authors.clean_author(
        form_values['author'], pU.get_users_list_controll(users.get_users()))

    utilities_values = set_utilities_values_publication()

    validate = validatePublications.ValidatePublications()
    try:
        validate.validate_publication_form(form_values)
    except validatePublications.ValidationException as e:
        utilities_values.update({'errors': validate.errors})
        return bottle.template("add_publication", dict(username=username, ptypes=ptypes,
                                                       publication=form_values,
                                                       utilities_values=utilities_values))

    # publication to add looks fine -> adding publication

    add, errors = publication.add_publication(**form_values)
    if not add:
        utilities_values.update({'errors': errors})
        return bottle.template("add_publication", dict(username=username, ptypes=ptypes,
                                                       utilities_values=utilities_values,
                                                       publication=form_values))
    msg = " Publication: <br> <b> %s </b> added" \
          "<br> add new <a href='/add_publication'> publication</a>" % form_values['title']
    return bottle.template("welcome", dict(username=username, msg=msg, is_admin=True))


@bottle.get('/modify_publications')
@valid_admin()
def show_modify_valid_publication():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    default_errors = {'start_date_error': "", 'end_date_error': ""}

    return bottle.template('modify_publications', dict(username=username,
                                                       start_date="", end_date="",
                                                       errors=default_errors))


@bottle.post('/modify_publications')
@valid_admin()
def process_modify_publications():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    start_date_str = bottle.request.forms.get("start_date")
    end_date_str = bottle.request.forms.get("end_date")
    title = bottle.request.forms.get('title')

    validate = validatePublications.ValidatePublications()

    if start_date_str:
        try:
            validate.validate_dates(start_date_str, end_date_str)
        except validatePublications.ValidationException as e:
            return bottle.template("modify_publications", {'username': username,
                                                           'start_date': start_date_str,
                                                           'end_date': end_date_str, 'errors': validate.errors})

        if not end_date_str:
           end_date_str = c.END_DATE

        start_date = datetime.strptime(start_date_str, c.DATE_FORMAT)
        end_date = datetime.strptime(end_date_str, c.DATE_FORMAT)

        pub = publication.get_publications(start_date=start_date, end_date=end_date, title=title)

    else:

        pub = publication.get_publications(title=title)

    return bottle.template('publications_list_to_modify', dict(publications=pub, username=username))


#remove is done by ajax
@bottle.post('/remove_publication')
@valid_admin()
def process_remove():
    id = bottle.request.forms.get("id")

    if not publication.remove_publication(id):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body="success")


@bottle.post('/publications_update_category')
@valid_admin()
def process_missions_update():
    id = (bottle.request.forms.get("id").split("-"))[1]
    value = bottle.request.forms.get("categories")
    category_list = value.split(",")

    if not publication.update_categories(id, category_list):
        return "error updating missions"
    else:
        return '<br>'.join(category_list)


@bottle.post('/publications_update_projects')
@valid_admin()
def process_missions_update():
    id = (bottle.request.forms.get("id").split("-"))[1]
    projects_list = bottle.request.forms.get("projects").split(",")

    projects_list = [p.split("|")[1] for p in projects_list]

    if not publication.update_projects(id, projects_list):
        return "error updating projects"
    else:
        return '<br>'.join(['%s' % p for p in projects_list])





@bottle.get("/modify_publication_detail/<id>")
@valid_admin()
def show_publication_to_modify(id="notfound"):
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    asi_authors = [dict(name="%s %s" % (u['name'].title(),
                                        u['lastname'].title()), value=u['lastname'].lower()) for u in users.get_users()]

    pub = publication.get_publication_id(id)

    if not pub:
        bottle.redirect("/publication_not_found")

    validate = validatePublications.ValidatePublications()
    utilities_values = set_utilities_values_publication()
    utilities_values.update({'errors': validate.errors})
    utilities_values.update({'asi_authors': asi_authors})


    return bottle.template("update_publication", dict(publication=pub,
                                                      username=username,
                                                      is_admin=is_admin,
                                                      ptypes=publication.get_publications_type(),
                                                      utilities_values=utilities_values))

@bottle.post('/update_publication')
@valid_admin()
def process_update_publication():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    ptypes = publication.get_publications_type()

    form_values = fill_form_values(bottle.request.forms)

    form_values['authors_to_show'] = bottle.request.forms.get('authors_to_show', '')
    form_values['ASI_authors'] = bottle.request.forms.getall('asi_authors')
    form_values['_id'] = bottle.request.forms.get('_id')


    validate = validatePublications.ValidatePublications()
    try:
        validate.validate_publication_update(form_values)
    except validatePublications.ValidationException as e:
        utilities_values = set_utilities_values_publication()
        utilities_values.update({'errors': validate.errors})
        asi_authors = [dict(name="%s %s" % (u['name'].title(),
                            u['lastname'].title()), value=u['lastname'].lower()) for u in users.get_users()]
        utilities_values.update({'asi_authors': asi_authors})
        form_values['pub_date'] = datetime.strptime(form_values['pub_date'], c.SHORT_DATE_FORMAT)
        return bottle.template("update_publication", dict(username=username, ptypes=ptypes,
                                                          publication=form_values,
                                                          utilities_values=utilities_values))

    # have to override the link tag - since there is a different handling
    form_values['link'] = form_values['link'].split()

    # go to confirmation page
    return bottle.template("publication_detail_confirm", dict(username=username, publication=form_values,
                                                             is_admin=True))


@bottle.post('/confirm_update')
@valid_admin()
def process_confirm_update():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    publication_to_update = bottle.request.forms.get('publication')

    # few tuning before to go in DB

    pub_to_save = ast.literal_eval(publication_to_update)
    pub_to_save['pub_date'] = datetime.strptime(pub_to_save['pub_date'], c.SHORT_DATE_FORMAT)

    msg = ''
    if not publication.update_publication(pub_to_save):
        msg = 'error updating the publication. Please contact admin'
    else:
        msg = "Publication <b>%s</b> updated. <br>" \
              " Return to the " \
              "<a href='/modify_publications'>modification page</a>" % pub_to_save['title']

    return bottle.template("welcome", dict(username=username, is_admin=True, msg=msg))













