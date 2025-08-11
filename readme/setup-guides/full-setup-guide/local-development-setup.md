# Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/dorm-manage-system.git
cd dorm-manage-system
```



### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```



### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```



### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Database Configuration
DB_NAME=dormitoriesplus
DB_USER=dorm_user
DB_PASSWORD=dorm_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Optional)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```



### Step 5: Run Database Migrations

```bash
python manage.py migrate
```



### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```



### Step 7: Compile Translations

```bash
# Compile all supported languages
python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
```



### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```



### Step 9: Run the Development Server

```bash
python manage.py runserver
```

Your application is now running at `http://localhost:8000`
