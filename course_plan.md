# DeskMochi AI Agent Course — Complete Production Plan

> **Purpose:** This document is the master blueprint for a 10-video course (+ 1 foundations module) that teaches non-programmers how to build AI agents that do real work. Each section contains enough detail to serve as the basis for a full video script.

**Product:** DeskMochi — a physical desk companion (ESP32 + speaker + display) connected to a local AI server that executes tasks via the DOE Framework.

**Target Audience:** Non-programmers who want to build AI agents that take action in the real world.

**Unique Differentiator:** Physical hardware companion + framework-first teaching + working automations by Video 7.

**Total Runtime:** ~4-4.5 hours across 11 videos

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
- [Video 8: More Skills + Idea Generator](#video-8-more-cool-agent-skills--idea-generator)
- [Video 9: Advanced Patterns](#video-9-advanced-patterns--memory-pipelines-and-self-healing)
- [Video 10: Build Your Own Agent — Graduation](#video-10-build-your-own-agent--graduation-project)
- [Appendix A: Complete Concept Glossary](#appendix-a-complete-concept-glossary)
- [Appendix B: Glossary Card System](#appendix-b-glossary-card-system)
- [Appendix C: Course Summary Table](#appendix-c-course-summary-table)

---

## Course Arc

```
Video 0:    FOUNDATIONS — tech vocabulary for non-programmers
Video 1-2:  WHAT are agents? (Philosophy + the DOE mental model)
Video 3:    THE HARDWARE — DeskMochi physical build
Video 4-5:  THE SOFTWARE — setting up + building your first agent with Copilot
Video 6:    THE SERVER — running autonomously without Copilot
Video 7-8:  REAL SKILLS — 7+ working agent skills connected to real APIs
Video 9:    ADVANCED — memory, pipelines, self-healing, safety
Video 10:   GRADUATION — build your own agent from scratch
```

**Pedagogical flow:** Each video builds on the previous. No concept is used before it's explained. By Video 7, the student has a working physical AI companion doing real tasks on their desk.

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

**Duration:** ~18-20 min
**Type:** Talking head + screen diagrams + 3 short demos
**Goal:** Build the mental model of what agents are and generate excitement for what they'll build.

### Concepts Introduced Just-In-Time

> These concepts appear for the FIRST TIME in this video. Use glossary cards (5-second on-screen pop-ups) when first mentioned.

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **LLM (Large Language Model)** | When explaining the "brain" of an agent | "An AI brain trained on text. It reads, reasons, and generates — but can't act on its own." |
| **Prompt** | When showing how you talk to agents | "The text you send to an LLM. Better instructions → better results." |
| **Token** | When discussing LLM costs briefly | "How LLMs measure text. ~1 token ≈ ¾ of a word. API providers charge per token." |

### Learning Objectives
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

### Section 1.3 — Three Types of AI Interaction (~3 min)

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

### Section 1.4 — The Capability Overhang (~3 min)

**What to cover:**
- LLMs are already incredibly capable — most people just don't connect them to the real world
- It's like having a genius employee who can think and plan perfectly, but has no arms and legs
- Agents give the AI arms and legs (scripts that do things)
- The gap between "what AI can do" and "what people use AI for" is enormous — that gap is the opportunity

**Talking points:**
- "The AI overhang isn't about smarter models. It's about connecting existing models to real tools."
- "You don't need a PhD in AI. You need to know how to give AI access to APIs."

### Section 1.5 — Three Live Demos (~3 min)

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

### Section 1.6 — What We'll Build (~2 min)

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
- Run the setup script → watch it install packages + create `.env`

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

### Section 4.6 — Quick Reference Card (~2 min)

**What to show on screen:**
```
WHAT                           WHERE
─────────────────────────────────────────────
Agent's brain rules            AGENTS.md
Task instructions              directives/*.md
Python scripts                 execution/*.py
API keys & secrets             .env
Temporary data                 .tmp/
```
- "Bookmark this. You'll use it every video."

### Video 4 Key Takeaway
> Your workspace is your agent's home. It took 10 minutes to set up. Directives tell the AI what to do, scripts do it, .env gives them access. That's the entire structure.

---

## Video 5: Your First Agent — "Get the Weather"

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

### Section 5.5 — Connect to DeskMochi (~4 min)

**What to cover:**
- Show how the weather result would flow to DeskMochi:
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

### Section 6.3 — Choosing an LLM Provider (~5 min)

**What to cover:**
- The server needs an LLM brain. You have 5 options:

| Provider | Cost | Quality | Best For |
|----------|------|---------|----------|
| **Ollama** (local) | $0 — completely free | Good | Beginners, offline use, privacy |
| **Groq** | Free tier available | Great | Free + fast |
| **DeepSeek** | ~$0.27/M tokens (~10x cheaper) | Excellent | Best value |
| **OpenAI** (GPT-4o) | ~$2.50/M tokens | Excellent | Most popular |
| **Anthropic** (Claude) | ~$3.00/M tokens | Best | Highest quality |

- "For this course, I recommend starting with **Ollama** (free, runs on your PC) or **Groq** (free tier, cloud). You can upgrade later."
- **Ollama setup** (show live):
  - Install: go to ollama.ai → download → install
  - Pull a model: `ollama pull llama3.1`
  - It's now running at `http://localhost:11434`
  - No API key needed, no internet required, no cost

### Section 6.4 — Start the Server (~5 min)

**What to cover:**
- Set the LLM provider in `.env`:
  ```
  LLM_PROVIDER=ollama
  ```
- Start the server:
  ```
  python execution/local_server.py
  ```
- Terminal shows: "Server running on localhost:8000"
- Explain what's happening:
  - Server is now listening for WebSocket connections from DeskMochi
  - It loaded all directives from `directives/`
  - It's ready to accept requests

### Section 6.5 — Test with DeskMochi (~4 min)

**What to cover:**
- DeskMochi should auto-connect (it's been looking for the server since Video 3!)
- Display changes: "Connecting..." → "Connected!" → "Ready!"
- Test: Press button → "What's the weather in Hyderabad?"
- Watch the server logs in the terminal:
  ```
  [19:30:01] DeskMochi connected
  [19:30:05] Request: "What's the weather in Hyderabad?"
  [19:30:05] Loading directive: get_weather.md
  [19:30:06] LLM decided: run get_weather.py --city "Hyderabad"
  [19:30:07] Script returned: {"temp": 28, "condition": "Sunny"}
  [19:30:07] LLM formatted: "It's 28°C and Sunny in Hyderabad"
  [19:30:07] Sent to DeskMochi
  ```
- DeskMochi display: "28°C ☀️ Sunny"
- DeskMochi speaker: "It's 28 degrees and sunny in Hyderabad"

### Section 6.6 — Close VS Code — It Still Works! (~2 min)

**What to cover:**
- Close VS Code entirely
- Press DeskMochi button → "What time is it?" → DeskMochi responds
- "The server is running in the terminal. Copilot isn't needed anymore."
- "This is Mode 2 of the DOE Framework — standalone deployment."

### Video 6 Key Takeaway
> The server replaces Copilot as the brain. Same directives, same scripts — just a different orchestrator. DeskMochi now works 24/7 on your desk, no VS Code required.

---

## Video 7: Making DeskMochi Useful — Real-World Skills

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
> Each skill follows the exact same pattern: (1) Write directive, (2) Generate/write script, (3) Test, (4) Connect to DeskMochi. By Skill 3, the student should recognize the pattern and it should feel natural.

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

**Step 4 — DeskMochi:**
- Display: "✅ Recipe saved!"
- Speaker: "Your butter chicken recipe is in Google Sheets!"

**Teaching moment:** "Notice the pattern? Directive → Script → Test → DeskMochi. Every skill follows this."

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
> Every skill follows the same pattern: directive → script → test → DeskMochi. You built 4 real skills in 30 minutes. The pattern is the superpower.

---

## Video 8: More Cool Agent Skills + Idea Generator

**Duration:** ~22-25 min
**Type:** Build 2-3 more skills + creative brainstorm
**Goal:** Expand the skill library, show tool discovery, and inspire students to think of their own.

### Concepts Introduced Just-In-Time

| Concept | When It Appears | Glossary Card Text |
|---------|----------------|-------------------|
| **Rate Limiting** | When API rejects a call | "APIs limit how many times you can call per minute. Hit the limit = temporarily rejected." |

### Learning Objectives
- Build more complex skills
- Use the tool registry to discover available scripts
- Generate ideas for custom agents
- Understand which tasks are good candidates for automation

### Skill 5: Email Summarizer (~8 min)

**The ask:** "Summarize my unread emails"

**Directive:** fetch unread emails via Gmail API → LLM summarizes the batch → DeskMochi reads summary

**What this demonstrates:**
- LLM doing the "thinking" (summarization) — this is a valid use of the AI brain
- Script doing the "doing" (Gmail API call) — deterministic
- The distinction: scripts fetch data, the LLM interprets it

**DeskMochi output:**
- Display: scrollable list of 3-5 email summaries
- Speaker: "You have 7 unread emails. Three are from your team about the project deadline. Two are newsletters. One is from Amazon about your order."

### Skill 6: Price Tracker / Shopping Assistant (~7 min)

**The ask:** "Track the price of PlayStation 5 on Amazon"

**Directive:** scrape product page → extract price → save to sheet → compare with previous prices → alert if it drops

**What this demonstrates:**
- Multi-step pipelines
- Persistent data (price history in Google Sheet)
- Conditional logic ("only alert me if price drops below ₹40,000")
- Scheduled tasks (check daily)

### Skill 7: Focus Timer / Pomodoro (~5 min)

**The ask:** "Start a 25-minute focus timer"

**What this demonstrates:**
- Not everything needs an API! This is purely local.
- DeskMochi shows a countdown on display
- Plays a gentle sound when done
- No LLM needed — direct ESP32 firmware feature
- "Agents aren't always about AI. Sometimes a simple timer on your desk companion is the most useful thing."

### Section 8.4 — Tool Registry: Discovering What's Available (~5 min)

**What to cover:**
- Show the tool registry command:
  ```
  python execution/tool_registry.py find "spreadsheet"
  python execution/tool_registry.py list
  python execution/tool_registry.py show append_to_sheet
  ```
- "Before building a new skill, check what tools already exist. You might not need to write a new script at all."
- Walk through 2-3 tool schemas to show what's available

### Section 8.5 — Brainstorm: What Will YOU Build? (~5 min)

**What to show on screen — an idea grid to inspire:**

| Category | Agent Skill Ideas |
|----------|-------------------|
| **Productivity** | Calendar reminders, email drafts, meeting summaries, to-do lists |
| **Finance** | Expense tracking, invoice generation, stock/crypto price alerts |
| **Health** | Water reminders, medication alerts, workout logging, step count |
| **Social** | Birthday reminders, auto-reply on messages, social media posting |
| **Home** | Grocery lists from recipes, appliance control, energy monitoring |
| **Learning** | Flashcard quizzer, article summarizer, language practice |
| **Business** | Lead tracking, report generation, CRM updates, invoice creation |
| **Fun** | Joke of the day, trivia quizzer, random fact, fortune cookie |
| **Communication** | Quick translator, voice notes to text, meeting scheduler |

**Key question to ask the student:**
- "What's one thing you do every day that's repetitive and boring? That's your first agent."

### Video 8 Key Takeaway
> You now have 7+ skills and a method for building more. Any task that follows "get input → call API → deliver result" is a candidate. Use the tool registry to find what already exists.

---

## Video 9: Advanced Patterns — Memory, Pipelines, and Self-Healing

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
- "Now you have a physical AI companion on your desk that checks weather, creates spreadsheets, sends WhatsApp messages, controls your smart home, and gives you morning briefings."
- "More importantly, you have a *framework*. DOE works for any agent — not just DeskMochi."
- "The directive tells the AI what. Scripts tell it how. The AI connects the two. That's it."
- "Every automation you'll ever build follows this pattern. You now have the pattern."
- "Go build something cool."

### Video 10 Key Takeaway
> You don't need to be a programmer to build agents. You need to be clear about what you want (directive), let the AI figure out how (orchestration), and give it reliable tools (execution). That's DOE. Now go build.

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

### Video 1 — AI Agents (3 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 14 | LLM (Large Language Model) | An AI brain that reads, reasons, and generates text. |
| 15 | Prompt | The text you send to an LLM to get a response. |
| 16 | Token | How LLMs measure text. ~1 token ≈ ¾ word. Providers charge per token. |

### Video 2 — DOE Framework (4 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 17 | Deterministic vs Probabilistic | Same input → same output (calculator) vs slightly different (LLM). |
| 18 | SOP (Standard Operating Procedure) | Step-by-step task checklist. Directives are SOPs. |
| 19 | Framework | A reusable pattern for solving a class of problems. |
| 20 | Markdown | Simple text formatting: `#` = heading, `**` = bold, `-` = bullet. |

### Video 3 — Hardware (6 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 21 | Microcontroller (ESP32) | Tiny computer with WiFi. Controls displays and speakers. |
| 22 | Firmware | Software flashed onto hardware. Runs every time the device powers on. |
| 23 | WiFi (device perspective) | How ESP32 finds your PC on the same network. |
| 24 | WebSocket | Persistent two-way connection. Like a phone call that doesn't hang up. |
| 25 | Serial / USB Communication | How your PC talks to ESP32 through the USB cable. |
| 26 | TTS (Text-to-Speech) | Converting text to spoken audio. |

### Video 4 — Development Environment (14 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 27 | IDE / Code Editor | Fancy text editor for code. VS Code is ours. |
| 28 | Terminal / Command Line | Text interface for typing commands. Bottom panel in VS Code. |
| 29 | Command | An instruction typed into the terminal. |
| 30 | Command-Line Argument | Extra info passed to a command: `--city "Hyderabad"`. |
| 31 | Python | Programming language. You run Python files; AI writes them. |
| 32 | pip / Package Manager | Downloads code libraries. App store for Python. |
| 33 | Library / Package | Code someone else wrote that you reuse. |
| 34 | requirements.txt | Shopping list of packages. One command installs all. |
| 35 | .env File | Secret file storing API keys. Never share it. |
| 36 | Environment Variable | A named value in memory. Scripts read it by name. |
| 37 | Virtual Environment (venv) | Isolated package bubble per project. |
| 38 | Git | Tracks file changes over time. |
| 39 | GitHub | Website that stores Git projects online. |
| 40 | Cloning a Repository | Downloading a project from GitHub. One command. |

### Video 5-6 — Agent Building + Server (8 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 41 | HTTP (GET, POST) | Web language. GET = give me data. POST = here's data. |
| 42 | URL / Endpoint | Address of a specific API function. |
| 43 | REST | Conventions for API design. URLs for resources, GET to read, POST to create. |
| 44 | Status Code | API's one-word answer. 200 = OK. 404 = not found. 500 = broken. |
| 45 | localhost | Your own computer as a network address. |
| 46 | Port | Numbered door. Different services use different ports. |
| 47 | FastAPI | Python package for building servers easily. |
| 48 | Agentic Loop | LLM reads → decides tool → script runs → result → repeat. |

### Video 7-8 — External Services (4 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 49 | OAuth | Secure login flow. Grant permission once via browser. |
| 50 | Webhook | Reverse API. Service pushes data to you when events happen. |
| 51 | Spreadsheet ID | Unique code in a Google Sheet URL identifying which sheet. |
| 52 | Third-Party Service | External product whose API you call (Twilio, Google, etc.). |
| 53 | Rate Limiting | API limits on calls per minute/day. Hit it = temporarily rejected. |

### Video 9 — Advanced Patterns (5 concepts)

| # | Concept | One-Line Definition |
|---|---------|-------------------|
| 54 | Database | Structured permanent data storage. Agent memory lives here. |
| 55 | SQLite | Database in a single file. No setup needed. |
| 56 | DAG (Directed Acyclic Graph) | Steps with arrows showing order. No loops. |
| 57 | Caching | Saving data copies as backup when live source fails. |
| 58 | Concurrency / Parallelism | Running multiple tasks at the same time. |

**Total: 58 concepts** — introduced gradually across 10 videos, never more than 14 in a single video (and that's Video 4, which is the setup video where concepts appear naturally as you install things).

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

Package all 58 concepts as a printable 2-page PDF:
- Page 1: Concepts 1-30 (Foundations through Development)
- Page 2: Concepts 31-58 (Building through Advanced)
- Include in course materials download
- Students can keep it on their desk next to DeskMochi

---

## Appendix C: Course Summary Table

| Video | Title | Duration | Skills Built | Concepts Introduced | Cumulative Concepts |
|-------|-------|----------|-------------|-------------------|-------------------|
| 0 | The Language of Tech | ~22 min | — | 13 | 13 |
| 1 | What Is an AI Agent? | ~18 min | — (3 demos) | 3 | 16 |
| 2 | The DOE Framework | ~20 min | — | 4 | 20 |
| 3 | Building DeskMochi | ~18 min | Hardware assembled | 6 | 26 |
| 4 | Setting Up Your Workshop | ~24 min | Dev environment ready | 14 | 40 |
| 5 | Your First Agent | ~26 min | Weather skill | 4 | 44 |
| 6 | The Local Server | ~24 min | Standalone server | 4 | 48 |
| 7 | Real-World Skills | ~32 min | Recipe, WhatsApp, Alexa, Briefing | 4 | 52 |
| 8 | More Skills + Ideas | ~22 min | Email, Price Tracker, Timer | 1 | 53 |
| 9 | Advanced Patterns | ~24 min | Memory, Pipelines, Self-Healing | 5 | 58 |
| 10 | Build Your Own | ~28 min | Custom graduation project | 0 | 58 |
| | **TOTAL** | **~4.2 hrs** | **7+ working skills** | **58 concepts** | |

---

## Production Notes

### Required Course Materials (to create before filming)
- [ ] ESP32 DeskMochi firmware (Arduino/PlatformIO project)
- [ ] `execution/local_server.py` — FastAPI + WebSocket + agentic loop
- [ ] `execution/pipeline_runner.py` — provider-agnostic LLM orchestrator
- [ ] `execution/get_weather.py` — OpenWeatherMap wrapper
- [ ] `execution/send_whatsapp.py` — Twilio/Green API wrapper
- [ ] `execution/smart_home.py` — Home Assistant API wrapper
- [ ] `execution/get_calendar.py` — Google Calendar API wrapper
- [ ] `execution/get_news.py` — News API wrapper
- [ ] `directives/` for all 7+ skills
- [ ] `device_map.json` — smart home device mapping
- [ ] `contacts.json` — phone contacts mapping
- [ ] Wiring diagram (Fritzing or similar)
- [ ] 3D print files or cardboard template for DeskMochi housing
- [ ] Downloadable 2-page glossary cheatsheet (PDF)
- [ ] DOE Framework cheatsheet (1-page, PDF)
- [ ] Glossary card graphics (58 cards)

### Video Production Order
Recommended filming order (not the release order):
1. Film Videos 0, 1, 2 first (talking head / diagrams — no code dependency)
2. Film Video 3 (hardware — independent of software)
3. Film Videos 4, 5 (sequential — setup then first skill)
4. Build `local_server.py` and `pipeline_runner.py`, then film Video 6
5. Film Videos 7, 8 (skills — need server working)
6. Film Video 9 (advanced — needs skills working)
7. Film Video 10 last (wraps everything up)