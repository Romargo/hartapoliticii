# coding=utf8

'''
Created on November 1st, 2012

Go through the definitions of electoral colleges from becparlamentare2012.ro
and extract the definition for each of the colleges.

@author: vivi
'''

import urllib
import re

from datetime import datetime
from dateutil import parser

from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError
from xml.etree.ElementTree import parse

from ro.vivi.hplib import *


COUNTY_LIST = [
  "ALBA",
  "ARAD",
  "ARGES",
  "ARGEȘ",
  "BACAU",
  "BACĂU",
  "BIHOR",
  "BISTRITA NASAUD",
  "BOTOSANI",
  "BRASOV",
  "BRAILA",
  "BUZAU",
  "CARAS SEVERIN",
  "CALARASI",
  "CLUJ",
  "CONSTANTA",
  "COVASNA",
  "DAMBOVITA",
  "DOLJ",
  "GALATI",
  "GIURGIU",
  "GORJ",
  "HARGHITA",
  "HUNEDOARA",
  "IALOMITA",
  "IASI",
  "ILFOV",
  "MARAMURES",
  "MEHEDINTI",
  "MURES",
  "NEAMT",
  "OLT",
  "PRAHOVA",
  "SATU MARE",
  "SALAJ",
  "SIBIU",
  "SUCEAVA",
  "TELEORMAN",
  "TIMIS",
  "TULCEA",
  "VASLUI",
  "VALCEA",
  "VRANCEA",
  "BUCURESTI",
  "STRAINATATE"
]

# Given the URL from a becparlamentare2012.ro college description, extract the
# content of the description from the page.
#
# It's quite a shame that these pages were made in Microsoft Word or whatever.
#
def get_college_data(url, num, county):
  data = urllib.urlopen(url)
  if data.getcode() == 404:
    return None

  try:
    soup = BeautifulSoup(data, "lxml")
  except HTMLParseError:
    return None

  content = soup.findAll('p', {'class': 'MsoNormal'})
  if content is None:
    return None

  result = ''
  for p in content:
    text = p.text.strip().replace("\n", " ")
    text = re.sub("([ ]+)", " ", text)

    if text == "":
      continue

    if 'Termeni' in text:
      continue

    text.replace("'", "\'")

    print "INSERT INTO electoral_colleges(name_cdep, description, source) " + \
          "VALUES('d%s %s', '%s', '%s');" % (
            num, county.lower().replace("'", " "), text, url)

  return result



# Given the URL from a becparlamentare2012.ro college description, extract the
# content of the description from the page.
#
# It's quite a shame that these pages were made in Microsoft Word or whatever.
#
def get_senat_college_data(url, num, county):
  data = urllib.urlopen(url)
  if data.getcode() == 404:
    return None

  try:
    soup = BeautifulSoup(data, "lxml")
  except HTMLParseError:
    return None

  content = soup.findAll('p', {'class': 'MsoNormal'})
  if content is None:
    return None

  # TOTAL HACK
  if county == "ARGEȘ":
    county = "ARGES"
  if county == "BACĂU":
    county = "BACAU"

  print "-- " + url
  for p in content:
    text = p.text.strip().replace("\n", " ")
    text = re.sub("([ ]+)", " ", text)

    if text == "":
      continue

    if 'Termeni' in text or not text.startswith("Colegiul uninominal"):
      continue

    # Remove the entire beginning of the string, which is
    # "Colegiul uninominal pentru alegerea Camerei Deputaţilor nr. "
    remove_size = \
        len("Colegiul uninominal pentru alegerea Camerei Deputaţilor nr.")

    county = county.lower().replace("'", " ")
    print (u"UPDATE electoral_colleges SET name_senat='s%s %s' " +
        u", source_senat='%s' "
        u"WHERE name_cdep='d%s %s';") % (
          num, county, url.decode("utf-8"), text[remove_size:], county)

  return 'done'


def go_through_cdep_colleges():
  for county in COUNTY_LIST:
    not_found = False
    num = 1

    while not not_found:
      url = "http://www.becparlamentare2012.ro/CD%s-%s.html" % (num, county)
      text = get_college_data(url, num, county)

      if text is None:
        # Try again, with a separate URL now.
        url = "http://www.becparlamentare2012.ro/C%s-%s.html" % (num, county)
        text = get_college_data(url, num, county)

      print "-- --------------------------------------"

      # If text is still none, it means we're out of numbers.
      if text is None:
        not_found = True
      else:
        num += 1


def go_through_senat_colleges():
  for county in COUNTY_LIST:
    not_found = False
    num = 1

    while not not_found:
      url = "http://www.becparlamentare2012.ro/S%s-%s.html" % (num, county)
      text = get_senat_college_data(url, num, county)

      if text is None:
        # Try again, with a separate URL now.
        url = "http://www.becparlamentare2012.ro/SenatC%s-%s.html" % (num, county)
        text = get_senat_college_data(url, num, county)

      print "-- --------------------------------------"

      # If text is still none, it means we're out of numbers.
      if text is None:
        print "-- ++++++++++++++++++++++++++"
        print "-- done with " + county

        not_found = True
      else:
        num += 1



#print "DELETE FROM electoral_colleges WHERE 1"
go_through_senat_colleges()