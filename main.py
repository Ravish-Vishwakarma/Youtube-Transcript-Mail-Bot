import sys

from youtube import get_todays_videos, get_transcript
from ai import generate_email_html
from mail import send_email

CHANNELS = [
    "Fireship",
    "mehulmpt",
    "theAIsearch",
    "bogxd",
    "LowLevelTV",
    "TwoMinutePapers",
    "ThePrimeTimeagen",
    "t3dotgg"
]


def collect_todays_videos():
    all_videos = []

    for channel in CHANNELS:
        videos = get_todays_videos(channel)
        if not videos:
            print(f"[{channel}] No video uploaded today")
            continue

        print(f"[{channel}] {len(videos)} video(s) today")

        for v in videos:
            print(f"  Fetching transcript for: {v['title']}")
            try:
                v["transcript"] = get_transcript(v["video_id"])
                print(f"    {len(v['transcript'])} chars")
                all_videos.append(v)
            except Exception as e:
                print(f"    Transcript failed: {e}")

    return all_videos


def main():
    dry_run = "--dry-run" in sys.argv
    videos = collect_todays_videos()

    if not videos:
        print("No videos with transcripts to process")
        return

    if dry_run:
        print(f"\nDRY RUN — {len(videos)} video(s) collected, skipping AI and email")
        return

    print(f"\nGenerating HTML newsletter for {len(videos)} video(s)...")
    try:
        html_body = generate_email_html(videos)
    except Exception as e:
        print(f"AI generation failed: {e}")
        return

    send_email("📺 Today's YouTube Videos", html_body)
    print("Done!")


if __name__ == "__main__":
    main()
