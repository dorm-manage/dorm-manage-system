# Development Workflow

### Local Development

1.  **Start the development server**:

    ```
    python manage.py runserver
    ```
2. **Make changes** to your code or templates
3. **Test changes** in your browser at `http://localhost:8000`
4.  **For translation changes**:

    ```
    python manage.py makemessages -a
    # Edit .po files in locale/ directory
    python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
    ```



### Docker Development

1.  **Start containers**:

    ```
    docker-compose up --build
    ```
2. **Make changes** to your code or templates
3.  **Rebuild containers** (if needed):

    ```
    docker-compose up --build
    ```
4.  **For translation changes**:

    ```
    docker-compose exec web python manage.py makemessages -a
    # Edit .po files in locale/ directory
    docker-compose exec web python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv

    ```
