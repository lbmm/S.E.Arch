__author__ = 'federicamoscato'

import csv
import pymongo

import pubblicazioniASI.contractDAO as contractDAO

FILE_TO_LOAD = 'docs/Contratti_scientifici_ASI per biblioteca.csv'

connection_string = ""
connection = pymongo.MongoClient(connection_string)
database = connection.publicationASI
contracts = contractDAO.ContractDAO(database)


class InsertError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Contract(object):

    def __init__(self, contract_id, contract_name, institution, start_date, is_active):
        self.contract_id = contract_id
        self.contract_name = contract_name
        self.contract_type = 'Ricerca Scientifica'
        self.institution = institution
        self.start_date = start_date
        self.is_active = is_active



def insertIntoDB(contract):

     return contracts.add_contract(contract_id=contract.contract_id, contract_name=contract.contract_name,
                                   institution=contract.institution, start_date=contract.start_date,
                                   is_active=contract.is_active, date_format='%m/%d/%y', contract_type=contract.contract_type)

def isActive(str):

    return str.startswith('In corso')

def main():

    print 'starting to load contracts in DB'

    with open(FILE_TO_LOAD) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if row[3].startswith('Ricerca'):
                try:
                    new_contract = Contract(row[2].strip(), row[4], row[6], row[1], isActive(row[0]))
                    if not insertIntoDB(new_contract):
                        raise InsertError("error inserting author %s  " % row[2])
                except InsertError as e:
                    print e.value

    print "end of load all the contracts"



if __name__ == '__main__':

    main()

