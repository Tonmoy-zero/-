import os
import logging
from typing import Optional
from generative_model import init_genai, generate_response
import time

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Set to DEBUG for more detailed logs
)

class ChatHandler:
    def __init__(self):
        """Initialize the ChatHandler"""
        logger.info("Initializing chat handler")
        try:
            init_genai()
            logger.info("Gemini API initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
            raise

    def get_response(self, user_input: str, max_retries: int = 3) -> str:
        """Generate an AI response for the user's question with retries"""
        if not user_input:
            return "Please provide a question to get started."

        logger.debug(f"Processing question: {user_input}")

        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries} - Generating response")
                response = generate_response(user_input)

                if response:
                    logger.info("Successfully generated response")
                    return response

                logger.warning(f"Empty response on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Progressive backoff
                    logger.info(f"Waiting {wait_time} seconds before retry")
                    time.sleep(wait_time)
                    continue

            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
                error_msg = str(e).lower()

                # Check for specific error types
                if "api" in error_msg or "token" in error_msg:
                    if attempt == max_retries - 1:
                        return "I'm having trouble with my knowledge connection. Please try again in a moment."
                elif "timeout" in error_msg:
                    if attempt == max_retries - 1:
                        return "I took too long to think about that. Could you try a simpler question?"
                elif attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Waiting {wait_time} seconds before retry")
                    time.sleep(wait_time)
                    continue
                else:
                    return "I encountered an error. Please try rephrasing your question."

        return "I couldn't understand that question well enough. Could you try asking it differently?"