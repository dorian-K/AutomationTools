from spotify_cli import runPlayPlaylistOn
import asyncio
import types
import http.server
from urllib.parse import urlparse
import socketserver
PORT = 23851

class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        uri = query_components["uri"]
        device = query_components["device"]
        sp_dc = query_components["sp_dc"]
        asyncio.run(runPlayPlaylistOn(types.SimpleNamespace(uri=uri, device=device, sp_dc=sp_dc)))

        self.send_response(204)
        self.end_headers()
 
Handler = MyHttpRequestHandler
 
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()
