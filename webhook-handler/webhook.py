#!/usr/bin/env python3
"""
GitHub Webhook Handler - Basic version
Receives webhook events from GitHub
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

class WebhookHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data)
            event = self.headers.get('X-GitHub-Event', 'unknown')
            logging.info(f"Received {event} event")
            logging.info(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            
        except Exception as e:
            logging.error(f"Error: {e}")
            self.send_response(500)
            self.end_headers()

def run(port=8080):
    server = HTTPServer(('', port), WebhookHandler)
    print(f"Server running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    run()
