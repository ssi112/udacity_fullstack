# -*- coding: utf-8 -*-
# this is for version < 3 python
# https://docs.python.org/2/library/basehttpserver.html

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
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

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                # get all restaurants
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<h1>Objective 1 - List all Restaurants</h1>"
                output += "<ul>"
                for restaurant in restaurants:
                    output += "<li>" + restaurant.name + "</li>"
                output += "</ul><h3>Python Version 2.7</h3>"
                output += "</body></html>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()

