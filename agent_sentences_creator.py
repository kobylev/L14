import anthropic
from typing import Generator


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

    sentences_generated = 0
    batch_size = 50  # Generate in batches to ensure we get all sentences

    while sentences_generated < count:
        remaining = count - sentences_generated
        batch_count = min(batch_size, remaining)

        user_prompt = f"Generate exactly {batch_count} diverse English sentences inspired by 'Foundation' by Isaac Asimov. Each sentence must be between 10-20 words."

        response = call_claude_agent(user_prompt, system_prompt, api_key)

        # Split response into individual sentences
        sentences = [s.strip() for s in response.split('\n') if s.strip()]

        for sentence in sentences[:batch_count]:
            yield sentence
            sentences_generated += 1
            if sentences_generated >= count:
                break
