'''
Created by Aryan Govil, 2024

'''
#!/usr/bin/env python3

import os
import subprocess
import sys
import time
import textwrap
import shutil

from groq import Groq

os.system('cls' if os.name == 'nt' else 'clear')

model="mixtral-8x7b-32768"
#model="llama2-70b-4096"

class Color:
    RED = '\033[91m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    RED_BOLD = '\033[1;31m'
    ORANGE = '\033[33m'
    BLUE = '\033[94m'
    DARK_BLUE = '\033[34m'
    PURPLE_BOLD = '\033[1;95m'

print()
groq = Color.RED + "   ___                    __ _             ___    _                _     \n" \
       "  / __|     _ _    ___   / _` |           / __|  | |_     __ _    | |_   \n" \
       " | (_ |    | '_|  / _ \\  \\__, |     _    | (__   | ' \\   / _` |   |  _|  \n" \
       "  \\___|   _|_|_   \\___/   __|_|   _(_)_   \\___|  |_||_|  \\__,_|   _\\__|  \n" \
       "_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"| \n" \
       "`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'" + Color.RESET

chat = Color.WHITE + Color.RESET
print(groq + chat)
print("\n\n")
print(Color.PURPLE_BOLD + "Created by Aryan Govil" + Color.RESET)
print()
print(Color.RED_BOLD + "Powered by Groq LPU" + Color.RESET)
print(Color.ORANGE + "Model: "+ model + Color.RESET)
print()


def simulate_typing(text, typing_speed=0.00005):
    terminal_width = shutil.get_terminal_size((80, 20)).columns  # Default to 80 columns if detection fails
    current_line_length = 0
    
    words = text.split(' ')  # Split the text into words
    
    for word in words:
        # Check if adding the next word exceeds the terminal width
        if current_line_length + len(word) + 1 > terminal_width:
            sys.stdout.write('\n')  # Move to a new line
            current_line_length = 0  # Reset current line length
        
        # Print the word
        for char in word:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(typing_speed)
        
        # Print a space after the word and increment current_line_length
        sys.stdout.write(' ')
        current_line_length += len(word) + 1  # +1 for the space
        
    print()  # Ensure you move to a new line after finishing the typing effect

# Modified get_valid_input function to use simulate_typing for output
def get_valid_input(prompt, min_value, max_value, is_float=True):
    while True:
        user_input = input(prompt)
        if user_input.strip() == '/reset':
            return user_input
        try:
            if is_float:
                value = float(user_input)
            else:
                value = int(user_input)
            if min_value <= value <= max_value:
                return value
            else:
                error_message = f"Please enter a value between {min_value} and {max_value}."
                simulate_typing(error_message)  # Using simulate_typing here
        except ValueError:
            simulate_typing("Invalid input. Please enter a numerical value.")  # And here

def print_green_divider():
    green_start = "\033[92m"
    green_end = "\033[0m"  # Resets the color to default
    print()
    print(green_start + "-" * 40 + green_end)  # Print green divider
    print()

def chat_interaction(client, temperature, max_tokens):
    # Initialize conversation history with system prompt
    conversation_history = [
        {
            "role": "system",
            "content": "You are a good assistant that will give answers that are straight to the point and relevant to the asked question. You will thoroughly elaborate on a particular subject if asked."
        }
    ]
    
    # Adjusted initial user prompt to reflect system's guidance
    user_prompt = "Please enter your initial question or type '/reset' to start over: "
    
    while True:
        user_context = input(user_prompt)
        
        if user_context.strip() == '/reset':
            return True
        
        # Append user message to the conversation history
        conversation_history.append({"role": "user", "content": user_context})
        
        print_green_divider()  # Print green divider after user input
        
        start_time = time.time()  # Capture start time

        # Make the chat completion request
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model=model,
            temperature=temperature,
            max_tokens=int(max_tokens),
        )
        
        end_time = time.time()  # Capture end time

        # Get the response and print it
        response_content = chat_completion.choices[0].message.content
        simulate_typing(response_content)

        duration = end_time - start_time  # Calculate duration
        estimated_tokens = len(response_content) / 4  # Estimate the number of tokens
        tokens_per_second = estimated_tokens / duration  # Calculate tokens per second
        
        print(f"\033[95m\nTokens/second: {tokens_per_second:.2f}\033[0m")  # Print tokens per second
        
        print_green_divider()  # Print green divider after response
        
        # Append model's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_content})

        # Update the user prompt for follow-up questions, making it clear they can continue the conversation
        user_prompt = "Enter your follow-up question or type '/reset' to start over: "

def main():
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("API key not found. Please set the GROQ_API_KEY environment variable and try again.")
        return
    
    client = Groq(api_key=api_key)
    
    while True:
        # Prompt the user for temperature and max tokens within the allowed ranges
        temperature = get_valid_input("Enter the temperature (0.0 to 2.0): ", 0.0, 2.0)
        if temperature == '/reset':
            continue
        max_tokens = get_valid_input("Enter the max tokens (Mixtral = 32768, Llama = 4096): ", 1, 32768, is_float=False)
        if max_tokens == '/reset':
            continue
        
        # Start chat
        reset_requested = chat_interaction(client, temperature, max_tokens)
        
        if reset_requested:
            print("Resetting...\n")
            python_executable = sys.executable  # Get the path to the Python interpreter
            subprocess.call([python_executable, sys.argv[0]])  # Restart the script
            sys.exit()  # Exit the current instance of the script

if __name__ == '__main__':
    main()