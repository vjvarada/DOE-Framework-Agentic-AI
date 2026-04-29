# DeskMochi AI Agent Course — Complete Production Plan

> **Purpose:** This document is the master blueprint for a 10-video course (+ 1 foundations module) that teaches non-programmers how to build AI agents that do real work. Each section contains enough detail to serve as the basis for a full video script.

**Product:** DeskMochi — a physical desk companion (ESP32 + speaker + display) connected to a local AI server that executes tasks via the DOE Framework.

**Target Audience:** Non-programmers who want to build AI agents that take action in the real world.

**Unique Differentiator:** Physical hardware companion + framework-first teaching + working automations by Video 7.

**Total Runtime:** ~4-4.5 hours across 11 videos

---

## Two Learning Tracks

This course is designed to be valuable whether or not you own a DeskMochi.

| | 🖥️ Software Track | 🤖 DeskMochi Track |
|---|---|---|
| **Who it's for** | Anyone with a laptop | DeskMochi owners |
| **What you need** | Python + VS Code + GitHub Copilot | All of the above + DeskMochi hardware |
| **What you get** | Working AI agents you control from your PC | All agents *plus* a physical desk companion |
| **Hardware** | None | DeskMochi (~$20 in parts) |
| **Videos required** | 0, 1, 2, 4, 5, 6, 7, 8, 9, 10 | All 11 videos |
| **Video 3** | Optional/skip | Required |

> **Key principle:** The entire DOE Framework, all agent skills, and all live demos work 100% without DeskMochi hardware. The hardware adds a physical "face" to your agent — but the intelligence layer is identical. Every section of this course that is hardware-specific is clearly marked with 🤖. Sections without that marker work for both tracks.

**For the Software Track:** Anywhere DeskMochi "shows on display" or "speaker reads aloud," the equivalent output is printed in the terminal or displayed in a simple local web dashboard (a one-page HTML file, served from the local server). This is set up automatically during the Video 4 environment setup.

**For video production:** Record the Software Track version first (no hardware dependencies). Add DeskMochi hardware segments as clearly labeled addon sections. This allows the footage to be edited into two separate versions of each video if needed.

---

## Table of Contents

