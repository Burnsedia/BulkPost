from __future__ import annotations

import random
from pathlib import Path

from pydantic import BaseModel

try:
    from pydantic_ai import Agent
except Exception:
    Agent = None


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_ROOT = PROJECT_ROOT / "prompts"
OPENCODE_AGENTS_ROOT = PROJECT_ROOT.parent / ".opencode" / "agents"


class DraftOutput(BaseModel):
    text: str
    relevance_score: float
    risk_score: float


def _load_prompt(slug: str) -> str:
    source_file = OPENCODE_AGENTS_ROOT / f"{slug}.md"
    overlay_file = PROMPTS_ROOT / "agents" / slug / "v1.enhanced.md"

    source_prompt = ""
    if source_file.exists():
        source_prompt = source_file.read_text(encoding="utf-8")

    overlay_prompt = ""
    if overlay_file.exists():
        overlay_prompt = overlay_file.read_text(encoding="utf-8")

    if source_prompt and overlay_prompt:
        return (
            "You must follow the source agency agent as the primary instruction set.\n\n"
            f"--- SOURCE AGENT ({source_file}) ---\n"
            f"{source_prompt}\n\n"
            "--- RUNTIME OVERLAY (MVP constraints) ---\n"
            f"{overlay_prompt}"
        )
    if source_prompt:
        return source_prompt
    if overlay_prompt:
        return overlay_prompt

    return "You are a concise growth copywriter. Keep output polite and actionable."


def _heuristic_scores(text: str) -> tuple[float, float]:
    length = max(len(text), 1)
    relevance = 65.0 + min(length / 6.0, 25.0)
    lowered = text.lower()
    risky_terms = ["guarantee", "hate", "idiot", "stupid", "scam", "always"]
    risk = 0.1
    if any(term in lowered for term in risky_terms):
        risk = 0.8
    return round(min(relevance, 99.0), 2), round(risk, 2)


def _fallback_tweet(idea: str, seed: int | None = None) -> str:
    random.seed(seed)
    hooks = [
        "Most founders underuse this growth loop:",
        "If I had to grow from zero again, I would:",
        "A practical way to grow on X without burnout:",
        "One repeatable system that compounds followers:",
    ]
    hook = random.choice(hooks)
    text = f"{hook} {idea.strip()} Keep it useful, specific, and consistent."
    return text[:280]


def _fallback_reply(target_text: str) -> str:
    summary = target_text.strip().replace("\n", " ")
    summary = summary[:150]
    return (
        "Great point. I like how you framed this. "
        f"One practical extension: {summary}. "
        "What has worked best for you in the last 30 days?"
    )[:280]


def _run_agent(system_prompt: str, user_prompt: str) -> str:
    if Agent is None:
        raise RuntimeError("pydantic-ai is unavailable")

    model_name = "openai:gpt-4.1-mini"
    agent = Agent(model=model_name, system_prompt=system_prompt)
    result = agent.run_sync(user_prompt)
    return result.output.strip()


def generate_tweet_draft(idea: str, seed: int | None = None) -> DraftOutput:
    prompt = _load_prompt("ai-engineer")
    try:
        text = _run_agent(
            prompt,
            f"Write one tweet under 280 characters from this idea: {idea}. Keep tone polite and useful.",
        )
    except Exception:
        text = _fallback_tweet(idea, seed=seed)

    text = text.strip().strip('"')[:280]
    relevance, risk = _heuristic_scores(text)
    return DraftOutput(text=text, relevance_score=relevance, risk_score=risk)


def generate_reply_draft(source_text: str) -> DraftOutput:
    prompt = _load_prompt("brand-guardian")
    try:
        text = _run_agent(
            prompt,
            "Write one relevant, polite reply under 280 characters to this tweet: "
            f"{source_text}. Avoid generic praise and add one useful point.",
        )
    except Exception:
        text = _fallback_reply(source_text)

    text = text.strip().strip('"')[:280]
    relevance, risk = _heuristic_scores(text)
    return DraftOutput(text=text, relevance_score=relevance, risk_score=risk)
