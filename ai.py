import requests
import json
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

    if OPENROUTER_API_KEY:
        return _call_openrouter(prompt, system_instruction)

    raise RuntimeError("No AI API key configured (GOOGLE_AI_API_KEY or OPENROUTER_API_KEY)")


def generate_email_html(videos: list) -> str:
    videos_block = ""

    video_metadata = {}

    for video in videos:
        videos_block += f"\nVideo ID: {video["video_id"]}\n Transcript: {video["transcript"]}\n"
        video_metadata[video["video_id"]] = {
            "title": video['title'],
            "thumbnail_url": video['thumbnail_url'],
            }

    videos_json =   generate(        
        f'''You are a professional video transcript summarizer and key points extractor. You are given a lot of transcript data for multiple videos, and you have to return only and only the response in this format:

Response Format:

{{
    "explanation": "This is where you will give a one liner for the day",
    "videos": {{
        "video_id1": {{
            "category": "Give a simple category for the video, like AI, Tech, Gadget, Medical, etc..",
            "summary": "Give a simple 5-10 line video explanation",
            "keypoints": [
                "Give multiple keypoints for the video",
                "Like the most important event",
                "Or the crux of the video"
            ]
        }},
        "video_id2": {{
            "category": "Give a simple category for the video, like AI, Tech, Gadget, Medical, etc..",
            "summary": "Give a simple 5-10 line video explanation",
            "keypoints": [
                "Give multiple keypoints for the video",
                "Like the most important event",
                "Or the crux of the video"
            ]
        }}
    }}
}}

TRANSCRIPT:

{videos_block}
''',
        "You write clear, simple summaries in everyday English. "
        "Short sentences. Easy words. No jargon. "
        "Write substantive summaries with real takeaways from the content. "
        "Do NOT include any other message. Return ONLY valid json",
    )
    return turn_into_html(videos_json,video_metadata)




def turn_into_html(content,video_metadata):
    content = json.loads(content)
    explanation = content["explanation"]
    videos = content["videos"]
    
    html_content = ""
    for id, vid in videos.items():
         html_content += f"""
<tr>
    <td style="background:#fff; border:1px solid #111;">

        <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr>

                <td width="220" valign="top" style="padding:12px; border-right:1px solid #999;">
                    <a href="https://www.youtube.com/watch?v={id}" style="text-decoration:none;">
                        <img src="{video_metadata[id]['thumbnail_url']}" width="200" alt="VIDEO IMAGE"
                            style="display:block; width:100%; max-width:200px; height:auto;">
                    </a>
                </td>

                <td valign="top" style="padding:12px;">

                    <div
                        style="display:inline-block; border:1px solid #777; padding:3px 5px; font-size:9px; font-weight:bold; letter-spacing:0.5px; margin-bottom:9px;">
                        {vid['category']}
                    </div>

                    <div style="font-size:16px; font-weight:bold; margin-bottom:9px;">
                        {video_metadata[id]['title']}
                    </div>

                    <div style="font-size:12px; line-height:1.5; color:#333; margin-bottom:12px;">
                        {vid['summary']}
                    </div>

                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                        style="background:#fafafa; border:1px solid #ddd;">
                        <tr>
                            <td style="padding:12px;">

                                <div style="font-size:12px; font-weight:bold; margin-bottom:5px;">
                                    KEY TAKEAWAYS:
                                </div>

                                <ul style="margin:0; padding-left:16px; font-size:12px; line-height:1.5;">
                                    {"".join(f"<li>{x}</li>" for x in vid["keypoints"])}
                                </ul>

                            </td>
                        </tr>
                    </table>

                </td>

            </tr>
        </table>

    </td>
</tr>

<tr>
    <td height="10"></td>
</tr>
"""
    return f"""<body style="margin:0; padding:0; background:#f4f4f1; font-family:Arial, Helvetica, sans-serif; color:#111;">

    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f4f4f1;">
        <tr>
            <td align="center" style="padding:30px 15px;">

                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;">

                    <tr>
                        <td style="background:#fff; border:1px solid #111; padding:18px 16px 16px 16px;">

                            <div style="font-size:25px; font-weight:bold; margin-bottom:6px;">
                                Today's Top YouTube Insights
                            </div>

                            <div style="font-size:16px; color:#555;">
                               {explanation}
                            </div>

                        </td>
                    </tr>



                    <tr>
                        <td height="14"></td>
                    </tr>
                    {html_content}
                    <tr>
                        <td
                            style="border:1px solid #111; background:#fff; padding:9px; text-align:center; font-size:10px; font-weight:bold; letter-spacing:0.5px;">
                            END OF DIGEST
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>"""

