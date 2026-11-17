# 🏫 CPS Parent Guide: Your Education Assistant

An AI-powered chat assistant that helps Chicago Public Schools parents get information about enrollment, programs, policies, and resources.

## 🚀 Features

- **AI-Powered Q&A**: Get instant answers about CPS schools and programs
- **Multi-Chat Support**: Manage multiple conversation threads
- **Comprehensive Coverage**: Information about enrollment, transportation, nutrition, health services, and more
- **Parent-Friendly Interface**: Easy-to-use chat interface designed for parents

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Pinecone API key
- Pinecone index with CPS data

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd askneuUI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export PINECONE_API_KEY="your-pinecone-api-key"
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and set the path to `ask.py`
   - Click "Deploy"

3. **Set environment variables in Streamlit Cloud**
   - Go to your app settings
   - Add the following secrets:
     ```
     PINECONE_API_KEY = "your-pinecone-api-key"
     OPENAI_API_KEY = "your-openai-api-key"
     ```

### Option 2: Heroku

1. **Create Procfile**
   ```bash
   echo "web: streamlit run ask.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

2. **Create runtime.txt**
   ```bash
   echo "python-3.9.18" > runtime.txt
   ```

3. **Deploy to Heroku**
   ```bash
   heroku create your-cps-parent-guide
   heroku config:set PINECONE_API_KEY="your-pinecone-api-key"
   heroku config:set OPENAI_API_KEY="your-openai-api-key"
   git push heroku main
   ```

### Option 3: Railway

1. **Connect your GitHub repository to Railway**
2. **Set environment variables** in Railway dashboard
3. **Deploy automatically**

## 🔧 Configuration

### Environment Variables

- `PINECONE_API_KEY`: Your Pinecone API key
- `OPENAI_API_KEY`: Your OpenAI API key

### Pinecone Index Setup

Make sure your Pinecone index (`cps_parents`) contains:
- CPS school information
- Enrollment policies
- Academic programs
- Transportation guidelines
- Health and nutrition information
- Parent resources

## 📱 Usage

1. **Open the deployed application**
2. **Enter your OpenAI API key** in the sidebar
3. **Start asking questions** about CPS schools and programs
4. **Use the chat management** to organize multiple conversations

## 🎯 Example Questions

- "How do I enroll my child in CPS?"
- "What are the requirements for kindergarten enrollment?"
- "Tell me about IB programs in CPS"
- "How does school transportation work?"
- "What are the free lunch program requirements?"
- "How can I get involved in my child's school?"

## 🔗 Resources

- **CPS Main Office**: (773) 553-1000
- **CPS Website**: [cps.edu](https://cps.edu)
- **Parent Portal**: [parent.cps.edu](https://parent.cps.edu)
- **Emergency Hotline**: (773) 535-4400

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Important Notes

- **API Keys**: Never commit API keys to version control
- **Data Privacy**: Ensure compliance with student data privacy laws
- **Accuracy**: Always verify information with official CPS sources
- **Updates**: Keep the knowledge base updated with current CPS policies 