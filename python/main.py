#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2

MAIN_PAGE_FOOTER_TEMPLATE = """
    <h1>Welcome　%s!</h1>
    <p> Lets mix letters!</p>
    <form action="/mix_letter" method="post">
      <div>
        <p>Write first word</p>
        <input type="text" name="first_word" rows="1" cols="10"></input>
      </div>
      <br>
      <div>
        <p>Write second word</p>
        <input type="text" name="second_word" rows="1" cols="10"></input>
      </div>
      <div><input type="submit" value="mix letter"></div>
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
    def post(self):
        self.response.write('<html><body>The words you wrote were mixed!<pre>')
        first_word = self.request.get('first_word')
        second_word = self.request.get('second_word')
        first_li = list(first_word)
        second_li = list(second_word)
        smaller_li = min(first_li, second_li)
        bigger_li = max(first_li, second_li)
        new_word = ""
        for i in range(0, len(smaller_li)):
            new_word += first_li[i] + second_li[i]
        for i in range(len(smaller_li), len(bigger_li)):
            new_word += bigger_li[i]
        self.response.write(cgi.escape(new_word))
        self.response.write('</pre></body></html>')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/mix_letter', MixLetter),
], debug=True)
