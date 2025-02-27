import os
import logging
import google.generativeai as genai
import time
from typing import Optional

logger = logging.getLogger(__name__)

def init_genai():
    """Initialize the Gemini API client"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    try:
        genai.configure(api_key=api_key)
        # Test the configuration with a simple call
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        logger.info("Gemini API initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Gemini API: {str(e)}")
        raise

def generate_response(user_input: str) -> Optional[str]:
    """Generate a response using the Gemini model"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        logger.debug(f"Processing query: {user_input}")

        # Complete context with all survey data
        context = """You are a survey chatbot. Only answer questions based on this exact data:

1. Employment Data:
- Company Types: Manufacturing, Information technology, Construction, Transportation
- Job Description: Information technology, Human resource
- Job Title: CTO, chief technology officer, chief information officer
- Job Responsibility: Director
- Job Sector: IT

2. Financial Information:
- Company Annual Revenue: $100M to $500M
- Annual Income (before tax): $150,000 to $200,000
- Investable Assets: More than $500,000, less than $999,999
- Credit Score: 600 to 799
- Household Yearly Income: $100,000 to $200,000

3. Demographics:
- Race/Ethnicity: White, Hispanic/Latino
- Housing: Homeowner
- Car Owner: Yes
- Pets: Cat & Dog

4. Entertainment:
- TV/Streaming Weekly Watch Time: 20+ hours
- Video Subscriptions: Netflix, Hulu, Amazon Prime, Apple TV+, Disney+
- TV Providers: DishTV, Fios-Verizon, Direct TV
- Music Streaming: YouTube Music, Spotify
- Movie Theater Visits: 10 in past year, 4-6 in past 6 months, 1 in past 2 months
- Gaming: 10-20 hours per week

5. Other Information:
- Education: Postgraduate/Masters/MA
- Health Conditions: Type 2 diabetes, COPD, migraine
- Prior Survey Participation: No

Instructions:
1. Return ONE specific answer matching the data above
2. For financial questions, format with $ and commas
3. Keep answers concise and exact
4. Do not add emojis or decorative elements
5. For unmatched questions, provide an AI-based response
6. Match similar questions to their exact data points"""

        prompt = f"""Context: {context}

Question: {user_input}
Required: Return a single, focused answer that exactly matches the data. For questions not in the dataset, provide a factual AI response.
Answer:"""

        logger.info("Generating response from Gemini API")

        try:
            config = genai.types.GenerationConfig(
                temperature=0.1,  # Very low temperature for consistent responses
                top_p=0.8,
                top_k=40,
                max_output_tokens=150  # Limit token length for focused answers
            )

            response = model.generate_content(
                prompt,
                generation_config=config
            )
            logger.debug(f"Raw API response: {response}")

            if response and hasattr(response, 'text'):
                cleaned_response = response.text.strip()
                logger.info(f"Generated response: {cleaned_response[:100]}...")
                return cleaned_response

            logger.warning("Invalid or empty response received from model")
            return None

        except Exception as api_error:
            logger.error(f"API call failed: {str(api_error)}")
            raise

    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        raise