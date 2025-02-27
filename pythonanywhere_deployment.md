# Deploying Survey Chatbot on PythonAnywhere

## 1. Setup PythonAnywhere Account
1. Create a PythonAnywhere account at https://www.pythonanywhere.com/
2. Choose 'Web' from your dashboard and create a new web app
3. Select Python 3.11 and choose 'Manual Configuration'

## 2. Upload Your Code
1. In PythonAnywhere, open a Bash console
2. Clone your repository:
```bash
git clone https://github.com/Tonmoy-zero/survey-help2.1.git
```
3. Create a virtual environment and install dependencies:
```bash
mkvirtualenv --python=/usr/bin/python3.11 survey-bot-env
pip install google-generativeai python-telegram-bot flask python-dotenv
```

## 3. Configure Environment Variables
1. In PythonAnywhere dashboard:
   - Go to the 'Files' tab
   - Navigate to your project directory
   - Create a new file named `.env`
2. Add your environment variables:
```
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

## 4. Setup Supervisor
1. Install supervisor in your PythonAnywhere account:
```bash
pip install supervisor
```
2. Copy the contents of `supervisor_config.txt` to a new file:
```bash
mkdir -p ~/survey-help2.1/logs
cp supervisor_config.txt ~/survey-help2.1/supervisor.conf
```
3. Start supervisor with your configuration:
```bash
supervisord -c ~/survey-help2.1/supervisor.conf
```

## 5. Start the Bot
1. Use supervisor to manage the bot process:
```bash
supervisorctl status surveybot
supervisorctl start surveybot
```

## 6. Monitor and Maintenance
1. Check bot status:
```bash
supervisorctl status surveybot
```
2. View logs:
```bash
tail -f ~/survey-help2.1/logs/supervisor.out.log
```
3. Restart bot if needed:
```bash
supervisorctl restart surveybot
```

## Troubleshooting
1. If the bot fails to start, check:
   - Environment variables are set correctly
   - All dependencies are installed
   - Log files for specific error messages
2. Common issues:
   - Permission errors: Make sure log directory exists and is writable
   - Import errors: Verify all packages are installed in the virtual environment
   - Token errors: Double-check your API keys in .env file

## Important Notes
- Keep your API keys secure and never share them
- PythonAnywhere free tier has CPU usage limits
- Consider upgrading to a paid plan for production use
- Monitor the bot's performance and logs regularly