---
name: hello-world
description: >
  Output a multi-line ASCII art banner/sign that reads "HELLO WORLD" using only
  plain ASCII characters (no Unicode, no emoji, no box-drawing characters).
  Use this skill whenever the user asks for a hello world sign, hello world in
  ASCII, a hello-world banner, or wants to see hello world displayed as ASCII
  art — even if they just say "show me hello world in ascii", "print hello world
  as a sign", or "hello world ascii mode".
---

# Hello World ASCII Skill

When this skill is triggered, output a bold, multi-line ASCII art sign that spells out **HELLO WORLD** using only printable ASCII characters (character codes 32–126). No Unicode box-drawing characters, no emoji, no non-ASCII symbols of any kind.

## Why ASCII-only matters

The whole point of "ASCII mode" is that the output looks identical in any plain-text terminal, log file, or monospace environment — no rendering surprises. Stick to characters that every system can display: letters, digits, and punctuation marks like `*`, `#`, `/`, `\`, `|`, `_`, `-`, `+`, `(`, `)`, `.`.

## Output rules

1. Use block-letter style built from ASCII characters — each letter should be several rows tall (4–7 rows is a good target).
2. Separate each letter with at least one column of space so the word is readable.
3. Put a simple border around the whole sign using `-`, `|`, `+` or `*` characters.
4. Keep the total width under 80 characters so it fits in a standard terminal.
5. Output only the sign — no prose before or after unless the user asks for an explanation.

## Fallback

If the request is ambiguous (e.g., "just show me the skill"), default to outputting the standard `HELLO WORLD` sign.

## Examples

**Prompt:** "hello world ascii sign"
**Expected output style:**
```
+---------------------------------------------------------------+
|  #  #  ####  #     #     ###     #   #  ###  ####  #    ####  |
|  #  #  #     #     #    #   #    #   #  #  # #     #    #  #  |
|  ####  ###   #     #    #   #    # # #  #  # ###   #    #  #  |
|  #  #  #     #     #    #   #    # # #  #  # #     #    #  #  |
|  #  #  ####  ####  ####  ###      # #   ###  #     #### ####  |
+---------------------------------------------------------------+
```

**Prompt:** "print hello world as a sign in ascii mode"
**Expected output style:** same block-letter banner as above.

**Prompt:** "just give me hello world ascii"
**Expected output style:** same block-letter banner — output only the sign.

## What NOT to do

- Do not output Unicode characters (╔, ║, ═, █, etc.).
- Do not add lengthy explanations before or after the sign.
- Do not skip the border — the border is part of the sign aesthetic.
- Do not use lowercase letters in the sign body (the block letters should read as uppercase `HELLO WORLD`).
