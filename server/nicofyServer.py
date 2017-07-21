from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import parse_qs, urlparse

import nicofyDB #Import Database-Communication functions

url_Path = ['/','/succeed']

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        if path not in url_Path:
            try:
                new_Link = nicofyDB.get_Redirect_Link(path[1:]) #Doesn't send the '/'
                page = nicofyPages.get_Redirect(new_Link)
                self.send_response(200)
                self.send_header('Content-Type','text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(page)))
                self.end_headers()
                self.wfile.write(page.encode())
                return
            except LookupError:
                print "That link doesn't exist"
                page = nicofyPages.get_404_Notfound()
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(page)))
                self.end_headers()
                self.wfile.write(page.encode())
                return
        if path == '/':
            page = nicofyPages.send_response(200)



    def do_POST(self):
        print self.rfile.read(132).decode()

if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpDeploy = HTTPServer(server_address, WebHandler)
    httpDeploy.serve_forever()
