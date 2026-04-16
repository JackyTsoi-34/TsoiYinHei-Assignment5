"""
Simple LLM-based Agent Module
Handles interactions with DeepSeek's API for the dashboard.
"""

import os
import json
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIAgent:
    """Simple AI Agent that interacts with DeepSeek's API."""
    
    def __init__(self, model: str = "deepseek-chat", temperature: float = 0.7):
        """
        Initialize the AI Agent.
        
        Args:
            model: The model to use (default: deepseek-chat)
            temperature: Temperature for response generation (0.0-2.0)
        """
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
        
        if not self.api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY not found in environment variables. "
                "Please create a .env file with your API key."
            )
        
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)
        self.model = model
        self.temperature = temperature
        self.conversation_history = []
    
    def process(
        self, 
        user_input: str, 
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Process user input and return agent response.
        
        Args:
            user_input: The user's query/input
            temperature: Optional temperature override
            system_prompt: Optional custom system prompt
            
        Returns:
            The agent's response as a string
        """
        if not user_input or not user_input.strip():
            return "Error: Please provide a valid input."
        
        # Use provided temperature or instance default
        temp = temperature if temperature is not None else self.temperature
        
        # Default system prompt
        if system_prompt is None:
            system_prompt = (
                "You are a helpful AI assistant. Provide clear, concise, "
                "and accurate responses to user queries."
            )
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            # Call API (compatible with OpenAI format)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *self.conversation_history
                ],
                temperature=min(max(temp, 0.0), 2.0),
                max_tokens=500
            )
            
            # Extract response from OpenAI-compatible format
            agent_response = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": agent_response
            })
            
            return agent_response
            
        except Exception as e:
            return f"Error communicating with API: {str(e)}"
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def set_model(self, model: str):
        """Change the model."""
        self.model = model
    
    def set_temperature(self, temperature: float):
        """Update temperature setting."""
        self.temperature = min(max(temperature, 0.0), 2.0)


# Convenience function for quick interactions
def create_agent(model: str = "deepseek-chat", temperature: float = 0.7) -> AIAgent:
    """Factory function to create an AI agent."""
    return AIAgent(model=model, temperature=temperature)
