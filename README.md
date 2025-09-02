# 🎬 MovieSnacks - Movie Theatre Food Booking System

A simple, responsive food booking web app for movie theatre customers. Users can scan a QR code, select their seat, order food, and pay via UPI or cash. Perfect for quick and easy food ordering during movies.

## ✨ Features

### User Side
- **QR Code Access**: Scan QR code to access the food menu
- **Seat Selection**: Enter unique seat number for each customer
- **Food Menu**: Browse available food items with descriptions and prices
- **Shopping Cart**: Add/remove items, update quantities
- **Order Form**: Enter name and optional mobile number
- **Payment Options**: UPI or Cash payment methods
- **Order Confirmation**: Detailed order summary and payment instructions
- **No Login Required**: Simple and quick ordering process

### Admin/Owner Side
- **Django Admin Interface**: Manage food items and orders
- **Food Management**: Add, edit, delete food items, mark availability
- **Order Management**: View all orders, filter by status, update payment status
- **Real-time Updates**: Monitor orders and payment status
- **Search & Filter**: Find orders by seat number, customer name, or status

## 🛠️ Technology Stack

- **Backend**: Django 5.x with SQLite database
- **Frontend**: HTML templates with Tailwind CSS
- **Database**: SQLite (easily deployable)
- **Admin**: Django's built-in admin interface
- **Responsive**: Mobile-first design for all devices

## 📁 Project Structure

```
MovieTicket/
├── movie_ticket/          # Django project settings
├── food_booking/          # Main app
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── forms.py          # Django forms
│   ├── admin.py          # Admin interface
│   ├── urls.py           # URL routing
│   └── management/       # Custom commands
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   └── food_booking/     # App-specific templates
├── static/                # Static files
├── manage.py             # Django management
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   # If you have the project files, navigate to the directory
   cd MovieTicket
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (admin account)**
   ```bash
   python manage.py create_superuser
   # Default: username=admin, password=admin123
   ```
   
   **⚠️ IMPORTANT SECURITY NOTE:**
   - Only superusers can access the owner dashboard
   - Regular staff users cannot see owner features
   - Owner links are completely hidden from regular users
   - All owner views are protected with multiple security layers

6. **Populate sample food items**
   ```bash
   python manage.py populate_food_items
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - **User Interface**: http://127.0.0.1:8000/
   - **Admin Interface**: http://127.0.0.1:8000/admin/

## 🎯 Usage Guide

### For Customers
1. **Scan QR Code**: Use your phone to scan the QR code at your seat
2. **Browse Menu**: View available food items and prices
3. **Add to Cart**: Select items and quantities
4. **Complete Order**: Enter seat number, name, and payment method
5. **Payment**: Pay via UPI or cash on delivery
6. **Enjoy**: Wait for delivery to your seat (15-20 minutes)

### For Theatre Staff/Admin
1. **Login**: Access admin panel at `/admin/`
2. **Manage Menu**: Add/remove food items, update prices
3. **Monitor Orders**: View incoming orders and payment status
4. **Update Status**: Mark orders as paid, delivered, or cancelled
5. **Track Revenue**: Monitor order totals and payment methods

## 🔧 Customization

### Adding New Food Items
- Use Django admin interface at `/admin/`
- Or run: `python manage.py populate_food_items`

### Modifying Payment Methods
- Edit `PAYMENT_METHOD_CHOICES` in `models.py`
- Update templates accordingly

### Changing Styling
- Modify Tailwind CSS classes in templates
- Update `base.html` for global style changes

### Database Changes
- Modify models in `models.py`
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`

## 📱 QR Code Integration

To generate QR codes for your theatre:
1. Use any QR code generator (online or app)
2. Set the URL to your domain: `https://yourdomain.com/`
3. Print and place at each seat
4. Customers scan to access the menu

## 💳 Payment Integration

### UPI Payment
- Currently shows placeholder QR code
- Integrate with UPI payment gateways like:
  - Razorpay
  - Paytm
  - PhonePe
  - Google Pay

### Cash Payment
- Marked as pending until staff confirms
- Staff can update status in admin panel

## 🚀 Deployment

### Local Development
```bash
python manage.py runserver
```

### Production Deployment
1. **Set DEBUG = False** in `settings.py`
2. **Configure production database** (PostgreSQL recommended)
3. **Set up static file serving**
4. **Configure web server** (Nginx + Gunicorn)
5. **Set environment variables** for security

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS**: Scalable cloud hosting
- **PythonAnywhere**: Simple Python hosting

## 🔒 Security Features

- CSRF protection on all forms
- Input validation and sanitization
- Session-based cart management
- Admin interface protection
- SQL injection prevention via Django ORM

## 📊 Database Models

### FoodItem
- `name`: Food item name
- `description`: Detailed description
- `price`: Item price (decimal)
- `available`: Availability status
- `created_at`, `updated_at`: Timestamps

### Order
- `seat_number`: Customer's seat
- `customer_name`: Customer's name
- `mobile_number`: Contact number (optional)
- `payment_method`: UPI or Cash
- `payment_status`: Pending, Paid, Failed
- `total_amount`: Order total
- `created_at`, `updated_at`: Timestamps

### OrderItem
- `order`: Foreign key to Order
- `food_item`: Foreign key to FoodItem
- `quantity`: Item quantity
- `price`: Item price at time of order

## 🎨 UI/UX Features

- **Responsive Design**: Works on all device sizes
- **Modern Interface**: Clean, intuitive design
- **Cart Management**: Easy add/remove/update items
- **Real-time Updates**: Cart updates without page refresh
- **Mobile-First**: Optimized for mobile devices
- **Accessibility**: Clear labels and navigation

## 🔄 Future Enhancements

- **Real-time Notifications**: WebSocket for order updates
- **Kitchen Dashboard**: Staff view for order preparation
- **Analytics**: Sales reports and customer insights
- **Loyalty Program**: Customer rewards system
- **Multi-language Support**: Internationalization
- **SMS Integration**: Order confirmations via SMS
- **Payment Gateway**: Direct UPI integration
- **Inventory Management**: Stock tracking

## 🐛 Troubleshooting

### Common Issues

1. **Database errors**
   ```bash
   python manage.py migrate
   ```

2. **Static files not loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Admin access issues**
   ```bash
   python manage.py create_superuser
   ```

4. **Template errors**
   - Check template syntax
   - Verify template inheritance
   - Check context variables

### Debug Mode
- Set `DEBUG = True` in `settings.py` for detailed error messages
- Check Django debug toolbar for development

## 📞 Support

For issues or questions:
1. Check the Django documentation
2. Review error logs in console
3. Verify database migrations
4. Check template syntax

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Django framework and community
- Tailwind CSS for styling
- Movie theatre industry for inspiration

---

**🎬 Enjoy your movie and food ordering experience! 🍿**
