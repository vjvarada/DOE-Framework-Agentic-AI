---
name: startup_pr_outreach
description: >
  Migrated from directives/startup_pr_outreach.md
when_to_use: "User asks about startup pr outreach"
authority: read
cost_tier: 1
version: 0.1.0
---

﻿# Startup PR Outreach

## Goal
Run an end-to-end startup PR campaign: define strategy, identify the right journalists and outlets, find their real contact details, build a press/media kit, and execute personalized outreach with proper follow-ups — all tracked in a Google Sheets CRM.

## When to Use
- User is launching a product, funding round, milestone, or want top-of-funnel press
- User asks for help with "PR", "media outreach", "press release", "journalist list", "media kit", "press kit"
- User wants to pitch their startup to journalists, podcasters, or industry publications

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| Company / Product | Yes | Name, one-line pitch, sector, stage (pre-seed → Series X) |
| News Angle | Yes | What is being announced (launch, raise, milestone, hire, partnership, data, POV) |
| Target Geography | Yes | Countries / cities of focus (e.g. India + US) |
| Target Verticals | Yes | Categories of publication (e.g. AI, fintech, SaaS, climate, D2C, healthcare) |
| Founder Bios | Recommended | 2–4 lines each, plus LinkedIn URLs |
| Embargo Date | Optional | Date/time the news can go live |
| Existing assets | Optional | Logos, product screenshots, founder photos, demo video, deck |

## PR Strategy Framework

Before any outreach, work through this with the user (do NOT skip — this is the highest-leverage step):

### 1. Goals
Pick 1–3 measurable goals. Example:
- Tier-1 placement (TechCrunch / The Information / Forbes / FT / WSJ / YourStory / Inc42)
- N tier-2/3 placements in vertical media (e.g. AIM, MIT Tech Review, The Hindu BusinessLine)
- Podcast appearances (target list of 5–10)
- SEO halo (backlinks from DA 60+ sites)
- Investor / hiring signal

### 2. Narrative
Craft ONE primary narrative + 2–3 secondary angles. Each angle = headline + 2-sentence hook + supporting proof points.

### 3. Tiering
- **Tier 1**: 3–5 dream outlets, exclusive-worthy
- **Tier 2**: 10–20 vertical/regional outlets
- **Tier 3**: 30–50 trade press, newsletters, podcasts

### 4. Sequencing
- Offer exclusive to ONE Tier-1 outlet first (24–72 hr exclusive window)
- Embargo blast to Tier 2/3 to hit the day exclusive drops
- Follow-up wave at +3 days, +7 days

Document the strategy as a Google Doc (`create_google_doc.py`) so the user can review/edit.

## Workflow

### Step 1 — Strategy Doc
1. Interview the user on the inputs above (especially news angle + goals)
2. Draft narrative + tiering + sequencing
3. Create Google Doc: `PR Strategy — {Company} — {YYYY-MM-DD}`

### Step 2 — Build the Journalist List
Use SERP to find journalists who have *recently* (last 12 months) covered comparable stories. Recency matters more than fame.

```bash
python execution/serp_market_research.py \
  --mode search \
  --query "{vertical} startup raises OR launches site:techcrunch.com 2025..2026" \
  --num-results 20 \
  --location "United States"
```

Repeat across queries:
- `"{competitor name}" site:techcrunch.com`
- `"{vertical} startup" "by {firstname}" -site:linkedin.com` (find bylines)
- `"reporter" OR "writer" "{vertical}" "{outlet}"`
- `"{outlet}" "contact" "tips"` (for tip lines)
- Substack / podcast searches: `"{vertical}" site:substack.com`, `"{vertical} podcast" "host"`

For deeper outlet research:
```bash
python execution/web_research.py --topic "top {vertical} journalists {geography} 2025-2026" --depth 3
```

For each hit, extract:
- Journalist name, outlet, beat
- Recent article URL + headline + date (proof of relevance)
- Twitter/X handle, LinkedIn URL
- Outlet domain (for email guessing)