- [Course Arc](#course-arc)
- [Video 0: The Language of Tech — Foundations](#video-0-the-language-of-tech--foundations)
- [Video 1: What Is an AI Agent?](#video-1-what-is-an-ai-agent-and-why-you-should-care)
- [Video 2: How Agents Think — The DOE Framework](#video-2-how-agents-think--the-doe-framework)
- [Video 3: Building DeskMochi — The Hardware](#video-3-building-deskmochi--the-hardware)
- [Video 4: Setting Up Your Agent Workshop](#video-4-setting-up-your-agent-workshop)
- [Video 5: Your First Agent — "Get the Weather"](#video-5-your-first-agent--get-the-weather)
- [Video 6: The Local Server — Running Without Copilot](#video-6-the-local-server--running-without-copilot)
- [Video 7: Real-World Skills](#video-7-making-deskmochi-useful--real-world-skills)
- [Video 8: Cloud Brains, Model Showdown & More Skills](#video-8-cloud-brains-model-showdown--more-skills)
- [Video 9: Advanced Patterns](#video-9-advanced-patterns--memory-pipelines-and-self-healing)
- [Video 10: Build Your Own Agent — Graduation](#video-10-build-your-own-agent--graduation-project)
- [Appendix A: Complete Concept Glossary](#appendix-a-complete-concept-glossary)
- [Appendix B: Glossary Card System](#appendix-b-glossary-card-system)
- [Appendix C: Course Summary Table](#appendix-c-course-summary-table)
- [Appendix D: Interactive Modules (Brilliant-Style)](#appendix-d-interactive-modules-brilliant-style)

---

## Course Arc

### 🖥️ Software Track (no hardware required)
```
Video 0:    FOUNDATIONS — tech vocabulary for non-programmers
Video 1-2:  WHAT are agents? (Philosophy + the DOE mental model)
Video 4-5:  THE SOFTWARE — setting up + building your first agent with Copilot
Video 6:    THE SERVER — running autonomously with a local AI model
Video 7:    REAL SKILLS — 4 working agent skills connected to real APIs
Video 8:    CLOUD BRAINS — Groq free tier, model showdown, Opus 4.6 complex demo
Video 9:    ADVANCED — memory, pipelines, self-healing, safety
Video 10:   GRADUATION — build your own agent from scratch
```

### 🤖 DeskMochi Track (full experience)
```
Video 0:    FOUNDATIONS — tech vocabulary for non-programmers
Video 1-2:  WHAT are agents? (Philosophy + the DOE mental model)
Video 3:    THE HARDWARE — DeskMochi physical build  [🤖 Hardware only]
Video 4-5:  THE SOFTWARE — setting up + building your first agent with Copilot
Video 6:    THE SERVER — running autonomously with a local AI model
Video 7:    REAL SKILLS — 4 working agent skills connected to real APIs
Video 8:    CLOUD BRAINS — Groq free tier, model showdown, Opus 4.6 complex demo
Video 9:    ADVANCED — memory, pipelines, self-healing, safety
Video 10:   GRADUATION — build your own agent from scratch
```

**Pedagogical flow:** Each video builds on the previous. No concept is used before it's explained. By Video 7, the student has a working AI agent doing real tasks — on their desk companion (DeskMochi Track) or in a local web dashboard (Software Track).

---

## Video 0: The Language of Tech — Foundations

**Duration:** ~20-25 min
**Type:** Animated diagrams + real-world analogies. No code shown.
**Goal:** Give non-programmers the vocabulary they need so nothing in Videos 1-10 feels alien.

> This video is the "dictionary" for the entire course. Students should watch it once, then refer back to the downloadable cheatsheet as needed.

### Learning Objectives
- Understand the 13 foundational tech concepts used throughout the course
- Be able to read a file path and know what it means
- Understand the client-server model at a high level
- Know what an API is and why it matters

### Section 0.1 — Software vs Hardware (~2 min)

**What to cover:**
- Hardware = the physical thing you can touch (your PC, the ESP32, a keyboard)
- Software = the instructions that tell hardware what to do (apps, scripts, operating systems)
- Analogy: Hardware is the body. Software is the brain/instructions.
- In this course: DeskMochi (ESP32) is hardware. The agent code running on your PC is software.

**Key visual:** Show a photo of an ESP32 next to a screenshot of code. Label one "hardware" and the other "software."

### Section 0.2 — What Is a Computer Program / Script (~2 min)

**What to cover:**
- A program (or script) is a text file containing step-by-step instructions a computer follows
- It's like a recipe: "Step 1: Get the eggs. Step 2: Crack them into a bowl. Step 3: Whisk."
- The computer reads line 1, does it, reads line 2, does it, etc.
- A "script" is a short program — typically one file that does one job
- You don't need to write scripts from scratch — AI will write them for you. You need to understand what they do.

**Key visual:** Side-by-side of a cooking recipe and a simple Python script. Highlight the structural similarity.

### Section 0.3 — What Is a Server (~2 min)

**What to cover:**
- A server is a program that sits and waits for someone to ask it something, then responds
- It's like a receptionist: sits at a desk, waits for visitors, answers their questions, directs them
- A server doesn't have to be a big machine in a data center — it can be a program running on your laptop
- In this course: your PC runs a server. DeskMochi sends requests to it. The server thinks and responds.

**Key visual:** Animated receptionist at a desk. Someone walks up (DeskMochi) → asks a question → receptionist checks a book (LLM) → gives the answer.

### Section 0.4 — What Is a Client (~1 min)

**What to cover:**
- A client is the thing that asks the server for something
- Your web browser is a client (it asks websites to send you pages)
- DeskMochi is a client (it asks your PC server to do tasks)
- Your phone's weather app is a client (it asks a weather server for data)
- Client asks → Server answers. That's the fundamental pattern.

### Section 0.5 — Client-Server Architecture (~2 min)

**What to cover:**
- Almost every digital interaction follows this pattern:
  ```
  CLIENT  →  request  →  SERVER
  CLIENT  ←  response ←  SERVER
  ```
- Examples:
  - You open YouTube → your browser (client) asks YouTube's server for a video → server sends it
  - You ask Siri the weather → your phone (client) asks Apple's server → server responds
  - DeskMochi asks "What's the weather?" → ESP32 (client) asks your PC (server) → server calls weather API → sends result back
- The entire course is about building the server side of this conversation

**Key visual:** Animated arrows between DeskMochi (client) and a laptop (server), with the request and response labeled.

### Section 0.6 — What Is the Internet (at a Basic Level) (~1 min)

**What to cover:**
- Computers sending messages to each other using agreed-upon rules
- Your home WiFi is a tiny internet — all devices on it can talk to each other
- The "real" internet is just this at a global scale
- In this course: DeskMochi and your PC talk over your home WiFi. Your PC talks to external services (weather, Google Sheets) over the internet.

### Section 0.7 — What Is an API (~3 min)

**What to cover:**
- API = Application Programming Interface
- It's how two pieces of software talk to each other
- The restaurant analogy:
  ```
  You (your script)  →  API (waiter)  →  Service (kitchen)
       order              takes it          cooks
                     ←  response  ←
                     (your food)
  ```
- You don't walk into Google's kitchen. You talk to Google's waiter (API).
- Real examples they'll use:
  - Weather API — "What's the weather in Hyderabad?" → `{temp: 28, condition: "sunny"}`
  - Google Sheets API — "Add this row to my spreadsheet" → "Done, row added"
  - WhatsApp API — "Send this message to this number" → "Message sent"

**Key visual:** The restaurant analogy animated. Three examples shown as request/response pairs.

### Section 0.8 — What Is an API Key (~2 min)

**What to cover:**
- An API key is a password that identifies you to a service
- Without it: "Give me weather data" → "Who are you? Rejected."
- With it: "Give me weather data, here's my key: abc123" → "Here you go!"
- Each service gives you your own key when you sign up
- Rules:
  - Never share keys publicly (not on GitHub, not in screenshots)
  - Store them in a special `.env` file (covered in Video 4)
  - Each service has its own key

**Key visual:** Show a locked door with a keyhole. The API key is the key. Different services = different doors = different keys.

### Section 0.9 — What Is JSON (~2 min)

**What to cover:**
- JSON = the universal language for structured data
- Almost every API sends and receives JSON
- It looks like this:
  ```json
  {
    "city": "Hyderabad",
    "temperature": 28,
    "condition": "sunny",
    "is_raining": false
  }
  ```
- Think of it as a really neat, labeled list
- Curly braces `{ }` = a group of labeled values
- Square brackets `[ ]` = a list of items
- You don't need to write JSON — scripts produce and consume it. You just need to read it.

**Key visual:** A handwritten grocery list on the left → the same data as JSON on the right. Show the 1:1 mapping.

### Section 0.10 — What Is a File and a File Path (~2 min)

**What to cover:**
- A file is a container for data (text, images, code, anything)
- A file path is the "address" of a file on your computer
- Example: `C:\Users\You\Documents\project\execution\get_weather.py`
  - `C:\` = the drive
  - `Users\You\Documents\project\` = the folder hierarchy
  - `get_weather.py` = the file name
- Important symbols:
  - `\` (Windows) or `/` (Mac/Linux) = folder separator
  - `.` = separates name from extension
- In this course, you'll see paths like `execution/get_weather.py` — that's a *relative* path (starting from the project folder, not from `C:\`)

### Section 0.11 — What Is a Folder / Directory (~1 min)

**What to cover:**
- A folder (also called "directory") is a container for files and other folders
- Like folders in a filing cabinet — you organize things by category
- In our project:
  ```
  my-agent/
  ├── directives/    ← instructions
  ├── execution/     ← scripts
  └── .env           ← secrets
  ```

### Section 0.12 — What Is a File Extension (~1 min)

**What to cover:**
- The letters after the dot in a filename tell you what kind of file it is
- Extensions you'll see in this course:
  | Extension | What it is | Example |
  |-----------|-----------|---------|
  | `.py` | Python script | `get_weather.py` |
  | `.md` | Markdown document | `get_weather.md` |
  | `.json` | Structured data | `tool_registry.json` |
  | `.env` | Secret configuration | `.env` |
  | `.html` | Web page | `dashboard.html` |
  | `.txt` | Plain text | `requirements.txt` |

### Section 0.13 — What Is Plain Text vs Rich Text (~1 min)

**What to cover:**
- Plain text = just characters. No formatting, no fonts, no colors. What you see is what's stored.
- Rich text = formatted. Bold, italic, images, tables. (Word docs, Google Docs)
- All code, scripts, and directives in this course are plain text files
- VS Code is a plain text editor (with syntax highlighting to make it readable)
- Why plain text? Because computers need to read these files exactly, character by character. Rich formatting would get in the way.

### Video 0 Wrap-Up (~1 min)

**What to say:**
- "You now know every technical term you'll encounter in this course"
- "You don't need to memorize all of this — we'll remind you as we go, and there's a downloadable cheatsheet"
- "In the next video, we'll start talking about what AI agents actually are and why they matter"

---

## Video 1: What Is an AI Agent? (And Why You Should Care)

**Duration:** ~28-32 min
**Type:** Talking head + screen diagrams + animated explanations + 3 short demos
**Goal:** Build the mental model of what agents are, give an intuitive understanding of how LLMs work, and generate excitement for what they'll build.

### Concepts Introduced Just-In-Time

> These concepts appear for the FIRST TIME in this video. Use glossary cards (5-second on-screen pop-ups) when first mentioned.

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **LLM (Large Language Model)** | When explaining the "brain" of an agent | "An AI brain trained on text. It reads, reasons, and generates — but can't act on its own." |
| **Prompt** | When showing how you talk to agents | "The text you send to an LLM. Better instructions → better results." |
| **Token** | When discussing how LLMs process text | "How LLMs measure text. ~1 token ≈ ¾ of a word. API providers charge per token." |
| **Next-Token Prediction** | When explaining LLM mechanics | "How LLMs generate text: they predict the most likely next word, one at a time, like autocomplete on steroids." |
| **Hallucination** | When explaining LLM limitations | "When an LLM confidently generates incorrect information. It predicts likely-sounding text — it doesn't 'know' facts." |
| **Context Length / Context Window** | When explaining LLM memory limits | "The maximum text an LLM can 'see' at once. Like a desk that only fits so many pages." |
| **Temperature (LLM)** | When explaining output variability | "Controls how random/creative the output is. Low = predictable and safe. High = creative and risky." |
| **Tokens per Second (Inference Speed)** | When discussing local vs cloud speed | "How fast the LLM generates text. More tokens/sec = faster responses." |

### Learning Objectives
- Understand how LLMs actually work (next-token prediction) at an intuitive level
- Know why LLMs hallucinate and what affects their accuracy
- Understand tokens, context length, and inference speed
- Understand the difference between chatbots, copilots, and agents
- Grasp why agents matter now (the AI capability overhang)
- See three real examples of agents doing actual work
- Be excited to build their own

### Section 1.1 — The Problem with AI Right Now (~4 min)

**What to cover:**
- Most people use AI as a copy-paste machine: ask ChatGPT → get text → manually do the thing
- "Send an email to John about the meeting" → ChatGPT writes the email → *you* open Gmail, paste it, click send
- That's not work. That's a suggestion. The AI did the easy part (writing), you still did the hard part (executing).
- The gap: AI can *think* but it can't *act*

**Talking points:**
- Show a quick screen recording: "Hey ChatGPT, send an email to..." → ChatGPT says "I can't send emails, but here's a draft..."
- The irony: AI is smarter than ever, but 99% of people use it as a fancy text generator

### Section 1.2 — What an Agent Actually Is (~4 min)

**What to cover:**
- An agent is software that reads the situation, makes decisions, and **takes action**
- It doesn't just write the email — it *sends* the email
- It doesn't just find the recipe — it *creates the spreadsheet* with ingredients
- The three parts:
  - **Brain** = an LLM (like ChatGPT, Claude, Llama)
  - **Hands** = scripts that do specific things (call APIs, send messages, update sheets)
  - **Instructions** = written procedures that tell the brain what hands to use when
- Without hands, you have a chatbot. Without instructions, you have chaos. All three together = an agent.

**Key visual:**
```
┌──────────────────────────────────────────┐
│            AI AGENT                       │
│                                          │
│   🧠 Brain (LLM)     — decides          │
│   ✋ Hands (Scripts)  — acts             │
│   📋 Instructions     — guides           │
│        (Directives)                      │
└──────────────────────────────────────────┘
```

### Section 1.3 — Under the Hood: How LLMs Actually Work (~10 min)

> This is the "aha moment" section. Students don't need to understand the math — they need an intuitive mental model that explains hallucination, speed, context limits, and why accuracy is probabilistic. Use analogies and animated visuals throughout.

**What to cover:**

**Part A — Next-Token Prediction: The Core Trick (~3 min)**
- An LLM doesn't "think" or "understand" — it predicts the next word (token)
- Show the process step by step:
  ```
  Input:  "The capital of France is ___"
  LLM:    Paris (95%) | Lyon (2%) | Berlin (1%) | ... 
  Output: "Paris"
  
  Now:    "The capital of France is Paris. It is known for ___"
  LLM:    the (30%) | its (25%) | being (15%) | ...
  Output: "the"
  
  ...and so on, one token at a time
  ```
- Analogy: **Autocomplete on steroids.** Your phone keyboard predicts the next word — LLMs do the same thing, but trained on the entire internet.
- It's like a student who has read every book in the library and can complete *any* sentence — but has never actually visited Paris. They know what sounds right, not what *is* right.

**Key visual:** Animated text appearing one word at a time, with a probability bar chart flickering beside each word showing the top 5 candidates. The highest bar gets selected and added to the text.

**Part B — Why LLMs Hallucinate (~2 min)**
- Since LLMs predict "likely next words" rather than "true facts," they can confidently produce text that *sounds* right but *is* wrong
- Example: "Who won the 2023 Cricket World Cup?" → An LLM might say India (sounds right, India is famous in cricket) even if the training data is unclear
- Analogy: **A very confident student who never says "I don't know."** They'll always give an answer — sometimes it's right, sometimes it's a convincing guess.
- This is called **hallucination** — the LLM generates plausible-sounding text that isn't factually correct
- Why this matters for agents: if the LLM hallucinates which script to call, or makes up an API parameter, the agent breaks. That's why DOE separates "thinking" (LLM) from "doing" (deterministic scripts).

**Key visual:** Two side-by-side panels. Left: "What you asked" → Right: "What the LLM generates" — with a probability meter showing it's 75% confident but wrong. Then show a second example where it's 99% confident and right. "You can't tell from the confidence alone."

**Part C — Tokens: The Currency of AI (~2 min)**
- LLMs don't read words — they read **tokens**
- A token ≈ ¾ of a word. "Hyderabad" might be 3 tokens: "Hy" + "dera" + "bad"
- Why tokens matter:
  - **Cost:** Cloud LLM providers charge per token (input + output). A 1000-word conversation costs ~1300 tokens.
  - **Speed:** Measured in **tokens per second (tok/s)**. A local model on your PC might do 15-30 tok/s. A cloud API might do 80-150 tok/s. Faster = snappier DeskMochi responses.
  - **Limits:** Every LLM has a maximum token limit for a single conversation (context length).
- "When we run a local model on your PC later in the course, you'll see the speed in tok/s in real time — that's your model thinking."

**Key visual:** A sentence broken into colored blocks (tokens), with a counter. Show: "Hello world" = 2 tokens, "Hyderabad, India" = 4 tokens, a full paragraph = 45 tokens. Then show a speedometer-style gauge for tok/s.

**Part D — Context Length: The Agent's Working Memory (~1.5 min)**
- The **context window** is how much text the LLM can "see" at once — both what you send it AND what it generates back
- Think of it as a desk: it can only hold so many pages. Add a new page, the oldest one falls off.
- Typical context lengths:
  | Model | Context Length | In Plain English |
  |-------|---------------|------------------|
  | Small local model | ~4,000 tokens | ~3,000 words — a few pages |
  | Medium model | ~32,000 tokens | ~24,000 words — a short book |
  | Large cloud model | ~128,000+ tokens | ~96,000 words — a novel |
- Why this matters: If your agent needs to read a long directive + conversation history + script output, and it exceeds the context window, the LLM literally can't see the beginning of the conversation anymore.
- "This is why we keep directives short and scripts focused — we're being respectful of the context window."

**Key visual:** A desk with pages being stacked. When the stack gets too high, old pages fall off the back. A progress bar shows "Context used: 2,400 / 4,096 tokens."

**Part E — Temperature: The Creativity Dial (~1.5 min)**
- **Temperature** controls how "random" or "creative" the LLM's output is
- `Temperature = 0` → always picks the highest-probability word. Same input = same output. Very predictable.
- `Temperature = 1` → picks from a wider range of probable words. More creative, but more likely to go off-track.
- `Temperature > 1` → increasingly random. The LLM starts picking unlikely words. Gets weird fast.
- For agents, we typically use **low temperature** (0.0–0.3) because we want reliable, predictable decisions — not creative poetry.
- For brainstorming or creative tasks, higher temperature is fine.
- Analogy: **A volume knob for randomness.** Turn it down for "dependable assistant." Turn it up for "creative writer."

**Key visual:** A physical dial/knob labeled 0 to 2. At 0: the LLM outputs the same boring-but-correct sentence every time. At 0.5: slight variations but still accurate. At 1.5: wild, creative, sometimes nonsensical. Animate the output text changing as the dial turns.

**Wrap-up for this section:**
- "Now you know how the brain works — it predicts words, one at a time, based on probability. It's fast, it's impressive, but it doesn't *know* things. That's why agents need the DOE approach: let the LLM decide *what* to do, but let reliable scripts *do* it."

### Section 1.4 — Three Types of AI Interaction (~3 min)

**What to cover:**
- **Documents** — AI generates text you copy-paste. (ChatGPT default mode)
  - Example: "Write me a cover letter" → you paste into an email
- **Copilots** — AI assists while *you* drive. (GitHub Copilot, Cursor)
  - Example: You're coding, AI suggests the next line, you accept/reject
- **Agents** — AI drives, you supervise. (What we're building)
  - Example: "Send my wife a WhatsApp saying I'll be late" → it sends it, confirms with you

**Key visual:** A car analogy:
- Documents = AI gives you directions, you drive
- Copilot = AI sits in the passenger seat, helps navigate
- Agent = AI drives, you sit back and confirm the route

### Section 1.5 — The Capability Overhang (~3 min)

**What to cover:**
- LLMs are already incredibly capable — most people just don't connect them to the real world
- It's like having a genius employee who can think and plan perfectly, but has no arms and legs
- Agents give the AI arms and legs (scripts that do things)
- The gap between "what AI can do" and "what people use AI for" is enormous — that gap is the opportunity

**Talking points:**
- "The AI overhang isn't about smarter models. It's about connecting existing models to real tools."
- "You don't need a PhD in AI. You need to know how to give AI access to APIs."

### Section 1.6 — Three Live Demos (~3 min)

**What to show:** Quick, punchy screen recordings (30-45 seconds each):

**Demo 1: Weather**
- Press button on DeskMochi → "What's the weather?" → display shows "28°C, Sunny, Hyderabad" → speaker says it aloud
- Caption: "DeskMochi called a weather API and read you the result."

**Demo 2: Recipe Spreadsheet**
- Voice command → "Find a butter chicken recipe and put it in a spreadsheet" → Google Sheet appears with ingredients + steps
- Caption: "DeskMochi searched the web, extracted data, and created a spreadsheet."

**Demo 3: WhatsApp Message**
- Voice command → "Tell Priya I'll be 15 minutes late" → WhatsApp message sent → DeskMochi confirms "Message sent!"
- Caption: "DeskMochi composed a message and sent it through WhatsApp's API."

**After demos:**
- "Each of these took less than 10 seconds. Behind the scenes: an LLM decided what to do, a script executed it, and DeskMochi showed you the result."
- "By Video 7, you'll build all three of these yourself."

### Section 1.7 — What We'll Build (~2 min)

**What to cover:**
- By the end of this course:
  - A physical DeskMochi companion on your desk (hardware)
  - A local server on your PC (software)
  - 7+ working skills (weather, recipes, WhatsApp, home automation, morning briefings, etc.)
  - A complete framework (DOE) for building any future agent
- Course roadmap — show the video list at a glance
- "You don't need to know how to code. The AI writes the code. You need to know how to think about agents — that's what this course teaches."

### Video 1 Key Takeaway
> An agent = brain (LLM) + hands (scripts) + instructions (directives). The brain decides, the hands execute, the instructions guide. This course teaches you to build all three.

---

## Video 2: How Agents Think — The DOE Framework

**Duration:** ~20-22 min
**Type:** Whiteboard/animated diagrams + screen walkthrough
**Goal:** Teach the DOE Framework — the single most important concept in the course. Everything builds on this.

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **Deterministic vs Probabilistic** | The 90% accuracy problem | "Deterministic = same input, same output always (a calculator). Probabilistic = slightly different each time (an LLM)." |
| **SOP (Standard Operating Procedure)** | When explaining directives | "A step-by-step checklist for how to complete a task. Directives ARE SOPs for AI." |
| **Framework** | When introducing DOE | "A reusable pattern for solving a category of problems. DOE is a framework for building agents." |
| **Markdown** | When showing a directive file | "A simple way to format text: # for headings, ** for bold, - for bullets. All directives use it." |

### Learning Objectives
- Understand the 90% accuracy problem and why it matters
- Know the three layers of DOE (Directive, Orchestration, Execution)
- Understand separation of concerns — why you keep the brain and hands separate
- See a complete end-to-end example

### Section 2.1 — The Reliability Problem (~4 min)

**What to cover:**
- AI (LLMs) is *probabilistic* — the same question can give slightly different answers each time
- For one question, that's fine. 90% accuracy is great.
- But agents do multi-step tasks. If each step is 90% accurate:
  - 2 steps: 81%
  - 3 steps: 73%
  - 5 steps: 59%
  - 10 steps: 35%
- "If you ask an AI to do 10 things in a row and each thing might go slightly wrong... by the end, it's basically a coin flip."
- This is why "just tell ChatGPT to do everything" doesn't work for real tasks

**Key visual:** A bar chart showing accuracy dropping from 90% → 59% → 35% as steps increase. Make it visceral.

**The fix:** Don't make the AI do everything. Make it *decide* what to do, then hand the actual *doing* to reliable scripts that work 100% of the time.

### Section 2.2 — The Three Layers of DOE (~5 min)

**What to cover:**

```
┌─────────────────────────────────────────────┐
│  Layer 1: DIRECTIVE  (directives/*.md)      │
│  "What to do" — written in plain English    │
├─────────────────────────────────────────────┤
│  Layer 2: ORCHESTRATOR  (the AI brain)      │
│  "Decide how to do it" — makes decisions    │
├─────────────────────────────────────────────┤
│  Layer 3: EXECUTION  (execution/*.py)       │
│  "Actually do it" — reliable scripts        │
└─────────────────────────────────────────────┘
```

**Layer 1 — Directive:**
- A document written in plain English describing what to do
- Like an SOP (Standard Operating Procedure) at a company
- Contains: goal, inputs, which scripts to use, step-by-step workflow, edge cases
- This is the only part *you* write from scratch (and even that, AI helps with)

**Layer 2 — Orchestrator:**
- The AI brain (Copilot, Claude, GPT, Llama, etc.)
- Its ONLY job: read the directive, decide the order of steps, call scripts with the right inputs, handle errors
- It never does grunt work directly — it delegates to scripts
- Think of it as a project manager: doesn't do the work, but decides who does what and in what order

**Layer 3 — Execution:**
- Python scripts that each do exactly ONE thing reliably
- Call an API, read a file, write to a spreadsheet, send a message
- Same input → same output, every time (deterministic)
- These are the "hands" of the agent

### Section 2.3 — The Restaurant Analogy (~3 min)

**What to cover:**
- **Directive** = the menu + recipes
  - "Here's what we serve, here's how to make each dish"
- **Orchestrator** = the head chef
  - Reads the order, decides which cooks to assign, handles problems ("we're out of salmon — substitute trout")
- **Execution** = the line cooks
  - Each cook makes one thing perfectly. The pasta cook makes pasta. The grill cook grills. They don't decide *what* to make — they execute.
- The head chef (AI) never personally chops onions. The line cooks (scripts) never decide the menu. Everyone stays in their lane.

**Key visual:** Animated restaurant with labeled roles.

### Section 2.4 — Walk Through a Real Example (~4 min)

**What to cover:** "Get me the weather in Hyderabad" — end to end.

**Step 1 — Directive exists:**
```markdown
# Get Weather
## Goal
Get current weather for a city.
## Tools
- execution/get_weather.py — calls OpenWeatherMap API
## Workflow
1. Run get_weather.py with the city name
2. Format result: "It's {temp}°C and {condition} in {city}"
3. Return the formatted string
```

**Step 2 — You ask DeskMochi:** "What's the weather in Hyderabad?"

**Step 3 — Orchestrator reads the directive:**
- "I need to get weather. The directive says use `get_weather.py` with a city name."
- "The city is Hyderabad."
- "I'll run the script."

**Step 4 — Script executes:**
- `get_weather.py` calls OpenWeatherMap API with "Hyderabad"
- API returns: `{"temp": 28, "condition": "sunny"}`
- Script returns this data to the orchestrator

**Step 5 — Orchestrator formats and delivers:**
- "It's 28°C and sunny in Hyderabad"
- Sends to DeskMochi → display shows it, speaker reads it aloud

**Key visual:** Animated flow diagram with each step lighting up in sequence.

### Section 2.5 — Self-Annealing: The System Gets Smarter (~3 min)

**What to cover:**
- What happens when things break (and they will)?
- The self-annealing loop:
  ```
  Error occurs
       ↓
  Read the error message
       ↓
  Fix the script
       ↓
  Test the fix
       ↓
  Update the directive with what you learned
       ↓
  System is now stronger — that error can never happen again
  ```
- Quick example: "The weather API has a limit of 60 calls per minute. You hit it."
  - Fix: Add a pause between calls in the script
  - Update directive: "Note: API rate limit is 60/min. Script handles this automatically."
  - Now any AI reading the directive knows about this constraint upfront

### Section 2.6 — The Golden Rules (~2 min)

**What to cover:**
1. **The AI decides, scripts execute.** Never mix the two roles.
2. **Directives are living documents.** Update them every time you learn something.
3. **One script, one job.** Keep scripts small and focused.
4. **Self-anneal every time.** Fix → test → update directive.

### Video 2 Key Takeaway
> DOE = Directive (instructions) + Orchestration (AI decisions) + Execution (reliable scripts). The AI is the brain. Scripts are the hands. Directives are the playbook. Keep them separate and the system is reliable.

---

## Video 3: Building DeskMochi — The Hardware
> **🤖 DeskMochi Track only.** Software Track students skip this video entirely. You pick back up at Video 4.

**Duration:** ~18-20 min
**Type:** Hands-on build with wiring diagrams + overhead camera
**Goal:** Assemble and connect the physical DeskMochi device.

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **Microcontroller (ESP32)** | Opening — what's in the box | "A tiny, cheap computer the size of your thumb. Connects to WiFi, controls displays and speakers." |
| **Firmware** | When flashing code to ESP32 | "Software permanently installed on a device. Flash it once, runs every time the device turns on." |
| **WiFi (device perspective)** | When configuring network | "How the ESP32 finds your PC on the same network. Both must be on the same WiFi." |
| **WebSocket** | When explaining ESP32-to-server link | "A persistent two-way connection. Unlike an API call (ask → answer → hang up), a WebSocket stays open like a phone call." |
| **Serial / USB Communication** | When connecting ESP32 to PC | "How your PC talks to the ESP32 through the USB cable. Used for uploading firmware and debugging." |
| **TTS (Text-to-Speech)** | When setting up the speaker | "Converting written text into spoken audio. The server generates speech; DeskMochi plays it." |

### Learning Objectives
- Know what parts are needed and how they connect
- Successfully wire the ESP32 + display + speaker
- Flash the DeskMochi firmware
- See DeskMochi connect to the PC and display "Ready!"

### Section 3.1 — What's in the Box / Parts List (~3 min)

**What to cover:**
- List every part with a photo:
  - ESP32 Dev Module (the brain of DeskMochi)
  - Small display (OLED SSD1306 / TFT ILI9341 — depends on chosen model)
  - Speaker module (I2S DAC + small speaker, or MAX98357A amplifier board)
  - Micro USB cable
  - Breadboard + jumper wires (for prototyping)
  - (Optional) 3D-printed enclosure / cardboard housing for the "desk companion" look
- Where to buy (links in description)
- Total cost estimate: ~$15-25 for components

### Section 3.2 — Wiring It Up (~5 min)

**What to cover:**
- Clear overhead camera showing each wire connection
- Step-by-step: Display first, then speaker, then power
- Show a clean wiring diagram (color-coded)
- Pin mapping table:
  | Component | ESP32 Pin | Notes |
  |-----------|-----------|-------|
  | Display SDA | GPIO 21 | I2C data |
  | Display SCL | GPIO 22 | I2C clock |
  | Speaker BCLK | GPIO 26 | I2S bit clock |
  | Speaker LRC | GPIO 25 | I2S word select |
  | Speaker DIN | GPIO 27 | I2S data |
- "If you wire it wrong, nothing will break — it just won't work. Double-check connections against the diagram."

### Section 3.3 — Flashing the Firmware (~5 min)

**What to cover:**
- Install Arduino IDE (or PlatformIO — pick one, don't overwhelm)
- Add ESP32 board support (walk through the exact menu clicks)
- Open the DeskMochi firmware file (provided with course materials)
- Configure WiFi: edit 2 lines in the code with your WiFi name + password
- Click "Upload" → watch it flash → success message
- What the firmware does:
  - Connects to WiFi on boot
  - Opens a WebSocket connection to your PC (at a pre-configured IP + port)
  - Listens for messages from server → shows on display, plays on speaker
  - Sends button presses / voice commands to the server

### Section 3.4 — First Power-On (~3 min)

**What to cover:**
- Plug in USB → DeskMochi powers on
- Display shows: "Connecting to WiFi..."
- Then: "Connecting to server..." (this will fail because we haven't built the server yet — that's OK!)
- Explain: "DeskMochi is looking for a server on your PC at port 8000. We'll build that server in Video 6."
- For now: show a quick test with a minimal server script (provided) that just sends "Hello DeskMochi!" to the display
- Display shows: "Hello DeskMochi!" → speaker says it → celebrate!

### Section 3.5 — How DeskMochi Fits the Architecture (~2 min)

**What to cover:**
- Map DeskMochi to the DOE layers:
  ```
  [You] → speak/press button → [DeskMochi ESP32]   ← CLIENT
                                      ↓ WebSocket
                            [Your PC - Local Server]  ← ORCHESTRATOR + EXECUTION
                                      ↓
                            [LLM API + Scripts]
                                      ↓
                            [Result → DeskMochi]       ← DISPLAY + SPEAKER
  ```
- DeskMochi is the **interface**. It's the "face" of the agent. The intelligence lives on your PC.
- "Think of DeskMochi as a walkie-talkie. It sends your request to headquarters (your PC), headquarters figures out the answer, and radios it back."

### Video 3 Key Takeaway
> DeskMochi is the physical face of your agent. It communicates over WebSocket to a server on your PC. The hardware is simple — the intelligence lives in software.

---

## Video 4: Setting Up Your Agent Workshop

> **Both tracks.** Software Track students skip Section 4.6 (DeskMochi pairing). The agent dashboard is set up automatically as part of the workspace generator.

**Duration:** ~22-25 min
**Type:** Screen share walkthrough — step by step
**Goal:** Get the complete development environment running and generate the first workspace.

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **IDE / Code Editor** | Installing VS Code | "A fancy text editor for code. VS Code has a file browser, terminal, and AI assistant built in." |
| **Terminal / Command Line** | First time opening it | "A text interface where you type commands. The black panel at the bottom of VS Code." |
| **Command** | First `python` command | "An instruction typed into the terminal. Press Enter to run it." |
| **Command-Line Argument** | `--name "My Agent"` | "Extra info you pass to a command, like filling in blanks: `get_weather.py --city ____`." |
| **Python** | Installation | "A programming language. You don't need to master it — you need to run Python files and read them at a high level." |
| **pip / Package Manager** | `pip install` | "Downloads code libraries other people wrote. Like an app store for Python packages." |
| **Library / Package** | `requirements.txt` | "Code someone else wrote that you can reuse. `requests` = a package for calling APIs." |
| **requirements.txt** | Installing dependencies | "A shopping list of packages your agent needs. One command installs them all." |
| **Environment Variable** | Explaining `.env` | "A named value stored in memory. Scripts read it by name: 'give me the API_KEY'." |
| **.env File** | Adding first API key | "A secret file storing API keys. Scripts read from it. Never share it." |
| **Virtual Environment (venv)** | Setup script creates one | "An isolated bubble for Python packages. Each project has its own so they don't clash." |
| **Git** | Cloning the repo | "Tracks changes to files over time. Like 'Track Changes' in Word, but for code." |
| **GitHub** | Downloading the project | "A website that stores code projects. You'll download the course code from here." |
| **Cloning a Repository** | `git clone` | "Downloading a full project from GitHub. One command, you get every file." |

### Learning Objectives
- Install Python, VS Code, and GitHub Copilot
- Clone the course repository
- Generate a DeskMochi agent workspace
- Configure the first API key
- Verify everything works

### Section 4.1 — Install the Tools (~5 min)

**What to cover — show every click:**
1. **Python 3.10+:**
   - Go to python.org → Download → Run installer
   - IMPORTANT: Check "Add Python to PATH" ✅
   - Verify: Open terminal → type `python --version` → see version number
2. **VS Code:**
   - Go to code.visualstudio.com → Download → Install
   - Open it for the first time
3. **GitHub Copilot Extension:**
   - Click Extensions sidebar → Search "GitHub Copilot" → Install
   - Sign in with GitHub account
   - Verify: Open Copilot Chat panel (Ctrl+Shift+I)
4. **Git:**
   - Windows: already installed or `winget install Git.Git`
   - Verify: `git --version` in terminal

### Section 4.2 — Clone the Course Repository (~3 min)

**What to cover:**
- Open terminal in VS Code
- Run: `git clone <repo-url>`
- Explain what just happened: "You downloaded every file from the course's GitHub page to your computer."
- Open the cloned folder in VS Code
- Tour the folder structure (briefly — don't linger):
  ```
  directives/   → Instructions (SOPs for the agent)
  execution/    → Python scripts (the tools)
  AGENTS.md     → The agent's brain rules
  .env          → Your secrets (we'll create this)
  ```
- "Don't worry about understanding every file. We'll explore them as we need them."

### Section 4.3 — Generate a DeskMochi Workspace (~4 min)

**What to cover:**
- Run the generator:
  ```
  python execution/create_agent_workspace.py --name "DeskMochi Agent" --type custom
  ```
- Watch it generate files → explain what each is:
  - `AGENTS.md` — "This is the instruction manual for the AI brain."
  - `directives/` — "This is where our task instructions will live."
  - `execution/` — "This is where our scripts live."
  - `.env.example` — "This is a template for our API keys."
  - `setup.ps1` / `setup.sh` — "This sets up everything with one command."
  - `dashboard/index.html` — "This is your local agent dashboard — a simple web interface where you can send commands and see results. Software Track students use this instead of DeskMochi hardware."
- Run the setup script → watch it install packages + create `.env`

> **🖥️ Software Track note:** The workspace generator creates a local web dashboard at `dashboard/index.html`. When your server is running, open this in any browser. It's a simple interface: a text box to send commands, and a panel that shows the agent's responses. It's your "virtual DeskMochi" — same commands, same results, just on screen instead of on a physical device.

> **🤖 DeskMochi Track note:** The dashboard is still generated and available. You can use it to test skills before wiring them to the physical device, or as a fallback when DeskMochi is not nearby.

### Section 4.4 — Get Your First API Key (~5 min)

**What to cover:**
- We'll use OpenWeatherMap (free, no credit card needed)
- Step by step:
  1. Go to openweathermap.org → Sign up (free)
  2. Go to API Keys section → Copy your key
  3. Open `.env` in VS Code → Add: `OPENWEATHER_API_KEY=your_key_here`
  4. Save the file
- Explain:
  - "Every external service you use will give you a key like this."
  - "You'll add each key to `.env` as we need it."
  - "The scripts automatically read from `.env`, so you never hard-code secrets."

### Section 4.5 — Verify Everything Works (~3 min)

**What to cover:**
- Quick test: ask Copilot "What files are in the execution folder?"
- Copilot lists them → "Great, Copilot can see our workspace."
- Run a simple command to verify Python works:
  ```
  python -c "print('Hello from DeskMochi!')"
  ```
- "We're all set. In the next video, we build our first real agent skill."

### Section 4.6 — 🖥️ Software Track: Open Your Dashboard (~2 min)

> **Software Track only.** DeskMochi Track students skip ahead to 4.7.

**What to cover:**
- Make sure the server is started: `python execution/local_server.py`
- Open `dashboard/index.html` in your browser (or it auto-opens from the setup script)
- Show the interface:
  - A text input at the top: "Ask your agent something..."
  - A response panel below
  - A "Tools" sidebar showing available skills
- Type: "Hello! What can you do?"
- Agent responds in the panel
- "This is your virtual desk companion. Every command you'd give DeskMochi, you can give here. Every demo in this course works in this dashboard."

### Section 4.6b — 🤖 DeskMochi Track: Pair Your Device (~3 min)

> **DeskMochi Track only.** Assumes Video 3 is complete.

**What to cover:**
- Power on DeskMochi (you should have firmware flashed from Video 3)
- Check that your PC and DeskMochi are on the same WiFi network
- Start the server: `python execution/local_server.py`
- DeskMochi display should change from "Waiting..." to "Connected!"
- If it doesn't connect: troubleshooting steps (check IP address in firmware config, check firewall)
- Quick test: send a message from Copilot → verify it appears on DeskMochi display

### Section 4.7 — Quick Reference Card (~2 min)

**What to show on screen:**
```
WHAT                           WHERE
─────────────────────────────────────────────
Agent's brain rules            AGENTS.md
Task instructions              directives/*.md
Python scripts                 execution/*.py
API keys & secrets             .env
Temporary data                 .tmp/
Your interface (Software)      dashboard/index.html
Your interface (DeskMochi)     Physical device
```
- "Bookmark this. You'll use it every video."

### Video 4 Key Takeaway
> Your workspace is your agent's home. It took 10 minutes to set up. Directives tell the AI what to do, scripts do it, .env gives them access. Whether you're using the web dashboard or the physical DeskMochi device, the commands, skills, and framework are identical.

---

## Video 5: Your First Agent — "Get the Weather"

> **Both tracks.** Software Track students see output in the browser dashboard. DeskMochi Track students see it on the physical device. The directive, script, and Copilot orchestration are identical for both.

**Duration:** ~25-28 min
**Type:** Live coding with Copilot (Copilot mode)
**Goal:** Build a complete agent skill from scratch — the weather checker — and see DOE in action.

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **HTTP (GET, POST)** | When the script calls the API | "The language of the web. GET = 'give me data.' POST = 'here's data, do something.'" |
| **URL / Endpoint** | The weather API URL | "The address of a specific API function. Like a street address for a service." |
| **REST** | When explaining API patterns | "Conventions for how APIs work. Use URLs for resources, GET to read, POST to create." |
| **Status Code** | When handling errors | "The API's one-word answer. 200 = success. 404 = not found. 500 = server broke." |

### Learning Objectives
- Write a directive from scratch (in plain English)
- Have Copilot generate an execution script
- See the full Copilot orchestration loop
- Handle an error and self-anneal
- (Stretch) Connect output to DeskMochi

### Section 5.1 — Write the Directive (~5 min)

**What to cover:**
- Create `directives/get_weather.md` — type it out live, explaining each section:
  ```markdown
  # Get Weather

  ## Goal
  Get the current weather for a city and display it on DeskMochi.

  ## Inputs
  | Input | Required | Description |
  |-------|----------|-------------|
  | City  | Yes      | City name (e.g., "Hyderabad", "New York") |

  ## Tools/Scripts
  - `execution/get_weather.py` — calls OpenWeatherMap API
    - Requires: OPENWEATHER_API_KEY in .env
    - Input: --city "city name"
    - Output: JSON with temp, condition, humidity

  ## Workflow
  1. Run `execution/get_weather.py --city "{city}"`
  2. Read the JSON output
  3. Format: "It's {temp}°C and {condition} in {city}"
  4. Return the formatted weather string

  ## Edge Cases
  - If city name is misspelled, the API returns an error — ask user to correct
  - If API key is missing, remind user to set OPENWEATHER_API_KEY in .env
  ```
- "This took 2 minutes. There's no code here — just English. That's a directive."

### Section 5.2 — Have Copilot Write the Script (~8 min)

**What to cover:**
- Open Copilot Chat and say: "Read the directive at `directives/get_weather.md` and create the execution script `execution/get_weather.py` for me."
- Watch Copilot:
  1. Read the directive
  2. Understand what API to call
  3. Generate a complete Python script with:
     - `dotenv` loading for the API key
     - `argparse` for the `--city` argument
     - `requests.get()` call to OpenWeatherMap
     - JSON parsing and output
- Walk through the generated code at a HIGH level (don't teach Python — explain what each block does):
  - "This block loads your API key from `.env`"
  - "This block reads the city name you pass in"
  - "This block calls the weather API"
  - "This block prints the result"
- "The AI wrote the code. You wrote the instructions. That's the DOE pattern."

### Section 5.3 — Test It with Copilot (~4 min)

**What to cover:**
- Ask Copilot: "What's the weather in Hyderabad?"
- Watch the orchestration loop happen in real time:
  1. Copilot reads the directive
  2. Copilot identifies the city: "Hyderabad"
  3. Copilot runs: `python execution/get_weather.py --city "Hyderabad"`
  4. Script returns: `{"temp": 28, "condition": "Sunny", "humidity": 65}`
  5. Copilot formats: "It's 28°C and Sunny in Hyderabad"
- Try another city: "And what about Tokyo?" → watch it run again

### Section 5.4 — Make It Fail (On Purpose) (~4 min)

**What to cover:**
- Ask: "What's the weather in Hiderabad?" (misspelled)
- Watch what happens → API returns an error
- Copilot should handle it gracefully — if not, this is a live self-annealing moment:
  1. Read the error
  2. Copilot either fixes the script or updates the directive
  3. Test again
- "This is self-annealing in action. The system just got smarter."

### Section 5.5 — See Your Agent in Action (~4 min)

**🖥️ Software Track — Dashboard Output:**
- Show the result appearing in the `dashboard/index.html` panel in the browser
- The agent's response populates in the chat panel: "It's 28°C and Sunny in Hyderabad"
- "This is your agent. It read your instructions, ran a script, got live data, and responded. This is the DOE pattern working end-to-end — and you can do everything in this course from right here in your browser."

**🤖 DeskMochi Track — Physical Output:**
- Show how the weather result flows to DeskMochi:
  - Server receives formatted string
  - Sends over WebSocket to ESP32
  - Display shows: "28°C ☀️ Sunny — Hyderabad"
  - Speaker reads: "It's 28 degrees and sunny in Hyderabad"
- (If server isn't built yet, show a preview / mock. Full server comes in Video 6.)
- "Right now Copilot is the brain. In Video 6, we'll replace Copilot with a server so DeskMochi works even when VS Code is closed."

### Section 5.6 — Recap: What Just Happened (~2 min)

**What to cover:**
- "In 15 minutes you:"
  - Wrote instructions in English (directive)
  - Had AI generate the code (execution script)
  - Tested it end-to-end
  - Handled an error
  - Made the system smarter
- "That's the DOE loop. Every skill you build will follow this exact pattern."

### Video 5 Key Takeaway
> You wrote English instructions. AI wrote the code. You tested it. It worked. When it broke, you fixed it and updated the instructions. That's agent development — and you just did it in 15 minutes.

---

## Video 6: The Local Server — Running Without Copilot

> **Both tracks.** The server setup is identical. The only difference: the Software Track serves output to `dashboard/index.html`; the DeskMochi Track serves it to the physical device over WebSocket. Both are handled automatically by `local_server.py`.

**Duration:** ~22-25 min
**Type:** Architecture diagram + screen share
**Goal:** Build and run the local server so DeskMochi works 24/7 without VS Code open.

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **localhost** | Starting the server | "Your own computer, as a network address. `localhost:8000` = the server running on my PC, door 8000." |
| **Port** | `localhost:8000` | "A numbered door on your computer. Different services use different doors. Our server uses 8000." |
| **FastAPI** | Building the server | "A Python package for building servers. Handles the 'listen and respond' part for you." |
| **Agentic Loop** | Replacing Copilot | "The cycle: LLM reads → decides tool → script runs → result back → LLM decides next → repeat until done." |
| **Local Model** | Running AI on your own PC | "An LLM that runs entirely on your computer. No internet, no API key, no cost, full privacy." |

### Learning Objectives
- Understand why a server is needed (DeskMochi needs a 24/7 brain)
- See the architecture: what changes when Copilot is replaced
- Choose an LLM provider (free → paid options)
- Start the local server and test with DeskMochi

### Section 6.1 — Why Do We Need a Server? (~3 min)

**What to cover:**
- In Video 5, Copilot was the brain. But Copilot only works when:
  - VS Code is open
  - You're actively chatting
  - Your computer is powered on with VS Code running
- For DeskMochi to be a desk companion, it needs a brain that's *always available*
- The server replaces Copilot as Layer 2 (Orchestrator)
- Key insight: **Layers 1 and 3 don't change at all!** Same directives, same scripts. Only the brain swaps.

**Key visual:**
```
COPILOT MODE:                      SERVER MODE:
You → Copilot → Scripts            DeskMochi → Server → Scripts
     (in VS Code)                        (always running)
```

### Section 6.2 — The Architecture (~3 min)

**What to cover:**
```
[DeskMochi ESP32]
       ↓ WebSocket (persistent connection)
[Local Server — localhost:8000]
  ├── WebSocket handler (talks to DeskMochi)
  ├── Agentic Loop (reads directives, calls LLM, runs scripts)
  ├── Directive Loader (reads directives/*.md)
  └── Script Runner (runs execution/*.py)
       ↓ API call
[LLM Provider] (Ollama/DeepSeek/OpenAI/Claude)
```
- DeskMochi sends a message → server receives it → server reads the right directive → asks the LLM what to do → runs scripts → sends result back to DeskMochi
- "The server is doing exactly what Copilot did — reading instructions, making decisions, calling tools. It's just doing it as a Python program instead of inside VS Code."

### Section 6.3 — Running AI Locally: Your PC as the Brain (~7 min)

**What to cover:**
- The server needs an LLM brain. The most exciting option: **run it entirely on your own PC.**
- Why local matters:
  - **$0 cost** — no API fees ever
  - **Full privacy** — your data never leaves your machine
  - **No internet required** — works offline, on a plane, during outages
  - **No rate limits** — call it as much as you want
  - **You own it** — no vendor can take it away or change pricing

**Local Models That Run on a Decent PC:**

| Model | Size | RAM Needed | Speed (tok/s)* | Best For |
|-------|------|-----------|----------------|----------|
| **Google Gemma 3 (4B)** | ~2.5 GB | 8 GB | 25-40 tok/s | Fast, great for simple agent tasks |
| **Google Gemma 3 (12B)** | ~7 GB | 16 GB | 12-20 tok/s | Good balance of speed & quality |
| **Llama 3.1 (8B)** | ~4.7 GB | 16 GB | 15-25 tok/s | Versatile, well-rounded |
| **Mistral (7B)** | ~4 GB | 16 GB | 15-25 tok/s | Fast, good at following instructions |
| **Phi-3 Mini (3.8B)** | ~2.3 GB | 8 GB | 30-50 tok/s | Tiny but surprisingly capable |

*\*Speed varies by hardware. Measured on a mid-range PC with 16 GB RAM, no GPU.*

- "If your PC has 16 GB RAM and a halfway decent processor, you can run a solid local model. If you have a GPU (gaming PC, creative workstation), speeds jump 3-5x."
- **Google's Gemma models** are specifically designed to run well on consumer hardware — Google released them so anyone can run AI locally without needing a data center.

**Setting Up Ollama + a Local Model (live demo):**
  - Install: go to ollama.ai → download → install (one click)
  - Pull Google's Gemma 3: `ollama pull gemma3`
  - Test it: `ollama run gemma3` → type "Hello, what can you help with?" → instant response
  - "That response was generated entirely on your PC. No internet. No API key. No cost."
  - Show the inference speed in terminal: "See that? 28 tokens per second. That's your computer thinking."
  - It's now running at `http://localhost:11434` — the server will connect to this

**The speed you see (tok/s) maps directly to how fast DeskMochi responds:**
  - 15+ tok/s = natural conversational speed (good)
  - 30+ tok/s = snappy, feels instant
  - < 10 tok/s = noticeable delay, but still works

**Cloud alternatives (when you need more power):**

| Provider | Cost | Speed | Context Length | Quality | Best For |
|----------|------|-------|---------------|---------|----------|
| **Groq** (free tier) | $0 | ⚡ Blazing (500+ tok/s) | 8K-128K | Great | **Our go-to for API demos in this course** |
| **DeepSeek** | ~$0.27/M tokens | Fast | 64K | Excellent | Best value for cloud |
| **OpenAI** (GPT-4o) | ~$2.50/M tokens | Fast | 128K | Excellent | Most popular, huge ecosystem |
| **Anthropic** (Claude Opus 4.6) | ~$15/M tokens | Moderate | 200K | Best-in-class | Complex reasoning, long documents |
| **Anthropic** (Claude Sonnet) | ~$3/M tokens | Fast | 200K | Excellent | Great balance of cost & quality |

- "For this course, we use **local models via Ollama** for everyday DeskMochi tasks, and **Groq's free tier** to show how API-based agents work. The beautiful part: the exact same code works with OpenAI or Anthropic — you just change two lines in `.env`."
- "In Video 8, we'll switch to Groq and then show a jaw-dropping demo with Claude Opus 4.6 — to see just how much the choice of model changes what's possible."

### Section 6.4 — Start the Server (~5 min)

**What to cover:**
- Set the LLM provider in `.env`:
  ```
  LLM_PROVIDER=ollama
  LLM_MODEL=gemma3
  ```
- Start the server:
  ```
  python execution/local_server.py
  ```
- Terminal shows: "Server running on localhost:8000 — using Ollama (gemma3)"
- Explain what's happening:
  - Server is now listening for WebSocket connections from DeskMochi
  - It loaded all directives from `directives/`
  - It connected to the local Gemma 3 model via Ollama
  - It's ready to accept requests — no internet needed

### Section 6.5 — The Full Standalone Demo (~5 min)

**What to cover:**
- The server is now running autonomously — no VS Code open, no Copilot needed
- The server loaded all directives from `directives/`
- It connected to the local Gemma 3 model via Ollama
- It's processing requests in the terminal

**🖥️ Software Track demo:**
- Open `dashboard/index.html` in a browser (separate from VS Code)
- Close VS Code entirely
- Type in the dashboard: "What's the weather in Hyderabad?"
- Watch the server terminal logs react in real time:
  ```
  [19:30:01] Dashboard client connected
  [19:30:05] Request: "What's the weather in Hyderabad?"
  [19:30:05] Loading directive: get_weather.md
  [19:30:06] LLM (gemma3 @ 32 tok/s) decided: run get_weather.py --city "Hyderabad"
  [19:30:07] Script returned: {"temp": 28, "condition": "Sunny"}
  [19:30:07] LLM formatted: "It's 28°C and Sunny in Hyderabad"
  [19:30:07] Sent to dashboard
  ```
- Dashboard panel shows: "It's 28°C and Sunny in Hyderabad"
- "VS Code is closed. Copilot is not running. Your agent is working completely standalone."

**🤖 DeskMochi Track demo — emphasize this is 100% local:**
- "I'm going to turn off my WiFi now. Watch."
- Disable WiFi on screen → DeskMochi still says "Connected" (it's on LAN, not internet)
- Press button → "What's the weather in Hyderabad?"
- Watch the server logs in the terminal:
  ```
  [19:30:01] DeskMochi connected
  [19:30:05] Request: "What's the weather in Hyderabad?"
  [19:30:05] Loading directive: get_weather.md
  [19:30:06] LLM (gemma3 @ 32 tok/s) decided: run get_weather.py --city "Hyderabad"
  [19:30:07] Script returned: {"temp": 28, "condition": "Sunny"}
  [19:30:07] LLM formatted: "It's 28°C and Sunny in Hyderabad"
  [19:30:07] Sent to DeskMochi
  ```
- DeskMochi display: "28°C ☀️ Sunny"
- DeskMochi speaker: "It's 28 degrees and sunny in Hyderabad"
- "See the `32 tok/s` in the logs? That's Gemma 3 running on this PC, generating text in real time. No cloud. No API key. No cost."

**The power of local (both tracks):**
- "This entire interaction happened on your home network. The AI model ran on your PC. Your question never left your house."
- "That matters for privacy: your commands, your data, your conversations — all local."
- "And it's free. Run it a thousand times a day — no bill."

### Section 6.6 — Close VS Code — It Still Works! (~2 min)

**What to cover:**
- Close VS Code entirely
- **Software Track:** Open the dashboard in a browser → type "What time is it?" → agent responds
- **🤖 DeskMochi Track:** Press DeskMochi button → "What time is it?" → DeskMochi responds
- "The server is running in the terminal. Copilot isn't needed anymore."
- "This is Mode 2 of the DOE Framework — standalone deployment."
- "Your agent is alive. It's waiting for you. No cloud dependency, no subscription, no VS Code. Just a Python program running on your machine."

### Video 6 Key Takeaway
> The server replaces Copilot as the brain. Same directives, same scripts — just a different orchestrator. Whether you're using the browser dashboard or the physical DeskMochi device, your agent now works 24/7 without VS Code.

---

## Video 7: Making DeskMochi Useful — Real-World Skills

> **Both tracks.** The directive, script creation, and testing steps are identical for both tracks. The only difference is where results are displayed: Software Track uses the browser dashboard; DeskMochi Track uses the physical device. "Connect to DeskMochi" steps in this video should be presented as "Connect to your interface (dashboard or DeskMochi)."

**Duration:** ~30-35 min
**Type:** Build 4 skills live, each following the DOE pattern
**Goal:** Rapid-fire skill building. By the end, DeskMochi does 4 real-world tasks.

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **OAuth** | Google Sheets setup | "A secure login flow. You grant permission via browser once, then it works automatically." |
| **Webhook** | WhatsApp delivery confirmation | "Reverse API call: instead of you asking, the service pushes data to you when something happens." |
| **Spreadsheet ID** | Google Sheets | "The unique code in a Google Sheet URL — found between /d/ and /edit." |
| **Third-Party Service** | Connecting to Twilio, etc. | "Any external product whose API you call. Twilio, Google, Alexa are all third-party services." |

### Learning Objectives
- Build 4 working agent skills
- Internalize the DOE pattern through repetition
- Connect to real external services
- See DeskMochi as a practical daily tool

### Pacing Note
> Each skill follows the exact same pattern: (1) Write directive, (2) Generate/write script, (3) Test, (4) See it in your interface (dashboard or DeskMochi). By Skill 3, the student should recognize the pattern and it should feel natural. Both tracks are doing the exact same work — only the output surface differs.

### Skill 1: Recipe to Spreadsheet (~8 min)

**The ask:** "Find me a butter chicken recipe and save it to a spreadsheet"

**Step 1 — Directive** (`directives/recipe_to_sheet.md`):
```markdown
# Recipe to Spreadsheet

## Goal
Find a recipe by name, extract ingredients and steps, save to a Google Sheet.

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| Recipe name | Yes | e.g., "butter chicken", "pasta carbonara" |
| Sheet ID | Yes | Google Sheet to write to |

## Tools/Scripts
- execution/web_research.py — search the web for recipe data
- execution/append_to_sheet.py — write rows to a Google Sheet
  - Requires: Google OAuth (credentials.json)

## Workflow
1. Search for the recipe using web_research.py
2. Extract: dish name, ingredients list, step-by-step instructions
3. Format as rows: column A = ingredient/step, column B = quantity/detail
4. Append to the Google Sheet
5. Return: "Recipe saved! {sheet_url}"

## Edge Cases
- If recipe not found, suggest similar recipes
- If Google Sheet auth fails, tell user to re-run OAuth setup
```

**Step 2 — Script generation:** Show Copilot/server creating `execution/get_recipe.py` or using existing `web_research.py`

**Step 3 — Test:**
- "Find me a butter chicken recipe and save it to my spreadsheet"
- Show the Google Sheet populating with ingredients and steps

**Step 4 — Interface output:**
- **🖥️ Dashboard:** "Recipe saved!" notification in the panel + link to the Google Sheet
- **🤖 DeskMochi:** Display shows "✅ Recipe saved!" / Speaker says "Your butter chicken recipe is in Google Sheets!"

**Teaching moment:** "Notice the pattern? Directive → Script → Test → See the result. Every skill follows this. The interface doesn't change the work — it just changes where you see the celebration."

### Skill 2: Send a WhatsApp Message (~8 min)

**The ask:** "Send Priya a WhatsApp saying I'll be 15 minutes late"

**Step 1 — Directive** (`directives/send_whatsapp.md`):
```markdown
# Send WhatsApp Message

## Goal
Send a WhatsApp message to a contact via an API service.

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| Contact | Yes | Name or phone number |
| Message | Yes | What to say |

## Tools/Scripts
- execution/send_whatsapp.py — sends via Twilio/Green API
  - Requires: WHATSAPP_API_KEY, WHATSAPP_PHONE_ID in .env

## Workflow
1. Resolve contact name to phone number (from contacts.json or ask user)
2. Compose message
3. Send via WhatsApp API
4. Confirm delivery status
5. Return: "Message sent to {contact}!"

## Edge Cases
- Contact not found → ask user for phone number
- API failure → retry once, then report error
- Requires confirmation before sending (approval gate)
```

**Step 2 — Script:** `execution/send_whatsapp.py` using Twilio WhatsApp API or Green API

**Step 3 — Test and DeskMochi response**

**Teaching moment:** "This skill has an approval gate — DeskMochi asks 'Send to Priya: I'll be 15 minutes late. OK?' before sending. That's the human-in-the-loop pattern."

### Skill 3: Home Automation — Turn on a Light (~7 min)

**The ask:** "Turn on the living room light"

**Step 1 — Directive** (`directives/smart_home.md`):
```markdown
# Smart Home Control

## Goal
Control smart home devices (lights, switches, etc.)

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| Device | Yes | Device name (e.g., "living room light") |
| Action | Yes | What to do (on, off, brightness, color) |

## Tools/Scripts
- execution/smart_home.py — controls via Home Assistant REST API
  - Requires: HOME_ASSISTANT_URL, HOME_ASSISTANT_TOKEN in .env
  - Alternative: Alexa Smart Home API via skill invocation

## Workflow
1. Map device name to entity ID (from device_map.json)
2. Send command via Home Assistant API
3. Confirm state change
4. Return: "{device} is now {state}"
```

**Step 2 — Script:** calls Home Assistant's REST API (or Alexa API)

**Step 3 — Test:** "Turn on the living room light" → light turns on → DeskMochi shows 💡

**Teaching moment:** "This is the real power of agents — they bridge the digital and physical world. DeskMochi just controlled a real light in your house with a voice command."

### Skill 4: Morning Briefing (Chained Directive) (~8 min)

**The ask:** "Give me my morning briefing"

**This is special — it chains multiple skills together:**

**Step 1 — Directive** (`directives/morning_briefing.md`):
```markdown
# Morning Briefing

## Goal
Deliver a personalized morning briefing combining weather, calendar, and news.

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| City | No | Defaults to home city from memory |

## Tools/Scripts
- execution/get_weather.py — weather data
- execution/get_calendar.py — today's calendar events (Google Calendar API)
- execution/get_news.py — top headlines (News API)

## Workflow
1. Run all three scripts in parallel:
   - get_weather.py --city "{city}"
   - get_calendar.py --date "today"
   - get_news.py --category "technology" --limit 3
2. Combine results into a briefing:
   - "Good morning! It's {temp}°C and {condition}."
   - "You have {count} events today. First up: {event} at {time}."
   - "Top headlines: {headline1}, {headline2}, {headline3}."
3. Send full briefing to DeskMochi

## Edge Cases
- Calendar API not configured → skip calendar section
- News API down → skip news, mention it
```

**Step 2 — Test:** "Good morning! Give me my briefing"

**Step 3 — DeskMochi reads the whole briefing aloud while cycling through sections on display**

**Teaching moment:** "This is why the framework matters. You didn't write one giant script. You composed three small skills into a pipeline. Each one was already tested and working. That's the power of DOE — small, reliable pieces that combine into something powerful."

### Video 7 Key Takeaway
> Every skill follows the same pattern: directive → script → test → see the result. You built 4 real skills in 30 minutes. The pattern is the superpower. Both the browser dashboard and DeskMochi hardware show the same results — the intelligence and the work are identical.

---

## Video 8: Cloud Brains, Model Showdown & More Skills

> **Both tracks.** All content in this video is hardware-independent. Cloud LLM providers, model comparisons, and the Opus 4.6 demo work identically on both tracks.

**Duration:** ~30-35 min
**Type:** Live API setup + model comparison demo + skill building + brainstorm
**Goal:** Connect DeskMochi to cloud LLMs via Groq's free tier, show how model choice dramatically changes capabilities, and demonstrate a complex task with Claude Opus 4.6.

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **Rate Limiting** | When API rejects a call | "APIs limit how many times you can call per minute. Hit the limit = temporarily rejected." |
| **API-based LLM** | Switching to Groq | "An LLM running on someone else's servers. You send text, they send results. Fast but needs internet." |
| **Model Swapping** | Changing one line in .env | "Switching the AI brain your agent uses. Same directives, same scripts — different brain, different results." |
| **Inference** | When comparing model speeds | "The act of the LLM generating output. 'Running inference' = the model is thinking and producing tokens." |

### Learning Objectives
- Set up Groq's free tier and connect it to DeskMochi
- Understand that the same code works with any LLM provider (OpenAI, Anthropic, etc.)
- See first-hand how model choice affects speed, quality, context length, and capabilities
- Witness a complex multi-step task that only a frontier model can handle well
- Build more skills and generate ideas for custom agents

### Section 8.1 — Connecting to the Cloud: Groq Free Tier (~6 min)

**What to cover:**
- "So far, DeskMochi's brain has been running locally on your PC. That's great for privacy and cost. But what happens when you need a bigger brain?"
- Enter **Groq** — a free cloud LLM service:
  - Free tier: no credit card needed
  - Absurdly fast: 500+ tokens/second (vs 15-30 local)
  - Multiple models available (Llama, Mixtral, Gemma)
  - Same OpenAI-compatible API format — code that works with Groq works with OpenAI/Anthropic too

**Live setup (show every click):**
1. Go to [groq.com](https://groq.com) → Sign up (free, no credit card)
2. Go to API Keys → Create new key → Copy it
3. Open `.env` → Change two lines:
   ```
   LLM_PROVIDER=groq
   LLM_MODEL=llama-3.3-70b-versatile
   GROQ_API_KEY=gsk_your_key_here
   ```
4. Restart the server: `python execution/local_server.py`
5. Terminal shows: "Server running on localhost:8000 — using Groq (llama-3.3-70b-versatile)"

**Test it immediately:**
- Press DeskMochi button → "What's the weather in Hyderabad?"
- Response comes back *almost instantly* — noticeably faster than local
- "Same directive, same script, same DeskMochi — but the brain is now in the cloud, running on specialized hardware that generates 500 tokens per second."

**Key teaching moment: Provider portability**
- Show the `.env` file: "See how we only changed `LLM_PROVIDER`, `LLM_MODEL`, and added `GROQ_API_KEY`? That's it."
- "This exact same pattern works for ANY provider:"
  ```
  # Switch to OpenAI:
  LLM_PROVIDER=openai
  LLM_MODEL=gpt-4o
  OPENAI_API_KEY=sk-...

  # Switch to Anthropic:
  LLM_PROVIDER=anthropic
  LLM_MODEL=claude-sonnet-4-20250514
  ANTHROPIC_API_KEY=sk-ant-...

  # Switch back to local:
  LLM_PROVIDER=ollama
  LLM_MODEL=gemma3
  ```
- "Your directives don't change. Your scripts don't change. Your DeskMochi doesn't change. Only the brain swaps. That's the power of the DOE architecture — the intelligence layer is pluggable."

### Section 8.2 — The Model Showdown: Not All Brains Are Equal (~8 min)

> This is a critical teaching moment. Students need to viscerally understand that model choice is the single most impactful decision in agent design.

**What to cover:**
- "Switching models isn't like switching brands of bottled water. It's like switching between a bicycle, a car, and a jet. They all get you there — but the experience is completely different."

**Live side-by-side comparison — same prompt, different models:**

Prompt: *"I have a meeting with a Japanese client tomorrow. Draft a short email confirming the meeting, include a culturally appropriate greeting, suggest we meet at a nearby restaurant, and recommend a good time considering Tokyo is UTC+9 and I'm in Hyderabad (UTC+5:30)."*

| Dimension | Gemma 3 (local, 4B) | Llama 3.3 70B (Groq free) | Claude Opus 4.6 (Anthropic) |
|-----------|---------------------|---------------------------|----------------------------|
| **Speed** | ~30 tok/s | ~500 tok/s | ~40 tok/s |
| **Response time** | ~4 seconds | ~0.5 seconds | ~8 seconds |
| **Quality** | Basic email, generic greeting | Good email, gets timezone math right | Exceptional — nuanced cultural awareness, perfect timezone handling, suggests specific cuisine |
| **Context handling** | Handles this fine | Handles this fine | Could handle this with 50 pages of context attached |
| **Cost** | $0 | $0 (free tier) | ~$0.02 for this request |

**Show the actual outputs side by side on screen.** Let the student see the quality gap.

**Then show the comparison table that matters for agent design:**

| What You're Choosing | Small Local Model | Mid-Tier Cloud (Groq Free) | Frontier Model (Opus 4.6) |
|---------------------|-------------------|---------------------------|---------------------------|
| **Speed** | 15-40 tok/s | 500+ tok/s | 30-50 tok/s |
| **Context window** | 4K-8K tokens | 8K-128K tokens | 200K tokens |
| **Reasoning** | Simple decisions | Multi-step reasoning | Complex analysis, long chains of thought |
| **Cost** | $0 forever | $0 (free tier) / cheap | $15/M input tokens |
| **Privacy** | 100% local | Data sent to cloud | Data sent to cloud |
| **Internet needed** | No | Yes | Yes |
| **Good for** | Weather, timers, simple routing | Most DeskMochi skills, summarization | Business plans, legal analysis, research synthesis, multi-document reasoning |

**Key takeaway for students:**
- "There's no single 'best' model. There's the best model *for the job*."
- "DeskMochi checking the weather? Use local Gemma — instant, free, private."
- "DeskMochi summarizing 10 emails? Use Groq free tier — fast and smart enough."
- "DeskMochi analyzing a 50-page contract? You want Opus 4.6 — it can hold the entire document in context and reason about every clause."
- "The DOE framework makes this easy: same directive, same scripts, swap the brain in `.env`."

**What changes between models (make this visceral):**
- **Hallucination rate drops** as models get larger — a 4B model might hallucinate a function name, a 70B model rarely will, Opus 4.6 almost never does for simple tasks
- **Context window** is the biggest practical difference — small models forget mid-conversation, frontier models can read a whole book
- **Speed vs quality** is always a tradeoff — Groq is 10x faster than Opus but Opus handles complex reasoning better
- **Instruction following** improves dramatically — frontier models follow complex multi-step directives precisely, smaller models sometimes skip steps or misinterpret edge cases

### Section 8.3 — The Opus 4.6 Demo: When You Need a Bigger Brain (~7 min)

> This demo shows a task that would be painfully complex without a frontier model — and trivial with one. The contrast should be dramatic.

**The task: Full Business Analysis from a Raw Idea**

*"DeskMochi, I'm thinking about starting a weekend cloud kitchen in Hyderabad selling Korean-Indian fusion food. Analyze this idea: target market, competition, startup costs, legal requirements, revenue projections for year one, and top 3 risks. Put it all in a Google Sheet with multiple tabs."*

**Why this needs a frontier model:**
- It requires understanding TWO cuisines + local Hyderabad context
- It needs to reason about economics, regulations, and market dynamics simultaneously
- It must produce structured, multi-tab output (not just freeform text)
- A small model would hallucinate market data or produce vague, generic analysis
- The sheer length of the output (~3000-4000 tokens) plus the directive + context requires a large context window

**Live demo — switch to Opus 4.6:**
```bash
# In .env:
LLM_PROVIDER=anthropic
LLM_MODEL=claude-opus-4-20250514
ANTHROPIC_API_KEY=sk-ant-...
```
- Restart server → Ask DeskMochi the question
- Watch the server logs:
  ```
  [20:15:01] Request: "I'm thinking about starting a weekend cloud kitchen..."
  [20:15:01] Loading directive: business_analysis.md
  [20:15:02] LLM (claude-opus-4-20250514 @ 38 tok/s) reasoning...
  [20:15:15] LLM decided: run web_research.py --query "cloud kitchen market Hyderabad 2026"
  [20:15:18] Script returned: {market_data...}
  [20:15:19] LLM decided: run web_research.py --query "FSSAI cloud kitchen license requirements"
  [20:15:22] Script returned: {legal_data...}
  [20:15:23] LLM analyzing all data, generating 6-tab spreadsheet structure...
  [20:15:38] LLM decided: run append_to_sheet.py (6 tabs, 47 rows total)
  [20:15:41] Sheet created: https://docs.google.com/spreadsheets/d/...
  [20:15:41] Sent to DeskMochi
  ```
- DeskMochi: "Your business analysis is ready! I created a spreadsheet with 6 tabs: Market Overview, Competition, Startup Costs, Legal Requirements, Revenue Projections, and Risk Analysis."
- Open the Google Sheet on screen → walk through the tabs. The analysis should be **impressively specific** to Hyderabad + Korean-Indian fusion.

**Then try the same task with the local Gemma 3 model:**
- Switch back to `LLM_PROVIDER=ollama` → restart → ask the same question
- "Watch what happens with a smaller brain..."
- The local model produces a generic, shorter, less structured response — probably misses the multi-tab structure, hallucinates some market numbers, skips legal specifics
- "See the difference? Same directive, same scripts. Different brain, vastly different result."

**Teaching moment:**
- "This is why model choice matters. For your daily DeskMochi tasks — weather, timers, recipes — local is perfect. For complex business analysis, research, or anything requiring deep reasoning — you bring in the big guns."
- "And because our DOE framework separates the brain from the hands, swapping takes 10 seconds. You're not rewriting anything."
- "Groq's free tier with Llama 3.3 70B sits in the sweet spot for most tasks — free, fast, and smart enough. Reserve Opus 4.6 for the tasks that truly need it."
- Cost reality: "That entire business analysis cost about $0.40 with Opus 4.6. The same task with Groq free tier: $0. With local: $0. Pick based on the job."

### Skill 5: Email Summarizer (~4 min)

**The ask:** "Summarize my unread emails"

**Directive:** fetch unread emails via Gmail API → LLM summarizes the batch → DeskMochi reads summary

**What this demonstrates:**
- LLM doing the "thinking" (summarization) — this is a valid use of the AI brain
- Script doing the "doing" (Gmail API call) — deterministic
- The distinction: scripts fetch data, the LLM interprets it
- Good fit for Groq free tier: fast, free, handles summarization well

**DeskMochi output:**
- Display: scrollable list of 3-5 email summaries
- Speaker: "You have 7 unread emails. Three are from your team about the project deadline. Two are newsletters. One is from Amazon about your order."

### Skill 6: Price Tracker / Shopping Assistant (~4 min)

**The ask:** "Track the price of PlayStation 5 on Amazon"

**Directive:** scrape product page → extract price → save to sheet → compare with previous prices → alert if it drops

**What this demonstrates:**
- Multi-step pipelines
- Persistent data (price history in Google Sheet)
- Conditional logic ("only alert me if price drops below ₹40,000")
- Scheduled tasks (check daily)
- Doesn't even need a powerful model — local Gemma handles this fine since the LLM only decides "run the price script," the logic is in the script

### Skill 7: Focus Timer / Pomodoro (~3 min)

**The ask:** "Start a 25-minute focus timer"

**What this demonstrates:**
- Not everything needs an API! This is purely local.
- DeskMochi shows a countdown on display
- Plays a gentle sound when done
- No LLM needed — direct ESP32 firmware feature
- "Agents aren't always about AI. Sometimes a simple timer on your desk companion is the most useful thing."

### Section 8.7 — Tool Registry: Discovering What's Available (~3 min)

**What to cover:**
- Show the tool registry command:
  ```
  python execution/tool_registry.py find "spreadsheet"
  python execution/tool_registry.py list
  python execution/tool_registry.py show append_to_sheet
  ```
- "Before building a new skill, check what tools already exist. You might not need to write a new script at all."
- Walk through 2-3 tool schemas to show what's available

### Section 8.8 — Brainstorm: What Will YOU Build? (~3 min)

**What to show on screen — an idea grid to inspire:**

| Category | Agent Skill Ideas | Suggested Model |
|----------|-------------------|-----------------|
| **Productivity** | Calendar reminders, email drafts, meeting summaries, to-do lists | Groq free / Local |
| **Finance** | Expense tracking, invoice generation, stock/crypto price alerts | Groq free / Local |
| **Health** | Water reminders, medication alerts, workout logging, step count | Local |
| **Social** | Birthday reminders, auto-reply on messages, social media posting | Groq free |
| **Home** | Grocery lists from recipes, appliance control, energy monitoring | Local |
| **Learning** | Flashcard quizzer, article summarizer, language practice | Groq free |
| **Business** | Lead tracking, report generation, CRM updates, invoice creation | Groq free / Opus |
| **Research** | Literature review, market analysis, competitive intelligence | Opus 4.6 |
| **Fun** | Joke of the day, trivia quizzer, random fact, fortune cookie | Local |
| **Communication** | Quick translator, voice notes to text, meeting scheduler | Groq free |

**Key question to ask the student:**
- "What's one thing you do every day that's repetitive and boring? That's your first agent."
- "How complex is the thinking involved? That tells you which model to use."

### Section 8.9 — The Model Selection Rule of Thumb (~2 min)

**Show on screen:**
```
┌────────────────────────────────────────────────────────────┐
│         WHICH BRAIN SHOULD MY AGENT USE?                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Does the task need reasoning?                             │
│  ├── No (timers, simple lookups)  → No LLM / Local tiny   │
│  └── Yes                                                   │
│      ├── Simple (pick a script, format text) → Local Gemma │
│      ├── Medium (summarize, compose, multi-step) → Groq   │
│      └── Complex (analyze, plan, long docs)  → Opus 4.6   │
│                                                            │
│  Rule: Start local. Upgrade only when quality demands it.  │
│  The DOE framework makes switching instant.                │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Video 8 Key Takeaway
> Not all AI brains are equal. Groq's free tier gives you fast, capable cloud AI for $0. The same code works with OpenAI, Anthropic, or any provider — just change `.env`. Match the model to the task: local for simple, Groq for most things, Opus 4.6 when you need the best. The DOE framework makes switching instant.

---

## Video 9: Advanced Patterns — Memory, Pipelines, and Self-Healing

> **Both tracks.** Memory, pipelines, self-healing, and approval gates are all software patterns — they work identically regardless of the output interface.

**Duration:** ~22-25 min
**Type:** Screen share + architecture diagrams
**Goal:** Level up from "it works" to "it works reliably, remembers things, and handles complex tasks."

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **Database** | Agent memory | "A structured way to store and search data permanently. Like a filing cabinet your agent can search instantly." |
| **SQLite** | memory_db.py | "A database in a single file. No installation needed. Perfect for local agents." |
| **DAG (Directed Acyclic Graph)** | Task graphs | "Steps with arrows showing order: A → B → C. 'Must happen before.' No loops allowed." |
| **Caching** | Self-healing fallback | "Saving a copy of data so you don't need to fetch it again. Backup plan when APIs fail." |
| **Concurrency / Parallelism** | Parallel pipelines | "Running multiple things simultaneously. Fetch weather AND calendar at the same time." |

### Learning Objectives
- Understand agent memory and why it matters
- Build a multi-step pipeline with task graphs
- Implement self-healing (automatic error recovery)
- Understand approval gates for risky actions

### Section 9.1 — Memory: Making DeskMochi Remember (~7 min)

**The problem:**
- "What's the weather in Hyderabad?" → Agent answers
- "What about tomorrow?" → Agent doesn't know which city you meant!
- Without memory, every conversation starts from zero

**The solution — memory_db.py:**
- DeskMochi has a tiny database (SQLite) that stores two types of memory:
  - **Short-term memory:** Current conversation context (disappears after the task)
  - **Long-term memory:** Facts, preferences, lessons learned (permanent)
- Demo:
  - Ask about weather in Hyderabad → agent stores "current_city = Hyderabad" in short-term memory
  - Ask "what about tomorrow?" → agent reads short-term memory → knows you mean Hyderabad
  - Over time: agent learns "user's home city is Hyderabad" → stores in long-term memory → defaults to Hyderabad

**Analogy:**
- Short-term = sticky notes on your desk (temporary, task-specific)
- Long-term = filing cabinet (permanent, always accessible)

**Commands shown:**
```bash
python execution/memory_db.py search "weather"
python execution/memory_db.py add-fact "User lives in Hyderabad" --category preferences
python execution/memory_db.py stm set "current_city" "Hyderabad"
```

### Section 9.2 — Pipelines: Multi-Step Task Graphs (~6 min)

**The problem:**
- Some tasks have many steps with dependencies
- Morning briefing: weather + calendar + news → combine → speak
- Some can run in parallel, some must wait

**The solution — task_graph.py:**
- Create a plan with steps and dependencies:
  ```
  python execution/task_graph.py create "Morning Briefing" \
    --step "weather:Get weather" \
    --step "calendar:Get calendar" \
    --step "news:Get headlines" \
    --step "combine:Combine results:weather,calendar,news" \
    --step "speak:Read briefing:combine"
  ```
- The graph:
  ```
  [weather] ──┐
  [calendar] ──┼──→ [combine] ──→ [speak]
  [news] ─────┘
  ```
- Weather, calendar, and news run in parallel (no dependencies on each other)
- Combine waits for all three to finish
- If news fails → combine skips it → briefing still works (degraded but functional)

**Demo:** Run the morning briefing via task graph, show the visual status:
```
[+] weather    Get weather          Done in 1.2s
[+] calendar   Get calendar         Done in 2.1s
[X] news       Get headlines        FAILED: API key expired
[+] combine    Combine results      Done in 0.5s (skipped news)
[+] speak      Read briefing        Done
```

### Section 9.3 — Self-Healing: Automatic Error Recovery (~5 min)

**The problem:**
- APIs go down. Rate limits are hit. Networks flake. Data comes back wrong.
- A fragile agent stops at the first error. A robust agent recovers.

**What self-healing looks like:**
1. **Retry with backoff:** API returns 429 (rate limit) → wait 2 seconds → try again → works
2. **Fallback to cache:** Weather API is down → serve last known weather → mention it's cached
3. **Graceful degradation:** News section fails → morning briefing still delivers weather + calendar
4. **Learning from failure:** Error is stored as a fact in memory → next time the directive knows about it

**Demo:** Simulate a weather API failure:
- DeskMochi asks for weather → API returns error
- Server log shows: "Weather API failed. Using cached data from 2 hours ago."
- DeskMochi says: "Based on earlier data, it's about 28°C in Hyderabad. Note: live weather is temporarily unavailable."
- Agent stores: `add-fact "OpenWeatherMap had a brief outage on March 17, used cached data" --category api_issues`

### Section 9.4 — Approval Gates: Safety for Risky Actions (~4 min)

**The problem:**
- You don't want DeskMochi sending WhatsApp messages or spending money without asking
- "Order groceries" → what if it orders the wrong thing?

**The solution — confirm_action.py:**
- DeskMochi pauses before executing risky actions and asks for confirmation
- Display shows: "Send WhatsApp to Priya: 'I'll be 15 minutes late' — Confirm?"
- You press the button → "Confirmed" → message sends
- You press a different button → "Cancelled" → nothing happens

**Which actions need approval:**
- Sending messages (WhatsApp, email, SMS)
- Spending money (orders, API calls with significant cost)
- Modifying external data (updating shared spreadsheets, deleting files)
- Smart home actions that affect safety (locking doors, disabling alarms)

**Which actions auto-approve:**
- Reading data (weather, news, calendar)
- Local operations (timers, display changes)
- Calculations and formatting

### Video 9 Key Takeaway
> Memory makes DeskMochi contextual. Pipelines make it powerful. Self-healing makes it reliable. Approval gates make it safe. These four patterns are what separate a demo from a real tool.

---

## Video 10: Build Your Own Agent — Graduation Project

> **Both tracks.** The graduation project is identical for both. Software Track students demo in the browser dashboard. DeskMochi Track students can connect to the physical device. Either way, it's the same agent, same skill, same framework.

**Duration:** ~28-30 min
**Type:** Guided project + course wrap-up
**Goal:** Students apply everything they've learned to build a complete, original agent skill.

### Learning Objectives
- Apply the DOE pattern independently to a self-chosen task
- Build a skill end-to-end without hand-holding
- Prove to yourself that you understand the framework
- Graduate with confidence to build future agents alone

### Section 10.1 — The Challenge (~3 min)

**What to say:**
- "You've watched me build 7+ skills. Now it's your turn."
- "Pick ONE task from the brainstorm list (Video 8) or invent your own."
- "Build it end-to-end using the DOE pattern. You have 20 minutes."
- Suggested options (pick any):
  - **Option A:** Expense tracker — "Log ₹500 for lunch" → adds to spreadsheet with date + category
  - **Option B:** Daily quote — DeskMochi says an inspiring quote each morning
  - **Option C:** Quick translator — "How do you say 'thank you' in Japanese?" → display + audio

### Section 10.2 — Guided Build (Student Perspective) (~18 min)

**What to show:** Walk through the build as if you're a student doing it for the first time.

**Step 1: Define the task clearly (~2 min)**
- "What exactly should happen when I ask DeskMochi to do this?"
- Write the one-sentence goal: "When I say 'log expense ₹500 for lunch', it should add a row to my expenses spreadsheet with today's date, the amount, and the category."

**Step 2: Write the directive (~4 min)**
- Create `directives/log_expense.md`
- Write: Goal, Inputs, Tools, Workflow, Edge Cases
- "This should take 3-5 minutes. If it takes longer, the task is too complex — break it down."

**Step 3: Identify what you need (~2 min)**
- Do I need a new script? → Check tool registry: `python execution/tool_registry.py find "sheet"`
- Found: `append_to_sheet.py` — already exists!
- Do I need a new API key? → Already have Google Sheets configured
- "Sometimes building a new skill means writing zero new code — just a new directive that combines existing tools."

**Step 4: Create/generate the script (if needed) (~4 min)**
- If a new script is needed: have Copilot or the server generate it
- Walk through verification: does the script accept the right arguments? Does it handle errors?

**Step 5: Test end-to-end (~3 min)**
- Run via Copilot or server
- Verify the result (check the spreadsheet)
- Try an edge case (negative number, missing category)

**Step 6: Connect to DeskMochi (~2 min)**
- Test with the physical device
- Display + speaker confirmation

**Step 7: Self-anneal (~1 min)**
- Trigger an error intentionally
- Fix it, update the directive
- "Your system is now stronger."

### Section 10.3 — The DOE Cheatsheet (~3 min)

**Show on screen and explain:**
```
┌─────────────────────────────────────────────────────────┐
│              DOE FRAMEWORK CHEATSHEET                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  I want to...                    → I should...          │
│  ────────────────────────────────────────────────        │
│  Tell the agent what to do       → Write a directive    │
│                                    (directives/*.md)    │
│  Make it do something reliably   → Write/find a script  │
│                                    (execution/*.py)     │
│  Connect to a new service        → Get API key → .env   │
│  Remember things between tasks   → Use memory system    │
│  Chain multiple steps            → Use task graphs      │
│  Protect risky actions           → Add approval gates   │
│  Fix a bug permanently           → Fix → Test → Update  │
│                                    directive             │
│  Find what tools exist           → tool_registry.py     │
│                                    find "keyword"       │
│  Track what happened             → execution_trace.py   │
│                                                         │
│  THE GOLDEN RULES:                                      │
│  1. AI decides, scripts execute. Never mix.             │
│  2. Directives are living documents. Update them.       │
│  3. One script, one job. Keep it small.                 │
│  4. Self-anneal every time. Fix → Test → Update.        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Section 10.4 — Where to Go From Here (~3 min)

**What to cover:**
- **Share your DeskMochi build** — post photos, videos, skills in the community
- **Cloud deployment** — run the server on a cloud VM for 24/7 availability from anywhere
- **MCP servers** — plug-and-play tool connections without writing scripts
- **Multiple agents** — run specialized agents for different domains (work, home, health)
- **The adjacent possible** — each skill you build makes the next one easier. After 10 skills, you'll build new ones in minutes.

### Section 10.5 — Closing (~2 min)

**What to say:**
- "You started this course asking 'what is an AI agent?'"
- "Now you have an AI agent — on your desk, in your browser, or both — that checks weather, creates spreadsheets, sends WhatsApp messages, controls your smart home, and gives you morning briefings."
- "If you have DeskMochi: you have a physical companion that speaks, displays, and listens. If you don't: you have a browser interface that does the same work. The agent underneath is the same."
- "More importantly, you have a *framework*. DOE works for any agent — not just DeskMochi."
- "The directive tells the AI what. Scripts tell it how. The AI connects the two. That's it."
- "Every automation you'll ever build follows this pattern. You now have the pattern."
- "Go build something cool."

### Video 10 Key Takeaway
> You don't need to be a programmer to build agents. You don't need specific hardware. You need to be clear about what you want (directive), let the AI figure out how (orchestration), and give it reliable tools (execution). That's DOE. Now go build.

---

## Appendix A: Complete Concept Glossary

Every technical concept introduced in the course, organized by first appearance.

### Video 0 — Foundations (13 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 1 | Software vs Hardware | Software = instructions. Hardware = physical device. |
| 2 | Program / Script | A text file with step-by-step instructions for a computer. |
| 3 | Server | A program that waits for requests and responds. Like a receptionist. |
| 4 | Client | The thing that sends requests to a server. DeskMochi is a client. |
| 5 | Client-Server Architecture | Client asks → Server answers. The universal pattern. |
| 6 | Internet | Computers sending messages using agreed-upon rules. |
| 7 | API | How two programs talk. The waiter between you and the kitchen. |
| 8 | API Key | A password identifying you to a service. |
| 9 | JSON | Universal structured data format. Labeled lists and values. |
| 10 | File / File Path | A data container + its address on your computer. |
| 11 | Folder / Directory | A container for files. Folders in folders = hierarchy. |
| 12 | File Extension | Letters after the dot: `.py` = Python, `.md` = Markdown. |
| 13 | Plain Text vs Rich Text | Plain = just characters. Rich = formatted (Word docs). Code is plain text. |

### Video 1 — AI Agents & How LLMs Work (8 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 14 | LLM (Large Language Model) | An AI brain that reads, reasons, and generates text. |
| 15 | Prompt | The text you send to an LLM to get a response. |
| 16 | Token | How LLMs measure text. ~1 token ≈ ¾ word. Providers charge per token. |
| 17 | Next-Token Prediction | How LLMs generate text: predict the most likely next word, one at a time. |
| 18 | Hallucination | When an LLM confidently generates incorrect information. |
| 19 | Context Length / Context Window | Maximum text an LLM can "see" at once. Like a desk that only fits so many pages. |
| 20 | Temperature (LLM) | Controls output randomness. Low = predictable. High = creative & risky. |
| 21 | Tokens per Second (Inference Speed) | How fast the LLM generates text. More tok/s = faster responses. |

### Video 2 — DOE Framework (4 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 22 | Deterministic vs Probabilistic | Same input → same output (calculator) vs slightly different (LLM). |
| 23 | SOP (Standard Operating Procedure) | Step-by-step task checklist. Directives are SOPs. |
| 24 | Framework | A reusable pattern for solving a class of problems. |
| 25 | Markdown | Simple text formatting: `#` = heading, `**` = bold, `-` = bullet. |

### Video 3 — Hardware (6 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 26 | Microcontroller (ESP32) | Tiny computer with WiFi. Controls displays and speakers. |
| 27 | Firmware | Software flashed onto hardware. Runs every time the device powers on. |
| 28 | WiFi (device perspective) | How ESP32 finds your PC on the same network. |
| 29 | WebSocket | Persistent two-way connection. Like a phone call that doesn't hang up. |
| 30 | Serial / USB Communication | How your PC talks to ESP32 through the USB cable. |
| 31 | TTS (Text-to-Speech) | Converting text to spoken audio. |

### Video 4 — Development Environment (14 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 32 | IDE / Code Editor | Fancy text editor for code. VS Code is ours. |
| 33 | Terminal / Command Line | Text interface for typing commands. Bottom panel in VS Code. |
| 34 | Command | An instruction typed into the terminal. |
| 35 | Command-Line Argument | Extra info passed to a command: `--city "Hyderabad"`. |
| 36 | Python | Programming language. You run Python files; AI writes them. |
| 37 | pip / Package Manager | Downloads code libraries. App store for Python. |
| 38 | Library / Package | Code someone else wrote that you reuse. |
| 39 | requirements.txt | Shopping list of packages. One command installs all. |
| 40 | .env File | Secret file storing API keys. Never share it. |
| 41 | Environment Variable | A named value in memory. Scripts read it by name. |
| 42 | Virtual Environment (venv) | Isolated package bubble per project. |
| 43 | Git | Tracks file changes over time. |
| 44 | GitHub | Website that stores Git projects online. |
| 45 | Cloning a Repository | Downloading a project from GitHub. One command. |

### Video 5-6 — Agent Building + Server (9 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 46 | HTTP (GET, POST) | Web language. GET = give me data. POST = here's data. |
| 47 | URL / Endpoint | Address of a specific API function. |
| 48 | REST | Conventions for API design. URLs for resources, GET to read, POST to create. |
| 49 | Status Code | API's one-word answer. 200 = OK. 404 = not found. 500 = broken. |
| 50 | localhost | Your own computer as a network address. |
| 51 | Port | Numbered door. Different services use different ports. |
| 52 | FastAPI | Python package for building servers easily. |
| 53 | Agentic Loop | LLM reads → decides tool → script runs → result → repeat. |
| 54 | Local Model | An LLM running entirely on your PC. No internet, no cost, full privacy. |

### Video 7-8 — External Services + Cloud LLMs (8 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 55 | OAuth | Secure login flow. Grant permission once via browser. |
| 56 | Webhook | Reverse API. Service pushes data to you when events happen. |
| 57 | Spreadsheet ID | Unique code in a Google Sheet URL identifying which sheet. |
| 58 | Third-Party Service | External product whose API you call (Twilio, Google, etc.). |
| 59 | Rate Limiting | API limits on calls per minute/day. Hit it = temporarily rejected. |
| 60 | API-based LLM | An LLM on someone else's servers. Send text, get results. Needs internet. |
| 61 | Model Swapping | Switching the AI brain. Same directives, same scripts — different model. |
| 62 | Inference | The act of the LLM generating output. "Running inference" = the model is thinking. |

### Video 9 — Advanced Patterns (5 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 63 | Database | Structured permanent data storage. Agent memory lives here. |
| 64 | SQLite | Database in a single file. No setup needed. |
| 65 | DAG (Directed Acyclic Graph) | Steps with arrows showing order. No loops. |
| 66 | Caching | Saving data copies as backup when live source fails. |
| 67 | Concurrency / Parallelism | Running multiple tasks at the same time. |

**Total: 67 concepts** — introduced gradually across 10 videos, never more than 14 in a single video (and that's Video 4, which is the setup video where concepts appear naturally as you install things).

---

## Appendix B: Glossary Card System

For video production: display a 5-second on-screen card the FIRST time any concept is spoken aloud.

### Card Template
```
┌──────────────────────────────────┐
│  📖 CONCEPT NAME                 │
│                                  │
│  One-sentence definition.        │
│  Simple analogy if applicable.   │
│                                  │
└──────────────────────────────────┘
```

### Production Rules
1. Show the card the FIRST time the term is spoken — never again
2. Card appears in the corner (not blocking main content)
3. Duration: 5 seconds
4. Don't pause the narration — the card is supplementary
5. Use a consistent design throughout the course
6. Include a small icon per category (🔧 tools, 🌐 internet, 🧠 AI, 🔌 hardware)

### Downloadable Cheatsheet

Package all 67 concepts as a printable 2-page PDF:
- Page 1: Concepts 1-34 (Foundations through Development)
- Page 2: Concepts 35-67 (Building through Advanced)
- Include in course materials download
- Students can keep it on their desk next to DeskMochi

---

## Appendix C: Course Summary Table

| Video | Title | Duration | Track | Skills Built | Concepts Introduced | Cumulative Concepts |
|-------|-------|----------|-------|-------------|-------------------|-------------------|
| 0 | The Language of Tech | ~22 min | Both | — | 13 | 13 |
| 1 | What Is an AI Agent? + How LLMs Work | ~30 min | Both | — (3 demos) | 8 | 21 |
| 2 | The DOE Framework | ~20 min | Both | — | 4 | 25 |
| 3 | Building DeskMochi | ~18 min | 🤖 Only | Hardware assembled | 6 | 31 |
| 4 | Setting Up Your Workshop | ~24 min | Both | Dev environment + dashboard | 14 | 45 |
| 5 | Your First Agent | ~26 min | Both | Weather skill | 4 | 49 |
| 6 | The Local Server | ~24 min | Both | Standalone server + local AI | 5 | 54 |
| 7 | Real-World Skills | ~32 min | Both | Recipe, WhatsApp, Alexa, Briefing | 4 | 58 |
| 8 | Cloud Brains + Model Showdown | ~32 min | Both | Groq API, Opus demo, Email, Price, Timer | 4 | 62 |
| 9 | Advanced Patterns | ~24 min | Both | Memory, Pipelines, Self-Healing | 5 | 67 |
| 10 | Build Your Own | ~28 min | Both | Custom graduation project | 0 | 67 |
| | **TOTAL (Software Track)** | **~4.4 hrs** | **🖥️** | **10+ working skills** | **67 concepts** | |
| | **TOTAL (DeskMochi Track)** | **~4.7 hrs** | **🤖** | **10+ working skills + hardware** | **67 concepts** | |

---

## Production Notes

### Required Course Materials (to create before filming)

**Core (Both Tracks)**
- [ ] `execution/local_server.py` — FastAPI + WebSocket + agentic loop (provider-agnostic: Ollama/Groq/OpenAI/Anthropic)
- [ ] `execution/pipeline_runner.py` — provider-agnostic LLM orchestrator
- [ ] `execution/get_weather.py` — OpenWeatherMap wrapper
- [ ] `execution/send_whatsapp.py` — Twilio/Green API wrapper
- [ ] `execution/smart_home.py` — Home Assistant API wrapper
- [ ] `execution/get_calendar.py` — Google Calendar API wrapper
- [ ] `execution/get_news.py` — News API wrapper
- [ ] `execution/business_analysis.py` — Multi-tab spreadsheet generator for Opus 4.6 demo
- [ ] `directives/` for all 10+ skills (including `business_analysis.md` for Opus demo)
- [ ] `dashboard/index.html` — Local web dashboard (Software Track interface; serves as "virtual DeskMochi")
  - Simple chat panel (input box + response area)
  - Tools/skills sidebar
  - Auto-connects to `local_server.py` via WebSocket or HTTP polling
  - Mobile-friendly — works on phone browser too
- [ ] Groq free tier account + API key for Video 8 demo
- [ ] Anthropic API key for Claude Opus 4.6 demo (Video 8)
- [ ] Pre-recorded side-by-side model comparison outputs for Video 8 Section 8.2
- [ ] `device_map.json` — smart home device mapping
- [ ] `contacts.json` — phone contacts mapping
- [ ] Downloadable 2-page glossary cheatsheet (PDF)
- [ ] DOE Framework cheatsheet (1-page, PDF)
- [ ] Glossary card graphics (67 cards)

**DeskMochi Track Only (🤖)**
- [ ] ESP32 DeskMochi firmware (Arduino/PlatformIO project)
- [ ] Wiring diagram (Fritzing or similar)
- [ ] 3D print files or cardboard template for DeskMochi housing
- [ ] Parts list with buy links (~$20 BOM total)

### Video Production Order
Recommended filming order (not the release order):
1. Film Videos 0, 1, 2 first (talking head / diagrams — no code or hardware dependency)
2. Build `dashboard/index.html` and `local_server.py`, then film Videos 4, 5 (Software Track versions first — no hardware required)
3. Film Video 3 (hardware — independent, can be done any time)
4. Add 🤖 DeskMochi Track segments to Videos 4, 5 (pairing + device output)
5. Film Video 6 — both tracks (server works without hardware, just show dashboard version first, then add DeskMochi segment)
6. Film Video 7 (skills — need server + local model working; dashboard segment first, DeskMochi segment second for each skill)
7. Set up Groq free tier + Anthropic API key, then film Video 8 (fully hardware-independent)
8. Film Video 9 (advanced — needs skills + model swapping working; fully hardware-independent)
9. Film Video 10 last (wraps everything up; both tracks shown side by side in closing)

**Editing approach:** For each video that has hardware-specific segments, produce two edits:
- **Standard release** (both tracks interwoven): Keeps DeskMochi segments brief, notes they're optional, uses on-screen callout "🤖 DeskMochi Track" for hardware segments
- **Separate DeskMochi Track supplement** (optional): A short add-on video (~3-5 min) showing the DeskMochi-specific steps for each main video, distributed only to DeskMochi owners

---

## Appendix D: Interactive Modules (Brilliant-Style)

> **Purpose:** Brilliant.org-style interactive exercises that students complete in a web browser alongside each video. These reinforce concepts through hands-on manipulation rather than passive watching. Each module is self-contained and takes 3-8 minutes.

**Design Principles:**
- **No typing code** — use drag-and-drop, sliders, click-to-select, and fill-in-the-blank
- **Instant feedback** — every action shows immediate results (green checkmark, animated response, visual change)
- **Progressive disclosure** — start simple, add complexity one layer at a time
- **Fail safely** — wrong answers show helpful hints, never dead-ends
- **Mobile-friendly** — all modules work on phone/tablet for on-the-go learning

**Tech Stack Suggestion:** React + Framer Motion (or similar) for interactive components, deployed as a static site linked from each video description.

---

### Video 0 Modules — Foundations

#### Module 0.1: "Build a JSON Object" (Drag-and-Drop)
**Concept reinforced:** JSON structure
**How it works:**
- Screen shows a plain-English description: "A person named Ravi, age 25, who lives in Hyderabad and likes cricket and biryani"
- Student drags labeled tiles (`"name"`, `"Ravi"`, `{ }`, `[ ]`, `:`, `,`, `"age"`, `25`, etc.) into a JSON editor canvas
- Tiles snap into valid positions — curly braces at the top, key-value pairs inside
- Real-time validation: canvas glows green as each key-value pair is correctly placed
- **Bonus round:** Given a JSON object, translate it back to English (multiple choice)

#### Module 0.2: "Navigate the File System" (Interactive File Tree)
**Concept reinforced:** File paths, directories, extensions
**How it works:**
- An animated file explorer shows a project folder structure (mimicking the DeskMochi workspace)
- Challenges appear: "Click on the file that stores API secrets" → student clicks `.env`
- "What is the full path to the weather script?" → student clicks through folders, building the path segment by segment: `execution` → `/` → `get_weather.py`
- "Which files are Python scripts?" → student selects all `.py` files (highlights correct ones green)
- Final challenge: Given a file path like `directives/morning_briefing.md`, click to navigate there in the tree

#### Module 0.3: "Client-Server Ping Pong" (Animated Simulator)
**Concept reinforced:** Client-server architecture, request/response
**How it works:**
- Two characters on screen: a phone (client) and a laptop (server), connected by an animated line
- Student types a question in the phone: "What's the weather?"
- They click "Send" → animated message bubble travels along the line to the server
- Server lights up, "thinks," and a response bubble floats back: `{"temp": 28, "condition": "sunny"}`
- Student cycles through 3 scenarios: web browser + website, DeskMochi + local server, weather app + weather API
- Each scenario labels the client and server — student must correctly identify which is which (drag labels)

#### Module 0.4: "The API Restaurant" (Interactive Analogy)
**Concept reinforced:** APIs, API keys, requests/responses
**How it works:**
- Animated restaurant scene: student is the customer, there's a waiter (API), and a kitchen (service)
- Student picks from a menu of requests: "Get weather", "Send message", "Add spreadsheet row"
- Waiter asks: "Do you have your API key?" → student drags a key card from their wallet to the waiter
- Waiter walks to kitchen → kitchen prepares the response → waiter returns with JSON data on a plate
- If student sends a request WITHOUT the key → waiter rejects with "401 Unauthorized" (animated red stamp)
- If student requests something not on the menu → "404 Not Found"
- **Key teaching:** Different kitchens (services) require different keys — student matches keys to restaurants

---

### Video 1 Modules — What Is an AI Agent?

#### Module 1.1: "Chatbot vs Copilot vs Agent" (Sorting Game)
**Concept reinforced:** The three types of AI interaction
**How it works:**
- Three labeled buckets on screen: "Document Generator", "Copilot", "Agent"
- Cards drop in one at a time with scenarios:
  - "AI writes an email, you paste it into Gmail" → drag to Document Generator
  - "AI suggests the next line of code, you press Tab to accept" → drag to Copilot
  - "AI composes and sends the email for you" → drag to Agent
  - "AI creates a spreadsheet and shares it with your team" → drag to Agent
  - "AI generates a business plan, you copy to Google Docs" → drag to Document Generator
- 10 scenarios total, increasing in subtlety
- Score tracker + explanation for any wrong answers

#### Module 1.2: "Assemble an Agent" (Drag-to-Build)
**Concept reinforced:** Brain + Hands + Instructions = Agent
**How it works:**
- Empty agent blueprint on screen with three labeled slots: 🧠 Brain, ✋ Hands, 📋 Instructions
- Parts bin with items: "ChatGPT", "Python script", "Directive document", "Calculator app", "Random number generator", "Recipe book", "Weather API caller"
- Student drags correct items into each slot
- When all three slots are filled correctly, the agent "activates" — an animation shows it processing a request end to end
- Wrong combination shows what breaks: e.g., brain + brain + brain = "All thinking, no doing!"
- **Extension:** Build 3 different agents (weather agent, email agent, recipe agent) by selecting different hands and instructions

---

### Video 2 Modules — The DOE Framework

#### Module 2.1: "The Compound Error Calculator" (Interactive Slider)
**Concept reinforced:** Why 90% accuracy compounds badly over multiple steps
**How it works:**
- A horizontal slider for "Accuracy per step" (50%–100%) and a number input for "Number of steps" (1–20)
- As the student adjusts either value, a bar chart animates in real time showing the total success rate
- Pre-set scenarios to try:
  - "The ChatGPT approach": 90% accuracy × 10 steps = bar drops to 35%
  - "The DOE approach": 90% decision accuracy × 1 decision step + 100% script accuracy × 9 execution steps = 90% total
- A toggle switch: "Use deterministic scripts for execution?" — flipping it shows the bars jump up dramatically
- Final quiz: "An agent needs to do 5 things. Each step is 85% accurate. What's the chance everything works?" → student adjusts sliders to find the answer (44.4%), then toggles DOE mode to see it jump to 85%

#### Module 2.2: "Sort the Layers" (DOE Layer Assignment)
**Concept reinforced:** Which tasks belong to which layer
**How it works:**
- Three horizontal lanes labeled: **Directive** (top), **Orchestrator** (middle), **Execution** (bottom)
- Task cards appear one by one:
  - "Written in Markdown" → Directive
  - "Calls the OpenWeatherMap API" → Execution
  - "Decides which script to run next" → Orchestrator
  - "Contains edge cases and error handling notes" → Directive
  - "Reads the city name from the user's request" → Orchestrator
  - "Returns JSON with temperature data" → Execution
  - "Handles errors by trying a different approach" → Orchestrator
  - "Says which scripts are available" → Directive
- 12 cards total, shuffled each time
- Streak counter — get 5 in a row for a "DOE Master" badge

#### Module 2.3: "Walk the Request" (Step-Through Simulator)
**Concept reinforced:** End-to-end flow of a request through DOE layers
**How it works:**
- Animated pipeline: User → DeskMochi → Server → Directive → LLM → Script → API → Response → DeskMochi
- Student clicks "Next Step" to advance through each stage
- At each step, the active node highlights and shows what's happening:
  - Step 1: User says "What's the weather in Hyderabad?"
  - Step 2: DeskMochi sends message over WebSocket
  - Step 3: Server receives request, searches directives for "weather"
  - Step 4: Directive loaded — shows the actual markdown content
  - Step 5: LLM reads directive, decides: "run get_weather.py --city Hyderabad"
  - Step 6: Script runs, calls OpenWeatherMap API
  - Step 7: API returns `{"temp": 28, "condition": "sunny"}`
  - Step 8: LLM formats: "It's 28°C and sunny in Hyderabad"
  - Step 9: Server sends to DeskMochi → display + speaker
- At the end, labels appear on each node showing which DOE layer it belongs to
- **Challenge mode:** Three different requests (weather, recipe, WhatsApp) — student must predict which steps change and which stay the same

---

### Video 3 Modules — Hardware

#### Module 3.1: "Wire DeskMochi" (Virtual Wiring Simulator)
**Concept reinforced:** ESP32 pin connections, component wiring
**How it works:**
- A virtual breadboard with an ESP32, display module, and speaker module rendered to scale
- Student drags colored wires from ESP32 pins to component pins
- Pin labels visible on hover (GPIO 21, GPIO 22, etc.)
- Correct connections snap into place with a satisfying click and glow green
- Wrong connections bounce back with a gentle shake and a hint: "SDA goes to an I2C data pin — try GPIO 21"
- Once all wires are connected, the virtual DeskMochi "powers on" and shows "Hello!" on the simulated display
- **Timed challenge:** Wire it from memory (no labels shown) — leaderboard for fastest correct wiring

#### Module 3.2: "Signal Flow" (Trace the Data Path)
**Concept reinforced:** How data flows from voice command to display output
**How it works:**
- Bird's-eye diagram: Microphone → ESP32 → WiFi → PC Server → LLM → Script → API → back to PC → WiFi → ESP32 → Display + Speaker
- A glowing dot represents "the request" — student clicks nodes to advance the dot
- At each node, a quiz pops up:
  - "What protocol does the ESP32 use to talk to the PC?" → WebSocket / HTTP / Bluetooth (select one)
  - "What does the PC server do with the request?" → Reads directive and asks LLM / Sends directly to API / Shows on screen
  - "What comes back from the weather API?" → JSON data / An audio file / A webpage
- Correct answers advance the dot; wrong answers show the correct path highlighted

---

### Video 4 Modules — Development Environment Setup

#### Module 4.1: "Terminal Command Builder" (Fill-in-the-Blank)
**Concept reinforced:** Terminal commands, arguments, structure
**How it works:**
- Simulated terminal on screen with a blinking cursor
- Challenge prompts appear one at a time:
  - "Install the packages listed in requirements.txt" → student drags words: `pip` `install` `-r` `requirements.txt` into the command line in correct order
  - "Run the weather script for Tokyo" → `python` `execution/get_weather.py` `--city` `"Tokyo"`
  - "Check your Python version" → `python` `--version`
  - "Clone a repository from GitHub" → `git` `clone` `<url>`
- Each correct command "executes" with simulated terminal output
- Wrong order shows: "Almost! The command name always goes first, then flags, then arguments"
- **Speed round:** 8 commands, 60-second timer, drag-and-build as fast as you can

#### Module 4.2: "Map Your Workspace" (Interactive Folder Explorer)
**Concept reinforced:** DOE project structure — what lives where and why
**How it works:**
- An empty folder tree on the left, a pile of files on the right
- Files to sort: `get_weather.md`, `get_weather.py`, `.env`, `AGENTS.md`, `tool_registry.json`, `morning_briefing.md`, `send_whatsapp.py`, `requirements.txt`
- Student drags each file into the correct folder (`directives/`, `execution/`, or root)
- Tooltips explain WHY each file goes where it does
- After sorting, a "Why this structure?" reveal animation draws arrows between directive → script pairs, showing the relationship
- **Bonus:** "A new file arrives: `get_calendar.py` — where does it go?" Quick-fire sorting for 5 new files

---

### Video 5 Modules — First Agent

#### Module 5.1: "Write a Directive" (Guided Template Builder)
**Concept reinforced:** Directive structure — Goal, Inputs, Tools, Workflow, Edge Cases
**How it works:**
- A blank directive template on screen with 5 sections to fill
- The task: "Build a directive for checking stock prices"
- For each section, the student chooses from multiple-choice options:
  - **Goal:** "Get live stock price for a ticker" / "Buy stocks automatically" / "Show all NASDAQ stocks" → correct: option 1
  - **Inputs:** Student checks boxes: ☑ Ticker symbol, ☐ User's bank account, ☑ Exchange (optional), ☐ Social security number
  - **Tools:** Drag the right script: `get_stock_price.py` (not `send_whatsapp.py`)
  - **Workflow:** Reorder 4 jumbled steps into the right sequence
  - **Edge Cases:** Select which are real edge cases vs. irrelevant: ☑ "Invalid ticker symbol" ☑ "Market is closed" ☐ "User is left-handed"
- Completed directive renders as proper Markdown with a "Download" button
- **Key insight:** "You just wrote instructions for an AI — no code needed!"

#### Module 5.2: "HTTP Status Code Matcher" (Memory Card Game)
**Concept reinforced:** API status codes and what they mean
**How it works:**
- Grid of face-down cards (4×4)
- Cards have codes on one side (200, 401, 404, 500, 429, 201, 301, 503) and meanings on the other ("OK", "Unauthorized", "Not Found", "Server Error", "Rate Limited", "Created", "Redirected", "Service Unavailable")
- Classic memory match game — flip two cards, if code matches meaning, they stay face-up
- Timer + move counter for competitive replay
- After completing, a summary shows: "These are the 8 status codes you'll see most often when building agents"

#### Module 5.3: "Debug the API Call" (Spot-the-Error)
**Concept reinforced:** Common API errors and how to fix them
**How it works:**
- A simulated API request is shown with an error response
- Scenario 1: Request missing API key → 401 error → student clicks the highlighted issue ("no API key in header") → shown the fix
- Scenario 2: Wrong URL/endpoint → 404 error → student identifies the typo in the URL
- Scenario 3: Exceeded rate limit → 429 error → student selects the fix: "Add a delay between requests"
- Scenario 4: Server is down → 503 error → student selects: "Use cached data as fallback"
- Each fix is applied live, the request re-runs, and the student sees the success response
- Maps directly to the self-annealing concept: "You just debugged like an agent does"

---

### Video 6 Modules — Local Server

#### Module 6.1: "Pick Your LLM" (Interactive Comparison Tool)
**Concept reinforced:** LLM provider tradeoffs — cost, quality, speed, privacy
**How it works:**
- A dashboard with 5 LLM provider cards (Ollama, Groq, DeepSeek, OpenAI, Anthropic)
- Three slider inputs the student sets:
  - Budget: $0/month → $50/month
  - Quality needed: Low → High
  - Privacy priority: "Don't care" → "Nothing leaves my PC"
- As sliders move, provider cards animate — rising (good match) or falling (poor match) — ultimately ranking them
- Final recommendation highlights with a "Why?" expandable explanation
- Student clicks "Select" → next screen shows the exact `.env` configuration for their choice
- "You just made your first architecture decision!"

#### Module 6.2: "Trace the Agentic Loop" (Cycle Visualizer)
**Concept reinforced:** The LLM decision loop — read directive → decide tool → run script → check result → repeat
**How it works:**
- A circular diagram showing the agentic loop: READ → DECIDE → EXECUTE → EVALUATE → (loop or finish)
- Student is the orchestrator — a request comes in: "Send Priya a WhatsApp saying I'll be late"
- At each stage, student makes the choice:
  - **READ:** Which directive? → select `send_whatsapp.md` from a list
  - **DECIDE:** What to run? → select `send_whatsapp.py --contact "Priya" --message "I'll be late"`
  - **EXECUTE:** Script runs (animated) → returns `{"status": "needs_confirmation"}`
  - **EVALUATE:** What next? → "Ask user for approval" / "Send anyway" / "Abort" → correct: ask for approval
  - Loop again: User confirms → EXECUTE again → returns `{"status": "sent"}` → EVALUATE → "Done, report success"
- The loop has 2-3 cycles per scenario — teaches that agents iterate, not just run once
- **3 scenarios** of increasing complexity (weather = 1 loop, WhatsApp = 2 loops, morning briefing = 3+ loops)

---

### Video 7 Modules — Real-World Skills

#### Module 7.1: "Pipeline Plumber" (Connect-the-Skills)
**Concept reinforced:** Chaining multiple skills into a pipeline (morning briefing pattern)
**How it works:**
- A workspace shows individual skill blocks as "pipes" with input/output connectors (like a visual programming tool)
- Available blocks: Get Weather, Get Calendar, Get News, Format Text, Send to DeskMochi, Save to Sheet, Send WhatsApp
- Challenge: "Build a morning briefing pipeline"
  - Student connects: Get Weather + Get Calendar + Get News → all feed into Format Text → feeds into Send to DeskMochi
  - Parallel paths auto-detected and highlighted: "These three can run simultaneously!"
- Challenge 2: "Build a recipe-to-shopping-list pipeline"
  - Web Research → Extract Ingredients → Save to Sheet → Send WhatsApp (shopping list to partner)
- When the pipeline is complete, a "Run" button executes it with simulated data flowing through each block (animated particles along the pipes)
- Wrong connections show why: "Get Weather can't connect to Send WhatsApp directly — you need to format the data first"

#### Module 7.2: "Approval Gate Simulator" (Risk Assessment)
**Concept reinforced:** Human-in-the-loop for risky actions
**How it works:**
- Actions appear one at a time on a DeskMochi display mockup
- Student presses either ✅ "Auto-approve" or 🛑 "Requires confirmation" for each:
  - "Check weather in Mumbai" → Auto-approve ✅
  - "Send WhatsApp to boss: Meeting cancelled" → Requires confirmation 🛑
  - "Start a 25-minute focus timer" → Auto-approve ✅
  - "Order groceries from Zepto for ₹2,500" → Requires confirmation 🛑
  - "Read today's calendar events" → Auto-approve ✅
  - "Delete all rows from the expenses spreadsheet" → Requires confirmation 🛑
  - "Turn on the living room light" → Auto-approve ✅
  - "Unlock the front door" → Requires confirmation 🛑
- After each answer, explanation appears: "This action is [reversible/irreversible] and [affects only you / affects others / costs money]"
- Score at the end + the simple rule: "If it sends, spends, or deletes — confirm first."

---

### Video 8 Modules — Cloud Brains & Model Showdown

#### Module 8.1: "Model Showdown Simulator" (Interactive Comparison Dashboard)
**Concept reinforced:** How model choice dramatically affects speed, quality, context, and cost
**How it works:**
- A simulated DeskMochi interface with a prompt input and a model selector dropdown (Gemma 3 Local, Llama 3.3 Groq, Claude Opus 4.6)
- Student types or selects a pre-made prompt (e.g., "Draft a culturally appropriate email to a Japanese client")
- Clicks "Run on all three" → three response panels appear side by side, each with:
  - Simulated response text (pre-written to show quality differences)
  - A speedometer showing tok/s (30 vs 500 vs 40)
  - A context meter showing how much of the window was used
  - A cost counter ($0.00 / $0.00 / $0.02)
- Student can try 4 different prompts of increasing complexity:
  - Simple: "What's 2+2?" → all three nail it
  - Medium: "Summarize this email" → local is okay, Groq and Opus are better
  - Hard: "Analyze this business idea with market data" → local struggles, Groq is decent, Opus shines
  - Extreme: "Read this 30-page contract and list all obligations" → local can't fit it, Groq truncates, Opus handles the full document
- After all four, a summary: "Simple tasks → any model. Complex tasks → bigger brain. The DOE framework lets you switch in seconds."

#### Module 8.2: "Configure Your .env" (Interactive Setup Wizard)
**Concept reinforced:** Provider portability — same code, different brain
**How it works:**
- A simulated `.env` file editor on screen
- Three provider tabs: Local (Ollama), Groq (Free), Anthropic (Opus)
- Student clicks each tab → the `.env` fields update to show exactly what to change:
  - `LLM_PROVIDER=ollama` → `LLM_PROVIDER=groq` → `LLM_PROVIDER=anthropic`
  - Model name changes, API key field appears/disappears
- A "Test Connection" button simulates pinging each provider → shows "Connected! Speed: X tok/s"
- Quiz: "Your agent needs to analyze a 50-page document. Which provider should you use?" → Student clicks the right tab → sees the `.env` config they'd need
- **Key lesson:** "Three lines in `.env` is all that separates a free local brain from the world's most powerful AI."

#### Module 8.3: "Agent Idea Generator" (Interactive Decision Tree)
**Concept reinforced:** Identifying good automation candidates + choosing the right model
**How it works:**
- Student answers 5 questions in a guided wizard:
  1. "What area of your life?" → Personal / Work / Home / Finance / Health / Learning (click one)
  2. "What's the repetitive task?" → Free text input (or pick from examples)
  3. "Does it involve an external service?" → Yes (which?) / No (local only)
  4. "How complex is the reasoning?" → Simple / Medium / Complex
  5. "How often do you do it?" → Daily / Weekly / Monthly / On-demand
- The wizard generates a custom agent spec card:
  - Agent name, description, required APIs, difficulty rating (⭐ to ⭐⭐⭐)
  - **Recommended model tier** (Local / Groq Free / Opus) based on complexity answer
  - A pre-filled directive skeleton they can download
  - Similar skills from the course they can reference
- **Gallery mode:** Browse 30+ pre-made agent ideas (community-inspired). Each shows the spec card + model recommendation. Students can upvote favorites.

#### Module 8.4: "Tool Registry Explorer" (Interactive Search Interface)
**Concept reinforced:** Discovering existing tools before building new ones
**How it works:**
- Simulated terminal showing the tool registry interface
- Student types search queries and sees results:
  - Type "email" → shows `enrich_emails.py`, `welcome_client_emails.py`
  - Type "sheet" → shows `append_to_sheet.py`, `read_sheet.py`, `update_sheet.py`
  - Type "scrape" → shows `scrape_apify.py`, `scrape_google_maps.py`, `web_research.py`
- Clicking a result shows the full tool schema: inputs, outputs, required env vars, example usage
- Challenge: "You want to build a lead generation agent. Find all the tools you'd need." → student searches and checks off tools from a list
- Final reveal: "You found 4 of 5 existing tools — you only need to write ONE new script!"
- **Key lesson:** "Always check the registry. The best script is the one you don't have to write."

---

### Video 9 Modules — Advanced Patterns

#### Module 9.1: "Memory Manager" (Short-Term vs Long-Term Sorter)
**Concept reinforced:** When to store information in STM vs LTM
**How it works:**
- Two storage bins on screen: a desk with sticky notes (STM) and a filing cabinet (LTM)
- Information cards drop in:
  - "The user is currently asking about Tokyo weather" → STM (sticky note)
  - "The user's home city is Hyderabad" → LTM (filing cabinet)
  - "The last API call returned an error" → STM
  - "OpenWeatherMap rate limit is 60 calls/minute" → LTM
  - "User's preferred news category is technology" → LTM
  - "The current pipeline step is number 3 of 5" → STM
  - "Google Sheets OAuth needs re-auth every 7 days" → LTM
  - "User just said 'and what about tomorrow?'" → STM
- After sorting, the module shows what happens if you put everything in STM (info lost between sessions) or everything in LTM (database bloated with junk)
- The right balance: "Sticky notes for the current conversation. Filing cabinet for facts that are always true."

#### Module 9.2: "Build a Task Graph" (DAG Constructor)
**Concept reinforced:** Step dependencies, parallel execution, failure handling
**How it works:**
- A canvas with draggable task nodes and connectable arrows
- Challenge: "Build the plan for a morning briefing"
  - Available nodes: Get Weather, Get Calendar, Get News, Combine Results, Send to DeskMochi
  - Student places nodes and draws dependency arrows
  - Correct: Weather/Calendar/News are independent (no arrows between them), all feed into Combine, which feeds into Send
  - The system auto-detects parallelism and highlights: "These 3 run simultaneously — saves 6 seconds!"
- Challenge 2: "What happens if Get News fails?"
  - Student clicks the News node and selects: "Skip" / "Retry" / "Abort entire plan"
  - Correct: Skip → the graph re-renders with News greyed out, Combine recalculates, briefing still works
- Challenge 3: Build a more complex graph (lead generation pipeline with 7 steps)
- **Live execution mode:** Click "Run" → animated tokens flow through the graph. Parallel paths animate simultaneously. Failed nodes flash red. Student sees real timing.

#### Module 9.3: "Self-Healing Scenarios" (Error Recovery Simulator)
**Concept reinforced:** Retry, fallback, graceful degradation, learning from failure
**How it works:**
- Four mini-scenarios, each with an error the student must resolve:
- **Scenario 1 — Rate Limit:**
  - Agent calls weather API → gets 429 (rate limited)
  - Options: "Wait 2 seconds and retry" / "Use a different API" / "Crash and tell user" / "Pretend it worked"
  - Correct: Wait and retry → simulated retry succeeds → student sees the updated directive note
- **Scenario 2 — API Down:**
  - Weather API returns 503 (service unavailable)
  - Options: "Retry forever" / "Serve cached data, mention it's old" / "Return fake data" / "Do nothing"
  - Correct: Serve cached data → response shows "(cached from 2 hours ago)"
- **Scenario 3 — Bad Input:**
  - User says "weather in Hiderabad" (misspelled)
  - Options: "Fail with an error" / "Try closest match" / "Ask user to spell it again" / "Search for any city containing 'hider'"
  - Correct: Try closest match → show fuzzy matching in action
- **Scenario 4 — Chain Failure:**
  - Morning briefing: calendar and news both fail, only weather succeeds
  - Options: "Deliver weather only" / "Wait until all three work" / "Cancel the briefing"
  - Correct: Deliver weather only → graceful degradation
- After all four, a summary: "Fix, fallback, degrade, learn — the four patterns of resilient agents"

---

### Video 10 Modules — Graduation

#### Module 10.1: "Agent Design Canvas" (Full Skill Builder)
**Concept reinforced:** The complete DOE pattern applied independently
**How it works:**
- A multi-step guided builder combining all previous modules:
- **Step 1 — Choose your task** (from the brainstorm grid or custom)
- **Step 2 — Fill in the directive template** (Module 5.1 style)
- **Step 3 — Search for existing tools** (Module 8.2 style)
- **Step 4 — Draw the task graph** (Module 9.2 style, if multi-step)
- **Step 5 — Set approval gates** (Module 7.2 style)
- **Step 6 — Plan error handling** (Module 9.3 style)
- Final output: A complete agent design spec as a downloadable Markdown file
- **Shareable:** Students can share their design in a community gallery and see others' designs
- "You just designed a complete agent without writing a single line of code. The AI handles the rest."

#### Module 10.2: "DOE Framework Quiz" (Final Assessment)
**Concept reinforced:** All core concepts across the entire course
**How it works:**
- 20-question quiz mixing all module types:
  - Sort-the-layers (Module 2.2)
  - JSON building (Module 0.1)
  - Status code matching (Module 5.2)
  - Pipeline building (Module 7.1)
  - Memory sorting (Module 9.1)
  - Approval gate decisions (Module 7.2)
  - New situational questions testing understanding
- Adaptive difficulty: get 3 right in a row → harder questions. Get 2 wrong → review questions.
- Certificate of completion at the end with score + time + personalized strengths/weaknesses
- "You've mastered the DOE Framework. Now go build something real."

---

### Interactive Module Summary Table

| Video | Module | Type | Duration | Key Concept |
|-------|--------|------|----------|-------------|
| 0 | Build a JSON Object | Drag-and-drop | 3-4 min | JSON structure |
| 0 | Navigate the File System | Interactive explorer | 3-4 min | File paths & extensions |
| 0 | Client-Server Ping Pong | Animated simulator | 3-4 min | Request/response pattern |
| 0 | The API Restaurant | Interactive analogy | 4-5 min | APIs & API keys |
| 1 | Chatbot vs Copilot vs Agent | Sorting game | 3-4 min | AI interaction types |
| 1 | Assemble an Agent | Drag-to-build | 4-5 min | Brain + Hands + Instructions |
| 2 | Compound Error Calculator | Slider visualization | 3-4 min | Why deterministic scripts matter |
| 2 | Sort the Layers | Layer assignment | 3-4 min | DOE layer roles |
| 2 | Walk the Request | Step-through simulator | 5-6 min | End-to-end request flow |
| 3 | Wire DeskMochi | Virtual wiring | 5-8 min | ESP32 pin connections |
| 3 | Signal Flow | Trace-the-path quiz | 3-4 min | Data flow through hardware |
| 4 | Terminal Command Builder | Fill-in-the-blank | 4-5 min | Terminal commands & args |
| 4 | Map Your Workspace | Folder sorter | 3-4 min | DOE project structure |
| 5 | Write a Directive | Guided template | 5-6 min | Directive anatomy |
| 5 | HTTP Status Code Matcher | Memory card game | 3-4 min | API status codes |
| 5 | Debug the API Call | Spot-the-error | 4-5 min | API debugging & self-annealing |
| 6 | Pick Your LLM | Comparison dashboard | 4-5 min | LLM provider tradeoffs |
| 6 | Trace the Agentic Loop | Cycle visualizer | 5-6 min | Orchestrator decision loop |
| 7 | Pipeline Plumber | Visual pipe connector | 5-7 min | Chaining skills |
| 7 | Approval Gate Simulator | Risk assessment | 3-4 min | Human-in-the-loop |
| 8 | Model Showdown Simulator | Comparison dashboard | 5-6 min | Model choice impact on speed/quality/cost |
| 8 | Configure Your .env | Interactive setup wizard | 3-4 min | Provider portability |
| 8 | Agent Idea Generator | Decision tree wizard | 4-5 min | Identifying automation candidates + model selection |
| 8 | Tool Registry Explorer | Search interface | 3-4 min | Tool discovery |
| 9 | Memory Manager | STM vs LTM sorter | 3-4 min | Agent memory types |
| 9 | Build a Task Graph | DAG constructor | 5-7 min | Dependency graphs & parallelism |
| 9 | Self-Healing Scenarios | Error recovery sim | 5-6 min | Resilience patterns |
| 10 | Agent Design Canvas | Full skill builder | 8-10 min | Complete DOE application |
| 10 | DOE Framework Quiz | Final assessment | 8-10 min | All course concepts |

**Total: 29 interactive modules** across 11 videos, averaging ~2-3 per video.

### Production Priority

Build these modules in three tiers:

**Tier 1 — Ship with launch (11 modules):**
Modules 0.1, 0.3, 1.1, 2.1, 2.2, 5.1, 7.1, 8.1, 9.1, 9.2, 10.2
*(These cover the core DOE concepts, model selection, and provide the highest learning value)*

**Tier 2 — Ship within 2 weeks of launch (11 modules):**
Modules 0.2, 0.4, 1.2, 2.3, 4.1, 5.2, 6.2, 7.2, 8.2, 8.3, 9.3
*(These deepen understanding, add provider configuration practice, and add interactivity to more videos)*

**Tier 3 — Ship within 1 month (7 modules):**
Modules 3.1, 3.2, 4.2, 5.3, 6.1, 8.4, 10.1
*(Nice-to-haves that complete the full interactive experience)*