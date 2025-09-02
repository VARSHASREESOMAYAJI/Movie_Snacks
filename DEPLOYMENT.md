# 🚀 Deployment Guide - MovieSnacks

This guide will help you deploy the MovieSnacks food booking system to production.

## 🌐 Production Deployment Options

### Option 1: Heroku (Recommended for Beginners)

1. **Install Heroku CLI**
   ```bash
   # Windows
   https://devcenter.heroku.com/articles/heroku-cli
   
   # macOS
   brew install heroku/brew/heroku
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-moviesnacks-app
   ```

3. **Configure Environment Variables**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to production"
   git push heroku main
   ```

5. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py create_superuser
   heroku run python manage.py populate_food_items
   ```

### Option 2: DigitalOcean VPS

1. **Create Droplet**
   - Choose Ubuntu 22.04 LTS
   - Select plan based on expected traffic
   - Add SSH key for secure access

2. **Server Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3 python3-pip python3-venv nginx -y
   
   # Install PostgreSQL
   sudo apt install postgresql postgresql-contrib -y
   ```

3. **Application Setup**
   ```bash
   # Create user for app
   sudo adduser moviesnacks
   sudo usermod -aG sudo moviesnacks
   
   # Switch to user
   su - moviesnacks
   
   # Clone project
   git clone <your-repo-url>
   cd MovieTicket
   
   # Setup virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Database Configuration**
   ```bash
   # Create database
   sudo -u postgres psql
   CREATE DATABASE moviesnacks;
   CREATE USER moviesnacks_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE moviesnacks TO moviesnacks_user;
   \q
   ```

5. **Update Settings**
   ```python
   # settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com', 'your-ip-address']
   
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'moviesnacks',
           'USER': 'moviesnacks_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. **Gunicorn Setup**
   ```bash
   pip install gunicorn
   
   # Create gunicorn service
   sudo nano /etc/systemd/system/moviesnacks.service
   ```

   ```ini
   [Unit]
   Description=MovieSnacks Gunicorn daemon
   After=network.target
   
   [Service]
   User=moviesnacks
   Group=www-data
   WorkingDirectory=/home/moviesnacks/MovieTicket
   ExecStart=/home/moviesnacks/MovieTicket/venv/bin/gunicorn --workers 3 --bind unix:/home/moviesnacks/MovieTicket/moviesnacks.sock movie_ticket.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```

7. **Nginx Configuration**
   ```bash
   sudo nano /etc/nginx/sites-available/moviesnacks
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
   
       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /home/moviesnacks/MovieTicket;
       }
   
       location / {
           include proxy_params;
           proxy_pass http://unix:/home/moviesnacks/MovieTicket/moviesnacks.sock;
       }
   }
   ```

8. **Enable and Start Services**
   ```bash
   sudo systemctl start moviesnacks
   sudo systemctl enable moviesnacks
   sudo ln -s /etc/nginx/sites-available/moviesnacks /etc/nginx/sites-enabled
   sudo systemctl restart nginx
   ```

### Option 3: PythonAnywhere

1. **Create Account**
   - Sign up at www.pythonanywhere.com
   - Choose appropriate plan

2. **Upload Project**
   - Use Git clone or file upload
   - Install requirements

3. **Configure WSGI**
   - Update WSGI configuration file
   - Set environment variables

4. **Setup Database**
   - Use MySQL or PostgreSQL
   - Run migrations

## 🔧 Production Configuration

### Environment Variables
```bash
# Required
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-domain.com,your-ip-address

# Database (if using external DB)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Static Files
STATIC_ROOT=/path/to/static/files
MEDIA_ROOT=/path/to/media/files
```

### Security Settings
```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# If using HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic

# Configure web server to serve static files
# (Nginx, Apache, or CDN)
```

## 📱 QR Code Setup

1. **Generate QR Codes**
   ```bash
   # Install QR code generator
   pip install qrcode[pil]
   
   # Generate QR codes
   python generate_qr.py
   ```

2. **Update QR Code URLs**
   - Change `base_url` in `generate_qr.py`
   - Set to your production domain
   - Generate new QR codes

3. **Print and Distribute**
   - Print QR codes on adhesive labels
   - Place at each seat or section
   - Ensure good lighting for scanning

## 🔒 SSL/HTTPS Setup

### Let's Encrypt (Free SSL)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Update Nginx for HTTPS
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## 📊 Monitoring and Maintenance

### Log Monitoring
```bash
# Django logs
tail -f /var/log/django.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# System logs
sudo journalctl -u moviesnacks -f
```

### Backup Strategy
```bash
# Database backup
pg_dump moviesnacks > backup_$(date +%Y%m%d).sql

# File backup
tar -czf backup_$(date +%Y%m%d).tar.gz /home/moviesnacks/MovieTicket

# Automated backup script
# Create cron job for daily backups
```

### Performance Optimization
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Use Redis for caching
# Install: sudo apt install redis-server
```

## 🚨 Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic
   check STATIC_ROOT and STATIC_URL settings
   ```

2. **Database connection errors**
   ```bash
   check database credentials
   verify database service is running
   ```

3. **Permission denied errors**
   ```bash
   check file permissions
   verify user ownership
   ```

4. **500 Internal Server Error**
   ```bash
   check Django logs
   verify DEBUG=False in production
   ```

### Performance Issues

1. **Slow page loads**
   - Enable caching
   - Optimize database queries
   - Use CDN for static files

2. **High memory usage**
   - Reduce Gunicorn workers
   - Monitor memory usage
   - Optimize Django queries

## 📞 Support

- **Django Documentation**: https://docs.djangoproject.com/
- **Deployment Best Practices**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **Server Logs**: Check application and web server logs
- **Community**: Django forums and Stack Overflow

---

**🎬 Your MovieSnacks system is now ready for production! 🍿**
