def format_response(response):
    """Format the chatbot response for Telegram display"""
    if not response:
        return "I couldn't generate a response. Please try asking another question."

    # Clean up response text and remove any potential markdown/formatting
    formatted = response.strip()

    return formatted

def validate_command(command):
    """Validate bot commands"""
    valid_commands = ['/start', '/help']
    return command in valid_commands