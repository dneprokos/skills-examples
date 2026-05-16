---
name: slack-markdown-generator
description: >-
  Generate or convert any content into a Slack Block Kit JSON payload using
  markdown blocks, ready to paste into the Slack API or a webhook. Accepts
  freeform text, structured data (status updates, reports, meeting summaries),
  or existing standard markdown and handles Slack-specific quirks like the
  12,000-character limit, image-to-link conversion, and flat header rendering.
  Use this skill whenever the user says "format this for Slack", "create a Slack
  message", "convert to Slack markdown", "generate a Slack notification",
  "make this Slack-ready", "write a Slack announcement", or mentions Slack
  messages, Slack Block Kit, Slack webhooks, or Slack markdown — even if they
  just paste content and say "send this to Slack" or "post this in our channel".
argument-hint: "text, notes, data, or markdown to convert"
---

# Slack Markdown Message Generator

Turn any input into a Slack Block Kit JSON payload — ready to send via the Slack API, an incoming webhook, or the Block Kit Builder.

## When this skill fits

Use it for requests like:

- "format this status update for Slack"
- "convert my release notes to a Slack message"
- "turn these meeting notes into a Slack post"
- "create a Slack Block Kit payload from this markdown file"
- "make this announcement Slack-ready"
- "I want to post this in our team channel"

Do **not** use it for:

- Sending messages directly to Slack (this skill generates the payload; it does not call the Slack API)
- Rich interactive messages with buttons, select menus, or input blocks (this skill targets markdown blocks only)
- Slack mrkdwn format (the legacy `*bold*`, `_italic_` style) — this skill targets the newer `markdown` block type

## Inputs

The user may provide any combination of:

- **Freeform text** — a casual description, announcement, or notes
- **Structured data** — key/value pairs, a status template, a table of items
- **Existing markdown** — a `.md` file or pasted standard markdown content

If no input is provided, ask the user to supply content before proceeding. If the intent is ambiguous (e.g. just "make a Slack message" with nothing else), ask one focused clarifying question — what content should go in the message?

## Workflow

### 1. Understand the content

Read the input and identify its type:

- **Freeform text**: interpret the intent and shape the content into a clear, readable message
- **Structured data**: organise the fields into logical sections using headings, bold labels, and lists
- **Existing markdown**: preserve the structure as closely as possible, applying only the changes needed for Slack compatibility

If the content is long or multi-topic, plan to split it into multiple markdown blocks (see the character limit rule below).

### 2. Convert to Slack-compatible markdown

Before writing the output, read [`references/slack-markdown-spec.md`](./references/slack-markdown-spec.md). It contains the full syntax reference and gotchas. Key things to apply:

- **Images** (`![alt](url)`) are not rendered as images in Slack — convert them to hyperlinks `[alt](url)` or plain URLs
- **Header levels** all render at the same visual size in Slack. If the original uses heading hierarchy for visual structure, consider replacing deeper headings with **bold** labels or divider blocks to create separation
- **12,000-character limit**: the cumulative text across all `markdown` blocks in a single payload must not exceed 12,000 characters. If the content is long, split it naturally at section boundaries into multiple blocks
- **Unsupported HTML** — remove or convert any raw HTML tags; Slack's markdown block does not render HTML

### 3. Build the Block Kit payload

Wrap the converted content in the standard Block Kit structure:

```json
{
  "blocks": [
    {
      "type": "markdown",
      "text": "...your converted content..."
    }
  ]
}
```

Rules for the blocks array:

- Each section of content that is logically separate should be its own `markdown` block
- If you split for the character limit, each chunk becomes its own block
- Keep `block_id` out of markdown blocks — it is silently ignored by Slack
- If there is a clear title or header at the top, it can be its own short block for visual clarity

### 4. Output

Write the payload to a file named `slack-message.json` in the current working directory (or a path the user specifies).

After writing the file, show a brief preview in the response:

1. The file path
2. How many blocks the payload contains
3. The first ~300 characters of the first block's `text` field so the user can verify the content looks right
4. A note about any conversions made (images converted, headers flattened, content split, etc.)

## Hard rules

- Never fabricate content not present in the input
- Never produce a block whose `text` exceeds 12,000 characters
- Never include raw `![...](...)` image syntax in the output — always convert to a link
- If any conversion changes the meaning or drops content, call it out explicitly in your response