Push into a Google Sheet `Journalist CRM — {Company}` with columns:
`Name | Outlet | Beat | Tier | Recent Article | Date | Twitter | LinkedIn | Email | Phone | Status | Last Contact | Notes`

```bash
python execution/append_to_sheet.py --sheet-id {id} --range "Journalists!A:M" --values ...
```

### Step 3 — Find Real Contact Details

**Emails (in priority order):**
1. Public masthead / "Contact" / "Tips" pages of the outlet — scrape with `web_research.py`
2. Author bio pages (TechCrunch, Forbes, etc. often list emails or Twitter)
3. AnyMailFinder pattern matching:
   ```bash
   python execution/enrich_emails.py --sheet-id {id} --tab "Journalists" \
     --name-col "Name" --domain-col "OutletDomain" --email-col "Email"
   ```
4. Muck Rack / Pressfarm style profile guess (manual fallback)

**Phone numbers:**
- Most journalists do NOT publish phone numbers and cold calls are widely considered rude in PR. Default to email + Twitter DM.
- If the user *insists* on phone outreach (rare, usually only for breaking news tip-lines), find:
  - Outlet tip-line / newsroom number (public)
  - Journalist's public Twitter bio (some list Signal / WhatsApp)
  - LinkedIn profile (if they list it)
- Use `web_research.py` to surface public listings. Do NOT scrape paid people-finder sites — that's both legally and ethically dicey.
- Flag to user: "I found a tip-line number for {outlet}. Direct journalist phone numbers are generally not public — recommend opening over email first."

**Quality gate:** mark each contact's `Email Confidence` as `verified` / `pattern-guess` / `unverified`. Never blast a pattern-guess list — that destroys sender reputation.

### Step 4 — Build the Press / Media Kit

Create a Google Doc + a Drive folder containing:

1. **Press release** (1 page, inverted pyramid)
2. **Founder bios** + headshots
3. **Company one-pager** (problem, solution, traction, team, raise/milestone)
4. **Fact sheet** (founded, HQ, team size, customers, funding to date, investors)
5. **Quotes** (founder + 1–2 investors/customers, pre-approved)
6. **Logo pack** (PNG + SVG, light + dark)
7. **Product screenshots / demo video link**
8. **FAQ / objection-handling doc** (internal, for founder prep)

Use `create_google_doc.py` for each document, then collect links into a single "Press Kit Index" doc the user can share.

### Step 5 — Draft Personalized Pitches

For EACH Tier-1 / Tier-2 journalist, draft a unique 4–7 sentence pitch (Copilot mode: draft directly). Template:

```
Subject: {specific hook tied to their recent article}

Hi {FirstName},

I read your {Month} piece on {Topic} — particularly the point about {specific takeaway}.
That's the gap we're trying to close at {Company}: {one-sentence pitch}.

{One concrete proof point: revenue, users, named customer, novel data}.

We're {announcing X / raising Y / launching Z} on {date}. Happy to give you a first look under embargo, or just send the kit if useful.

{Link to press kit}

{Founder name}
{Title} · {Company} · {Phone for THEM to call back}
```

Rules:
- Reference a **specific** recent article (column `Recent Article` in the CRM) — generic pitches get auto-deleted
- One ask per email
- Press kit link, not attachments
- Founder's phone in signature (so journalist can call back, not the other way around)

Bulk personalization:
```bash
python execution/casualize_first_names_batch.py --sheet-id {id} --tab "Journalists"
python execution/casualize_company_names_batch.py --sheet-id {id} --tab "Journalists"
```

### Step 6 — Send & Track

**Tier 1 (exclusives):** Send manually from the founder's own inbox, one at a time. Do NOT use a sending tool — Tier-1 journalists can tell.

**Tier 2/3 (embargo blast):** Use Instantly.ai campaign.
```bash
python execution/instantly_create_campaigns.py --name "PR Launch — {Company} — Tier2" \
  --sheet-id {id} --tab "Journalists" --filter "Tier=2 OR Tier=3"
```

