---
name: dneprokos-medium-article-reviewer
description: >-
  Review a Medium article written by Kostiantyn Teltov (@dneprokos) and produce
  a section-by-section critique with actionable suggestions based on his
  established writing style. Use this skill whenever the user provides a Medium
  article URL and asks to review it, check its style, analyze a blog post,
  suggest improvements, or give feedback on a draft or published article — even
  if they say only "review this", "check my post", or paste a medium.com link.
argument-hint: "medium article URL"
---

# Medium Article Reviewer

Review a Medium article for alignment with Kostiantyn Teltov's personal writing style and produce a structured set of improvement suggestions per section.

## When to use this skill

- User provides a Medium URL and asks for a review or feedback
- User asks "check my article", "review my draft", "does this match my style?", "give me suggestions for my blog post"
- User pastes a medium.com link with any request about quality, improvement, or style

Do **not** use this skill for:
- General writing help unrelated to a specific article
- Reviewing non-Medium content (use a general writing review approach instead)
- Publishing or editing articles directly on Medium

---

## Workflow

### Step 1: Fetch the article

Use `WebFetch` with the URL provided by the user to retrieve the article content.

If the URL is not a public Medium article (behind paywall, login-required, 404), tell the user it could not be fetched and ask them to paste the article text directly.

### Step 2: Load the style guide

Read `references/writing-style-guide.md` in full. This is your scoring rubric — keep it in mind throughout the entire analysis.

### Step 3: Parse the article structure

Before writing the review, mentally map out the article:
- What sections/headings exist?
- Where does the intro end and the core content begin?
- Is there a conclusion/closing section?
- Does it include code, visuals, or callout quotes?

### Step 4: Analyze section by section

For each section in the article:
1. Identify what the section does (introduces concept, provides background, shows code, wraps up, etc.)
2. Compare it against the relevant categories in `references/writing-style-guide.md`
3. Note what aligns well with the style and what could be improved
4. For each suggestion, include: the specific issue, the reason it matters for this style, and a concrete recommended fix (a rewrite suggestion when helpful)

Be generous with praise where the style is well-executed — the goal is honest, balanced feedback, not just a list of problems.

### Step 5: Fill in the Style Checklist

Go through the Quick Reference checklist from the style guide. Mark each category as:
- `✅ Matches style` — clearly present and well done
- `⚠️ Partial` — present but could be stronger
- `❌ Missing` — not present, should be added

### Step 6: Produce the review output

Use the output format defined below. Keep the tone constructive and peer-like — this is a colleague review, not an audit.

---

## Output Format

Always use exactly this structure:

```
# Article Review: [Article Title]

## Overall Impression
(2–4 sentences. How well does this article reflect the author's established style?
What is the strongest aspect? What is the most significant gap?)

## Section-by-Section Feedback

### [Section name or "Opening / Introduction"]
**What works well:**
- (specific observation with brief quote if helpful)

**Suggestions:**
- [Issue]: (explain the gap and why it matters for this style)
  → Suggested rewrite: "[example of how it could read instead]"

### [Next section name]
...

(Repeat for every major section. Skip a section only if it has no meaningful feedback.)

## Style Checklist

| Category | Status | Notes |
|---|---|---|
| Opening & Greeting | ✅ / ⚠️ / ❌ | (one-line note) |
| Title & Subtitle | ✅ / ⚠️ / ❌ | |
| Tone & Voice | ✅ / ⚠️ / ❌ | |
| Article Structure | ✅ / ⚠️ / ❌ | |
| Concept Explanations | ✅ / ⚠️ / ❌ | |
| Code Examples | ✅ / ⚠️ / ❌ | (or "N/A — non-technical article") |
| Visual Elements | ✅ / ⚠️ / ❌ | |
| Paragraph Style | ✅ / ⚠️ / ❌ | |
| Closing & Conclusion | ✅ / ⚠️ / ❌ | |
| Technical Depth Balance | ✅ / ⚠️ / ❌ | (or "N/A") |
| Standalone Quoted Emphasis | ✅ / ⚠️ / ❌ | |

## Top 3 Suggestions

1. **[Category]** — [Most impactful thing to improve, in one or two sentences.]
2. **[Category]** — [Second most impactful suggestion.]
3. **[Category]** — [Third most impactful suggestion.]
```

---

## Review principles

**Be specific.** Vague feedback like "improve the tone" is not useful. Quote the actual sentence that could be better and show what it could look like.

**Respect the author's voice.** The goal is to bring the article closer to Kostiantyn's own established voice — not to rewrite it in a generic style. If something feels off from his personal voice, explain it in terms of his own patterns (e.g., "your other articles often open with a personal anecdote — this one jumps straight to a definition").

**Balance praise and suggestions.** If a section is already strong, say so clearly. Over-critiquing a well-written piece is as unhelpful as under-critiquing a weak one.

**Non-technical articles.** If the article has no code (process, culture, career topics), mark Code Examples as N/A and skip that category. The same applies to Technical Depth Balance. Focus your energy on tone, structure, and storytelling.

**Partial sections.** If the article is a draft and some sections are clearly unfinished, note that and offer directional guidance rather than trying to score incomplete content.
