#!/bin/bash

echo "🚀 CPS Parent Guide Deployment Script"
echo "====================================="

# Check if repository name is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your GitHub username as an argument"
    echo "Usage: ./deploy.sh YOUR_GITHUB_USERNAME"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="cps-parent-guide"

echo "📝 Setting up repository: $GITHUB_USERNAME/$REPO_NAME"

# Remove existing remote if any
git remote remove origin 2>/dev/null

# Add new remote
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Push to GitHub
echo "📤 Pushing code to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎯 Next Steps:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Repository: $GITHUB_USERNAME/$REPO_NAME"
    echo "5. Main file path: ask.py"
    echo "6. Click 'Deploy'"
    echo ""
    echo "🔑 Don't forget to set environment variables in Streamlit Cloud:"
    echo "   - PINECONE_API_KEY"
    echo "   - OPENAI_API_KEY"
else
    echo "❌ Failed to push to GitHub. Please check your repository URL."
fi 