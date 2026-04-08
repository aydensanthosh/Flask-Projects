from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from functools import wraps
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-in-production'
app.permanent_session_lifetime = timedelta(days=7)

# Mock database (replace with real database in production)
class MockDB:
    def __init__(self):
        self.users = {
            'john@example.com': {
                'id': 1,
                'username': 'john_doe',
                'password': 'password123',  # In production, store hashed passwords
                'email': 'john@example.com',
                'full_name': 'John Doe',
                'created_at': datetime.now().isoformat()
            }
        }
        self.bookings = [
            {
                'id': 1,
                'user_id': 1,
                'destination': 'Paris, France',
                'date': '2024-06-15',
                'status': 'confirmed',
                'price': 1299
            },
            {
                'id': 2,
                'user_id': 1,
                'destination': 'Tokyo, Japan',
                'date': '2024-08-20',
                'status': 'pending',
                'price': 2499
            }
        ]
        self.wishlist = [
            {
                'id': 1,
                'user_id': 1,
                'destination': 'Bali, Indonesia',
                'added_date': datetime.now().isoformat()
            }
        ]

db = MockDB()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor to make current user available in all templates
@app.context_processor
def utility_processor():
    def get_current_user():
        if 'user_id' in session:
            # Find user in mock db
            for user in db.users.values():
                if user['id'] == session['user_id']:
                    return user
        return None
    return dict(current_user=get_current_user())

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/destinations')
def destinations():
    # Mock destinations data
    destinations = [
        {
            'name': 'Paris, France',
            'image': 'paris.jfif',
            'price': 1299,
            'rating': 4.8,
            'description': 'The City of Light awaits with its romantic ambiance and world-class cuisine.'
        },
        {
            'name': 'Tokyo, Japan',
            'image': 'tokyo.jfif',
            'price': 2499,
            'rating': 4.9,
            'description': 'Experience the perfect blend of tradition and futurism.'
        },
        {
            'name': 'Bali, Indonesia',
            'image': 'bali.jfif',
            'price': 899,
            'rating': 4.7,
            'description': 'Tropical paradise with stunning beaches and rich culture.'
        },
        {
            'name': 'New York, USA',
            'image': 'nyc.jfif',
            'price': 1599,
            'rating': 4.6,
            'description': 'The city that never sleeps, with endless entertainment options.'
        },
        {
            'name': 'Rome, Italy',
            'image': 'rome.jfif',
            'price': 1399,
            'rating': 4.8,
            'description': 'Ancient history, incredible food, and romantic atmosphere.'
        },
        {
            'name': 'Sydney, Australia',
            'image': 'sydney.jfif',
            'price': 2899,
            'rating': 4.7,
            'description': 'Stunning harbor, beautiful beaches, and laid-back lifestyle.'
        }
    ]
    return render_template('destinations.html', destinations=destinations)

@app.route('/tours')
def tours():
    # Mock tours data
    tours = [
        {
            'name': 'European Explorer',
            'duration': '14 days',
            'price': 3499,
            'image': 'europe.jpg',
            'description': 'Visit 7 countries in 14 days including France, Italy, Switzerland, and more.'
        },
        {
            'name': 'Asian Adventure',
            'duration': '12 days',
            'price': 2799,
            'image': 'asia.jpg',
            'description': 'Explore Japan, Thailand, and Singapore in this amazing tour.'
        },
        {
            'name': 'American Road Trip',
            'duration': '10 days',
            'price': 2199,
            'image': 'usa.jpg',
            'description': 'Drive through the iconic Route 66 and visit major US cities.'
        }
    ]
    return render_template('tours.html', tours=tours)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/blog')
