# Management Commands

#### Available Commands

```bash
# Send overdue item notifications
python manage.py send_overdue_notifications

# Test email configuration
python manage.py test_email
```

#### Creating Custom Commands

Place new commands in `DormitoriesPlus/management/commands/`:

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Your command description'
    
    def handle(self, *args, **options):
        # Command logic here
        pass
```
