# GitBook Setup Guide

This guide explains what to do with the `book.json` file and how to set up your documentation.

## 📚 What is `book.json`?

The `book.json` file is the configuration file for GitBook. It tells GitBook:
- How to structure your documentation
- Which plugins to use
- What settings to apply
- How to customize the appearance

## 🚀 Setup Options

### Option 1: GitBook.com (Recommended)

**Best for**: Easy setup, automatic hosting, collaboration

1. **Go to [gitbook.com](https://gitbook.com)**
2. **Create an account** or sign in
3. **Create a new space**
4. **Import your repository**:
   - Connect your GitHub repository
   - Or upload the `docs/` folder manually
5. **GitBook will automatically detect** and use your `book.json` configuration

**Benefits**:
- ✅ Automatic hosting
- ✅ Real-time collaboration
- ✅ Version control integration
- ✅ Custom domains
- ✅ Analytics

### Option 2: GitHub Pages (Free)

**Best for**: Free hosting, GitHub integration

1. **Enable GitHub Pages** in your repository settings
2. **Set source to GitHub Actions**
3. **Push your changes** - the GitHub Actions workflow will automatically build and deploy

**Benefits**:
- ✅ Free hosting
- ✅ Automatic deployment
- ✅ GitHub integration
- ✅ Custom domains

### Option 3: Local Development

**Best for**: Development, testing

```bash
# Install GitBook CLI
npm install -g gitbook-cli@2.3.2
gitbook install

# Build documentation
cd docs
gitbook build

# Serve locally
gitbook serve
```

## 🛠️ Using the Management Script

We've created a script to help you manage the documentation:

```bash
# Install GitBook CLI
./scripts/manage-docs.sh install

# Build documentation
./scripts/manage-docs.sh build

# Serve locally
./scripts/manage-docs.sh serve

# Deploy to GitHub Pages
./scripts/manage-docs.sh deploy

# Validate structure
./scripts/manage-docs.sh validate
```

## 📁 File Structure

```
docs/
├── README.md              # Main documentation page
├── SUMMARY.md             # Navigation structure
├── book.json              # GitBook configuration (JSON)
├── .gitbook.yaml          # GitBook configuration (YAML)
├── quick-start-guide.md   # Quick start instructions
├── local-and-docker-setup.md  # Comprehensive setup
└── [other documentation files]
```

## ⚙️ Configuration Options

### `book.json` vs `.gitbook.yaml`

Both files serve the same purpose. We provide both for compatibility:

- **`book.json`** - JSON format, older GitBook versions
- **`.gitbook.yaml`** - YAML format, newer GitBook versions

### Key Configuration Settings

```json
{
  "title": "DormitoriesPlus Documentation",
  "description": "Comprehensive documentation for DormitoriesPlus",
  "plugins": [
    "expandable-chapters",    // Collapsible chapters
    "copy-code-button",       // Copy code buttons
    "search-plus",           // Enhanced search
    "theme-default",         // Default theme
    "highlight",             // Syntax highlighting
    "sharing",              // Social sharing
    "fontsettings",         // Font customization
    "livereload"            // Auto-reload during development
  ]
}
```

## 🌐 Deployment Options

### 1. GitBook.com Deployment

```bash
# 1. Push to GitHub
git add docs/
git commit -m "Update documentation"
git push

# 2. Connect to GitBook.com
# - Go to gitbook.com
# - Create new space
# - Connect GitHub repository
# - GitBook will auto-deploy
```

### 2. GitHub Pages Deployment

```bash
# 1. Push changes
git add docs/
git commit -m "Update documentation"
git push

# 2. GitHub Actions will automatically:
# - Build the documentation
# - Deploy to GitHub Pages
# - Available at: https://your-username.github.io/dorm-manage-system/docs/
```

### 3. Manual Deployment

```bash
# Build locally
./scripts/manage-docs.sh build

# Upload docs/_book/ to your web server
```

## 🔧 Customization

### Adding Plugins

Edit `book.json` or `.gitbook.yaml`:

```json
{
  "plugins": [
    "your-custom-plugin"
  ],
  "pluginsConfig": {
    "your-custom-plugin": {
      "option": "value"
    }
  }
}
```

### Custom Theme

```json
{
  "plugins": [
    "theme-default"
  ],
  "pluginsConfig": {
    "theme-default": {
      "showLevel": true,
      "styles": {
        "website": "styles/website.css",
        "ebook": "styles/ebook.css",
        "pdf": "styles/pdf.css",
        "mobi": "styles/mobi.css",
        "epub": "styles/epub.css"
      }
    }
  }
}
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: GitBook CLI not found
```bash
# Solution
npm install -g gitbook-cli@2.3.2
gitbook install
```

**Issue**: Build fails
```bash
# Check structure
./scripts/manage-docs.sh validate

# Reinstall GitBook
gitbook install
```

**Issue**: GitHub Pages not updating
```bash
# Check GitHub Actions
# Go to Actions tab in your repository
# Ensure the workflow completed successfully
```

### Validation

```bash
# Validate your documentation structure
./scripts/manage-docs.sh validate
```

## 📊 Next Steps

1. **Choose your deployment option** (GitBook.com recommended)
2. **Customize the configuration** if needed
3. **Add more documentation** as your project grows
4. **Set up custom domain** for professional appearance
5. **Enable analytics** to track usage

## 🎯 Quick Commands

```bash
# Full setup (local development)
./scripts/manage-docs.sh install
./scripts/manage-docs.sh build
./scripts/manage-docs.sh serve

# Deploy to GitHub Pages
./scripts/manage-docs.sh deploy

# Validate everything
./scripts/manage-docs.sh validate
```

---

**Your documentation is ready! 🚀**

Choose your preferred deployment option and start sharing your documentation with the world. 