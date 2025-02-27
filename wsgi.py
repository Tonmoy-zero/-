import os
import sys

# Add your project directory to Python path
project_home = os.path.expanduser('~/survey-help2.1')
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your telegram bot application
from telegram_bot import main

# Run the bot
if __name__ == '__main__':
    main()