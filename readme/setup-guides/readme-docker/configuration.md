# Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database settings
DB_NAME=dormitoriesplus
DB_USER=dorm_user
DB_PASSWORD=dorm_password
DB_HOST=db
DB_PORT=5432

# Email settings (for production)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=dormitoriesplus.notifications@gmail.com

# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### Database Configuration

The application uses PostgreSQL with the following default settings:

* **Database**: dormitoriesplus
* **User**: dorm\_user
* **Password**: dorm\_password
* **Host**: db (container name)
* **Port**: 5432

see .env file for all info.

### Redis Configuration

Redis is used for caching and session storage:

* **Host**: redis (container name)
* **Port**: 6379
