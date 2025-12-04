from flask import Flask, render_template, request, send_file, jsonify
from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime
import html
from io import BytesIO
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

def parse_basket_html(html_content):
    """Parse basket HTML and return products list and delivery date."""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Extract delivery date
        delivery_date = "unknown_date"
        date_label = soup.find("div", string=re.compile("Date:", re.IGNORECASE))
        if date_label:
            date_line = date_label.find_next("li")
            if date_line:
                raw_date = date_line.get_text(strip=True)
                try:
                    parsed_date = datetime.strptime(raw_date, "%A, %d %B %Y")
                    delivery_date = parsed_date.strftime("%d-%m-%y")
                except Exception as e:
                    print(f"⚠️ Could not parse delivery date: {e}")
        
        # Extract products
        products = []
        for item in soup.find_all("div", {"data-auto-id": "item"}):
            try:
                name_tag = item.find("h3", class_="ingredient__title")
                name = name_tag.get_text(strip=True) if name_tag else "Unnamed Product"

                price_tag = item.find("strong", class_="ingredient__price")
                price = price_tag.get_text(strip=True) if price_tag else "£0.00"

                unit_price_tag = item.find("span", class_="department-item__price-uom")
                unit_price = unit_price_tag.get_text(strip=True) if unit_price_tag else "N/A"

                quantity_input = item.find("input", {"name": "quantity-value"})
                quantity = quantity_input["value"] if quantity_input else "1"

                products.append({
                    "name": ' '.join(name.split()).replace('\xa0', ' '),
                    "price": html.unescape(price.strip()),
                    "unit_price": ' '.join(unit_price.split()).replace('\xa0', ' '),
                    "quantity": quantity.strip()
                })
            except Exception as e:
                print(f"⚠️ Error parsing item: {e}")
        
        return products, delivery_date
    except Exception as e:
        raise Exception(f"Failed to parse HTML: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and parsing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.html'):
        return jsonify({'error': 'Only HTML files are supported'}), 400
    
    try:
        html_content = file.read().decode('utf-8')
        products, delivery_date = parse_basket_html(html_content)
        
        if not products:
            return jsonify({'error': 'No products found in HTML file'}), 400
        
        return jsonify({
            'success': True,
            'products': products,
            'delivery_date': delivery_date,
            'filename': f"basket_{delivery_date}.json"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/download', methods=['POST'])
def download_json():
    """Generate and download JSON file."""
    try:
        data = request.get_json()
        products = data.get('products', [])
        filename = data.get('filename', 'basket.json')
        
        json_bytes = BytesIO(json.dumps(products, indent=2, ensure_ascii=False).encode('utf-8'))
        json_bytes.seek(0)
        
        return send_file(
            json_bytes,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
