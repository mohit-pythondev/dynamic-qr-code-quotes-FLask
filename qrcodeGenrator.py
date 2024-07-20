from flask import Flask, render_template, make_response, url_for, redirect
import json
import random
import qrcode
from io import BytesIO

app = Flask(__name__)

def get_random_quote():
    # Load the JSON data from the file
    with open('motivational_quotes.json', 'r') as file:
        data = json.load(file)
    
    # Get a random quote
    random_quote = random.choice(data['quotes'])['quote']
    
    return random_quote

def generate_qr_code(text):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    # Create an image from the QR code instance
    img = qr.make_image(fill='black', back_color='white')
    return img

@app.route('/')
def index():
    quote = get_random_quote()
    return render_template('index.html', quote=quote)

@app.route('/qr-code/<quote>')
def qr_code(quote):
    img = generate_qr_code(quote)
    
    # Save the image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return make_response(img_io.getvalue(), 200, {'Content-Type': 'image/png'})

@app.route('/new-quote')
def new_quote():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
