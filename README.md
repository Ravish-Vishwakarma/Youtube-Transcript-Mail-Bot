This script retrives the latest video by the youtubers whose id are listed in the `main.py` file.

The script uses the openrouter api.


.env FORMAT:

```
YOUTUBE_API_KEY=
GOOGLE_AI_API_KEY=
OPENROUTER_API_KEY=
EMAIL_ADDRESS=
EMAIL_PASSWORD=
EMAIL_RECIPIENT=
```
```mermaid
flowchart TD
    Main[Main] --> Collect[collect_todays_videos]
    Collect --> Email[generate_email_html]
    Email --> Send[send_email]

    subgraph VideoCollection["Video collection"]
        Collect --> GetVideos[get_todays_videos]
        GetVideos --> Transcript[get_transcript]

        GetVideos --> ChannelID[get_channel_id]
        GetVideos --> ChannelVideos[get_channel_videos]
    end

    subgraph EmailGeneration["Email generation"]
        Email --> Generate[generate]
        Generate --> HTML[turn_into_html]
    end
```


It makes a mail for the summary for the videos and mail it to you, like this:

<img width="625" height="3074" alt="Today-s-YouTube-Videos-ravishvishwakarma2010-gmail-com-Gmail-09-11-2026_11_51_PM" src="https://github.com/user-attachments/assets/82decb83-3f23-4432-b845-a3a305277eef" />
