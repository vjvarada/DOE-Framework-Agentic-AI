# Meeting Minutes Agent — Directive

## Goal
Take a Google Meet meeting transcript (or audio/video recording) and produce professional, structured meeting minutes delivered as a Google Doc.

## Context
- User has a **free Gmail account** (no Google Workspace). Built-in Meet transcription is NOT available.
- This agent supports three input paths that all converge into the same minutes-generation pipeline.

---

## Input Paths

### Path A: Chrome Extension Transcript Export (FREE — Recommended)
**Setup (one-time):**
1. User installs one of these free Chrome extensions:
   - **Tactiq** (https://tactiq.io) — free tier captures full transcript, exports .txt
   - **MeetGeek** (https://meetgeek.ai) — free tier, auto-records & transcribes
   - **Google Meet Transcript** (Chrome Web Store) — lightweight, exports .txt
   - **Fireflies.ai** (https://fireflies.ai) — free tier, join bot + transcript

2. During the meeting, the extension captures live captions automatically.
3. After the meeting, user exports a `.txt`, `.srt`, or `.vtt` file.

**Agent workflow:**
1. User provides the transcript file path (e.g., `.tmp/meeting_transcript.txt`)
2. Skip transcription — go directly to minutes generation
3. Run `generate_meeting_minutes.py --input <file> --mode extract --copilot`
4. Copilot analyzes the transcript and extracts structured data
5. Run `generate_meeting_minutes.py --mode format --input <extracted_json>`
6. Save to Google Doc via `create_google_doc.py`

### Path B: Record Meeting + Local Whisper Transcription (FREE)
**Setup (one-time):**
1. Install **OBS Studio** (https://obsproject.com) or use any screen/audio recorder
2. In OBS: set to record audio only (Settings → Output → Recording → Audio only, .mp3 or .wav)
3. Alternative: use phone to record, or Windows Game Bar (Win+G → Record)

**Agent workflow:**
1. User provides the audio/video file path (e.g., `.tmp/meeting_recording.mp4`)
2. Run `transcribe_audio.py --input <file> --method local --model medium`
   - Uses OpenAI Whisper locally (runs on CPU, free, ~1x realtime speed)
   - For better speed with GPU: `--model small` or `--model base`
   - Output: `.tmp/transcript.json` with timestamped segments
3. Proceed to minutes generation (same as Path A step 3+)

**Model size guide:**
| Model   | VRAM   | Speed (1hr audio) | Quality |
|---------|--------|-------------------|---------|
| tiny    | ~1 GB  | ~5 min            | Basic   |
| base    | ~1 GB  | ~8 min            | OK      |
| small   | ~2 GB  | ~15 min           | Good    |
| medium  | ~5 GB  | ~30 min           | Great   |
| large   | ~10 GB | ~60 min           | Best    |

**CPU-only (no GPU):** Expect 2-4x slower. Use `tiny` or `base` for speed.

### Path C: Record Meeting + Whisper API (CHEAP — ~$0.006/min)
**Setup:**
1. Get an OpenAI API key (https://platform.openai.com/api-keys)
2. Set `OPENAI_API_KEY` in `.env`

**Agent workflow:**
1. User provides the audio/video file path
2. Run `transcribe_audio.py --input <file> --method api`
   - Uploads to OpenAI Whisper API
   - Fast (a 1hr meeting processes in ~2-3 minutes)
   - Cost: ~$0.006/min → 1hr meeting ≈ $0.36
   - Auto-splits files > 25MB into chunks
3. Proceed to minutes generation

---

## Minutes Generation Pipeline

Regardless of input path, once we have transcript text:

### Step 1: Extract (structured data from raw transcript)
```bash
python generate_meeting_minutes.py --input .tmp/transcript.txt --mode extract --copilot
```
- In **Copilot mode** (`--copilot`): Outputs a prompt for Copilot to analyze. Copilot reads the transcript and extracts:
  - Attendees (names/roles if identifiable from speech)
  - Topics discussed
  - Key points per topic
  - Action items (who, what, when)
  - Decisions made
- Copilot writes the extracted data to `.tmp/extracted_data.json`

- In **standalone mode** (no `--copilot`): Script calls OpenAI/Anthropic API directly to extract

### Step 2: Format (structured data → readable minutes)
```bash
python generate_meeting_minutes.py --input .tmp/extracted_data.json --mode format --output .tmp/minutes.md
```
- Takes the extracted JSON and produces clean Markdown meeting minutes
- Template includes: Title, Date, Attendees, Agenda, Discussion, Action Items, Decisions, Next Steps

### Step 3: Publish to Google Doc
```bash
python create_google_doc.py --title "Meeting Minutes - [Date]" --content-file .tmp/minutes.md
```
- Creates a new Google Doc with the minutes
- Returns the shareable URL

---

## Output Format

The final minutes must follow this structure:

```markdown
# Meeting Minutes: [Meeting Title/Topic]

**Date:** [Date and Time]  
**Duration:** [Duration]  
**Attendees:** [List of participants]  
**Minutes taken by:** AI Agent

---

## Agenda
1. [Topic 1]
2. [Topic 2]
...

## Discussion Summary

### [Topic 1]
- [Key point]
- [Key point]
- Speaker highlights: "[Notable quote or statement]"

### [Topic 2]
...

## Action Items

| # | Action Item | Owner | Deadline | Status |
|---|------------|-------|----------|--------|
| 1 | [Task]     | [Name]| [Date]   | Open   |
| 2 | [Task]     | [Name]| [Date]   | Open   |

## Decisions Made
1. [Decision and rationale]
2. [Decision and rationale]

## Key Takeaways
- [Important insight or conclusion]

## Next Steps
- [What happens next]
- Next meeting: [Date/TBD]
```

---

## Edge Cases & Learnings

1. **Long meetings (>2 hours):** Split recording into chunks before local Whisper. `transcribe_audio.py` handles this automatically for API mode (25MB limit).
2. **Poor audio quality:** Use `--model medium` or `large` for better accuracy. Add `--language en` to force English.
3. **Multiple speakers hard to distinguish:** Whisper doesn't do speaker diarization. Mention in minutes that speaker attribution is approximate. For better results, recommend `pyannote.audio` (needs HuggingFace token, free).
4. **Transcript from extension has timestamps:** The extract step will use timestamps to determine discussion flow and topic transitions.
5. **Non-English meetings:** Whisper supports 99 languages. Use `--language <code>` flag.
6. **Google OAuth first run:** First time running `create_google_doc.py`, a browser window opens for Google login. After that, `token.json` is cached.

---

## Environment Variables

| Variable | Required? | Purpose |
|----------|-----------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes (for Google Doc output) | Path to Google OAuth `credentials.json` |
| `OPENAI_API_KEY` | Only for Path C or standalone | Whisper API + LLM summarization |
| `ANTHROPIC_API_KEY` | Only for standalone | Alternative LLM for summarization |

---

## Quick Start

```bash
# One-time setup
pip install -r requirements.txt

# Path A: From transcript file
python generate_meeting_minutes.py --input meeting.txt --mode extract --copilot
# → Copilot analyzes and writes .tmp/extracted_data.json
python generate_meeting_minutes.py --input .tmp/extracted_data.json --mode format --output .tmp/minutes.md
python create_google_doc.py --title "Meeting Minutes - Feb 2026" --content-file .tmp/minutes.md

# Path B: From audio recording (free, local)
python transcribe_audio.py --input recording.mp4 --method local --model medium
python generate_meeting_minutes.py --input .tmp/transcript.txt --mode extract --copilot
python generate_meeting_minutes.py --input .tmp/extracted_data.json --mode format --output .tmp/minutes.md
python create_google_doc.py --title "Meeting Minutes - Feb 2026" --content-file .tmp/minutes.md

# Path C: From audio recording (cloud, fast)
python transcribe_audio.py --input recording.mp4 --method api
# then same as above...
```