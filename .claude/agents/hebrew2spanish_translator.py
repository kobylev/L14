"""
---
name: hebrew2spanish_translator
description: Translates Hebrew text to Spanish using Claude API with Haiku model for minimal token usage
author: AI Expert
version: 1.0.0
---
"""

import anthropic
import os
from dotenv import load_dotenv

def translate_with_claude(text, source_lang, target_lang, api_key=None, show_tokens=True):
    """
    Translates text from source language to target language using Claude API.

    Args:
        text: The text to translate
        source_lang: Source language (e.g., 'English', 'Spanish')
        target_lang: Target language (e.g., 'French', 'German')
        api_key: Anthropic API key (if None, uses ANTHROPIC_API_KEY env var)
        show_tokens: Whether to return token usage info (default: True)

    Returns:
        tuple: (translated_text, token_usage) if show_tokens=True, else just translated_text
    """
    client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

    system_prompt = (
        "You are a professional translator. Translate the given text accurately "
        "from the source language to the target language. Output ONLY the translated "
        "text with no additional commentary, explanations, or metadata."
    )

    user_prompt = f"Translate this text from {source_lang} to {target_lang}:\n\n{text}"

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    # Token usage tracking
    if show_tokens:
        token_usage = {
            'input_tokens': message.usage.input_tokens,
            'output_tokens': message.usage.output_tokens,
            'total_tokens': message.usage.input_tokens + message.usage.output_tokens
        }
        return message.content[0].text, token_usage

    return message.content[0].text


def main():
    """Claude Agent for Hebrew to Spanish translation"""
    print("=== Claude Translation Agent (Hebrew → Spanish) ===\n")

    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found")
        print("Please create a .env file with: ANTHROPIC_API_KEY=your-api-key")
        return

    # Ask if user wants to see token usage
    show_tokens_input = input("Show token usage? (y/n, default=y): ").strip().lower()
    show_tokens = show_tokens_input != 'n'

    # Get user input once
    text = input("Enter Hebrew text to translate: ")

    print("\nTranslating...\n")

    # Perform translation from Hebrew to Spanish
    result = translate_with_claude(text, "Hebrew", "Spanish", api_key, show_tokens)

    # Display results
    if show_tokens:
        translated_text, token_usage = result
        print(f"Translation:")
        print(f"{translated_text}")
        # Token usage information
        print(f"\n--- Token Usage ---")
        print(f"Input tokens: {token_usage['input_tokens']}")
        print(f"Output tokens: {token_usage['output_tokens']}")
        print(f"Total tokens: {token_usage['total_tokens']}")
    else:
        print(f"Translation:")
        print(f"{result}")


if __name__ == "__main__":
    main()
