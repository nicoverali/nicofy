from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import parse_qs, urlparse

import nicofyDB #Import Database-Communication functions

url_path = ['/','/succeed']

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        if path not in url_Path:
            try:
                new_link = nicofyDB.get_Redirect_Link(path[1:]) #Doesn't send the '/'
                redirection = nicofyPages.get_Redirect(new_Link)
                send_Page(redirection, 200, self)
                return
            except LookupError:
                try:
                    searched_file = open('../' + path[1:])
                    content = searched_file.read()
                    searched_file.close()
                    send_Page(content, 200, self)
                    return
                except IOError:
                    print "That link doesn't exist"
                    notfound_page = nicofyPages.get_404_Notfound()
                    send_Page(notfound_page, 404, self)
                    return
        if path == '/':
            home = nicofyPages.get_Home()
            send_Page(home, 200, self)
        if path == '/succeed':
            query_url = parse_qs(url.query)['url'][0]
            succeed_page = nicofyPages.get_Succeed(query_url)
            send_Page(succeed_page, 200, self)
    def do_POST(self):
        print self.rfile.read(132).decode()

############# END REQUEST HANDLER #################

def send_Page(page, status_code, handler):
    encoded_page = page.encode()
    page_length = str(len(encoded_page))
    handler.send_response(status_code)
    handler.send_header('Content-Type', 'text/html; charset=utf-8')
    handler.send_header('Content-Length', page_length)
    handler.end_headers()
    handler.wfile.write(encoded_page)


if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpDeploy = HTTPServer(server_address, WebHandler)
    httpDeploy.serve_forever()
