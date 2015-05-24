__author__ = 'federicamoscato'

def clean_author(string_authors, users_lastnames_names):

    repls = {"\\`{": "", "\\'{": "", '{': '', '}': "", '\\`': "",
             "\'": "", '\~': '', "\"": "", "\\": ""}

    repls_names = {".": "", ",":""}

    authors_asi = []
    try:
       #e' questa finalmente la formula magica per gli unicode !!!!!!
       string_authors = string_authors.encode('utf-8', 'ignore').decode('ascii', 'ignore')
       authors_string = reduce(lambda a, kv: a.replace(*kv), repls.iteritems(), string_authors)
       users_list_lastname = users_lastnames_names.keys()
    except UnicodeDecodeError, e:
        print e
        return string_authors, authors_asi

    array_authors = authors_string.split(" and ")
    if len(array_authors) < 2:
        array_authors = authors_string.split(";")
    if len(array_authors) < 2:
        array_authors = authors_string.split(",")

    authors_cleaned = []

    ASI_aut = False

    for index, authors in enumerate(array_authors):
        try:
            authors.encode('ascii', 'ignore')
            name, lastname = '', ''
            authors = authors.strip()
            if ',' in authors:
                lastname, name = authors.split(",", 1)
            elif '.' in authors:
                name, lastname = authors.rsplit(".", 1)
            elif ';' in authors:
                lastname, name = authors.rsplit(";", 1)


            elif ' ' in authors:
                name,lastname = authors.rsplit(" ", 1)



            lastname = lastname.lower()
            name = reduce(lambda a, kv: a.replace(*kv), repls_names.iteritems(), name.lower())


        except Exception as e:
            print e
            print "error on the authors name".join([authors]).encode('utf-8').strip()
            authors_cleaned.append('ASI collaboration')
            continue


        if index < 3:

            if lastname in users_list_lastname:

                if users_lastnames_names[lastname].startswith(name.strip()):
                    authors = "<b> %s </b>" % authors
                    authors_asi.append(lastname)
                    ASI_aut = True

            authors_cleaned.append(authors)

        else:

            if lastname in users_list_lastname:
                if users_lastnames_names[lastname].startswith(name.strip()):
                    authors_cleaned.append('...<b>%s</b>' % authors)
                    authors_asi.append(lastname)
                    ASI_aut = True

    controll_char = (authors_cleaned[-1].replace("<b>", "")).replace("</b>", "").replace("...", "")
    if not authors_string.endswith(controll_char):
          authors_cleaned.append(' et al.')

    if not ASI_aut:
        authors_cleaned.append('- <b>ASI Sponsor</b>')

    return ' ; '.join(authors_cleaned), authors_asi











