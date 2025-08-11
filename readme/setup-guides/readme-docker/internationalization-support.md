# Internationalization Support

### Supported Languages

The Docker setup includes full internationalization support for:

* **Hebrew (עברית)** - Default language
* **English** - Secondary language
* **Arabic (العربية)** - RTL support
* **Chinese (中文)** - Simplified Chinese

### Translation Features

* **Automatic compilation** of `.po` files during Docker build
* **Runtime language switching** via URL parameters or cookies
* **RTL layout support** for Hebrew and Arabic
* **Unicode support** for all languages
* **Fallback handling** for missing translations

### Translation Management

```bash
# Compile translations manually (if needed)
docker-compose exec web python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh

# Create new translation files
docker-compose exec web python manage.py makemessages -l he -l en -l ar -l zh

# Update existing translations
docker-compose exec web python manage.py makemessages -a
```

### Language Switching

Users can switch languages by:

1. **URL parameter**: `?lang=en`
2. **Cookie setting**: `django_language=en`
3. **Browser language detection** (automatic)
