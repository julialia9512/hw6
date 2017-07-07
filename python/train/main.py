#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import webapp2

MAIN_PAGE_FOOTER_TEMPLATE = """
    <h1>Welcome %s!</h1>
    <p> Lets transit!</p>
    <form action="/result" method="post">
      <div>
        <p>From what station</p>
        <input type="text" name="from_st"></input>
      </div>
      <br>
      <div>
        <p>To what station</p>
        <input type="text" name="to_st"></input>
      </div>
      <div><input type="submit" value="search"></div>
    </form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
            self.response.write(MAIN_PAGE_FOOTER_TEMPLATE % user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


class MixLetter(webapp2.RequestHandler):
    def getdata():
        url = 'http://www.google.com/humans.txt'
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            self.response.write(result.content)
        else:
            self.response.status_code = result.status_code
    except urlfetch.Error:
        logging.exception('Caught exception fetching url')
    def post(self):
        self.response.write('<html><body>The words you wrote were mixed!<pre>')
        from_st = self.request.get('from_st')
        to_st = self.request.get('to_st')
        self.response.write(cgi.escape(new_word))
        self.response.write('</pre></body></html>')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/mix_letter', MixLetter),
], debug=True)
