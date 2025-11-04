# services.py
import os
from typing import Optional

import tweepy
from django.utils import timezone
from pydantic import BaseModel
from pydantic_ai import Agent as PAgent

from .models import Post, ProviderCredential, Category

# -------- Strategy wrapper (keeps your tweet style + category variations)
def build_user_prompt(category: Optional[str], base_prompt: str) -> str:
    if category == Category.VALUE:
        prefix = "Create a value-driven tip with quick practical steps.\n"
    elif category == Category.ENGAGEMENT:
        prefix = "Ask for opinions or choices to spark replies.\n"
    elif category == Category.AUTHORITY:
        prefix = "Share a hard-won lesson or metric confidently.\n"
    elif category == Category.CONTRAST:
        prefix = "Use contrast (A vs B / Before vs After) to make a clear point.\n"
    elif category == Category.TRANSFORMATION:
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

def build_agent(system_prompt: str, model_name: str, temperature: float, api_key: Optional[str]=None):
    # PydanticAI will route to the default OpenAI provider env if set;
    # we pass model string directly. For BYOK, set OPENAI_API_KEY temporarily.
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key  # scoped per run; safe in single-process cron
    return PAgent[Tweet](
        system_prompt=system_prompt or SYSTEM_FALLBACK,
        model=model_name,
        temperature=temperature,
        response_type=Tweet,
    )

def generate_tweet_text(system_prompt, model_name, temperature, user_prompt: str, openai_key: Optional[str]) -> str:
    agent = build_agent(system_prompt, model_name, temperature, openai_key)
    result = agent.run_sync(f"Write a tweet: {user_prompt}")
    text = (result.text or "").strip().strip('"') if hasattr(result, "text") else result.reply.text
    return text[:280]

def load_openai_key_for(user) -> Optional[str]:
    cred = ProviderCredential.objects.filter(user=user, platform="openai").first()
    return cred.openai_api_key if cred and cred.openai_api_key else os.getenv("OPENAI_API_KEY")

def post_to_twitter_for(user, text: str) -> tuple[bool, str, str]:
    """
    Returns (ok, twitter_id, error)
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
    # Compose user prompt with strategy wrapper
    category = post.prompt.category or ""
    user_prompt = build_user_prompt(category, post.prompt.text)

    # Pick system params
    sp = post.system_prompt
    openai_key = load_openai_key_for(post.user)

    # Generate with PydanticAI
    tweet_text = generate_tweet_text(sp.content, sp.model_name, sp.temperature, user_prompt, openai_key)
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
