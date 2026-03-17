#!/usr/bin/env python3
"""
Generate structured meeting minutes from a transcript.

Modes:
  extract  — Parse raw transcript and extract structured data (attendees, topics, actions, decisions)
  format   — Take extracted data (JSON) and produce clean Markdown minutes

In Copilot mode (--copilot): outputs a prompt for Copilot to process instead of calling an LLM API.
In standalone mode: calls OpenAI or Anthropic API directly.

Usage:
    # Copilot mode — extract structured data (Copilot answers the prompt)
    python generate_meeting_minutes.py --input .tmp/transcript.txt --mode extract --copilot

    # Copilot mode — format into minutes
    python generate_meeting_minutes.py --input .tmp/extracted_data.json --mode format --output .tmp/minutes.md

    # Standalone — extract using OpenAI
    python generate_meeting_minutes.py --input .tmp/transcript.txt --mode extract --provider openai

    # Full pipeline shortcut
    python generate_meeting_minutes.py --input .tmp/transcript.txt --mode full --copilot
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

TMP_DIR = Path(".tmp")


def ensure_tmp_dir():
    TMP_DIR.mkdir(exist_ok=True)


def read_input(input_path: str) -> str:
    """Read transcript or JSON data from a file."""
    path = Path(input_path)
    if not path.exists():
        print(f"ERROR: File not found: {input_path}")
        sys.exit(1)
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # If it's a JSON file with 'text' key (from transcribe_audio.py), extract text
    if path.suffix == ".json":
        try:
            data = json.loads(content)
            if isinstance(data, dict) and "text" in data:
                return data["text"]
            return content  # Return raw JSON string for format mode
        except json.JSONDecodeError:
            pass
    
    return content


def extract_copilot(transcript: str, output_path: str) -> str:
    """
    Generate a prompt for Copilot to extract structured meeting data.
    Copilot reads this prompt and produces the output.
    """
    prompt = f"""=== MEETING TRANSCRIPT EXTRACTION TASK ===

Below is a raw transcript from a meeting. Please analyze it and extract the following information
into a JSON structure. Save the result to: {output_path}

**Instructions:**
1. Identify all speakers/attendees (infer names from context if possible, otherwise use "Speaker 1", "Speaker 2", etc.)
2. Identify the main topics/agenda items discussed
3. For each topic, summarize the key discussion points (2-4 bullet points each)
4. Extract ALL action items with: task description, owner (who is responsible), and deadline (if mentioned, otherwise "TBD")
5. Extract ALL decisions that were made
6. Note any notable quotes or statements worth highlighting
7. Estimate the meeting duration if timestamps are available

**Output JSON format:**
```json
{{
    "meeting_title": "Best guess at meeting topic/name",
    "date": "{datetime.now().strftime('%Y-%m-%d')}",
    "estimated_duration": "X minutes",
    "attendees": [
        {{"name": "Person Name", "role": "Role if identifiable"}}
    ],
    "topics": [
        {{
            "title": "Topic Name",
            "key_points": ["Point 1", "Point 2"],
            "notable_quotes": ["Relevant quote if any"]
        }}
    ],
    "action_items": [
        {{
            "task": "Description of the action",
            "owner": "Person responsible",
            "deadline": "Date or TBD",
            "priority": "high/medium/low"
        }}
    ],
    "decisions": [
        {{
            "decision": "What was decided",
            "rationale": "Why, if discussed"
        }}
    ],
    "key_takeaways": ["Important insight 1", "Important insight 2"],
    "next_steps": ["What happens next"]
}}
```

=== TRANSCRIPT START ===
{transcript[:50000]}
=== TRANSCRIPT END ===

Please analyze the above transcript and write the extracted JSON to: {output_path}
"""
    return prompt


def extract_standalone(transcript: str, provider: str = "openai") -> dict:
    """
    Use LLM API to extract structured meeting data from transcript.
    """
    system_prompt = """You are an expert meeting analyst. Given a raw meeting transcript, extract structured data including:
- Meeting title/topic
- Attendees with roles
- Discussion topics with key points  
- Action items with owners and deadlines
- Decisions made with rationale
- Key takeaways and next steps

Return ONLY valid JSON matching the requested schema. No other text."""

    user_prompt = f"""Extract structured meeting data from this transcript:

{transcript[:50000]}

