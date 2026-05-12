from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

INSECURE_HTML = """<html><body>
<h2>Insecure Payment Gateway</h2>
<form method=POST action=/pay.php>
User: <input name=user><br>
Pass: <input name=pass type=password><br>
Card: <input name=card><br>
CVV: <input name=cvv><br>
Amount: <input name=amount value=5000><br> <!-- THIS IS THE BUG -->
<input type=submit value='Pay Now'>
</form></body></html>"""

class InsecureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(INSECURE_HTML.encode())
    
    def do_POST(self):
        data = parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())
        amount = data.get('amount', ['0'])[0] # TRUSTS USER INPUT - VULNERABLE
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"<h1>Payment Successful</h1><h2>Amount Charged: ₹{amount}</h2><p>VULNERABLE: Server trusted your amount!</p>".encode())

HTTPServer(('localhost', 8001), InsecureHandler).serve_forever()