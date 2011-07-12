#coding: utf-8

import HTMLParser
import httplib
import base64

class TrackerAuthParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.mode = None
    def handle_starttag(self, tag, attrs):
        if tag == 'guid':
            self.mode = 'guid'
    def handle_data(self, data):
        if self.mode == 'guid':
            self.guid = data
    def handle_endtag(self, tag):
        self.mode = None


class IterationsAndStoriesParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.mode = None
        self.iterations = []
    def handle_starttag(self, tag, attrs):
        if tag == 'iteration':
            self.current = {}
            self.iterations.append(self.current)
            self.mode = None
            return
        if tag == 'stories':
            self.iterations[-1]['stories'] = []
            self.mode = None
            return
        if tag == 'story':
            self.current = {}
            self.iterations[-1]['stories'].append(self.current)
            self.mode = None
            return
        self.mode = tag
        self.current_data = ''
    def handle_data(self, data):
        if self.mode:
            self.current_data += data
    def handle_charref(self, name):
        if self.mode:
            self.current_data += unichr(int(name))

    def handle_endtag(self, tag):
        if self.mode:
            self.current[tag] = self.current_data
        self.mode = None


class Tracker(object):
    def authenticate(self, username, password):
        headers = {'Authorization': base64.encodestring('%s:%s' % (username, password)) }
        conn = httplib.HTTPSConnection('www.pivotaltracker.com')
        conn.request('GET', '/services/v3/tokens/active', '', headers)
        parser = TrackerAuthParser()
        parser.feed(conn.getresponse().read())
        self.token = parser.guid

    def get_stories(self, project_id):
        headers = {'X-TrackerToken': self.token }
        conn = httplib.HTTPSConnection('www.pivotaltracker.com')
        conn.request('GET', '/services/v3/projects/%s/iterations'%(project_id), '', headers)
        parser = IterationsAndStoriesParser()
        parser.feed(conn.getresponse().read())
        return parser.iterations

