from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime
import html

# Paths
BASKET_DIR = "basket_file"
OUTPUT_DIR = "JSON_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Find HTML files
basket_files = [f for f in os.listdir(BASKET_DIR) if f.endswith(".html")]
if not basket_files:
    print("❌ No HTML files found in 'basket_file'.")
    exit()

# Read the first HTML file (or loop for more later)
html_path = os.path.join(BASKET_DIR, basket_files[0])
with open(html_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# --- Extract delivery date ---
delivery_date = "unknown_date"
date_label = soup.find("div", string=re.compile("Date:", re.IGNORECASE))
if date_label:
    date_line = date_label.find_next("li")
    if date_line:
        raw_date = date_line.get_text(strip=True)
        # Expected: "Sunday, 18 May 2025"
        try:
            parsed_date = datetime.strptime(raw_date, "%A, %d %B %Y")
            delivery_date = parsed_date.strftime("%d-%m-%y")
        except Exception as e:
            print(f"⚠️ Could not parse delivery date: {e}")

# --- Extract products ---
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

# --- Save output ---
output_filename = f"basket_{delivery_date}.json"
output_path = os.path.join(OUTPUT_DIR, output_filename)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f"✅ {len(products)} products saved to {output_path}")