import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class Chatbot:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.system_prompt = system_prompt
        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]
    
    def get_response(self, user_input):
        """Get response from the LLM and maintain conversation history."""
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run(self):
        """Run the chatbot interactively."""
        print("Welcome to the Python LLM Chatbot with Memory! Type 'exit' to quit.")
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Chatbot: Goodbye!")
                break
            
            response = self.get_response(user_input)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    # Create and run the chatbot
    bot = Chatbot(system_prompt="You are a helpful and friendly AI assistant.")
    bot.run()