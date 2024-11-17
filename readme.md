# Text Alchemy ✨

Text Alchemy is an AI-powered text summarization tool that transforms lengthy articles into concise, meaningful summaries. With seamless Telegram integration, you can access your summaries on the go!

![Text Alchemy Banner](images/logo.jpg)

## ✨ Features

- 📝 Convert long articles into concise summaries
- 📱 Telegram integration for mobile access
- 📊 CSV file support for batch processing
- 🎨 Beautiful, user-friendly interface
- 🚀 Real-time processing

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Shantnu-singh/text-alchemy.git
cd app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the project root
   - Add required credentials:
```env
GOOGLE_API_KEY= your_gemini_api_token
```

### Running the Application

1. Start the Telegram bot:
```bash
python bot.py
```

2. Launch the web application:
```bash
streamlit run app.py
```

## 📖 Usage

1. Upload your CSV file containing articles
2. Click "Generate Summaries"
3. Access summaries via the web interface or Telegram bot

## 📱 Telegram Integration

1. Click "Open Telegram Bot" in the web interface
2. Start the bot with `/start`
3. Use `/summary` to view your latest summaries

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

