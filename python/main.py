#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import webapp2
import json

stations_list = [{"Name":"East Road","Stations":["Grey Havens","Tower Hills","Far Downs","White Downs","Michel Delving","Hobbiton","Buckland","Old Forest","Barrow Downs","Bree","Midgewater Marshes","Weathertop","Last Bridge","Fords of Bruinen","Rivendell"]},{"Name":"Mirkwood Circle","Stations":["Caras Galadon","Gladden Fields","Old Ford","The Carrock","Rhimdath Crossing","Framburg","Elvenking's Halls","Esgaorth","Dale","Erebor"]},{"Name":"Misty Mountain Way","Stations":["Lond Daer","Tharbad","Ost-in-Edhil","Gate of Moria","Moria","Mirromere","Lorien Forest","Caras Galadon","Dol Guldur"]},{"Name":"Rohan Railroad","Stations":["Minas Tirith","Duradan Forest","Firienholt","Edoras","Helm's Deep","Fords of Isen","Isengard","Fangorn Forest","Field of Celebrant","Caras Galadon"]},{"Name":"Gondor Limited","Stations":["Dol Amroth","Edhellond","Calembel","Ethring","Linhir","Pelargir","Emyn Arnen","Minas Tirith"]},{"Name":"Mordor Monorail","Stations":["Minas Tirith","Osgiliath","Minas Morgul","Mount Doom","Barad-dûr"]},{"Name":"Green Way","Stations":["Michel Delving","Sarn Ford","Tharbad","Fords of Isen"]}]


MAIN_PAGE_MIX_WORD = """
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

MAIN_PAGE_FIND_ROUTE_1= """
    <form action="/find_rout" method="post">
      <div>
        <p>find rout</p>
        <p>from where?</p>
"""
MAIN_PAGE_FIND_ROUTE_2="""
      </div>
      <br>
      <div>
        <p>To where?</p>
"""
MAIN_PAGE_FIND_ROUTE_3="""
      </div>
      <div><input type="submit" value="find route"></div>
    </form>
"""

class MainPage(webapp2.RequestHandler):
    def show_stations(self):
        # url = 'http://lotr.fantasy-transit.appspot.com/net?format=json'
        # try:
        #     result = urlfetch.fetch(url)
        #     if result.status_code == 200:
        #         print(result.content)
        #         stations_dict = json.loads(result.content)

        #         print (stations_dict)
        #
        #         # stations_dict = json.loads(stations_js)
        #         self.response.write(stations_dict)
        #         self.response.write(stations_dict[0])
        #
        #     else:
        #         self.response.status_code = result.status_code
        # except urlfetch.Error:
        #     logging.exception('Caught exception fetching url')
        select_menu=""
        for i in range(len(stations_list)):
            line = stations_list[i]["Name"]
            stations_in_one_line = stations_list[i]["Stations"]
            for i in range(len(stations_in_one_line)):
                select_menu += "<option value=\"" + stations_in_one_line[i] +"\">" + stations_in_one_line[i] + "</option>"
        self.response.write(select_menu)
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
            self.response.write(MAIN_PAGE_MIX_WORD % user.nickname())

            self.response.write(MAIN_PAGE_FIND_ROUTE_1)
            self.response.write("<select name =\"from_where\"")
            self.show_stations()
            self.response.write("</select>")
            self.response.write(MAIN_PAGE_FIND_ROUTE_2)
            self.response.write("<select name =\"to_where\"")
            self.show_stations()
            self.response.write("</select>")
            self.response.write(MAIN_PAGE_FIND_ROUTE_3)

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

class FindRout(webapp2.RequestHandler):
    def find_station(self, station):
        line_and_index = []
        for i in range(len(stations_list)):
            line = stations_list[i]["Name"]
            stations_in_one_line = stations_list[i]["Stations"]
            for i in range(len(stations_in_one_line)):
                if station == stations_in_one_line[i]:
                    line_and_index += [line,i]
        return line_and_index

    def find_rout(self):
        from_where = self.request.get('from_where')
        to_where = self.request.get('to_where')
        self.response.write(" From " + from_where + " To " + to_where)
        print(self.find_station(from_where))

    def post(self):
        self.response.write('<html><body>Your best transit plan is ')
        self.find_rout()
        self.response.write('</body></html>')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/mix_letter', MixLetter),
    ('/find_rout', FindRout),
], debug=True)
