# Bot configuration settings

# Welcome message shown on /start
WELCOME_TEXT = """
👋 Welcome to the Survey Chatbot!

I can help answer questions about:
📊 Company types and job information
💰 Financial information (income, revenue, assets)
👥 Demographics (race, housing, pets)
🎮 Entertainment preferences
🏥 Health conditions

Feel free to ask questions in your own words - I'll understand!
"""

# Help message shown on /help
HELP_TEXT = """
Here are some example questions you can ask:

💼 Job related:
• "What kind of work do people do?"
• "Tell me about the jobs people have"

💰 Financial:
• "How much are people making?"
• "What's the typical income?"

👥 Demographics:
• "Tell me about where people live"
• "What pets do people have?"

🎮 Entertainment:
• "What shows do people watch?"
• "How much time do they spend gaming?"

Just ask naturally and I'll do my best to help!
"""

# Error messages
ERROR_MESSAGES = {
    'general': "Sorry, I encountered an error. Please try again.",
    'invalid_input': "I couldn't understand that input. Please try rephrasing your question.",
    'no_response': "I couldn't generate a response. Please try asking another question."
}