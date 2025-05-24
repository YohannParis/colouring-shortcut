#!/usr/bin/env python3
"""
Simple HTTP Server that generates and prints coloring pages
Usage: python3 coloring_server.py
Access: http://localhost:8080?idea=dinosaur
"""

import http.server
import socketserver
import urllib.parse
import subprocess
import json
import os
import sys
from pathlib import Path

PORT = 8080
HOST = '0.0.0.0'  # Listen on all network interfaces

class ColoringHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse the URL and query parameters
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            
            # Get the idea from parameters
            idea = query_params.get('idea', [None])[0]
            
            if not idea:
                self.send_error_response("Missing 'idea' parameter. Usage: ?idea=dinosaur", 400)
                return
            
            # Execute the coloring script
            result = self.generate_coloring_page(idea)
            
            # Send successful response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                'status': 'success',
                'idea': idea,
                'message': result['message'],
                'error': result['error'],
                'return_code': result['return_code']
            }
            
            self.wfile.write(json.dumps(response_data, indent=2).encode())
            
        except Exception as e:
            self.send_error_response(f"Server error: {str(e)}", 500)
    
    def generate_coloring_page(self, idea):
        """Generate and print a coloring page based on the idea"""
        
        # Check if OpenAI API key is set
        if not os.environ.get('OPENAI_API_KEY'):
            return {
                'message': '',
                'error': 'OPENAI_API_KEY environment variable is not set',
                'return_code': 1
            }
        
        # Path to your coloring script
        script_path = os.path.expanduser('coloring_script.sh')  # Adjust path as needed
        
        # Check if script exists
        if not os.path.exists(script_path):
            return {
                'message': '',
                'error': f'Coloring script not found at {script_path}. Please update the script_path in the server.',
                'return_code': 1
            }
        
        try:
            # Execute the coloring script with the idea as argument
            print(f"Generating coloring page for: {idea}")
            result = subprocess.run(
                ['bash', script_path, idea], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                message = f"Coloring page for '{idea}' has been generated and sent to printer!"
            else:
                message = f"Script executed but returned error code {result.returncode}"
            
            return {
                'message': message,
                'error': result.stderr.strip() if result.stderr else '',
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'message': '',
                'error': 'Script execution timed out (30 seconds)',
                'return_code': 1
            }
        except Exception as e:
            return {
                'message': '',
                'error': f'Error executing script: {str(e)}',
                'return_code': 1
            }
    
    def send_error_response(self, message, code):
        """Send an error response"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_data = {
            'status': 'error',
            'message': message,
            'code': code
        }
        
        self.wfile.write(json.dumps(error_data, indent=2).encode())
    
    def log_message(self, format, *args):
        """Custom log message format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    import socket
    
    # Get the computer's hostname and local IP
    hostname = socket.gethostname()
    bonjour_name = hostname if hostname.endswith('.local') else f"{hostname}.local"
    
    # Get local IP address
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
    except:
        local_ip = "Unable to determine"
    
    print(f"Starting Coloring Page HTTP Server")
    print(f"Listening on all network interfaces, port {PORT}")
    print(f"\nAccess the server using:")
    print(f"  Local:     http://localhost:{PORT}")
    print(f"  LAN IP:    http://{local_ip}:{PORT}")
    print(f"  Bonjour:   http://{bonjour_name}:{PORT}")
    print(f"\nExample usage:")
    print(f"  http://{bonjour_name}:{PORT}?idea=dinosaur")
    print(f"  http://{bonjour_name}:{PORT}?idea=princess%20castle")
    print(f"  http://{bonjour_name}:{PORT}?idea=fire%20truck")
    print(f"\nMake sure:")
    print(f"  - OPENAI_API_KEY environment variable is set")
    print(f"  - Your coloring script is at coloring_script.sh (or update script_path)")
    print(f"  - Printer is connected and ready")
    print(f"  - Firewall allows connections on port {PORT}")
    print(f"\nPress Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), ColoringHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    main()
