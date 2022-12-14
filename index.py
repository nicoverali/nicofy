from server import nicofyDB  # Import Database-Communication functions
from server import nicofyPages  # Import pages creator
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import string
import random
import os  # To set PORT to be configurable for Heroku

# For threading
import threading
from socketserver import ThreadingMixIn


class ThreadHTTPServer(ThreadingMixIn, HTTPServer):
    "This is an HTTPServer that supports thread-based concurrency."


url_path = ['/', '/succeed']


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        if path not in url_path:
            try:
                new_link = nicofyDB.get_Redirect_Link(
                    path[1:])  # Doesn't send the '/'
                redirection = nicofyPages.get_Redirect(new_link)
                send_Page(redirection, 200, self)
                return
            except LookupError:
                try:
                    searched_file = open(path[1:])
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
                    print("That link doesn't exist")
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
        print('Message: ' + query)
        query = parse_qs(query)
        print(query)
        old_link = query['url'][0]
        username = query['username'][0]
        print(old_link, username)
        unique_id = random_ID()
        while nicofyDB.check_For_Existing_Link(unique_id):
            unique_id = random_ID()
        nicofyDB.add_Link(old_link, unique_id, username)
        response_link = '/succeed?url=' + unique_id
        self.send_response(303)
        self.send_header('Location', response_link)
        self.end_headers()


############# END REQUEST HANDLER #################

def send_Page(page, status_code, handler, typeof='html'):
    encoded_page = page.encode('utf-8')
    page_length = str(len(encoded_page))
    handler.send_response(status_code)
    content_type = 'text/' + typeof + '; charset=utf-8'
    handler.send_header('Content-Type', content_type)
    handler.send_header('Content-Length', page_length)
    handler.end_headers()
    handler.wfile.write(encoded_page)


def random_ID(size=6, chars=(string.ascii_lowercase + string.digits)):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpDeploy = ThreadHTTPServer(server_address, handler)
    print('Server is running on PORT = ' + str(port))
    httpDeploy.serve_forever()
