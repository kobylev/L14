import anthropic
import os
from typing import List, Tuple, Generator
from dotenv import load_dotenv


def call_claude_agent(prompt: str, system_prompt: str, api_key: str) -> str:
    """
    Helper function to call Claude API with a specific system prompt and user prompt.

    Args:
        prompt: The user message/prompt to send to Claude
        system_prompt: The system prompt that defines the agent's role
        api_key: Claude API key

    Returns:
        The text response from Claude
    """
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def english_spanish_translator(text: str, api_key: str) -> str:
    """
    Agent 2: Translates text from English to Spanish.

    Args:
        text: English text to translate
        api_key: Claude API key

    Returns:
        Spanish translation
    """
    system_prompt = "You are a translation agent. Your ONLY task is to translate from English to Spanish. Output ONLY the translated Spanish text with no explanations, comments, or additional text whatsoever."
    return call_claude_agent(text, system_prompt, api_key)


def spanish_hebrew_translator(text: str, api_key: str) -> str:
    """
    Agent 3: Translates text from Spanish to Hebrew.

    Args:
        text: Spanish text to translate
        api_key: Claude API key

    Returns:
        Hebrew translation
    """
    system_prompt = "You are a translation agent. Your ONLY task is to translate from Spanish to Hebrew. Output ONLY the translated Hebrew text with no explanations, comments, or additional text whatsoever."
    return call_claude_agent(text, system_prompt, api_key)


def hebrew_english_translator(text: str, api_key: str) -> str:
    """
    Agent 4: Translates text from Hebrew to English.

    Args:
        text: Hebrew text to translate
        api_key: Claude API key

    Returns:
        English translation
    """
    system_prompt = "You are a translation agent. Your ONLY task is to translate from Hebrew to English. Output ONLY the translated English text with no explanations, comments, or additional text whatsoever."
    return call_claude_agent(text, system_prompt, api_key)


def sentences_creator(api_key: str, count: int = 100) -> Generator[str, None, None]:
    """
    Generator function that creates diverse English sentences inspired by 'Foundation' by Isaac Asimov.
    Yields sentences one at a time to enable pipeline processing.

    Args:
        api_key: Claude API key
        count: Number of sentences to generate (default: 100)

    Yields:
        Individual English sentences (10-20 words each)
    """
    system_prompt = (
        "You are a creative sentence generator. Generate diverse, grammatically correct English sentences "
        "inspired by the themes, style, and tone of Isaac Asimov's 'Foundation' series. "
        "Each sentence must be between 10-20 words long. "
        "Output ONLY the sentences, one per line, with no numbering, explanations, or additional text."
    )

    user_prompt = f"Generate exactly {count} diverse English sentences inspired by 'Foundation' by Isaac Asimov. Each sentence must be between 10-20 words."

    response = call_claude_agent(user_prompt, system_prompt, api_key)

    # Split response into individual sentences and yield them
    sentences = [s.strip() for s in response.split('\n') if s.strip()]

    for sentence in sentences[:count]:  # Ensure we don't exceed requested count
        yield sentence


def run_translation_pipeline(api_key: str):
    """
    Orchestrator: Manages the complete translation pipeline.

    This function coordinates:
    1. Sentence generation via sentences_creator (100 sentences)
    2. Pipeline execution through all three translation agents for each sentence
    3. Synchronized output of original and final translated results

    The pipeline processes sentences as they are generated, enabling quasi-parallel execution:
    English -> Spanish (Agent 2) -> Hebrew (Agent 3) -> English (Agent 4)

    Args:
        api_key: Claude API key for all agent operations
    """
    print("=== Multi-Agent Translation Pipeline ===")
    print("Pipeline: English -> Spanish -> Hebrew -> English")
    print("Generating and processing 100 sentences...\n")

    sentence_count = 0

    # Process sentences as they are generated (synchronized pipeline)
    for original_sentence in sentences_creator(api_key, count=100):
        sentence_count += 1

        # Execute the translation chain for this sentence
        # Agent 2: English -> Spanish
        spanish_output = english_spanish_translator(original_sentence, api_key)

        # Agent 3: Spanish -> Hebrew
        hebrew_output = spanish_hebrew_translator(spanish_output, api_key)

        # Agent 4: Hebrew -> English
        final_english_output = hebrew_english_translator(hebrew_output, api_key)

        # Output the synchronized result
        print(f"Original: {original_sentence} | Final Translated: {final_english_output}")

    print(f"\n=== Pipeline Complete: Processed {sentence_count} sentences ===")


def run_translation_chain(input_sentences_list: List[str], claude_api_key: str) -> List[Tuple[str, str]]:
    """
    Execute a three-agent chained translation system that processes sentences through:
    English -> Spanish -> Hebrew -> English

    Args:
        input_sentences_list: List of English sentences to translate
        claude_api_key: Claude API key for authentication

    Returns:
        List of tuples containing (original_sentence, final_translated_sentence)
    """
    results = []

    for i, original_sentence in enumerate(input_sentences_list, 1):
        print(f"Processing sentence {i}/{len(input_sentences_list)}: {original_sentence[:50]}...")

        # Agent 2: English -> Spanish
        spanish_translation = english_spanish_translator(original_sentence, claude_api_key)

        # Agent 3: Spanish -> Hebrew
        hebrew_translation = spanish_hebrew_translator(spanish_translation, claude_api_key)

        # Agent 4: Hebrew -> English
        final_english_translation = hebrew_english_translator(hebrew_translation, claude_api_key)

        results.append((original_sentence, final_english_translation))

    return results


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
    """Main entry point - runs the multi-agent translation pipeline"""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set ANTHROPIC_API_KEY or create a .env file")
        return

    # Run the complete orchestrator pipeline
    run_translation_pipeline(api_key)


if __name__ == "__main__":
    main()
