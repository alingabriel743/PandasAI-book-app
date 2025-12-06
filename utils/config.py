import os
import time
import random
from openai import OpenAI
try:
    from pandasai import Agent
    from pandasai.llm.base import BaseOpenAI
except ImportError:
    from pandasai import SmartDataframe
    from pandasai.llm.base import BaseOpenAI

# Custom Groq LLM class for PandasAI
class GroqLLM(BaseOpenAI):
    def __init__(self, api_token, model="llama-3.3-70b-versatile"):
        # Initialize parent class without parameters
        super().__init__()
        
        # Set required attributes
        self.api_token = api_token
        self.model = model
        self._is_chat_model = True
        self._max_retries = 3
        
        # Create Groq client (using OpenAI compatible client)
        self.openai_client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_token,
        )
        
        # Create a mock client object that PandasAI expects
        class MockClient:
            def __init__(self, openai_client, model):
                self.openai_client = openai_client
                self.model = model
            
            def create(self, **kwargs):
                # Convert PandasAI parameters to OpenAI format
                messages = kwargs.get('messages', [])
                max_tokens = kwargs.get('max_tokens', 1000)
                temperature = kwargs.get('temperature', 0)
                
                max_retries = 5
                base_delay = 2
                
                for attempt in range(max_retries):
                    try:
                        response = self.openai_client.chat.completions.create(
                            extra_headers={
                                "HTTP-Referer": "https://pandasai-app.com",
                                "X-Title": "PandasAI App",
                            },
                            model=self.model,
                            messages=messages,
                            max_tokens=max_tokens,
                            temperature=temperature
                        )
                        return response
                    except Exception as e:
                        if "429" in str(e) and attempt < max_retries - 1:
                            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                            print(f"Rate limit hit. Retrying in {delay:.2f}s...")
                            time.sleep(delay)
                        else:
                            raise e
        
        self.client = MockClient(self.openai_client, self.model)
    
    def _generate_text(self, prompt: str) -> str:
        max_retries = 5
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = self.openai_client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://pandasai-app.com",
                        "X-Title": "PandasAI App",
                    },
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=4000,
                    temperature=0
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limit hit. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
                elif attempt == max_retries - 1:
                    raise Exception(f"Groq API error: {str(e)}")
                else:
                    raise Exception(f"Groq API error: {str(e)}")
    
    @property
    def type(self) -> str:
        return "groq"

def get_agent(df, api_key, model="llama-3.3-70b-versatile"):
    """Create and return a PandasAI agent"""
    llm = GroqLLM(
        api_token=api_key,
        model=model
    )
    
    # Disable cache to avoid DuckDB lock issues with multiple Streamlit sessions
    agent = Agent(df, config={
        "llm": llm, 
        "verbose": True,
        "enable_cache": False,
        "custom_whitelisted_dependencies": ["requests"]
    })
    return agent

def test_groq_connection(api_key):
    """Test Groq connection"""
    try:
        groq_client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
        )
        
        test_completion = groq_client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://pandasai-app.com",
                "X-Title": "PandasAI App",
            },
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Just testing the connection. Please respond with 'Connection successful!'"
                }
            ],
            max_tokens=50
        )
        # Ensure the response is properly encoded
        response_content = test_completion.choices[0].message.content
        return True, response_content.encode('utf-8', errors='ignore').decode('utf-8')
    except Exception as e:
        # Ensure error message is properly encoded
        error_msg = str(e).encode('utf-8', errors='ignore').decode('utf-8')
        return False, error_msg
