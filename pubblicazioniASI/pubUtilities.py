__author__ = 'fmoscato'

"""
utilities module for the publications project
"""

import os


def str2bool(string):
    return string in ('true', 'T', 'True', 'Y', 1)

def strValue2bool(string, value):
    return string.lower() in (value.lower())

def find_nth(s, x, n):
    """
    find the nth occurence in a string
    takes string where to search, substring, nth-occurence
    """
    i = -1
    for _ in range(n):
        i = s.find(x, i + len(x))
        if i == -1:
            break
    return i


def clean_string(a_str):
    """
    remove left/right white spaces, special characters
    @param : string from the form
    @return : clean string
    """

    a_str = a_str.replace('\n', '')
    a_str = a_str.replace('\r', '')
    a_str = a_str.rstrip()
    a_str = a_str.lstrip()

    return a_str


def clean_from_latex(a_str):
    """
    utilities that remove special latex characters
    :param a_str:
    :return: the clean string
    """

    repls = {"\\ldots": "", "\\`{": "", '{': '', '}': '', '\\`': '', "\'": "", '\~': '', "\"": "", "$": ""}

    return reduce(lambda a, kv: a.replace(*kv), repls.iteritems(), a_str)


def handle_url(a_url):
    """
    utilities that handle multiple url, return a list of escaped url
    :param a_url:
    :return: list of url escaped

    """
    d = 'http'

    return [d+e.replace("\\", "") for e in a_url.split(d) if e != ""]


def sendMail(to, sub, body):
    """
    TODO: here update the sender !!!
    """
    sendmail_location = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % sendmail_location, "w")
    p.write("From: %s\n" % "moscato@asdc.asi.it")
    p.write("To: %s\n" % to)
    p.write("Subject: %s \n" % sub)
    p.write("\n") # blank line separating headers from body
    p.write(body)
    p.close()

    return True



def get_users_list_controll(users_list):

    return {user['lastname'].lower(): user['name'].lower() for user in users_list}