def blog():
    # Mock blog posts
    posts = [
        {
            'title': '10 Tips for Solo Travel',
            'excerpt': 'Discover the best practices for traveling alone safely and enjoyably.',
            'author': 'Sarah Johnson',
            'date': '2024-01-15',
            'image': 'solo-travel.jpg',
            'comments': 24
        },
        {
            'title': 'Best Beaches in Thailand',
            'excerpt': 'From Phuket to Koh Samui, find your perfect tropical paradise.',
            'author': 'Mike Chen',
            'date': '2024-01-10',
            'image': 'thailand-beach.jpg',
            'comments': 18
        },
        {
            'title': 'European Backpacking Guide',
            'excerpt': 'How to see Europe on a budget without missing the best spots.',
            'author': 'Emma Wilson',
            'date': '2024-01-05',
            'image': 'europe-backpack.jpg',
            'comments': 32
        }
    ]
    return render_template('blog.html', posts=posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically send an email or save to database
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        # Check credentials (mock authentication)
        if email in db.users and db.users[email]['password'] == password:
            session.permanent = True if remember else False
            session['user_id'] = db.users[email]['id']
            session['username'] = db.users[email]['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        if email in db.users:
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Create new user (mock)
        new_id = len(db.users) + 1
        db.users[email] = {
            'id': new_id,
            'username': username,
            'password': password,  # In production, hash this!
            'email': email,
            'full_name': username,
            'created_at': datetime.now().isoformat()
        }
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    user = None
    for u in db.users.values():
        if u['id'] == session['user_id']:
            user = u
            break
    return render_template('profile.html', user=user)

@app.route('/bookings')
@login_required
def bookings():
    user_bookings = [b for b in db.bookings if b['user_id'] == session['user_id']]
    return render_template('bookings.html', bookings=user_bookings)

@app.route('/wishlist')
@login_required
def wishlist():
    user_wishlist = [w for w in db.wishlist if w['user_id'] == session['user_id']]
    return render_template('wishlist.html', wishlist=user_wishlist)

@app.route('/faq')
def faq():
    faqs = [
        {
            'question': 'How do I book a tour?',
            'answer': 'You can book a tour by visiting our Tours page, selecting your preferred tour, and clicking the "Book Now" button.'
        },
        {
            'question': 'What is your cancellation policy?',
            'answer': 'Free cancellation up to 30 days before departure. Cancellations within 30 days may incur fees. Visit our Cancellation Policy page for details.'
        },
        {
            'question': 'Do I need travel insurance?',
            'answer': 'While not mandatory, we strongly recommend travel insurance for all bookings to protect against unexpected events.'
        },
        {
            'question': 'What payment methods do you accept?',
            'answer': 'We accept all major credit cards, PayPal, and bank transfers for group bookings.'
        }
    ]
    return render_template('faq.html', faqs=faqs)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/cancellation')
def cancellation():
    return render_template('cancellation.html')

@app.route('/travel_insurance')
def travel_insurance():
    insurance_plans = [
        {
            'name': 'Basic',
            'price': 49,
            'coverage': ['Medical emergencies', 'Trip cancellation', 'Lost baggage'],
            'recommended': False
        },
        {
            'name': 'Premium',
            'price': 99,
            'coverage': ['All Basic benefits', 'Emergency evacuation', 'Travel delay', 'Rental car coverage'],
            'recommended': True
        },
        {
            'name': 'Comprehensive',
            'price': 149,
            'coverage': ['All Premium benefits', 'Cancel for any reason', 'Adventure sports', 'Pre-existing conditions'],
            'recommended': False
        }
    ]
    return render_template('travel_insurance.html', insurance_plans=insurance_plans)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    
    # Mock search results
    if query:
        destinations = [
            {'name': 'Paris, France', 'type': 'destination', 'url': url_for('destinations')},
            {'name': 'Tokyo, Japan', 'type': 'destination', 'url': url_for('destinations')},
            {'name': 'Bali, Indonesia', 'type': 'destination', 'url': url_for('destinations')},
            {'name': 'European Explorer Tour', 'type': 'tour', 'url': url_for('tours')},
            {'name': 'Asian Adventure Tour', 'type': 'tour', 'url': url_for('tours')}
        ]
        
        results = [item for item in destinations if query in item['name'].lower()]
    
    return render_template('search.html', query=query, results=results)

# API routes for AJAX requests
@app.route('/api/newsletter', methods=['POST'])
def newsletter_signup():
    data = request.get_json()
    email = data.get('email')
    
    if email:
        # Here you would save email to database
        return jsonify({'success': True, 'message': 'Successfully subscribed!'})
    return jsonify({'success': False, 'message': 'Invalid email'}), 400

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    # Process contact form
    return jsonify({'success': True, 'message': 'Message sent successfully!'})

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)