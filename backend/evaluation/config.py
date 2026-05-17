import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI

load_dotenv()

def get_llm():
    """
    Get LLM instance. Falls back to mock if keys are missing.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if not openai_key and not google_key:
        print("⚠️  No API keys found. Using mock LLM for evaluation.")
        return MockLLM()
    
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                api_key=openai_key,
                model="gpt-3.5-turbo",
                temperature=0
            )
        except Exception as e:
            print(f"⚠️  OpenAI init failed: {e}. Using mock LLM.")
            return MockLLM()
    
    if google_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                api_key=google_key,
                model="gemini-pro",
                temperature=0
            )
        except Exception as e:
            print(f"⚠️  Google GenAI init failed: {e}. Using mock LLM.")
            return MockLLM()

class MockLLM:
    """Mock LLM for testing when no API keys available"""
    def invoke(self, prompt):
        return type('obj', (object,), {'content': 'Mock evaluation response'})()