Update CRM status after each send: `Pitched → Opened → Replied → Interviewed → Published → Passed → No-reply`.

### Step 7 — Follow-Ups & Conversation Drafting

- **+3 days**: short bump ("just floating this back up, embargo still open")
- **+7 days**: final nudge with a new angle or fresh data
- After 2 follow-ups with no reply, mark `No-reply` and move on. Do NOT spam.

When a journalist replies, help draft the response:
- Answer their specific question first, in 2–3 sentences
- Offer founder availability (give 3 time slots, founder's timezone)
- Attach / link only what they asked for
- For interview prep: generate a Q&A brief based on the journalist's past 5 articles (use `web_research.py` on their byline)

### Step 8 — Measure & Learn
After the campaign:
- Update the strategy doc with: # sent / # opened / # replied / # published / Tier-1 hits
- Log lessons into memory:
  ```bash
  python execution/memory_db.py add-insight "Hook X outperformed hook Y by Nx in {vertical}"
  python execution/memory_db.py add-fact "{Journalist} prefers exclusives, 48h embargo, replies within 24h" --category journalist
  ```

## Output

Deliverables (all in Google Drive, not local files):
1. **PR Strategy Doc**
2. **Journalist CRM Sheet** (with verified contacts)
3. **Press Kit folder** (release, bios, fact sheet, quotes, logos, screenshots)
4. **Pitch Drafts Doc** (one personalized pitch per Tier-1/Tier-2 contact)
5. **Outreach campaign** running in Instantly.ai (Tier 2/3)
6. **Status dashboard** (the CRM sheet doubles as this)

Intermediate files go in `.tmp/` — scraped article lists, raw SERP dumps, draft snippets.

## Edge Cases

### User has no news angle
Don't invent one. Walk through the angle-generation checklist: new product, new round, new hire, new customer, new data/report, contrarian POV, anniversary milestone, response to a news cycle. If none apply, recommend they wait — bad PR is worse than no PR.

### Tier-1 outlet ghosts the exclusive
After 48 hr no-reply on an exclusive offer, withdraw politely and move to Tier 1B. Never blast embargo to everyone if Tier 1 hasn't responded — burns the relationship.

### Email confidence is low for whole list
Stop. Going out with a pattern-guess list of 50+ journalists will tank the founder's sending domain reputation. Either verify manually (open each outlet's masthead) or skip cold email and pitch via Twitter/LinkedIn DM.

### User wants phone numbers for cold-calling journalists
Push back gently. Cold-calling journalists is widely seen as poor form and burns goodwill. Offer alternatives: Twitter DM, LinkedIn InMail, warm intro via a mutual connection (search the user's network), or showing up to industry events.

### Embargo broken by one outlet
Lift embargo for everyone immediately. Send a quick note: "Embargo lifted — story has gone live at {outlet}, you're free to publish." Note in CRM which outlet broke it (don't offer them embargoes again).

### User wants to handle a crisis (negative press)
Different SOP. Switch to crisis mode:
1. Do NOT respond publicly within the first hour
2. Establish facts internally (timeline, who, what)
3. Draft a single holding statement (acknowledge → action → contact)
4. Decide: respond directly to the reporter, or let it pass
5. Document the incident in memory for future reference

## Quality Checklist (before any send)

- [ ] Each pitch references a specific recent article by that journalist
- [ ] Subject line is < 60 chars and hook-driven, not pitch-driven
- [ ] Email is < 150 words
- [ ] Press kit link works and the doc is set to "Anyone with link can view"
- [ ] Founder phone is in the signature
- [ ] Embargo date/time is stated explicitly with timezone if applicable
- [ ] CRM row updated with `Status=Pitched`, `Last Contact={today}`
- [ ] Email-confidence column is `verified` or `pattern-guess` (never `unverified`)
