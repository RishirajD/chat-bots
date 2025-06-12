import os
import json
import anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Anthropic API key
api_key = os.getenv("ANTHROPIC_API_KEY")
claude_client = anthropic.Anthropic(api_key=api_key)

class ClaudeChatbot:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.system_prompt = system_prompt
        self.conversation_history = []
        
    def get_response(self, user_input):
        """Get response from the Claude API."""
        # Convert conversation history to Claude format
        messages = []
        
        for i, msg in enumerate(self.conversation_history):
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                messages.append({"role": "assistant", "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                system=self.system_prompt,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )
            
            # Store the conversation
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": response.content[0].text})
            
            return response.content[0].text
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def save_conversation(self, filename="claude_conversation.json"):
        """Save the conversation history to a file."""
        with open(filename, "w") as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"Conversation saved to {filename}")
    
    def run(self):
        """Run the chatbot interactively."""
        print("Welcome to the Claude Chatbot! Type 'exit' to quit or 'save' to save the conversation.")
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() == "exit":
                print("Claude: Goodbye!")
                break
            
            elif user_input.lower() == "save":
                self.save_conversation()
                continue
            
            response = self.get_response(user_input)
            print(f"Claude: {response}")

if __name__ == "__main__":
    # Create and run the Claude chatbot
    bot = ClaudeChatbot(system_prompt="You are Claude, a helpful and friendly AI assistant created by Anthropic.")
    bot.run()