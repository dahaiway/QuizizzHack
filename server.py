#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler
import socketserver
from requests import post
from urllib.parse import urlparse, parse_qs
from os import system

PORT = 1999

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            q = parse_qs(urlparse(self.path).query)
            r = post(
                "https://game.quizizz.com/play-api/awardPowerup",
                headers={"referer": q['ref'][0]},
                json={
                    "roomHash": q['hsh'][0],
                    "playerId": q['pid'][0],
                    "powerup": {
                        "name": q['pwr'][0]
                    }
                }
            )
            if r.status_code == 200:
                self.send_response(200)
            else:
                self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            print("ERR", self.date_time_string(), self.client_address, self.requestline, self.headers.as_string(), r.status_code, r.json(), q)
        except KeyError:
            print("ERR", self.date_time_string(), self.client_address, self.requestline, self.headers.as_string(), q)
            pass


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            httpd.shutdown()
            print()
            system("fuser -k %s/tcp" % PORT)
