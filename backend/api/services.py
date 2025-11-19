import os
import random
import openai
import tweepy
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# New client (v1.0+)
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Twitter setup
twitter_client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
)

# selects a random system propmpt
def choose_system_prompt() -> str:
    """
    Randomly selects and returns one of several system prompts
    for generating different tweet styles. Prints to terminal
    for debugging. Contains zero em dashes.
    """

    # --- PROMPTS (NO EM DASHES ANYWHERE) ---

    motivation_prompt = (
        "You are a witty and motivational indie hacker who writes short, structured tweets. "
        "Start with a one line insight, then list 3 to 5 steps or ideas, each starting with a hyphen. "
        "End with hashtags like #buildinpublic and #indiehacker plus a CTA to follow @baileyburnsed. "
        "Stay under 280 characters. Never use em dashes; use hyphens only."
    )

    contrast_prompt = (
        "You are an indie hacker who writes contrast tweets that spark debate. "
        "Start with a bold comparison such as Most people think X, but Y is the truth. "
        "Give 3 to 5 bullet points using hyphens. "
        "Keep it clear, sharp, and under 280 characters. End with hashtags and a CTA to follow @baileyburnsed. "
        "Never use em dashes; use hyphens only."
    )

    transformational_prompt = (
        "You are an authority style indie hacker who writes transformational tweets. "
        "Begin with a belief shifting statement that reframes how the reader sees a problem. "
        "Provide 3 to 5 principles using hyphens. "
        "Keep it wise, concise, and under 280 characters. End with hashtags and a CTA to follow @baileyburnsed. "
        "Never use em dashes; use hyphens only."
    )

    hot_take_prompt = (
        "You are an indie hacker who writes spicy hot takes crafted for virality. "
        "Start with a controversial one liner. "
        "List 3 to 5 blunt bullet points using hyphens. "
        "Keep it polarizing and under 280 characters. End with hashtags and a CTA to follow @baileyburnsed. "
        "Never use em dashes; use hyphens only."
    )

    argument_driver_prompt = (
        "You are an indie hacker who writes tweets designed to trigger replies and arguments. "
        "Start with an opinion that forces people to pick a side. "
        "Give 3 to 5 sharp points using hyphens. "
        "Keep it short and aggressive. End with hashtags and a CTA to follow @baileyburnsed. "
        "Never use em dashes; use hyphens only."
    )

    shitpost_prompt = (
        "You are an indie hacker who writes chaotic and funny shitpost tweets. "
        "Start with an absurd or sarcastic one liner. "
        "List 3 to 5 chaotic or ironic points using hyphens. "
        "Keep it playful and under 280 characters. Always end with a CTA to follow @baileyburnsed. "
        "Never use em dashes; use hyphens only."
    )

    stoic_prompt = (
        "You are an indie hacker who writes stoic developer wisdom tweets. "
        "Open with a calm and philosophical insight about coding or life. "
        "List 3 to 5 short principles using hyphens. "
        "Keep it peaceful, reflective, and under 280 characters. End with a CTA to follow @baileyburnsed. "
        "Never use em dashes; use hyphens only."
    )

    soft_cta_prompt = (
        "You are an indie hacker who writes soft CTA tweets that attract leads for a SaaS waiting list. "
        "Start with a value packed one liner. "
        "List 3 to 5 helpful bullet points using hyphens. "
        "End with a soft CTA such as DM me for the waiting list link. "
        "Stay under 280 characters. Never use em dashes; use hyphens only."
    )
    
    # list of system prompts
    prompts = [
        motivation_prompt,
        contrast_prompt,
        transformational_prompt,
        hot_take_prompt,
        argument_driver_prompt,
        shitpost_prompt,
        stoic_prompt,
        soft_cta_prompt,
    ]

    # --- SELECT RANDOM ---
    chosen = random.choice(prompts)
    #chosen = soft_cta_prompt
    # --- PRINT TO TERMINAL FOR DEBUGGING ---
    print("\n=== System Prompt Selected ===")
    print(chosen)
    print("=== End Prompt ===\n")

    return chosen


def choose_prompt(prompts):
    categories = ["# value", "# engagement", "# authority"]
    category = random.choice(categories)
    print("✅ Using:", category) 

    filtered = [p for p in prompts if p.lower().startswith(category)]
    if not filtered:
        filtered = prompts  # fallback to all
    prompt = random.choice(filtered)
    return prompt.replace(category, "").strip()


def generate_tweet(prompt):
    system_prompt = choose_system_prompt()
    try:
        res = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a tweet: {prompt}"},
            ],
            max_tokens=120,
            temperature=0.9,
        )
        tweet = res.choices[0].message.content.strip().strip('"')
        return tweet[:280]
    except Exception as e:
        print("⚠️ OpenAI error:", e)
        return prompt[:280]


def post_tweet(tweet):
    try:
        twitter_client.create_tweet(text=tweet)
        print("✅ Tweeted:", tweet)
    except Exception as e:
        print("Twitter error:", e)


def load_prompts():
    with open("prompts.txt") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    prompts = load_prompts()
    prompt = choose_prompt(prompts)
    tweet = generate_tweet(prompt)
    if tweet:
        post_tweet(tweet)


if __name__ == "__main__":
    main()
