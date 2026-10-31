SHOPEASE - PYTHON E-COMMERCE COLLEGE PROJECT
============================================

PROJECT FEATURES
- Attractive responsive website
- Product listing and category filters
- Product search
- Add to cart and quantity update/remove
- Checkout form
- Order confirmation
- SQLite database stores demo orders
- Orders page to view saved orders

REQUIREMENTS
- Windows 10/11 or macOS
- Python 3.10 or newer
- Internet connection only for downloading Flask and Google Fonts (website itself runs locally)

WINDOWS PAR RUN KARNE KE STEPS
1. ZIP file ko Extract All karein.
2. Extracted folder `easy_python_ecommerce` open karein.
3. Folder ke address bar par click karein, `cmd` type karein aur Enter press karein.
   Isse isi folder mein Command Prompt open hoga.
4. Check Python:
       python --version
   Agar command nahi chale, Python install karein: https://www.python.org/downloads/
   Install karte waqt "Add Python to PATH" checkbox tick karein.
5. Virtual environment banayein:
       python -m venv venv
6. Virtual environment activate karein:
       venv\Scripts\activate
7. Flask install karein:
       pip install -r requirements.txt
8. Website run karein:
       python app.py
9. Browser mein open karein:
       http://127.0.0.1:5000
10. Website band karne ke liye Command Prompt mein Ctrl + C press karein.

AGAR `python` COMMAND NA CHALE
Try:
       py --version
       py -m venv venv
       venv\Scripts\activate
       py -m pip install -r requirements.txt
       py app.py

MAC PAR RUN KARNE KE STEPS
1. Terminal open karke project folder mein jaayein.
2. Run:
       python3 -m venv venv
       source venv/bin/activate
       pip install -r requirements.txt
       python3 app.py
3. Browser mein http://127.0.0.1:5000 open karein.

PROJECT DEMO KAISE DIKHAYEIN
1. Home page par product cards aur categories dikhayein.
2. Search box se "watch" search karein.
3. Kisi product par + Add click karein.
4. Cart open karein, quantity change karke Update cart click karein.
5. Proceed to checkout par click karke name, email aur address fill karein.
6. Place demo order click karein.
7. Orders menu kholkar saved order show karein.

PROJECT FILES
app.py                 Python Flask backend and routes
templates/             HTML pages using Jinja templates
static/style.css       Website design and responsive styles
requirements.txt       Python package dependency
shop.db                First run par automatically create hone wali SQLite database

VIVA KE LIYE IMPORTANT POINTS
- Frontend: HTML, CSS, Jinja templates
- Backend: Python Flask
- Database: SQLite
- GET request: page ya data display karne ke liye
- POST request: form submit, cart update aur order save karne ke liye
- Session: cart data ko browser session mein rakhne ke liye
- SQL INSERT: checkout order database mein save karta hai
- Routes: /, /cart, /checkout, /orders, /about

IMPORTANT
Yeh academic demo project hai. Isme real payment gateway, login/authentication,
production-level security ya real shipping integration nahi hai. Real customer data
ya real payment ke liye ise as-is deploy na karein.
