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

1. Go to the trolley/basket page of the order you want to extract and right-click on the page, then click Inspect.

2. As shown in the pictures below, go to the body element and then the div with the id 'root' and copy the Inner HTML: ![image](https://github.com/user-attachments/assets/fcee32c1-8557-42e0-ba94-118b2a93b766)
   ![image](https://github.com/user-attachments/assets/07ebde75-9569-4ea3-af5d-6f09eb951509)


3. Place the copied HTML into an .html file.

4. Put that file inside the basket_file/ folder.

5. Run the script.

```bash
python main.py
```

6. The script will create a JSON file in the `JSON_output/` folder with the delivery date in the filename:

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
