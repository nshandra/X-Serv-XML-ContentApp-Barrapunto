#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from ContentApp.models import RSS
from django.db import IntegrityError
import urllib.request
import sys


class myContentHandler(ContentHandler):

    title = ""

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                line = ("<a href=" + self.theContent +
                        ">" + self.title + "</a><br>")
                try:
                    RSS(link=line).save()
                except IntegrityError:
                    print("Entry repeated")
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


def parse():
    # Get rss
    print("Parsing: http://barrapunto.com/index.rss")
    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')

    # get XML encoding
    line = str(xmlFile.readline())
    if "encoding=" in line:
        xml_encoding = line.split(' ')[2].split('\"')[1]
        print("Encoding:", xml_encoding)
    else:
        xml_encoding = 'utf-8'

    # Load parser and driver
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    # Parse
    theParser.parse(xmlFile)

    print('Parse done')
