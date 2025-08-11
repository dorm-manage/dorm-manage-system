# Translation Support

### Supported Languages

The application supports multiple languages:

* **Hebrew (עברית)** - Default language
* **English** - Secondary language
* **Arabic (العربية)** - RTL support
* **Chinese (中文)** - Simplified Chinese



### Translation Management

**Compile Translations**

```
# Local development
python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv

# Docker
docker-compose exec web python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
```

**Create New Translations**

```
# Local development
python manage.py makemessages -l he -l en -l ar -l zh

# Docker
docker-compose exec web python manage.py makemessages -l he -l en -l ar -l zh
```

**Update Existing Translations**

```
# Local development
python manage.py makemessages -a

# Docker
docker-compose exec web python manage.py makemessages -a
```



### Testing Translations

```
# Test Docker translation setup
./scripts/test-docker-translations.sh
```
