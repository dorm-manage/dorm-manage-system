# Web Application

* **Port**: 8080 (development) / 80 (production via nginx)
* **Framework**: Django 3.1.12
* **WSGI Server**: Gunicorn (production)
* **Development Server**: Django runserver (development)

### Database

* **Service**: PostgreSQL 13
* **Port**: 5432
* **Volume**: postgres\_data (persistent storage)

### Cache

* **Service**: Redis 6
* **Port**: 6379
* **Volume**: redis\_data (persistent storage)

### Web Server (Production)

* **Service**: Nginx
* **Port**: 80
* **Features**: Reverse proxy, static file serving, rate limiting

### Database Management (Development)

* **Service**: pgAdmin 4
* **Port**: 5050
* **Credentials**: admin@dormitoriesplus.com / admin123
