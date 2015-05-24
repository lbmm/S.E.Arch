__author__ = 'federicamoscato'

import pymongo
import bibtexparser
from datetime import  datetime

import pubblicazioniASI.publicationDAO as publicationDAO
import pubblicazioniASI.userDAO as userDAO
import pubblicazioniASI.ASI_authors as ASI_authors
import pubblicazioniASI.pubUtilities as pu

FILE_TO_LOAD = 'documentations/Mendeley2202.bib'

connection_string = ""
connection = pymongo.MongoClient(connection_string)
database = connection.publicationASI
publications = publicationDAO.PublicationDAO(database)
users = userDAO.UserDAO(database)
users_list_controll = {user['lastname'].lower(): user['name'].lower() for user in users.get_users()}


class InsertError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PrePublication(object):

    def __init__(self, bib):
        self.author = bib.get('author', '')
        self.authors_to_show, self.ASI_authors = ASI_authors.clean_author(self.author, users_list_controll)
        self.title = pu.clean_from_latex(bib['title'])
        self.abstract = pu.clean_from_latex(bib.get('abstract', ''))
        self.journal = pu.clean_from_latex(bib.get('journal', ''))
        pub_date_str = '%s/%s' % (bib.get('month', 'jan'), bib.get('year', 1970))
        self.pub_date = datetime.strptime(pub_date_str, "%b/%Y")
        self.keyword = pu.clean_from_latex(bib.get('keyword', ''))
        self.link = pu.handle_url(bib.get('link', ''))

class Publication(PrePublication):

    def __init__(self, bib):
        super(Publication, self).__init__(bib)
        #IDs
        self.isbn = bib.get('isbn', '')
        self.issn = bib.get('issn', '')
        self.doi = bib.get('doi', '')
        self.number = bib.get('number', '') #issue
        self.volume = bib.get('volume', '')
        self.type = 'Article Journal'

class BookPublication(Publication):

    def __init__(self, bib):

        super(BookPublication, self).__init__(bib)
        self.publisher = bib.get('publisher', '')
        self.volume = bib.get('volume', '')
        self.booktitle = bib.get('booktitle', '')
        self.series = bib.get('series', '')
        self.pages = bib.get('pages', '')
        self.type = 'Book'


class Inproceedings(Publication):

    def __init__(self, bib):

        super(Inproceedings, self).__init__(bib)
        self.booktitle = bib.get('booktitle', '')
        self.publisher = bib.get('publisher', '')
        self.doi = bib.get('doi', '')
        self.type = 'Conference Proceedings'

class InCollection(BookPublication):

    def __init__(self, bib):

        super(InCollection, self).__init__(bib)
        self.type = 'Book Section'


class TechReport(object):

     def __init__(self, bib):

        self.title = pu.clean_from_latex(bib['title'])
        self.booktitle = bib.get('booktitle', '')
        self.author = bib.get('author', '')
        self.authors_to_show, self.ASI_authors = ASI_authors.clean_author(self.author, users_list_controll)
        self.abstract = pu.clean_from_latex(bib.get('abstract', ''))
        self.link = pu.handle_url(bib.get('link', ''))
        pub_date_str = '%s/%s' % (bib.get('month', 'jan'), bib.get('year', 1970))
        self.pub_date = datetime.strptime(pub_date_str, "%b/%Y")
        self.keyword = pu.clean_from_latex(bib.get('keyword', ''))
        self.volume = bib.get('volume', '')
        self.number = bib.get('number', '')
        self.type = 'Report'

class PhdThesis(TechReport):

    def __init__(self, bib):
        super(PhdThesis, self).__init__(bib)
        self.type = 'Thesis'

class Misc(Publication):

    def __init__(self, bib):
        super(Misc, self).__init__(bib)
        self.booktitle = bib.get('booktitle', '')
        self.type = 'misc'

class Unpublished(PrePublication):

    def __init__(self, bib):
        super(Unpublished, self).__init__(bib)
        self.type = "unpublished"


def loadPublication(type, bib):

    return {
        'article': Publication(bib),
        'inproceedings': Inproceedings(bib),
        'incollection': InCollection(bib),
        'techreport': TechReport(bib),
        'phdthesis': PhdThesis(bib),
        'unpublished': Unpublished(bib),
        'book': BookPublication(bib),
        'misc': Misc(bib)
    }.get(type)


def main():

    print 'starting to load publications from Mendley in DB'
    with open(FILE_TO_LOAD) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    for i, bib in enumerate(bib_database.entries):
        try:
            type = bib.get('type', '')
            if not publications.add_publication(publication_obj=loadPublication(type, bib)):
                raise InsertError("error inserting publication ")
            print i
        except InsertError as e:
                print e.value

    #print type_bib
    print "end of load all the publications"


if __name__ == '__main__':

    main()

