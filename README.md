<<<<<<< HEAD
# Online_Food_Service
=======
# Laziz Khana

A modern online food ordering and delivery platform inspired by Food Panda and Foodie (Bangladesh).

## Features
- User registration, login, profile, and address management
- Restaurant discovery, search, and filtering
- Menu browsing, cart, checkout, and order tracking
- Reviews, ratings, promo codes, and admin panel
- Responsive, modern UI with Bootstrap and animations

## Deployment: PythonAnywhere (Free Plan)

### 1. Clone the Repository
```
git clone <your-repo-url>
cd food_order_delivery
```

### 2. Set Up Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Django Setup
```
python manage.py migrate
python manage.py createsuperuser  # Create admin account
```

### 4. Load Sample Data
```
python manage.py loaddata restaurants/fixtures/sample_restaurants.json
python manage.py loaddata restaurants/fixtures/sample_menu.json
```

### 5. Collect Static Files
```
python manage.py collectstatic --noinput
```

### 6. PythonAnywhere Configuration
- Go to the **Web** tab on PythonAnywhere dashboard.
- Set **Source code** to your project directory.
- Set **WSGI configuration file** to point to your project’s `wsgi.py`.
- Set **Virtualenv** path.
- Add `/static/` and `/media/` as static file mappings:
  - `/static/` → `/home/<your-username>/food_order_delivery/staticfiles/`
  - `/media/` → `/home/<your-username>/food_order_delivery/media/`
- Reload the web app.

### 7. Environment Settings
- Set `DEBUG = False` in `lazizkhana/settings.py` for production.
- Set a secure `SECRET_KEY` using environment variables.

### 8. Admin Panel
- Visit `/admin/` to manage users, restaurants, menus, orders, and more.

### 9. Free Tier Limitations
- Email verification uses console backend (no real emails sent).
- No external APIs unless whitelisted by PythonAnywhere.

---

## Credits
- Built with Django, Bootstrap, Animate.css
- Images: Unsplash, Pexels (sample only)

---

For any issues, please open an issue on the repository. 
>>>>>>> 638cd72 (Initial commit: Laziz Khana full project)
