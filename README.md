# Chat Assistant

This chat assistant is powered by Groq LPU and developed by Aryan Govil.

## Setup

To use this chat assistant, you need to set up the Groq API key as an environmental variable. Follow these steps:

1. **Get Groq API Key**: Obtain your Groq API key from [Groq](https://groq.com).

2. **Set Environmental Variable**: Set the `GROQ_API_KEY` environmental variable on your computer. You can do this by executing the following command in your terminal, replacing `<your-api-key-here>` with your actual API key:

    ```
    export GROQ_API_KEY=<your-api-key-here>
    ```

    Alternatively, you can add this command to your shell profile file (e.g., `.bash_profile` or `.zshrc`) to make the variable persistent across sessions.

## Usage

Once you have set up the environmental variable, you can run the chat assistant. This assistant interacts with the Groq API to provide responses to user queries.

**To run the chat assistant, execute the chat.py file.**


Follow the prompts to enter the temperature and max tokens for the chat interaction. You can also type '/reset' at any time to start over.

## Note

Make sure your computer is connected to the internet while running the chat assistant, as it requires access to the Groq API.


