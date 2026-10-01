#!/usr/bin/env python3
"""One-off: convert always-open Q/A blocks inside modals into <details> accordions.

Matches a wrapper <div> holding exactly a question <p data-kr="Q. ..."> followed by an
answer <p>, and rewrites it as <details class="ed-faq"> keeping both data-kr/data-en pairs.
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
s = open(path, encoding="utf-8").read()

ATTRS = r"(?:\s+[\w:-]+=(?:\"[^\"]*\"|'[^']*'))*"
BLOCK = re.compile(
    r"<div class=\"(?P<wrap>[^\"]*)\">\s*"
    r"<p(?P<qattrs>" + ATTRS + r")\s*>(?P<q>(?:(?!</p>).)*)</p>\s*"
    r"<p(?P<aattrs>" + ATTRS + r")\s*>(?P<a>(?:(?!</p>).)*)</p>\s*"
    r"</div>",
    re.S,
)


def drop_class(attrs):
    return re.sub(r"\s+class=(?:\"[^\"]*\"|'[^']*')", "", attrs)


def convert(m):
    q_kr = re.search(r"data-kr=(\"[^\"]*\"|'[^']*')", m.group("qattrs"))
    if not q_kr or not q_kr.group(1)[1:].lstrip().startswith("Q."):
        return m.group(0)
    return (
        '<details class="ed-faq">'
        f'<summary><span class="ed-faq-q"{drop_class(m.group("qattrs"))}>{m.group("q").strip()}</span>'
        '<span class="ed-plus" aria-hidden="true"></span></summary>'
        f'<div class="ed-faq-a"{drop_class(m.group("aattrs"))}>{m.group("a").strip()}</div>'
        "</details>"
    )


out, n = BLOCK.subn(convert, s)
count = out.count('<details class="ed-faq">')
open(path, "w", encoding="utf-8").write(out)
print(f"converted {count} Q/A blocks")
