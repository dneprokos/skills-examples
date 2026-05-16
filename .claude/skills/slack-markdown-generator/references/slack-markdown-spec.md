# Slack Markdown Block — Syntax Reference

This document summarises the supported syntax for the `"type": "markdown"` block in Slack Block Kit, key limits, and conversion gotchas. Consult this file when generating or converting content for a Slack markdown block.

Source: https://docs.slack.dev/reference/block-kit/blocks/markdown-block/

---

## Limits

| Constraint | Value |
|---|---|
| Cumulative character limit (all `markdown` blocks in one payload) | **12,000 characters** |
| `block_id` support | Not retained — omit it |

If your content exceeds 12,000 characters, split it across multiple `markdown` blocks at natural section boundaries (paragraph breaks, section headings, list ends). Each block must individually be under the cumulative cap — practically this means aim for each block to be well under 12,000 chars if you have several.

---

## Supported syntax

### Text emphasis

| Effect | Syntax | Result |
|---|---|---|
| Bold | `**bold**` or `__bold__` | **bold** |
| Italic | `*italic*` or `_italic_` | *italic* |
| Bold + italic | `***all important***` | ***all important*** |
| Bold with nested italic | `**extremely _important_**` | **extremely _important_** |
| Strikethrough | `~~strikethrough~~` | ~~strikethrough~~ |

### Headings

```
# Heading 1
## Heading 2
### Heading 3
```

All heading levels (H1 through H6) render at the **same visual size** in Slack. There is no visual hierarchy. Use headings for semantic separation only, not for visual nesting. If hierarchy matters, prefer:

- **Bold labels** for sub-sections
- `---` dividers to separate major sections
- Distinct blocks per section

### Links

```
[link text](https://example.com)
```

Standard markdown hyperlinks are supported.

### Lists

**Unordered:**
```
- first item
- second item
- third item
```

**Ordered:**
```
1. first item
2. second item
3. third item
```

### Task lists

```
- [ ] incomplete task
- [x] completed task
```

Renders with checkboxes.

### Code

**Inline:**
```
`code snippet`
```

**Fenced block (no language):**
````
```
code block here
```
````

**Fenced block with syntax highlighting:**
````
```python
print("hello")
```
````

Supported languages include common ones (python, javascript, typescript, json, bash, sql, yaml, etc.).

### Blockquote

```
> This is a block quote.
```

### Divider / horizontal rule

```
---
```

Renders as a visible horizontal divider line. Useful for separating sections when heading hierarchy is not meaningful.

### Tables

```
| Column 1 | Column 2 |
| -------- | -------- |
| A        | B        |
```

Renders as a formatted table.

---

## Unsupported / converted syntax

### Images — convert to links

`![alt text](https://example.com/image.png)` **does not render as an image**. Slack translates it into a hyperlink: `[alt text](https://example.com/image.png)`.

**Always convert image syntax explicitly:**

```
Before:  ![Dashboard screenshot](https://cdn.example.com/screenshot.png)
After:   [Dashboard screenshot](https://cdn.example.com/screenshot.png)
```

Or use a plain URL if the alt text adds no value.

### HTML tags — remove or convert

Raw HTML (e.g. `<br>`, `<strong>`, `<ul>`) is not rendered in Slack markdown blocks. Remove it or convert it to equivalent markdown syntax.

### Nested lists

Deeply nested lists (3+ levels) may not render cleanly. Prefer flattening to 2 levels maximum.

---

## Block Kit payload structure

```json
{
  "blocks": [
    {
      "type": "markdown",
      "text": "**Your content here**\n\nMore content..."
    },
    {
      "type": "markdown",
      "text": "A second section if needed."
    }
  ]
}
```

- `type` must be `"markdown"` (lowercase)
- `text` contains the markdown string
- `block_id` is silently ignored — omit it to keep the payload clean
- Multiple blocks are displayed sequentially in the message

---

## Conversion checklist

Before finalising the payload, verify:

- [ ] No `![...](...)` image syntax present — all images converted to links
- [ ] No raw HTML tags in the text
- [ ] Total character count across all `text` fields ≤ 12,000
- [ ] No `block_id` fields on markdown blocks
- [ ] Long content split at logical boundaries into separate blocks
- [ ] Heading hierarchy warnings surfaced to the user if the original relied on H1/H2/H3 for visual structure
