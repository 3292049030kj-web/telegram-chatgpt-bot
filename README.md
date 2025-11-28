# Telegram ChatGPT Bot (fixed)

Files:
- bot.py: main bot script (uses environment variables BOT_TOKEN and OPENAI_API_KEY)
- requirements.txt: Python dependencies (compatible with Python 3.12)
- runtime.txt: forces Python 3.12 on Render
- Procfile: worker process

Deployment notes (Render):
1. In Render Web Service settings set Start Command to: `python3 bot.py`
2. Add Environment Variables: BOT_TOKEN and OPENAI_API_KEY
3. Ensure the service uses the repository's main branch and redeploy.
