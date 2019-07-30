# version >= 3
# note the use of bytes() to convert string to bytes with encoding UTF-8
#
# if [Errno 98] Address already in use
# kill it with the following command
# $ sudo fuser -k 8080/tcp
#

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi

hostName = "localhost"
hostPort = 8080

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Python Simple Webserver.</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><p>Hello! This is a test.</p>", "utf-8"))
            self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes('''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>''', "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            """
            ORIGINAL LESSON CODE
            output = ""
            output += "<html><body>Hello!</body></html>"
            self.wfile.write(bytes(output, "utf-8"))
            print(output)
            """
            return
        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Python Simple Webserver.</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><p>&#161 Hola! This is a test.</p>", "utf-8"))
            self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes('''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>''', "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            """
            ORIGINAL LESSON CODE
            output = ""
            output += "<html><body>Hello!</body></html>"
            self.wfile.write(bytes(output, "utf-8"))
            print(output)
            """
            return
        else:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            #######################################################################
            # CHECKE THESE:
            # https://stackoverflow.com/questions/42688246/do-post-method-failing-in-python-3-6
            # https://stackoverflow.com/questions/2121481/python3-http-server-post-example
            # https://stackoverflow.com/questions/36484184/python-make-a-post-request-using-python-3-urllib
            #
            # THIS MIGHT BE THE BEST ANSWER:
            # https://stackoverflow.com/questions/31486618/cgi-parse-multipart-function-throws-typeerror-in-python-3
            #
            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields.get('message')
            #######################################################################
            if self.path.endswith("/hello"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print("Fields value is", fields)
                    messagecontent = fields.get('message')
                    print("Message is ", messagecontent[0].decode("utf-8"))
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/hello')
                    self.end_headers()

            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))
            print(output)
        except:
            print("Inside the exception block")


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
