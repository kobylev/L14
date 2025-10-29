import anthropic


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
