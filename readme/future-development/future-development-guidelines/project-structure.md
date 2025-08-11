# Project Structure

```
DormitoriesPlus/
├── DormitoriesPlus/                 # Main Django app
│   ├── management/commands/         # Custom management commands
│   ├── migrations/                  # Database migrations
│   ├── templatetags/                # Custom template tags
│   ├── tests/                       # Test files
│   ├── models.py                    # Data models
│   ├── views.py                     # View functions
│   ├── api_views.py                 # API endpoints
│   ├── urls.py                      # URL routing
│   └── admin.py                     # Admin interface
├── DormitoriesPlus_project/         # Project settings
│   ├── settings.py                  # Main settings
│   ├── test_settings.py             # Test-specific settings
│   └── urls.py                      # Root URL configuration
├── templates/                       # HTML templates
│   ├── BM_pages/                    # Building Manager pages
│   ├── OM_pages/                    # Office Manager pages
│   ├── Student_pages/               # Student pages
│   └── emails/                      # Email templates
├── static/                          # Static files (CSS, JS)
├── media/                           # User-uploaded files
├── scripts/                         # Deployment scripts
└── requirements.txt                 # Python dependencies
```
