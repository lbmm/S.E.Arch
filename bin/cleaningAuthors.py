__author__ = 'fmoscato'


import pymongo
import bson


auhtor_to_controll = ['giommi', 'cavazzuti']
author_to_eliminate = 'longo'

title_array = ['fermi', 'agile', 'grb', 'gamma']
title = 'gamma'



class CleaningDAO(object):

    def __init__(self, database):
        self.db = database
        self.publications = database.publications


    def find_authors(self):

        for auth in auhtor_to_controll:

            cursor = self.publications.find({'$and': [{'ASI_authors': {'$in' :[auth]}},
                                            {'ASI_authors': {'$in':[author_to_eliminate]}}]})



            for publication in cursor:

                string_to_clean = publication['authors_to_show']
                string_array = string_to_clean.split("...")
                new_string = []

                for authors_in_bold in string_array:

                    if author_to_eliminate in authors_in_bold.lower():
                        continue

                    new_string.append(authors_in_bold)


                publication['authors_to_show'] = ''.join(new_string)
                publication['ASI_authors'] = [x for x in publication['ASI_authors'] if x != author_to_eliminate]
                print publication['authors_to_show']
                print publication['ASI_authors']

                _id = publication['_id']
              #then i have to remove, otherwhise it will not update
                del publication['_id']
                self.publications.update({'_id': bson.ObjectId(_id)},
                                          publication)



    def find_fermi(self):

        for auth in auhtor_to_controll:

            cursor = self.publications.find({'ASI_authors': {'$in': [author_to_eliminate]}})



            for publication in cursor:
                title_to_check = publication['title']

                if title not in title_to_check.lower():
                    continue

                string_to_clean = publication['authors_to_show']
                string_array = string_to_clean.split("...")
                new_string = []

                for authors_in_bold in string_array:

                    if author_to_eliminate in authors_in_bold.lower():
                        continue

                    new_string.append(authors_in_bold)


                publication['authors_to_show'] = ''.join(new_string)
                publication['ASI_authors'] = [x for x in publication['ASI_authors'] if x != author_to_eliminate]
                print publication['authors_to_show']
                print publication['ASI_authors']

                _id = publication['_id']
              #then i have to remove, otherwhise it will not update
                del publication['_id']
                self.publications.update({'_id': bson.ObjectId(_id)},
                                          publication)






def main():

    print 'starting to clean author %s' %author_to_eliminate


    connection_string = ""
    connection = pymongo.MongoClient(connection_string)
    database = connection.publicationASI
    publication_db = CleaningDAO(database)

    #publication_db.find_authors()
    publication_db.find_fermi()


    #print type_bib
    print "end of cleaning"


if __name__ == '__main__':

    main()







