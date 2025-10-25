import os
from openai import OpenAI
try:
    from pandasai import Agent
    from pandasai.llm.base import BaseOpenAI
except ImportError:
    from pandasai import SmartDataframe
    from pandasai.llm.base import BaseOpenAI

# Custom OpenRouter LLM class for PandasAI
class OpenRouterLLM(BaseOpenAI):
    def __init__(self, api_token, model="meta-llama/llama-3.3-70b-instruct:free"):
        # Initialize parent class without parameters
        super().__init__()
        
        # Set required attributes
        self.api_token = api_token
        self.model = model
        self._is_chat_model = True
        self._max_retries = 3
        
        # Create OpenRouter client
        self.openai_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
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
        
        self.client = MockClient(self.openai_client, self.model)
    
    def _generate_text(self, prompt: str) -> str:
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
                max_tokens=1000,
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    @property
    def type(self) -> str:
        return "openrouter"

def get_agent(df, api_key, model="qwen/qwen-2.5-72b-instruct:free"):
    """Create and return a PandasAI agent"""
    llm = OpenRouterLLM(
        api_token=api_key,
        model=model
    )
    
    # Disable cache to avoid DuckDB lock issues with multiple Streamlit sessions
    agent = Agent(df, config={
        "llm": llm, 
        "verbose": True,
        "enable_cache": False
    })
    return agent

def test_openrouter_connection(api_key):
    """Test OpenRouter connection"""
    try:
        openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        test_completion = openrouter_client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://pandasai-app.com",
                "X-Title": "PandasAI App",
            },
            model="qwen/qwen-2.5-72b-instruct:free",
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
