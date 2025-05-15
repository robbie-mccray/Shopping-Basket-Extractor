# 🛒 Shopping-Basket-Extractor

This tool extracts structured data from the basket page HTML of the [ASDA](https://groceries.asda.com) website and saves it as a JSON file. It's useful for creating shopping lists, budgeting, or meal planning based on your current basket.

---

## ✅ What It Does

- Parses ASDA's basket HTML page
- Extracts each product's:
  - `name`
  - `price`
  - `unit_price`
  - `quantity`
- Auto-detects the **delivery date** and uses it in the output filename
- Outputs a clean and human and computer readable **JSON file**

---

## 📁 Project Structure

```
SHOPPING-BASKET-EXTRACTOR/
├── basket_file/           # Put your HTML basket page here
│   └── basketpagehtml1.html
├── JSON_output/           # Where cleaned JSON outputs are saved
│   └── basket_18-05-25.json
├── main.py                # Main extraction script (run)
└── README.md              # This file
```

---

## 🚀 How to Use

1. Go to the trolley/basket page of the order you want to extract and right click on the page and click inspect.
2. ![tutorialimage1](https://github.com/user-attachments/assets/2cbbb4b8-2f52-4418-b072-4c77532da4ec)
   As shown in the picture above go to the top <html> element and copy the inner HTML.
4. Place copied html into a html file.
5. Place it inside the `basket_file/` folder.
6. Run the script:

```bash
python main.py
```

4. The script will create a JSON file in the `JSON_output/` folder with the delivery date in the filename:

```
basket_{delivery_date}.json (date is in DD-MM-YY)
```

---

## 📦 Output Format (example)

```json
{
  "name": "ASDA Bolognese Pasta Sauce",
  "price": "£0.69",
  "unit_price": "500g , 13.9p/100g",
  "quantity": "1"
}
```

---

## 🛠️ Dependencies

- Python 3.x
- `beautifulsoup4` (install via `pip install beautifulsoup4`)

---
