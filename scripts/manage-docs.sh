#!/bin/bash

# Documentation Management Script
# This script helps manage the GitBook documentation

echo "📚 DormitoriesPlus Documentation Manager"
echo "========================================"

case "$1" in
    "build")
        echo "🔨 Building documentation..."
        cd docs
        if command -v gitbook &> /dev/null; then
            gitbook build
            echo "✅ Documentation built successfully!"
            echo "📁 Output: docs/_book/"
        else
            echo "❌ GitBook CLI not found. Please install it first:"
            echo "   npm install -g gitbook-cli@2.3.2"
            echo "   gitbook install"
        fi
        ;;
        
    "serve")
        echo "🌐 Starting documentation server..."
        cd docs
        if command -v gitbook &> /dev/null; then
            echo "📖 Documentation available at: http://localhost:4000"
            gitbook serve
        else
            echo "❌ GitBook CLI not found. Please install it first:"
            echo "   npm install -g gitbook-cli@2.3.2"
            echo "   gitbook install"
        fi
        ;;
        
    "install")
        echo "📦 Installing GitBook CLI..."
        npm install -g gitbook-cli@2.3.2
        echo "📚 Installing GitBook..."
        gitbook install
        echo "✅ GitBook installed successfully!"
        ;;
        
    "deploy")
        echo "🚀 Deploying documentation..."
        echo "📝 This will trigger GitHub Actions to deploy to GitHub Pages"
        echo "🌐 Documentation will be available at: https://your-username.github.io/dorm-manage-system/docs/"
        git add docs/
        git commit -m "Update documentation"
        git push
        echo "✅ Documentation deployment triggered!"
        ;;
        
    "validate")
        echo "🔍 Validating documentation structure..."
        if [ -f "docs/README.md" ]; then
            echo "✅ README.md found"
        else
            echo "❌ README.md missing"
        fi
        
        if [ -f "docs/SUMMARY.md" ]; then
            echo "✅ SUMMARY.md found"
        else
            echo "❌ SUMMARY.md missing"
        fi
        
        if [ -f "docs/book.json" ] || [ -f "docs/.gitbook.yaml" ]; then
            echo "✅ GitBook configuration found"
        else
            echo "❌ GitBook configuration missing"
        fi
        
        echo "📊 Documentation validation complete!"
        ;;
        
    *)
        echo "Usage: $0 {build|serve|install|deploy|validate}"
        echo ""
        echo "Commands:"
        echo "  build     - Build the documentation"
        echo "  serve     - Start local documentation server"
        echo "  install   - Install GitBook CLI"
        echo "  deploy    - Deploy to GitHub Pages"
        echo "  validate  - Validate documentation structure"
        echo ""
        echo "Examples:"
        echo "  $0 install    # Install GitBook CLI"
        echo "  $0 build      # Build documentation"
        echo "  $0 serve      # Start local server"
        echo "  $0 deploy     # Deploy to GitHub Pages"
        ;;
esac 