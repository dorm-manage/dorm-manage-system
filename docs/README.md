# DormitoriesPlus Documentation

Welcome to the comprehensive documentation for DormitoriesPlus - a modern dormitory management system with multi-language support.

## 📚 Documentation Overview

### 🚀 Getting Started
- **[Quick Start Guide](quick-start-guide.md)** - Get up and running in minutes
- **[Local and Docker Setup](local-and-docker-setup.md)** - Comprehensive setup instructions

### 🌐 Features
- **Multi-language Support** - Hebrew, English, Arabic, and Chinese
- **Role-based Access** - Students, Building Managers, and Office Managers
- **Inventory Management** - Track and manage dormitory equipment
- **Fault Reporting** - Report and track maintenance issues
- **Loan System** - Manage equipment borrowing and returns

### 🛠️ Development
- **Translation Management** - How to add and manage translations
- **Docker Configuration** - Containerized deployment
- **API Documentation** - REST API endpoints
- **Testing Guide** - How to run tests and ensure quality

## 🎯 Quick Navigation

### For New Users
1. Start with the **[Quick Start Guide](quick-start-guide.md)**
2. Choose your setup method (Docker or Local)
3. Follow the step-by-step instructions

### For Developers
1. Review the **[Local and Docker Setup](local-and-docker-setup.md)**
2. Set up your development environment
3. Explore the translation system
4. Contribute to the project

### For Administrators
1. Understand the **[Docker Setup](local-and-docker-setup.md#docker-setup)**
2. Configure production environment
3. Manage translations and updates

## 🌟 Key Features

### Multi-language Support
- **Hebrew (עברית)** - Default language with RTL support
- **English** - Secondary language
- **Arabic (العربية)** - RTL layout support
- **Chinese (中文)** - Simplified Chinese

### User Roles
- **Students** - Report faults, request equipment loans
- **Building Managers** - Manage specific building operations
- **Office Managers** - System-wide administration

### Core Functionality
- **Inventory Management** - Track equipment and supplies
- **Fault Reporting** - Report and track maintenance issues
- **Loan System** - Manage equipment borrowing
- **User Management** - Manage student and staff accounts

## 🚀 Quick Start

### Docker (Recommended)
```bash
git clone https://github.com/your-username/dorm-manage-system.git
cd dorm-manage-system
./scripts/docker-translation-setup.sh dev
# Access at http://localhost:8080
```

### Local Development
```bash
git clone https://github.com/your-username/dorm-manage-system.git
cd dorm-manage-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Access at http://localhost:8000
```

## 📊 System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux

### Recommended Requirements
- **RAM**: 8GB+
- **Storage**: 5GB free space
- **CPU**: Multi-core processor

## 🔧 Technology Stack

- **Backend**: Django 3.1+
- **Database**: PostgreSQL (with SQLite for development)
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker & Docker Compose
- **Translation**: Django Internationalization (i18n)

## 📱 Access Points

- **Local Development**: http://localhost:8000
- **Docker Development**: http://localhost:8080
- **Docker Production**: http://localhost:80

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Translation Contributions
- Add translations to `.po` files in the `locale/` directory
- Test translations with `python manage.py compilemessages`
- Ensure RTL support for Hebrew and Arabic

## 🐛 Support

### Getting Help
1. **Check the documentation** - Most questions are answered here
2. **Review troubleshooting sections** - Common issues and solutions
3. **Search existing issues** - Your problem might already be solved
4. **Create a new issue** - Provide detailed information

### Common Issues
- **Translation warnings** - Expected for Django built-in strings
- **Docker startup issues** - Check Docker Desktop is running
- **Port conflicts** - Stop existing containers or change ports

## 📈 Roadmap

### Upcoming Features
- **Mobile App** - Native iOS and Android applications
- **Advanced Analytics** - Detailed reporting and insights
- **API Enhancements** - RESTful API for third-party integrations
- **Additional Languages** - Support for more languages

### Recent Updates
- ✅ **Multi-language Support** - Hebrew, English, Arabic, Chinese
- ✅ **Docker Configuration** - Containerized deployment
- ✅ **Translation Management** - Comprehensive i18n support
- ✅ **Role-based Access** - Student, Building Manager, Office Manager roles

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Community** - For the excellent web framework
- **Translation Contributors** - For helping with multi-language support
- **Open Source Community** - For the tools and libraries used

---

**Happy coding! 🚀**

For questions or support, please [create an issue](https://github.com/your-username/dorm-manage-system/issues) or check our [documentation](local-and-docker-setup.md). 