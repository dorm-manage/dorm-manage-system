# Quick Start Options

### Option 1: Docker (Recommended)

**Prerequisites**: Docker Desktop

```bash
# Clone the repository
git clone https://github.com/your-username/dorm-manage-system.git
cd dorm-manage-system

# Start with Docker (Development mode)
./scripts/docker-translation-setup.sh dev

# Access the application
# Open http://localhost:8080 in your browser
```

see [readme-docker](../readme-docker/ "mention") for mor info.



### Option 2: Local Development

**Prerequisites**: Python 3.8+, pip, Git

```bash
# Clone the repository
git clone https://github.com/your-username/dorm-manage-system.git
cd dorm-manage-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env  # Create environment file
python manage.py migrate
python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver

# Access the application
# Open http://localhost:8000 in your browser
```
