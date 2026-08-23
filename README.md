This script retrives the latest video by the youtubers whose id are listed in the `main.py` file.

The script uses the free google api , if the quota runs out then for backup it uses the openrouter api.

It makes a mail for the summary for the videos and mail it to you, like this:

<img width="816" height="1225" alt="mail image" src="https://github.com/user-attachments/assets/1ab0bd23-9068-4d22-b556-cf1fd420155c" />

.env FORMAT:

```
YOUTUBE_API_KEY=
GOOGLE_AI_API_KEY=
OPENROUTER_API_KEY=
EMAIL_ADDRESS=
EMAIL_PASSWORD=
EMAIL_RECIPIENT=
```
