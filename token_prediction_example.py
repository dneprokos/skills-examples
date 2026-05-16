"""
Demonstrates how an LLM iteratively predicts tokens one at a time.

An LLM does not "think" the full answer and then output it — it predicts
the next token from the current context, appends it, and repeats.
Streaming exposes this process in real time.

Setup:
    pip install anthropic python-dotenv
    cp .env.example .env
    # then fill in your key in .env

Run:
    python token_prediction_example.py
"""

import time

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-6"

client = anthropic.Anthropic()


def stream_with_token_display(prompt: str) -> str:
    """Stream Claude's response, printing each chunk on its own line, then the full text."""
    print(f"\nPrompt: {prompt}")
    print("-" * 60)
    print("Chunks arriving one per line (each line = one streaming delta):\n")

    full_text = ""
    token_count = 0
    start_time = time.perf_counter()

    with client.messages.stream(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text_delta in stream.text_stream:
            # Represent whitespace visually so newline/space chunks are visible.
            display = repr(text_delta)[1:-1]  # e.g. '\n' → '\\n', ' ' → ' '
            print(f"  [{token_count + 1:>3}] {display!r}", flush=True)
            full_text += text_delta
            token_count += 1

    elapsed = time.perf_counter() - start_time
    final = stream.get_final_message()

    print(f"\n{'=' * 60}")
    print("Full response assembled from chunks:\n")
    print(full_text)

    print(f"\n{'=' * 60}")
    print(f"Streaming deltas received : {token_count}")
    print(f"Output tokens (API count) : {final.usage.output_tokens}")
    print(f"Input tokens              : {final.usage.input_tokens}")
    print(f"Wall-clock time           : {elapsed:.2f}s")
    print(
        f"Approx tokens/sec         : {final.usage.output_tokens / elapsed:.1f}"
    )
    return full_text


def interactive_session():
    """Simple REPL — type a prompt and watch Claude predict tokens live."""
    print("=" * 60)
    print(" LLM Token Prediction Demo")
    print("=" * 60)
    print(
        "Each chunk printed to the terminal is one streaming delta —\n"
        "a window into how the model predicts the next token from\n"
        "everything it has generated so far.\n"
    )
    print("Type a prompt and press Enter. Type 'quit' to exit.\n")

    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not prompt:
            continue
        if prompt.lower() in {"quit", "exit", "q"}:
            print("Bye!")
            break

        stream_with_token_display(prompt)
        print()


if __name__ == "__main__":
    interactive_session()
