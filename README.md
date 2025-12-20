
# 🧠 BulkPost — Autonomous Motivational Tweet Generator

BulkPost is a **fully automated AI agent** that generates and posts **motivational tweets for indie hackers**.  
You set it up once — and it keeps your Twitter account active forever.

---

## 💡 What It Does

- 🤖 **AI-Generated Tweets** — Creates motivational and insightful posts for indie hackers  
- 🕒 **Automated Scheduling** — Posts on a configurable schedule (daily, hourly, or custom)  
- 🧠 **Autonomous Agent** — No human prompts required after setup  
- 🔐 **Secure Posting** — Uses the official Twitter API (v2)  
- 📈 **Consistent Growth** — Keeps your account active and discoverable without burnout  

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django REST Framework |
| **Automation** | Celery + Redis |
| **AI Layer** | OpenAI / Ollama / PydanticAI |
| **Database** | PostgreSQL |
| **Deployment** | Docker + Fly.io |
| **API** | Twitter API v2 via Tweepy |

---

## ⚙️ Quick Start

```bash
# Clone the repo
git clone https://github.com/Burnsedia/bulkpost.git
cd bulkpost

# Backend setup
cd backend
cp .env.example .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

By default, the scheduler posts once per day.  
You can change this in `settings.py` or your Celery config.

---

## 🔧 Environment Variables

| Variable | Description |
|-----------|--------------|
| `OPENAI_API_KEY` | Key for AI tweet generation |
| `TWITTER_API_KEY` | Twitter API consumer key |
| `TWITTER_API_SECRET` | Twitter API secret key |
| `TWITTER_ACCESS_TOKEN` | Twitter access token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter access token secret |
| `POSTGRES_URL` | Database connection string |
| `REDIS_URL` | Redis connection string |

---

## 🧠 How It Works

1. **Generate** – AI agent writes 5–10 new motivational tweets daily  
2. **Queue** – Tweets are stored in a local queue with timestamps  
3. **Schedule** – Celery worker posts them at the configured interval  
4. **Log** – Each post is stored in the database for analytics or reuse  

---

## 🧭 Roadmap

- [x] AI tweet generation  
- [x] Scheduled posting  
- [ ] Topic-based generation (“motivation”, “startups”, “build in public”)  
- [ ] Analytics dashboard  
- [ ] Multi-account support  
- [ ] Hashtag optimizer  

---

## 🧑‍💻 Contributing

Pull requests are welcome!  
1. Fork this repo  
2. Create a branch (`feature/your-feature`)  
3. Submit a pull request  

---

## 📜 License

Licensed under **AGPLv3** — open-source and self-hostable.  
Running a hosted SaaS version requires open-sourcing your modifications.

---

## 🧩 About

Created by **[Bailey Burnsed](https://baileyburnsed.dev)** — Software Engineer • Indie Hacker • Creator of [Virtue Tracker](https://github.com/Burnsedia) and [Dracula](https://github.com/Burnsedia).

Follow for updates:  
🐙 [GitHub](https://github.com/Burnsedia) | 🐦 [Twitter](https://twitter.com/baileyburnsed) | 💼 [LinkedIn](https://www.linkedin.com/in/bailey-burnsed-50051115a/)
