## Shopping Basket Extractor – AI Developer Guide

### Purpose
Web-based tool to parse HTML shopping basket files (from grocery websites) and extract product data into JSON format with a user-friendly UI.

### Architecture

**Stack:**
- **Backend:** Flask (Python 3) with BeautifulSoup HTML parsing
- **Frontend:** HTML5 + Vanilla JS (drag-drop, async file upload)
- **Bundling:** PyInstaller wraps Flask app + templates into a single `.exe`

**Data Flow:**
1. User drags HTML file onto UI → `/api/upload` endpoint
2. Backend parses HTML using BeautifulSoup selectors
3. Extracts delivery date, product items → returns JSON response
4. UI displays products in table, user clicks "Download JSON" → `/api/download` endpoint
5. Downloaded as `basket_{dd-mm-yy}.json`

### Key Files & Directories

- `app.py` – Flask server, parsing logic (reused from `main.py`), API endpoints
- `templates/index.html` – Single-page UI with drag-drop, product display, download button
- `build.spec` – PyInstaller config (bundles `app.py` + `templates/` into `.exe`)
- `requirements.txt` – Dependencies: Flask, beautifulsoup4, Werkzeug, PyInstaller
- `dist/Shopping-Basket-Extractor.exe` – Final built executable (after running `pyinstaller build.spec`)

### Running the App

**Development (local testing):**
```bash
pip install -r requirements.txt
python app.py
# Navigate to http://localhost:5000 in browser
```

**Production (standalone .exe):**
1. Run `pyinstaller build.spec` to build executable
2. Double-click `dist/Shopping-Basket-Extractor.exe`
3. Browser opens automatically to http://localhost:5000
4. App runs until you close the terminal window

### HTML Parsing Patterns (exact CSS selectors)

These selectors target a specific supermarket website's HTML structure. **Do not change without sample HTML test cases.**

| Element | Selector | Example |
|---------|----------|---------|
| Product item container | `div[data-auto-id="item"]` | Wraps entire product |
| Product name | `h3.ingredient__title` | "Apples, 6 Pack" |
| Total price | `strong.ingredient__price` | "£2.50" |
| Unit price | `span.department-item__price-uom` | "£0.42/each" |
| Quantity | `input[name="quantity-value"]` | value="2" |
| Delivery date container | `div` with text matching `/Date:/i` | – |
| Delivery date value | Next `<li>` after date label | "Sunday, 18 May 2025" |

**Date format expected:** `%A, %d %B %Y` (e.g., `Sunday, 18 May 2025`) → converts to `dd-mm-yy` (18-05-25)

### Project Conventions

- **Output JSON structure (immutable):** Array of objects with `name`, `price`, `unit_price`, `quantity` keys
- **HTML entity/whitespace normalization:** `html.unescape()`, `.replace('\xa0', ' ')` applied to all string fields
- **Currently single-file processing:** Script reads first `.html` in `basket_file` dir (if extending to multi-file, update loop in `app.py`)
- **Error handling:** Graceful fallback to "unknown_date" if parsing fails; missing fields default to N/A or "1"

### Frontend Behavior & UX

- **Drag-drop:** Upload area changes color on hover/dragover
- **Feedback:** Loading spinner during parse, success/error messages shown inline
- **Results display:** Products list (scrollable if >10), delivery date badge, download button
- **Reset:** "Upload Another" clears results and prepares for next file

### Common Workflows & Debugging

**Adding a new HTML variant (new supermarket):**
1. Get sample HTML file from user
2. Open in browser dev tools, inspect selectors for equivalent elements
3. Update selectors in `parse_basket_html()` in `app.py`
4. Test with `/api/upload` endpoint using Postman or curl
5. Rebuild `.exe` with `pyinstaller build.spec`

**Testing without running full .exe:**
```bash
python app.py  # Starts Flask dev server on localhost:5000
# Upload in browser, inspect Network tab & console for errors
```

**Common issues:**
- Missing `templates/` folder → PyInstaller build fails; ensure `build.spec` has `datas=[('templates', 'templates')]`
- Selectors not matching → Inspect HTML in browser DevTools, verify class names & attributes
- Port 5000 in use → Change `app.run(port=5001)` in `app.py`

### Dependencies & Versions

- **Flask 3.0.0** – Web framework
- **Werkzeug 3.0.1** – WSGI utilities (required by Flask)
- **beautifulsoup4 4.12.2** – HTML/XML parsing
- **PyInstaller 6.1.0** – Bundle Python app to standalone .exe

Install: `pip install -r requirements.txt`

### Building the .exe

```bash
pyinstaller build.spec
# Creates dist/Shopping-Basket-Extractor.exe (~70-100MB depending on Python version)
```

The spec file ensures:
- Templates bundled into `.exe` (not in external folder)
- All Flask & BeautifulSoup dependencies included
- Console window shown (can hide by setting `console=False` in `.spec`)

### API Endpoints

| Method | Route | Input | Output |
|--------|-------|-------|--------|
| POST | `/api/upload` | Multipart form: `file` (HTML) | JSON: `{success, products[], delivery_date, filename}` |
| POST | `/api/download` | JSON: `{products[], filename}` | Binary: JSON file attachment |

### Non-Goals (Don't change without human confirmation)

- Do not change output JSON schema → downstream tools may depend on it
- Do not remove/modify drag-drop UI → core UX feature
- Do not hard-code file paths → user may run `.exe` from any directory

### When in Doubt

- If a selector breaks for a new HTML variant, **ask for a sample HTML file**
- If modifying parser logic, **test with representative sample files first**
- If adding new features, **preserve backward compatibility** with existing JSON output

---

**Last updated:** December 4, 2025
