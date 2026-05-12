from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# This is the "database" on the server
PRODUCTS = {1: {'name': 'Course Fee', 'price': 5000}}

form = '''<html><body>
<h2>Secure Payment Gateway</h2>
<p>Product: Course Fee</p>
<p>Price: ₹5000</p>
<form method="POST" action="/pay.php">
<input type="hidden" name="product_id" value="1">
User: <input name="user" required><br><br>
Pass: <input name="pass" type="password" required><br><br>
Card: <input name="card" required><br><br>
CVV: <input name="cvv" required><br><br>
<input type="submit" value="Pay Now">
</form></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(form.encode())
    
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode()
        params = urllib.parse.parse_qs(data)
        
        # Key Fix: Server gets price from its own DB, not from user
        product_id = int(params.get('product_id',['0'])[0])
        real_amount = PRODUCTS.get(product_id, {}).get('price', 0)
        user_sent_amount = params.get('amount',['not sent'])[0]
        
        response = f'''<h1>Payment Successful</h1>
        <h2>Amount Charged: ₹{real_amount}</h2>
        <p><b>Security Check:</b> Server ignored client amount. User tried to send: {user_sent_amount}</p>'''
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(response.encode())

HTTPServer(('localhost',8000), Handler).serve_forever()