# -*- coding: utf-8 -*-
# version = 3.6
# https://docs.python.org/3.5/library/http.server.html
#
# note the use of bytes() to convert string to bytes with encoding UTF-8
#
# if [Errno 98] Address already in use
# kill it with the following command
# $ sudo fuser -k 8080/tcp
#

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
# common gateway interface to process data submitted thru <form>
import cgi

# from lesson 1 database_setup.py
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# create a db session and connect
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

hostName = "localhost"
hostPort = 8080

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Objective #1 list all restaurants
        # Objective #2 edit and delete links
        if self.path.endswith("/restaurants"):
            # get all restaurants
            restaurants = session.query(Restaurant).all()
            output = ""
            output += "<html><head><title>Edit Restaurant</title></head><body>"
            output += "<h1>Objective 4 - Edit Restaurant Name</h1>"
            output += "<strong><a href='/restaurants/new'>Add New Restaurant</a></strong><hr />"
            output += "<table><tr><th>Restaurant</th><th colspan=\"2\">CRUD</th></tr>"
            for restaurant in restaurants:
                output += "<tr>"
                output += "<td>{0}</td>".format(restaurant.name)
                output += "<td> <a href ='/restaurants/{0}/edit'> Edit </a> </td>".format(restaurant.id)
                output += "<td> <a href ='/restaurants/{0}/delete'> Delete </a> </td>".format(restaurant.id)
                output += "</tr>"
            output += "</table><h3>Python Version 3.6</h3>"
            output += "</body></html>"
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(output, "utf-8"))
            return
        # Objective #3 add new restaurant
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><head><title>New Restaurant</title></head>"
            output += "<body><h2>Add New Restaurant</h2>"
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
            output += "<input name='newRestaurant' type='text' placeholder='Enter new restaurant name'>"
            output += "<br /><br /><input type='submit' value='Add'>"
            output += "</form></body></html>"
            self.wfile.write(bytes(output, "utf-8"))
            return
        # Objective 4 edit restaurant name
        if self.path.endswith("/edit"):
            # split returns a list of words separated by '/'
            restaurantID = self.path.split("/")[2]

            # query for the 1st restaurant using ID
            getRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()

            # make certain we have a good ID
            if getRestaurant:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1> {0} - {1} </h1>".format(getRestaurant.name, restaurantID)
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/{0}/edit' >".format(restaurantID)
                output += "<input name = 'newRestaurantName' type='text' placeholder = '{0}' >".format(getRestaurant.name)
                output += "<input type = 'submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
            return
        if self.path.endswith("/delete"):
            restaurantID = self.path.split("/")[2]

            # query for the 1st restaurant using ID
            getRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()

            # make certain we have a good ID
            if getRestaurant:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1> Name: {0} - ID #{1} </h1>".format(getRestaurant.name, restaurantID)
                output += "<h2>Are you certain you want to delete this restaurant?</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/{0}/delete' >".format(restaurantID)
                output += "<input type = 'submit' value = 'Delete'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
            return
        else:
            self.send_error(404, "File Not Found {0}".format(self.path))
    def do_POST(self):
        try:
            #Objective 5 delete restaurant
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            # Objective 4 edit restaurant name
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    # ERROR on content-length with python 3.7
                    content_len = int(self.headers.get('Content-Length'))

                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantID = self.path.split("/")[2]
                    getRestaurantID = session.query(Restaurant).filter_by(id=restaurantID).one()
                    if getRestaurantID != []:
                        getRestaurantID.name = messagecontent[0].decode("utf-8")

                        print(content_len)

                        session.add(getRestaurantID)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        # self.send_header('Content-Length', content_len)
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            # Objective #3 add new restaurant
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print("Fields value is", fields)
                    messagecontent = fields.get('newRestaurant')
                    print("Message is ", messagecontent[0].decode("utf-8"))

                    # add the restaurant - make sure it is string and not bytes
                    newRestaurant = Restaurant(name = messagecontent[0].decode("utf-8"))
                    session.add(newRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except Exception as ex:
            print("Exception occurred")
            print(ex)

def main():
    try:
        server = HTTPServer((hostName, hostPort), webserverHandler)
        print("Server Starting: {0} on: {1} port: {2}".format(time.asctime(), hostName, hostPort))
        server.serve_forever()
    except KeyboardInterrupt:   # ctrl-c
        print("^C entered, stopping web server...")
        print("Server Stopped: {0}".format(time.asctime()))
        server.socket.close()

if __name__ == '__main__':
    main()
