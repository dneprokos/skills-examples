# Kostiantyn Teltov — Writing Style Guide

This guide codifies the consistent writing patterns observed across Kostiantyn Teltov's Medium articles. Use it as a checklist when reviewing a new article for style alignment.

---

## 1. Opening & Greeting

**What it looks like:**
- Starts with a warm, informal salutation: "Hi folks,", "Hi colleagues,", "Hello to all quality enthusiasts."
- Immediately follows the greeting with a short personal hook — a reflection, a question to the reader, or a statement of motivation for writing the article.
- May mention a previous article or personal experience that prompted this piece.
- Sets a conversational tone from line one; never opens with a cold definition or an abstract statement.

**Check for:**
- [ ] A personal greeting in the opening line
- [ ] A brief motivation hook (1–3 sentences explaining why the article was written)
- [ ] No abrupt jump into definitions or facts without warming up the reader

**Example (from "Breaking Silos with QA Guilds"):**
> "Hi folks,
> How often do you feel like you're working in silos? It might be within your project, your department, or even across the entire organization. Many of us have experienced that moment when we realize we don't really understand what's happening outside our own bubble."

---

## 2. Title & Subtitle

**What it looks like:**
- Main title is punchy, direct, and topic-focused.
- Subtitle is often creative, metaphorical, or a pop-culture reference ("The Tool Awakens", "The Watchers of Software Quality", "The Magic of Python Data Structures").
- The title+subtitle combination balances clarity (what it's about) with intrigue (a reason to click).

**Check for:**
- [ ] A clear main title describing the subject
- [ ] A creative, thematic, or culturally referencing subtitle (optional but preferred)
- [ ] The combination of both creates curiosity without being misleading

---

## 3. Tone & Voice

**What it looks like:**
- First-person throughout ("I", "my", "we").
- Directly addresses the reader using "you" and "we" to build shared experience.
- Honest about limitations, uncertainty, and personal doubts — never overclaims.
- Uses rhetorical questions to engage the reader and guide them to think.
- Light humor appears naturally — a joke, a playful emoji, a wink at the reader.
- Stays professional but never stiff or academic.

**Check for:**
- [ ] First-person voice is consistent
- [ ] Reader is addressed directly ("you", "we")
- [ ] Honest acknowledgment of limitations or uncertainty where relevant
- [ ] At least one rhetorical question or reader engagement moment
- [ ] No overly formal or passive-voice-heavy sentences

**Signature phrases to watch for (good signs they are present):**
- "Let's be honest..."
- "In my opinion..."
- "Good." (as a standalone transition sentence)
- "Of course,..."
- "But wait..."

---

## 4. Article Structure & Flow

**What it looks like:**
- Clear H2-level sections for each major topic.
- Flows from general to specific: sets context, introduces concepts, then dives into practical application.
- A "Background/Why" section or paragraph always comes before the technical content.
- Practical/hands-on examples follow the theory, not before it.
- Pros & Cons (advantages/disadvantages) section is common in technical articles.
- Ends with a conclusion section ("Final Thoughts", "In the end", "Conclusion") and a personal reflection or key takeaways.

**Typical article arc:**
1. Greeting + motivation hook
2. Background / foundational concepts (why this matters)
3. Core concept explanation (progressive, building up)
4. Practical section (step-by-step, examples, demos)
5. Advantages & Disadvantages (for technical or tool-focused articles)
6. Conclusion / Final Thoughts
7. Motivational closing line

**Check for:**
- [ ] H2 sections are present and logically ordered
- [ ] Background/context is established before diving into technical details
- [ ] Practical content follows theory, not precedes it
- [ ] A closing/conclusion section is present
- [ ] The article does not feel like it ends abruptly

---

## 5. Explaining Concepts

**What it looks like:**
- Introduces analogies and metaphors to make abstract concepts tangible.
  - "Think of MCP like a USB hub."
  - "The LLM / Agent is your laptop. The MCP Server is the USB hub."
  - "Playwright MCP is the engine, and Playwright Test Agents are the drivers."
- Uses the pattern **"In simple words:"** or **"In simple terms:"** before a plain-language summary.
- Breaks complex ideas into short bullet lists instead of long paragraphs.
- Provides a "to summarize" or "in short" recap block after covering multiple sub-points.

**Check for:**
- [ ] At least one analogy or metaphor for the main concept
- [ ] "In simple words/terms" framing used where appropriate
- [ ] Bullet lists used for multi-item explanations
- [ ] A recap/summary included after a complex set of concepts

---

## 6. Code Examples

**What it looks like:**
- Code blocks are included for technical articles but never overwhelm the text.
- Every code block is introduced with a plain-language explanation of what it does.
- Code is real and runnable — not pseudo-code or simplified placeholders (unless explicitly labelled).
- After a code block, a short follow-up sentence or paragraph explains the key parts.
- Code is contextualized within a narrative: "Here's what we did and why."

**Check for:**
- [ ] Each code block is preceded by an explanation of what it demonstrates
- [ ] Code is followed by a brief walkthrough of key parts
- [ ] Code examples are real and relevant (not just filler)
- [ ] Non-technical articles skip code entirely (no forced inclusion)

---

## 7. Visual Elements & Images

**What it looks like:**
- Images and diagrams appear frequently — roughly every 2–4 sections.
- Visuals serve as section separators as much as explanations.
- Diagrams explain architecture, flows, or relationships (e.g., MCP flow diagrams).
- Emojis appear selectively in section headers of technical or lighter-tone articles (e.g., "🧠 MCP server and Playwright agents", "🔐 Security Risks").
- Emojis are NOT used in the body text of more formal/process articles.

**Check for:**
- [ ] Images are referenced or included at appropriate intervals
- [ ] Emojis in headers are used only when the article tone calls for it (light/technical)
- [ ] Emojis are NOT scattered randomly through the body text

---

## 8. Paragraph Style

**What it looks like:**
- Paragraphs are short to medium length: 2–5 sentences as the standard.
- Long paragraphs are rare and only when building up a complex argument.
- Sentences are direct and clear.
- Scannable: the reader can skim headers and first sentences to understand the article.
- Standalone one-sentence paragraphs are used intentionally for emphasis:
  - "We introduce abstraction."
  - "They only optimize for 'what sounds most likely next'."
  - "Good."

**Check for:**
- [ ] Most paragraphs are 2–5 sentences
- [ ] No walls of text without visual breaks or list items
- [ ] Intentional short single-sentence paragraphs used for emphasis where appropriate

---

## 9. Closing & Conclusion

**What it looks like:**
- The conclusion is never abrupt — it always feels like a proper landing.
- Recaps the key message in 2–4 sentences.
- Includes a personal reflection: what the author learned, what they still wonder about, or what changed for them.
- Ends with a motivational, encouraging, or thematically resonant sign-off line:
  - "May the force be with you!"
  - "Set sail — and good luck on your journey."
  - "Thank you for reading."
- A "Key Takeaways" bullet list is used in process/conceptual articles for quick summary reference.

**Check for:**
- [ ] A dedicated conclusion section
- [ ] Personal reflection included (not just a mechanical summary)
- [ ] A memorable, thematically fitting closing line
- [ ] Key Takeaways bullet list present in longer conceptual articles

---

## 10. Technical Depth & Accessibility Balance

**What it looks like:**
- Technical articles always start with foundational concepts, even if the audience is assumed to be experienced.
- The author explicitly notes when going deep: "I don't want to go too deep here" or "this is a simplified view."
- Beginner-friendly explanations and advanced details coexist in the same article.
- Limitations and tradeoffs are always acknowledged — no technology is presented as perfect.

**Check for:**
- [ ] Foundational concepts introduced before advanced ones
- [ ] Explicit scoping statements ("we won't cover X here", "simplified view")
- [ ] Tradeoffs and limitations acknowledged, not glossed over
- [ ] The article is readable by someone one level below the target audience

---

## 11. Standalone Quoted Emphasis

**What it looks like:**
- Key insights or takeaway phrases are sometimes formatted as standalone block-quote-style lines — set apart from surrounding text, visually prominent.
- These are typically short, memorable, and actionable.

**Examples:**
> "HR can be your good friend."

> "Find your allies."

> "There are no stupid questions — and no stupid suggestions."

**Check for:**
- [ ] High-value insights are broken out for visual emphasis rather than buried in a paragraph
- [ ] These standalone quotes feel earned — they summarize something that was built up before them

---

## Quick Reference: Style Checklist Summary

| Category | Key Signal |
|---|---|
| Opening | Personal greeting + motivation hook |
| Title | Creative subtitle with thematic flair |
| Tone | First-person, reader-inclusive, honest, humorous |
| Structure | General → Specific → Practical → Pros/Cons → Conclusion |
| Explanations | Analogies, "in simple words", bullet lists, recaps |
| Code | Real examples, introduced and followed up in text |
| Visuals | Images every few sections, selective emoji in headers |
| Paragraphs | Short to medium, intentional one-liners for emphasis |
| Closing | Personal reflection + memorable sign-off line |
| Depth | Fundamentals first, limitations acknowledged, accessible |
| Emphasis | Key insights pulled out as standalone quoted lines |
