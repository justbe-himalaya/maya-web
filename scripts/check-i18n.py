#!/usr/bin/env python3
"""Validate the data-kr / data-en bilingual markup in index.html.

Checks:
  1. every element with data-kr also has data-en (and vice versa)
  2. no data-tagged element is nested inside another data-tagged element
     (the parent's innerHTML swap would destroy the child)
  3. the static text of each data-tagged element matches its data-kr text
     (otherwise toggling KR -> EN -> KR silently reverts edits)

Usage: python3 scripts/check-i18n.py [path/to/index.html]
Exit code is non-zero when any problem is found.
"""
import html
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


def norm(s):
    s = re.sub(r"</?[a-zA-Z][^>]*>", " ", html.unescape(s))
    return re.sub(r"\s+", "", s)


class Checker(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.stack = []  # [tag, tagged, line, kr, start_offset]
        self.problems = []
        self.pairs = 0
        self.line_offsets = [0]
        for m in re.finditer("\n", src):
            self.line_offsets.append(m.end())

    def pos(self):
        line, col = self.getpos()
        return self.line_offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        has_kr, has_en = "data-kr" in a, "data-en" in a
        line = self.getpos()[0]
        if has_kr != has_en:
            self.problems.append(f"L{line}: <{tag}> has only {'data-kr' if has_kr else 'data-en'}")
        tagged = has_kr or has_en
        if tagged:
            self.pairs += 1
            parent = next((s for s in reversed(self.stack) if s[1]), None)
            if parent:
                self.problems.append(f"L{line}: <{tag}> data-tagged inside data-tagged <{parent[0]}> (L{parent[2]})")
        if tag in VOID:
            return
        end = self.pos() + len(self.get_starttag_text())
        self.stack.append([tag, tagged, line, a.get("data-kr"), end])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                t, tagged, line, kr, start = self.stack[i]
                del self.stack[i:]
                if tagged and kr is not None:
                    inner = self.src[start:self.pos()]
                    if norm(inner) != norm(kr):
                        self.problems.append(f"L{line}: <{t}> static text differs from data-kr")
                return


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    src = open(path, encoding="utf-8").read()
    # Only check markup outside <script> blocks.
    masked = re.sub(r"(<script\b[^>]*>)(.*?)(</script>)",
                    lambda m: m.group(1) + re.sub(r"[^\n]", " ", m.group(2)) + m.group(3),
                    src, flags=re.S)
    c = Checker(masked)
    c.feed(masked)
    for p in c.problems:
        print(p)
    print(f"{c.pairs} data-tagged elements, {len(c.problems)} problems")
    sys.exit(1 if c.problems else 0)


if __name__ == "__main__":
    main()
