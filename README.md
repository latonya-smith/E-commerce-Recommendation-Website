# E-commerce-Recommendation-Website


A simple **Flask-based e-commerce web application** with MySQL integration. Users can sign up, sign in, and explore products with **content-based recommendations** and trending items.

## Features

- User authentication (sign up / sign in)  
- Product recommendations and trending products  
- Randomized images and prices for recommended products  
- MySQL database integration via SQLAlchemy  
- Responsive front-end using Flask templates  

## Setup

1. Install dependencies:  
   ```bash
   pip install -r requirements.txt

1. Install dependencies:  
   ```bash
   pip install -r requirements.txt

2. Start MySQL (e.g., XAMPP) and import the ecom database.
   
3. Configure database in app.py:

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ecom'
    Run the app:
4. Run the app:
    ```bash
    flask run

5. Open http://127.0.0.1:5000 in your browser.

Notes
Replace placeholder images and prices with real data as needed.

Ensure your MySQL user has proper permissions.

If you encounter database connection issues, check your MySQL username, password, and port.