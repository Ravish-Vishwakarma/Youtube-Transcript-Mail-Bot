import requests

from helper import GOOGLE_AI_API_KEY, OPENROUTER_API_KEY

GOOGLE_MODEL = "gemini-flash-latest"


def _call_google(prompt: str, system_instruction: str = None) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GOOGLE_MODEL}:generateContent?key={GOOGLE_AI_API_KEY}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    if system_instruction:
        body["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    resp = requests.post(url, json=body)
    data = resp.json()

    if "error" in data:
        raise RuntimeError(f"Google AI: {data['error'].get('message', data['error'])}")

    return data["candidates"][0]["content"]["parts"][0]["text"]


def _call_openrouter(prompt: str, system_instruction: str = None) -> str:
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": "openrouter/free", "messages": messages},
    )
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"OpenRouter: {data['error'].get('message', data['error'])}")
    return data["choices"][0]["message"]["content"]


def generate(prompt: str, system_instruction: str = None) -> str:
    if GOOGLE_AI_API_KEY:
        try:
            return _call_google(prompt, system_instruction)
        except Exception as e:
            print(f"Google AI failed, falling back to OpenRouter: {e}")

    if OPENROUTER_API_KEY:
        return _call_openrouter(prompt, system_instruction)

    raise RuntimeError("No AI API key configured (GOOGLE_AI_API_KEY or OPENROUTER_API_KEY)")


def generate_email_html(videos: list) -> str:
    videos_block = ""
    for v in videos:
        videos_block += (
            f"Title: {v['title']}\n"
            f"Video ID: {v['video_id']}\n"
            f"Thumbnail URL: {v['thumbnail_url']}\n"
            f"Transcript (first 5000 chars):\n{v['transcript'][:5000]}\n"
            f"---\n"
        )

    return generate(
        f"Create an HTML email newsletter about today's YouTube videos. "
        f"Style it like a modern neo-brutalist SaaS interface with: "
        f"Swiss editorial typography, ultra-thin 1px borders, corner crop marks, "
        f"subtle offset shadows, monochrome UI panels, strict grid layout, "
        f"generous whitespace and spacing. "
        f"IMPORTANT: Do NOT add any fake system messages, terminal text, "
        f"bracketed labels, coordinates, IP addresses, or sci-fi decorations. "
        f"Keep it clean — just real content with the visual style. "
        f"Use a table layout with the video thumbnail on the left "
        f"and a DETAILED summary of what the video covers on the right. "
        f"Write in simple, conversational English — like explaining to a friend. "
        f"No jargon, no complex vocabulary, no buzzwords. "
        f"Include actual key points, insights, or takeaways from the video — "
        f"not just generic fluff. Each video is a row. "
        f"Include clickable links on the thumbnail "
        f"and title pointing to https://youtube.com/watch?v=VIDEO_ID. "
        f"Return ONLY valid HTML inside a <table> (no markdown, no code fences, no html wrapping).\n\n"
        f"Videos:\n{videos_block}",
        "You write clear, simple summaries in everyday English. "
        "Short sentences. Easy words. No jargon. "
        "Write substantive summaries with real takeaways from the content. "
        "Do NOT include any fictional system messages. Return ONLY valid HTML.",
    )
