from anthropic import Anthropic, BadRequestError, AuthenticationError, APIError

from src.config import ANTHROPIC_API_KEY


client = Anthropic(api_key=ANTHROPIC_API_KEY)


def run_claude_analysis(prompt):
    if not ANTHROPIC_API_KEY:
        return build_fallback_report(prompt, "No Anthropic API key was found.")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}],
        )

        return "\n".join(
            block.text for block in response.content if hasattr(block, "text")
        )

    except BadRequestError as error:
        return build_fallback_report(prompt, f"Claude API request failed: {error}")

    except AuthenticationError as error:
        return build_fallback_report(prompt, f"Claude authentication failed: {error}")

    except APIError as error:
        return build_fallback_report(prompt, f"Claude API error: {error}")


def build_fallback_report(prompt, reason):
    return f"""# GitHub Repo Scan Report

## Claude Analysis Status

Claude analysis could not run.

Reason:

```text
{reason}