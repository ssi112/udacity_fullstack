# -*- coding: utf-8 -*-
# version >= 3
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
        if self.path.endswith("/restaurants"):
            # get all restaurants
            restaurants = session.query(Restaurant).all()
            output = ""
            output += "<html><body>"
            output += "<h1>Objective 1 - List all Restaurants</h1>"
            output += "<ul>"
            for restaurant in restaurants:
                output += "<li>" + restaurant.name + "</li>"
            output += "</ul><h3>Python Version 3.6</h3>"
            output += "</body></html>"
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(output, "utf-8"))
            return
        else:
            self.send_error(404, "File Not Found {}".format(self.path))


def main():
    try:
        server = HTTPServer((hostName, hostPort), webserverHandler)
        # print("Web server running on port {}".format(port))
        print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))
        server.serve_forever()
    except KeyboardInterrupt:   # ctrl-c
        print("^C entered, stopping web server...")
        print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
        server.socket.close()

if __name__ == '__main__':
    main()
