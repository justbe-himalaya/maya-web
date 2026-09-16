#!/usr/bin/env python3
"""One-off: remove decorative emoji from index.html markup (not from <script> blocks).

Emoji are removed from static text AND data-kr / data-en attributes together, so the
language toggle never brings them back. Elements whose only content was emoji are
removed entirely. A few symbols are converted instead of deleted to keep meaning.
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
src = open(path, encoding="utf-8").read()

REPLACE = {"⚠️": "※", "⚠": "※", "➡️": "→", "➡": "→", "⏺️": "·", "⏺": "·"}
EMOJI = re.compile(
    "(?:[\U0001F1E6-\U0001F1FF]{2}"            # flags
    "|[\U0001F000-\U0001FAFF☀-➿⬀-⯿⏩-⏺]"
    "[️\U0001F3FB-\U0001F3FF]*"
    "(?:‍[♀♂☀-➿\U0001F000-\U0001FAFF]️?)*)"
)
KEEP = set("★✓✕✔")
SENT = "\x00"


def strip_chunk(chunk):
    for k, v in REPLACE.items():
        chunk = chunk.replace(k, v)
    chunk = EMOJI.sub(lambda m: m.group(0) if m.group(0) in KEEP else SENT, chunk)
    # elements (double- or single-quoted attrs) that contained only emoji -> drop
    empty = re.compile(r"<(span|div|i)((?:\s+(?:class|aria-hidden|role)=(?:\"[^\"]*\"|'[^']*'))*)\s*>\s*(?:\x00\s*)+</\1>\s*")
    prev = None
    while prev != chunk:
        prev = chunk
        chunk = empty.sub("", chunk)
    chunk = re.sub(r"\x00(?:\s|&nbsp;)*", "", chunk)
    return chunk


out, last = [], 0
for m in re.finditer(r"<script\b.*?</script>", src, flags=re.S):
    out.append(strip_chunk(src[last:m.start()]))
    out.append(m.group(0))
    last = m.end()
out.append(strip_chunk(src[last:]))
res = "".join(out)
# <head> meta/title content must not change
assert res[: res.index("<body")].count("<meta") == src[: src.index("<body")].count("<meta")
open(path, "w", encoding="utf-8").write(res)
print("done")
