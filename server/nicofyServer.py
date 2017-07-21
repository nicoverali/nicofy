from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import parse_qs, urlparse
import string
import random

import nicofyDB #Import Database-Communication functions
import nicofyPages #Import pages creator

url_path = ['/','/succeed']

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        if path not in url_path:
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
                    if 'css' in path:
                        send_Page(content, 200, self, 'css')
                        return
                    if 'js' in path:
                        send_Page(content, 200, self, 'js')
                        return
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
        message_lenght = int(self.headers.get('Content-Length'))
        query = self.rfile.read(message_lenght).decode()
        query = parse_qs(query)
        old_link = query['url'][0][1:-1]
        username = query['user'][0][1:-1]
        unique_id = random_ID()
        while nicofyDB.check_For_Existing_Link(unique_id):
            unique_id = random_ID()
        nicofyDB.add_Link(old_link, unique_id, username)
        self.send_response(303)
        self.send_header('Location', ('/succeed?url=%s',(unique_id,)))
        self.end_headers


############# END REQUEST HANDLER #################

def send_Page(page, status_code, handler, typeof='html'):
    encoded_page = page.decode('utf-8').encode('utf-8')
    page_length = str(len(encoded_page))
    handler.send_response(status_code)
    handler.send_header('Content-Type', ('text/%s; charset=utf-8',(typeof,)))
    handler.send_header('Content-Length', page_length)
    handler.end_headers()
    handler.wfile.write(encoded_page)

def random_ID(size=6, chars=(string.ascii_lowercase + string.digits)):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpDeploy = HTTPServer(server_address, WebHandler)
    httpDeploy.serve_forever()