Return JSON with: meeting_title, date, estimated_duration, attendees (name, role), topics (title, key_points, notable_quotes), action_items (task, owner, deadline, priority), decisions (decision, rationale), key_takeaways, next_steps."""

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("ERROR: OPENAI_API_KEY not set. Use --copilot mode or set the key.")
            sys.exit(1)
        
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        result_text = response.choices[0].message.content
    
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("ERROR: ANTHROPIC_API_KEY not set. Use --copilot mode or set the key.")
            sys.exit(1)
        
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        result_text = response.content[0].text
    else:
        print(f"ERROR: Unknown provider: {provider}")
        sys.exit(1)
    
    # Parse JSON from response
    try:
        # Try to find JSON in the response
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]
        
        return json.loads(result_text.strip())
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse JSON response. Saving raw text. Error: {e}")
        return {"raw_response": result_text, "parse_error": True}


def format_minutes(extracted_data: dict, output_path: str = None) -> str:
    """
    Take extracted structured data and produce clean Markdown meeting minutes.
    This is fully deterministic — no LLM needed.
    """
    if isinstance(extracted_data, str):
        try:
            extracted_data = json.loads(extracted_data)
        except json.JSONDecodeError:
            print("ERROR: Input must be valid JSON (from the extract step)")
            sys.exit(1)
    
    title = extracted_data.get("meeting_title", "Untitled Meeting")
    date = extracted_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    duration = extracted_data.get("estimated_duration", "Unknown")
    attendees = extracted_data.get("attendees", [])
    topics = extracted_data.get("topics", [])
    action_items = extracted_data.get("action_items", [])
    decisions = extracted_data.get("decisions", [])
    key_takeaways = extracted_data.get("key_takeaways", [])
    next_steps = extracted_data.get("next_steps", [])
    
    # Build markdown
    lines = []
    lines.append(f"# Meeting Minutes: {title}")
    lines.append("")
    lines.append(f"**Date:** {date}")
    lines.append(f"**Duration:** {duration}")
    
    if attendees:
        if isinstance(attendees[0], dict):
            attendee_strs = []
            for a in attendees:
                name = a.get("name", "Unknown")
                role = a.get("role", "")
                if role:
                    attendee_strs.append(f"{name} ({role})")
                else:
                    attendee_strs.append(name)
            lines.append(f"**Attendees:** {', '.join(attendee_strs)}")
        else:
            lines.append(f"**Attendees:** {', '.join(str(a) for a in attendees)}")
    
    lines.append("**Minutes taken by:** AI Agent")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Agenda
    if topics:
        lines.append("## Agenda")
        for i, topic in enumerate(topics, 1):
            topic_title = topic.get("title", f"Topic {i}") if isinstance(topic, dict) else str(topic)
            lines.append(f"{i}. {topic_title}")
        lines.append("")
    
    # Discussion Summary
    if topics:
        lines.append("## Discussion Summary")
        lines.append("")
        for topic in topics:
            if isinstance(topic, dict):
                topic_title = topic.get("title", "Topic")
                lines.append(f"### {topic_title}")
                for point in topic.get("key_points", []):
                    lines.append(f"- {point}")
                for quote in topic.get("notable_quotes", []):
                    if quote:
                        lines.append(f'- *"{quote}"*')
                lines.append("")
            else:
                lines.append(f"### {topic}")
                lines.append("")
    
    # Action Items
    if action_items:
        lines.append("## Action Items")
        lines.append("")
        lines.append("| # | Action Item | Owner | Deadline | Priority |")
        lines.append("|---|-----------|-------|----------|----------|")
        for i, item in enumerate(action_items, 1):
            if isinstance(item, dict):
                task = item.get("task", "")
                owner = item.get("owner", "TBD")
                deadline = item.get("deadline", "TBD")
                priority = item.get("priority", "medium")
                lines.append(f"| {i} | {task} | {owner} | {deadline} | {priority} |")
            else:
                lines.append(f"| {i} | {item} | TBD | TBD | medium |")
        lines.append("")
    
    # Decisions
    if decisions:
        lines.append("## Decisions Made")
        lines.append("")
        for i, decision in enumerate(decisions, 1):
            if isinstance(decision, dict):
                dec = decision.get("decision", "")
                rationale = decision.get("rationale", "")
                if rationale:
                    lines.append(f"{i}. **{dec}** — {rationale}")
                else:
                    lines.append(f"{i}. {dec}")
            else:
                lines.append(f"{i}. {decision}")
        lines.append("")
    
    # Key Takeaways
    if key_takeaways:
        lines.append("## Key Takeaways")
        lines.append("")
        for takeaway in key_takeaways:
            lines.append(f"- {takeaway}")
        lines.append("")
    
    # Next Steps
    if next_steps:
        lines.append("## Next Steps")
        lines.append("")
        for step in next_steps:
            lines.append(f"- {step}")
        lines.append("")
    
    # Footer
    lines.append("---")
    lines.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} by Meeting Minutes Agent*")
    
    minutes_text = "\n".join(lines)
    
    # Save if output path provided
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(minutes_text)
        print(f"Minutes saved to: {output_path}")
    
    return minutes_text


def main():
    parser = argparse.ArgumentParser(
        description="Generate structured meeting minutes from a transcript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Copilot mode: extract data (Copilot processes the prompt)
  python generate_meeting_minutes.py --input .tmp/transcript.txt --mode extract --copilot

  # Format extracted data into minutes
  python generate_meeting_minutes.py --input .tmp/extracted_data.json --mode format --output .tmp/minutes.md

  # Standalone: extract using OpenAI
  python generate_meeting_minutes.py --input .tmp/transcript.txt --mode extract --provider openai

  # Full pipeline (extract + format) in standalone mode
  python generate_meeting_minutes.py --input .tmp/transcript.txt --mode full --provider openai
        """
    )
    
    parser.add_argument("--input", "-i", required=True, help="Input file (transcript .txt or extracted .json)")
    parser.add_argument("--mode", "-m", required=True, choices=["extract", "format", "full"],
                        help="Mode: extract (transcript→JSON), format (JSON→minutes), full (both)")
    parser.add_argument("--copilot", action="store_true",
                        help="Copilot mode: output prompt for Copilot instead of calling API")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai",
                        help="LLM provider for standalone mode (default: openai)")
    parser.add_argument("--output", "-o", default=None, help="Output file path")
    parser.add_argument("--title", default=None, help="Override meeting title")
    
    args = parser.parse_args()
    ensure_tmp_dir()
    
    content = read_input(args.input)
    
    if args.mode == "extract":
        if args.copilot:
            # Output prompt for Copilot to process
            output_path = args.output or str(TMP_DIR / "extracted_data.json")
            prompt = extract_copilot(content, output_path)
            
            # Save the prompt so Copilot can read it
            prompt_path = str(TMP_DIR / "extraction_prompt.md")
            with open(prompt_path, "w", encoding="utf-8") as f:
                f.write(prompt)
            
            print(f"\n{'='*60}")
            print("COPILOT MODE: Extraction prompt ready")
            print(f"{'='*60}")
            print(f"Prompt saved to: {prompt_path}")
            print(f"Expected output: {output_path}")
            print(f"\nPlease read {prompt_path} and write the extracted JSON to {output_path}")
            print(f"Then run: python generate_meeting_minutes.py --input {output_path} --mode format")
        else:
            # Standalone: call LLM API
            print("Extracting meeting data using LLM API...")
            extracted = extract_standalone(content, provider=args.provider)
            
            output_path = args.output or str(TMP_DIR / "extracted_data.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(extracted, f, indent=2, ensure_ascii=False)
            
            print(f"\nExtracted data saved to: {output_path}")
            print(f"Next: python generate_meeting_minutes.py --input {output_path} --mode format")
    
    elif args.mode == "format":
        # Format JSON data into markdown minutes
        try:
            data = json.loads(content) if isinstance(content, str) else content
        except json.JSONDecodeError:
            print("ERROR: Input must be a valid JSON file (from the extract step)")
            sys.exit(1)
        
        if args.title:
            data["meeting_title"] = args.title
        
        output_path = args.output or str(TMP_DIR / "minutes.md")
        minutes = format_minutes(data, output_path)
        
        print(f"\n{'='*60}")
        print("MEETING MINUTES GENERATED")
        print(f"{'='*60}")
        print(f"Saved to: {output_path}")
        print(f"\nTo publish as Google Doc:")
        title = data.get('meeting_title', 'Meeting Minutes')
        print(f'  python create_google_doc.py --title "{title}" --content-file {output_path}')
    
    elif args.mode == "full":
        # Full pipeline: extract → format
        if args.copilot:
            print("Full mode with --copilot requires two steps:")
            print("  1. Run with --mode extract --copilot first")
            print("  2. Let Copilot process the prompt")
            print("  3. Run with --mode format")
            sys.exit(0)
        
        print("=== Step 1/2: Extracting structured data ===")
        extracted = extract_standalone(content, provider=args.provider)
        
        extracted_path = str(TMP_DIR / "extracted_data.json")
        with open(extracted_path, "w", encoding="utf-8") as f:
            json.dump(extracted, f, indent=2, ensure_ascii=False)
        
        if args.title:
            extracted["meeting_title"] = args.title
        
        print("\n=== Step 2/2: Formatting minutes ===")
        output_path = args.output or str(TMP_DIR / "minutes.md")
        minutes = format_minutes(extracted, output_path)
        
        print(f"\n{'='*60}")
        print("FULL PIPELINE COMPLETE")
        print(f"{'='*60}")
        print(f"Extracted data: {extracted_path}")
        print(f"Meeting minutes: {output_path}")
        title = extracted.get('meeting_title', 'Meeting Minutes')
        print(f'\nTo publish: python create_google_doc.py --title "{title}" --content-file {output_path}')


if __name__ == "__main__":
    main()
