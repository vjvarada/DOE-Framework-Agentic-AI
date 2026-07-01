import os

OUT = r"c:\Users\VijayRaghavVarada\Documents\Github\DOE Framework Agentic AI\mini_workshop.md"

content = """\
# Run Your First AI Agent in 30 Minutes
## Free Mini-Workshop

> **What this is:** A hands-on workshop where you clone a real, working AI agent, configure it on your laptop, and watch it search the live web, generate a formatted HTML report, and send it to your phone via Telegram — all from a single command. No prior experience required.
>
> **What this is NOT:** The full course. This workshop gets a real agent running on your machine so you can see exactly what's possible. The full "DOE Framework & DeskMochi AI Agent" course teaches you to design and build agents like this yourself, for any task you can imagine. Links at the end.

---

## What You'll Run

You type one sentence. Under 30 seconds later:

| Step | What happens |
|------|-------------|
| 1 | Agent searches the live internet for your query — no API key needed |
| 2 | Agent reads the top results and synthesizes them |
| 3 | Agent generates a formatted HTML research report |
| 4 | Report opens automatically in your browser |
| 5 | Report is sent to your phone as a Telegram file |

This is not a demo or a simulation. This is real code, running on your machine, connecting to the live internet, and delivering a result to your actual phone.

---

## Before You Start

**Time required:** ~30 minutes

**What you need:**
- A laptop (Windows, Mac, or Linux)
- Git installed → [git-scm.com](https://git-scm.com)
- Python 3.10+ installed → [python.org/downloads](https://python.org/downloads)
  - Windows: check "Add Python to PATH" during install
- Telegram on your phone → [telegram.org](https://telegram.org) (free)
- A Telegram Bot token + your Chat ID (~3 min to set up — steps below)

**You do NOT need:**
- Any paid services or subscriptions
- DeskMochi hardware
- Any prior programming experience

### Get Your Telegram Bot (3 min)

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` — choose any name and username (e.g. `MyResearchBot`)
3. BotFather sends you a token like: `7123456789:AAHdqTcvCHhvGHyzGQvk_z8fOm...` — save it
4. Search for **@userinfobot** → send `/start` → it replies with your Chat ID (e.g. `391847263`) — save that too

You'll need both values in Section 3.

---

## Section 1 — Why Agents Are Different (5 min)

Read this before running anything. It's the mental model that makes everything else click.

### The Problem With How Most People Use AI

You've probably done this: open ChatGPT, ask it something, copy the answer, then manually go do the thing yourself.

- Ask it to research a topic → it gives you a paragraph → you spend 30 more minutes cross-referencing sources
- Ask it to compare products → it gives a vague answer → you still end up with 8 browser tabs open
- Ask it to find information → it tells you → you manually format it, copy it, save it somewhere

That's not AI *working for you*. That's AI being a fancy search engine while you do all the actual work.

**The gap is enormous.** AI is more capable than ever, but most people use it as a text generator. The AI does the easy part (thinking). You still do the hard part (finding information, acting on it, saving the result).

### What an Agent Actually Does

An agent doesn't stop at answering your question. It searches the live web, reads the sources, synthesizes the findings, formats them into a document, and delivers it to you — without you lifting a finger.

```
Normal AI:   You ask → AI answers from memory → YOU go do the work

Agent:       You ask → Agent searches → Agent reads → Agent synthesizes
                     → Report in your browser → Report on your phone
```

The difference isn't smarter AI. It's AI connected to real tools — tools that search, generate documents, send messages. The AI makes decisions. The tools do the work.

### The DOE Framework

Every agent — simple or complex — has three layers. This is the architecture behind the agent you're about to run.

```
┌──────────────────────────────────────────────────┐
│                DOE FRAMEWORK                      │
│                                                  │
│   📋 Directive  — What should happen             │
│      Plain English instructions                  │
│      Written in a .md file                       │
│                                                  │
│   🧠 Orchestration — Decides what to do          │
│      Reads the directive                         │
│      Routes to the right tools                   │
│                                                  │
│   🔧 Execution — Does the actual work            │
│      Deterministic Python scripts                │
│      Each script does exactly one thing          │
└──────────────────────────────────────────────────┘
```

**Why separate layers?** AI is probabilistic — slightly unpredictable. Code is deterministic — perfectly reliable. Keeping them separate means each layer does what it's best at. The AI reasons. The scripts execute, the same way every time.

You're about to see this in action.

---

## Section 2 — What's in the Agent (5 min)

Before we clone anything, let's understand what we're running.

The research agent uses three tools working in sequence:

| Tool | What it does | Library |
|------|-------------|---------|
| 🔍 **Web Search** | Searches the live internet for your query | `ddgs` — free, no API key |
| 📄 **HTML Generator** | Synthesizes results into a formatted report | Python built-in |
| 📱 **Telegram Sender** | Sends the report file to your phone | Telegram Bot API — free |

Here's how the three DOE layers map to this agent:

```
📋 DIRECTIVE
   directives/research_agent.md
   └─ Plain English: "search the web, build an HTML report, send via Telegram"

🧠 ORCHESTRATION
   Reads the directive and decides the sequence:
   search → extract → synthesize → generate HTML → send

🔧 EXECUTION
   execution/research_agent.py
   └─ Tool 1: DDGS().text()  — live web search
   └─ Tool 2: HTML builder   — generates the report file
   └─ Tool 3: requests.post() — sends via Telegram Bot API
```

That's the whole agent. A plain-English instruction file, and a Python script that carries it out. You'll see both after you clone the repo.

---

## Section 3 — Clone & Set Up (8 min)

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone [REPO_URL]
cd doe-research-agent
```

You'll see this structure:

```
doe-research-agent/
├── directives/
│   └── research_agent.md       ← plain English instructions
├── execution/
│   └── research_agent.py       ← the script that runs the tools
├── requirements.txt            ← Python libraries needed
└── .env.example                ← template for your credentials
```

This is DOE in practice:
- `directives/research_agent.md` — the **Directive** layer
- `execution/research_agent.py` — the **Execution** layer
- The orchestration layer connects them at runtime

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs two libraries:
- **`ddgs`** — free web search, no API key, no signup
- **`requests`** — standard Python HTTP library for the Telegram API call

### Step 3: Configure Your Credentials

Copy the example config and fill it in:

```bash
cp .env.example .env
```

Open `.env` and add your two Telegram values:

```
TELEGRAM_TOKEN=7123456789:AAHdqTcvCHhvGHyzGQvk_z8fOm...
TELEGRAM_CHAT_ID=391847263
```

> **Why a `.env` file?** Credentials never live inside the code. If you share the script or push it to GitHub, your secrets stay safe in `.env`, which stays on your machine only.

---

## Section 4 — Run It (7 min)

### The First Run

In the terminal, run:

```bash
python execution/research_agent.py --query "best electric scooters in India 2026"
```

Watch the terminal:

```
Searching for: best electric scooters in India 2026
Found 5 results. Reading sources...
  ✓ Ather Energy 450X review - 2026 update
  ✓ OLA S1 Pro vs Ather: full comparison
  ✓ Top 10 electric scooters under ₹1 lakh
  ✗ Skipped (could not read)
  ✓ TVS iQube long-term review
Synthesizing report...
Saved: report.html
Opening in browser...
Sending to Telegram...
✓ Sent. Check your phone.
Done!
```

Two things happen at once:
1. **Browser opens** — a formatted, sectioned research report with sources
2. **Phone buzzes** — Telegram message with the HTML report attached

**This is the moment.** You didn't open a single browser tab. You didn't copy anything. One sentence in the terminal, and a formatted research brief is on your phone.

### Try Something You Actually Care About

```bash
python execution/research_agent.py --query "how to start a cloud kitchen in India"
```

```bash
python execution/research_agent.py --query "best laptops for students under 50000 rupees 2026"
```

```bash
python execution/research_agent.py --query "Python vs JavaScript which should I learn first 2026"
```

Each run: a new report, a new Telegram message, under 30 seconds. Try any topic you've been meaning to look into.

---

## Section 5 — A Peek Under the Hood (5 min)

Now that you've seen it work, let's look at what made it happen.

### The Directive

Open `directives/research_agent.md`. You'll see plain English:

```
# Research Agent

## Goal
Search the web for any topic, synthesize the results into a
formatted HTML report, and send it to the user via Telegram.

## Tools
1. Web Search — ddgs library, no API key
2. HTML Generator — creates a styled report file
3. Telegram Sender — sends the file to the user's phone

## Workflow
1. Search for the query (5 results by default)
2. Read each result page
3. Synthesize into: Overview, Key Findings, Breakdown, Sources
4. Save as report.html, open in browser
5. Send via Telegram with the query as the caption

## Edge Cases
- If a URL fails to read: skip it, continue
- If Telegram fails: print the error, don't crash
...
```

This is the Directive layer. Not code. Not configuration. Plain English that describes what the agent should do — the same way you'd describe a task to a person.

### The Execution Script

Open `execution/research_agent.py`. Around 90 lines. The structure at a glance:

```python
# Tool 1: Web Search
results = DDGS().text(query, max_results=5)        # search the web
pages   = [DDGS().extract(r["href"]) for r in results]  # read each page

# Tool 2: HTML Generator
html = build_report(query, pages)    # synthesize + format
save_and_open(html)                  # save file, open browser

# Tool 3: Telegram Sender
send_to_telegram(                    # deliver to phone
    file="report.html",
    token=os.environ["TELEGRAM_TOKEN"],
    chat_id=os.environ["TELEGRAM_CHAT_ID"]
)
```

Three tools. Each does exactly one thing. The script wires them together in sequence. If one step fails (e.g. a URL can't be read), the others still run.

### What this architecture means

- The **directive** can be updated without touching the script
- The **script** can be tested without touching the directive
- Each **tool** is independent — you can swap one out without breaking the others
- The whole thing is readable — you can look at every line and understand every step

This separation is why the DOE pattern scales. Each layer has one job, and the jobs don't bleed into each other.

---

## What Just Happened

| Step | What ran | DOE Layer |
|------|----------|-----------|
| Read the directive | Understood goal: search → report → Telegram | 📋 Directive |
| `DDGS().text()` | 5 live web results, no API key | 🔧 Execution |
| `DDGS().extract()` | Page content pulled as clean text | 🔧 Execution |
| Synthesize into sections | Overview, findings, sources, breakdown | 🧠 Orchestration |
| Save as `report.html` | Styled, self-contained HTML file | 🔧 Execution |
| `requests.post()` to Telegram | File delivered to your phone | 🔧 Execution |

One sentence in. A formatted research brief out. Delivered to your phone. That's an agent.

---

## What the Full Course Gives You

You just *ran* an agent. The full course teaches you to *build* one — from a blank directive to a working multi-tool pipeline, for any task you can imagine.

### More tools covered in the full course

| Tool | What it does | Used in... |
|------|-------------|------------|
| 📊 Google Sheets Writer | Push any data into a spreadsheet | Lead tracker, expense log, briefings |
| 💬 WhatsApp Sender | Send messages via WhatsApp | Alerts, summaries, client follow-ups |
| 📧 Gmail Sender | Compose and send emails | Proposals, reports, sequences |
| 🗓️ Google Calendar | Create and read events | Scheduling, planning |
| 🏠 Smart Home | Control lights, AC, plugs | Morning routines, automation |
| 🎙️ Voice Input | Transcribe speech via Whisper | Speak instead of typing |
| 🔊 Voice Output | Text-to-speech | Agent reads reports aloud |
| 📰 News Fetcher | Pull latest headlines by topic | Morning briefing, market updates |
| 🤖 DeskMochi Display | Show text on a physical desk device | Visual notifications, desk companion |
| 🧠 Agent Memory | SQLite memory across sessions | Agent remembers preferences |

### The full course vs. this workshop

| | Mini-Workshop (this) | Full Course |
|---|---|---|
| **What you do** | Clone and run a pre-built agent | Design and build your own agents |
| **Tools** | 3 (pre-built for you) | 10+ (you build each one) |
| **AI models** | Pre-configured | Local (free, private), Groq (free, fast), OpenAI, Claude |
| **Runs standalone** | No — needs a terminal open | Yes — 24/7 server, no terminal needed |
| **Agent memory** | None | Full memory — agent learns over sessions |
| **Pipelines** | Single linear script | Chained tools, parallel execution |
| **Physical companion** | None | 🤖 DeskMochi track — ESP32 display + speaker, ~$20 |
| **Graduation project** | — | Build a complete original agent from scratch |

### What's in the full course that you can't get from this workshop

**You learn to build, not just run.** Right now you have a working agent, but if you wanted to change what it does — connect a different service, change the output format, add a new step — you'd be starting from scratch. In the course, you understand every layer well enough to build anything yourself, from a blank file.

**The standalone server.** This agent only runs when you fire it manually from a terminal. In the course, you build a Python server that runs 24/7 on your PC — listening for commands, firing agents, delivering results — even when you're asleep.

**The AI upgrade.** The agent you ran uses a fixed configuration. In the course, you learn to choose and swap AI models: a local model running entirely on your laptop (free, private, no internet), Groq's free cloud API for speed, or the most powerful models available when the task demands it. You understand *when* to use each.

**The compound effect.** Every tool you learn to build can be combined with every other tool. By the end of the course you're not thinking "can I build that?" — you're thinking "which tools do I need and how do I connect them?"

> You ran one agent today. The course gives you the skills to build any agent you can imagine.

---

## Where to Go From Here

**Try more queries**

The agent is on your machine. Run it on anything you've been meaning to research:

```bash
python execution/research_agent.py --query "your question here"
```

A buying decision. A business question. A topic you're curious about. Something you'd normally spend an hour Googling. Let it run.

**Join the full course**

[Link to full course]

The course starts with the DOE framework you just saw in action — and by the end you'll have built 10+ working agents, a 24/7 autonomous server, and a graduation project of your own design.

---

## Quick Reference

```
WHAT YOU DID TODAY
──────────────────────────────────────────
git clone [REPO_URL]
cd doe-research-agent
pip install -r requirements.txt
cp .env.example .env
# fill in TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
python execution/research_agent.py --query "your question"

THE DOE FRAMEWORK
──────────────────────────────────────────
📋 Directive     → plain English instructions (.md file)
🧠 Orchestration → reads directive, routes to tools
🔧 Execution     → deterministic Python scripts, one job each

THE THREE TOOLS IN THIS AGENT
──────────────────────────────────────────
🔍 Web Search      ddgs — free, no API key
📄 HTML Generator  Python built-in — styled report file
📱 Telegram Sender Telegram Bot API — free, token from @BotFather
```

**Files in the repo:**
- `directives/research_agent.md` — the directive (plain English)
- `execution/research_agent.py` — the execution script
- `.env` — your credentials (stays on your machine, never committed)
- `report.html` — generated fresh every run
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Written: {content.count(chr(10))+1} lines, {len(content)} chars")

