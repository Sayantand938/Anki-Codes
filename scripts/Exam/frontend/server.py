import http.server
import socketserver
import os
import webbrowser
import threading

# Define the port to serve the files
PORT = 8000

# Define the directory to serve (current directory)
DIRECTORY = "."

# Define the HTML file to open in the browser
HTML_FILE = "index.html"  # Change this to your HTML file name

# Define the request handler
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

# Function to start the server
def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Function to open the HTML file in the default browser
def open_browser():
    url = f"http://localhost:{PORT}/{HTML_FILE}"
    webbrowser.open(url)

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Open the HTML file in the default browser
open_browser()

# Keep the main thread alive to serve requests
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Shutting down the server.")
