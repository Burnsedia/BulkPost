# services.py
import os
from typing import Optional, Tuple

import tweepy
from django.utils import timezone
from pydantic import BaseModel
from pydantic_ai import Agent

from .models import Post, ProviderCredential, Category


# -------- Strategy wrapper (keeps your tweet style + category variations)
def build_user_prompt(category: Optional[str], base_prompt: str) -> str:
    """Map your category (string or enum value) to a small prefix and compose the final user prompt."""
    cat = (category or "").lower()

    def _val(x: str) -> str:
        # Helper to safely grab TextChoices .value if present
        return getattr(getattr(Category, x.upper(), ""), "value", x)

    if cat in {_val("value"), "value"}:
        prefix = "Create a value-driven tip with quick practical steps.\n"
    elif cat in {_val("engagement"), "engagement"}:
        prefix = "Ask for opinions or choices to spark replies.\n"
    elif cat in {_val("authority"), "authority"}:
        prefix = "Share a hard-won lesson or metric confidently.\n"
    elif cat in {_val("contrast"), "contrast"}:
        prefix = "Use contrast (A vs B / Before vs After) to make a clear point.\n"
    elif cat in {_val("transformation"), "transformation"}:
        prefix = "Show the transformation: steps from problem to outcome.\n"
    else:
        prefix = ""

    return f"{prefix}Prompt: {base_prompt}"


SYSTEM_FALLBACK = (
    "You are a witty, motivational indie hacker.\n"
    "Tweet format: a punchy one-line insight, then 3–5 short hyphen-led lines.\n"
    "End with short relevant hashtags like #buildinpublic #indiehackers.\n"
    "Max 280 chars. No em dashes — only hyphens -."
)


class Tweet(BaseModel):
    text: str


def build_agent(
    system_prompt: str,
    model_name: str,
    temperature: float,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    org: Optional[str] = None,
) -> Agent[Tweet]:
    """
    Construct a PydanticAI Agent.
    For OpenAI-compatible providers, PydanticAI reads OPENAI_* env vars.
    If you’re BYOK or using Ollama/Groq/etc. behind an OpenAI-compatible /v1,
    pass api_key/base_url/org here.
    """
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    if base_url:
        os.environ["OPENAI_BASE_URL"] = base_url
    if org:
        os.environ["OPENAI_ORG"] = org

    return Agent[Tweet](
        model_name,                           # e.g. "openai:gpt-4o-mini", "ollama:llama3.1:8b"
        instructions=system_prompt or SYSTEM_FALLBACK,
        temperature=temperature,
        output_type=Tweet,                    # typed output: result.output is a Tweet
    )


def generate_tweet_text(
    system_prompt: str,
    model_name: str,
    temperature: float,
    user_prompt: str,
    openai_key: Optional[str],
    base_url: Optional[str] = None,
    org: Optional[str] = None,
) -> str:
    """Run the agent synchronously and return a <=280 char tweet."""
    agent = build_agent(system_prompt, model_name, temperature, openai_key, base_url, org)
    result = agent.run_sync(f"Write a tweet: {user_prompt}")

    # Prefer typed output (Tweet) first
    text = getattr(getattr(result, "output", None), "text", None)

    # Fallbacks for providers that don’t fill typed output
    if not text:
        text = getattr(getattr(result, "reply", None), "text", "") or ""

    text = (text or "").strip().strip('"')
    return text[:280]


def load_openai_key_for(user) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Load OpenAI-compatible creds for the given user.
    Returns (api_key, base_url, org), falling back to environment variables.
    Assumes ProviderCredential has platform='openai' and optional fields:
    - openai_api_key
    - base_url
    - organization
    """
    cred = ProviderCredential.objects.filter(user=user, platform="openai").first()
    api_key = (cred.openai_api_key if cred and getattr(cred, "openai_api_key", None) else os.getenv("OPENAI_API_KEY"))
    base_url = (getattr(cred, "base_url", None) or os.getenv("OPENAI_BASE_URL"))
    org = (getattr(cred, "organization", None) or os.getenv("OPENAI_ORG"))
    return api_key, base_url, org


def post_to_twitter_for(user, text: str) -> tuple[bool, str, str]:
    """
    Post a tweet with the user’s BYOK Twitter creds.
    Expects ProviderCredential(platform='twitter') with:
      - api_key, api_secret, access_token, access_token_secret
    Returns (ok, twitter_id, error).
    """
    cred = ProviderCredential.objects.filter(user=user, platform="twitter").first()
    if not cred:
        return False, "", "Missing Twitter credentials"
    try:
        client = tweepy.Client(
            consumer_key=cred.api_key,
            consumer_secret=cred.api_secret,
            access_token=cred.access_token,
            access_token_secret=cred.access_token_secret,
        )
        resp = client.create_tweet(text=text)
        twid = str(resp.data.get("id"))
        return True, twid, ""
    except Exception as e:
        return False, "", str(e)


def run_post_generation_and_publish(post: Post) -> Post:
    """Compose → generate via PydanticAI → post to Twitter → update Post record."""
    # Compose user prompt with strategy wrapper
    category = post.prompt.category or ""
    user_prompt = build_user_prompt(category, post.prompt.text)

    # Pick system params
    sp = post.system_prompt
    openai_key, base_url, org = load_openai_key_for(post.user)

    # Generate with PydanticAI
    tweet_text = generate_tweet_text(
        sp.content,
        sp.model_name,
        sp.temperature,
        user_prompt,
        openai_key,
        base_url,
        org,
    )
    post.text = tweet_text

    # Post to Twitter
    ok, twid, err = post_to_twitter_for(post.user, tweet_text)

    if ok:
        post.status = "posted"
        post.twitter_id = twid
        post.posted_at = timezone.now()
        post.error = ""
    else:
        post.status = "failed"
        post.error = err[:2000]

    post.save(update_fields=["text", "status", "twitter_id", "posted_at", "error"])
    return post

