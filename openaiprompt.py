import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class SpecializedChatbot:
    def __init__(self, bot_name="Assistant", bot_personality="helpful", expertise="general knowledge"):
        self.bot_name = bot_name
        self.bot_personality = bot_personality
        self.expertise = expertise
        
        # Construct a detailed system prompt
        self.system_prompt = f"""
        You are {bot_name}, a {bot_personality} AI assistant with expertise in {expertise}.
        
        Guidelines:
        - Provide accurate and concise information
        - If you don't know something, admit it instead of making up information
        - Format responses in a clear and readable way
        - Use examples to illustrate complex concepts
        - Respond in a conversational tone
        
        Current date: {os.getenv("CURRENT_DATE", "2025-03-08")}
        """
        
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Token and cost tracking
        self.total_tokens_used = 0
        self.total_cost = 0
        
    def get_response(self, user_input):
        """Get response from the LLM and maintain conversation history."""
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                temperature=0.7,  # Controls randomness (0-1)
                max_tokens=500,   # Maximum length of response
                top_p=0.9,        # Nucleus sampling
                frequency_penalty=0.5,  # Reduce repetition of similar phrases
                presence_penalty=0.5,   # Encourage model to talk about new topics
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Track token usage
            self.total_tokens_used += response.usage.total_tokens
            # Approximate cost calculation (adjust rates as needed)
            self.total_cost += (response.usage.total_tokens / 1000) * 0.002
            
            return assistant_response
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def save_conversation(self, filename="conversation.json"):
        """Save the conversation history to a file."""
        with open(filename, "w") as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"Conversation saved to {filename}")
    
    def load_conversation(self, filename="conversation.json"):
        """Load a conversation history from a file."""
        try:
            with open(filename, "r") as f:
                self.conversation_history = json.load(f)
            print(f"Conversation loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found.")
    
    def run(self):
        """Run the chatbot interactively."""
        print(f"Welcome to {self.bot_name}, your {self.bot_personality} assistant for {self.expertise}!")
        print("Type 'exit' to quit, 'save' to save the conversation, or 'load' to load a previous conversation.")
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() == "exit":
                print(f"{self.bot_name}: Goodbye!")
                print(f"\nSession statistics:")
                print(f"Total tokens used: {self.total_tokens_used}")
                print(f"Estimated cost: ${self.total_cost:.4f}")
                break
            
            elif user_input.lower() == "save":
                self.save_conversation()
                continue
                
            elif user_input.lower() == "load":
                filename = input("Enter filename to load: ")
                self.load_conversation(filename)
                continue
            
            response = self.get_response(user_input)
            print(f"{self.bot_name}: {response}")

if __name__ == "__main__":
    # Create a specialized chatbot
    bot = SpecializedChatbot(
        bot_name="TechHelper",
        bot_personality="friendly and educational",
        expertise="programming and technology"
    )
    bot.run()