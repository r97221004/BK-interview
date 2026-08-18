#!/usr/bin/env python3
"""Verify the question set: numbering, links, required sections, consistency.

Exits non-zero if anything fails, so it can gate a commit.
"""
import os
import re
import glob
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SECTIONS = ["In One Sentence", "Answer Shape", "Full Spoken Answer"]
# Optional, and always last: the lookup material - comparison tables, code
# samples - that would otherwise be read aloud badly. It is deliberately exempt
# from the bilingual paragraph rules, which only govern the spoken sections.
OPTIONAL_LAST = "Quick Reference"
STATUSES = ["Outline", "Draft", "Review", "Complete"]

NAV = re.compile(r"^---\n\n\| ⬅ Previous", re.M)


def sections(text):
    """Level-two sections of a question file, in order, minus the generated footer."""
    out = []
    for part in re.split(r"^## ", NAV.split(text)[0], flags=re.M)[1:]:
        name, _, rest = part.partition("\n")
        out.append((name.strip(), rest))
    return out


def paragraphs(text):
    """Non-empty Markdown paragraphs, which is how the bilingual pairs are counted."""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

failures = []


def check(label, bad, detail=lambda x: str(x)):
    if bad:
        failures.append(label)
        print("FAIL %s (%d)" % (label, len(bad)))
        for b in bad[:10]:
            print("       ", detail(b))
    else:
        print("ok   %s" % label)


files = sorted(glob.glob("docs/*/q*.md"))
body = {int(re.match(r"q(\d+)-", os.path.basename(f)).group(1)): open(f).read() for f in files}
nums = sorted(body)
total = len(nums)

check("no duplicate numbers", [n for n in nums if nums.count(n) > 1])

# Every link resolves - including directory links, which a .md-only check misses.
bad_links = []
for f in ["README.md"] + files + ["docs/_template-question.md", "docs/_glossary.md"]:
    base = os.path.dirname(f)
    for m in re.finditer(r"\]\((?!https?:|#)([^)]+)\)", open(f).read()):
        t = m.group(1)
        if "<" in t:
            continue
        target = os.path.normpath(os.path.join(base, t.split("#")[0]))
        if not os.path.exists(target):
            bad_links.append("%s -> %s" % (f, t))
check("all links resolve (files and directories)", bad_links)

sec = {n: sections(body[n]) for n in nums}
names = {n: [s for s, _ in sec[n]] for n in nums}

check("all required sections present",
      [(n, s) for n in nums for s in SECTIONS if s not in names[n]],
      lambda x: "Q%02d missing %s" % x)
check("sections appear in the expected order",
      [n for n in nums if names[n] not in (SECTIONS, SECTIONS + [OPTIONAL_LAST])],
      lambda n: "Q%02d has %s" % (n, " / ".join(names[n])))
check("Quick Reference carries a table or a code block",
      [n for n in nums if OPTIONAL_LAST in names[n] and
       not re.search(r"^\|---|^```", dict(sec[n])[OPTIONAL_LAST], re.M)],
      lambda n: "Q%02d Quick Reference is prose; fold it into the answer" % n)

check("status is one of the four progress values",
      [n for n in nums
       if (re.search(r"\*\*Status:\*\* (\w+)", body[n]) or [None]) and
       re.search(r"\*\*Status:\*\* (\w+)", body[n]).group(1) not in STATUSES],
      lambda n: "Q%02d" % n)


def has_cjk(text):
    return bool(re.search(r"[㐀-䶿一-鿿]", text))


# The interview format is bilingual and intentionally compact: one English and
# one Traditional Chinese paragraph for the short sections, then three or four
# matching paragraph pairs for the complete spoken answer.
bad_one_sentence_shape = []
bad_answer_shape = []
bad_spoken_shape = []
bad_language_order = []
for n in nums:
    text = dict(sec[n])
    one = paragraphs(text.get("In One Sentence", ""))
    shape = paragraphs(text.get("Answer Shape", ""))
    spoken = paragraphs(text.get("Full Spoken Answer", ""))

    if len(one) != 2:
        bad_one_sentence_shape.append((n, len(one)))
    if len(shape) != 2:
        bad_answer_shape.append((n, len(shape)))
    if len(spoken) not in (6, 8):
        bad_spoken_shape.append((n, len(spoken)))

    for section_name, section_paras in (("In One Sentence", one),
                                        ("Answer Shape", shape),
                                        ("Full Spoken Answer", spoken)):
        for i, paragraph in enumerate(section_paras):
            expected_cjk = i % 2 == 1
            if has_cjk(paragraph) != expected_cjk:
                bad_language_order.append((n, section_name, i + 1))

check("In One Sentence has one bilingual paragraph pair",
      bad_one_sentence_shape, lambda x: "Q%02d has %d paragraphs" % x)
check("Answer Shape has one bilingual paragraph pair", bad_answer_shape,
      lambda x: "Q%02d has %d paragraphs" % x)
check("Full Spoken Answer has three or four bilingual paragraph pairs",
      bad_spoken_shape, lambda x: "Q%02d has %d paragraphs" % x)
check("bilingual paragraphs alternate English then Traditional Chinese",
      bad_language_order, lambda x: "Q%02d %s paragraph %d" % x)

# README table agrees with each file's header.
readme = open("README.md").read()
tbl = {}
declared = []
for section in re.finditer(
        r"^### Importance (\d+)/10( \((\d+) questions?\))?\n(.*?)"
        r"(?=^### Importance|^## Progress Model)", readme, re.M | re.S):
    score = int(section.group(1))
    rows = re.findall(r"^\| \[.*?\]\(docs/[^/]+/q(\d+)-", section.group(4), re.M)
    for m in rows:
        tbl[int(m)] = score
    if section.group(3) is not None:
        declared.append((score, int(section.group(3)), len(rows)))
check("importance headings count their own rows",
      [d for d in declared if d[1] != d[2]],
      lambda d: "Importance %d/10 says %d, table has %d" % d)
check("README has a row per question", [n for n in nums if n not in tbl],
      lambda n: "Q%02d missing from table" % n)
check("importance matches between README and file header",
      [n for n in nums if n in tbl and
       tbl[n] != int(re.search(r"\*\*Importance:\*\* (\d+)/10", body[n]).group(1))],
      lambda n: "Q%02d" % n)
check("status matches between README and file header",
      [n for n in nums
       if not re.search(r"\| \[[^\]]*\]\(%s\) \| [^|]+ \| [^|]+ \| %s \|"
                        % (re.escape([f for f in files if "/q%02d-" % n in f][0]),
                           re.search(r"\*\*Status:\*\* (\w+)", body[n]).group(1)), readme)],
      lambda n: "Q%02d" % n)

# The prev/next footers must form one unbroken chain in README order, so every
# question is reachable by walking and nobody lands on a dead end.
order = []
for section in re.finditer(
        r"^### Importance \d+/10.*?\n(.*?)(?=^### Importance|^## Progress Model)",
        readme, re.M | re.S):
    order += re.findall(r"^\| \[.*?\]\((docs/[^)]+)\)", section.group(1), re.M)


def footer_row(i):
    """The one table row question i's footer must end with."""
    here = order[i]

    def link(j):
        title = open(order[j]).readline().strip()[2:]
        return "[%s](%s)" % (title, os.path.relpath(order[j], os.path.dirname(here))
                             .replace(os.sep, "/"))

    prev = "*(first question)*" if i == 0 else link(i - 1)
    nxt = "*(last question)*" if i == len(order) - 1 else link(i + 1)
    home = "[All %d questions](%s)" % (
        total, os.path.relpath("README.md", os.path.dirname(here)).replace(os.sep, "/"))
    return "| %s | %s | %s |" % (prev, home, nxt)


bad_nav = []
for i, path in enumerate(order):
    want = footer_row(i)
    if want not in open(path).read():
        bad_nav.append("%s footer is not %s" % (path, want))
check("prev/next footers chain in README order", bad_nav)

# A term's home question is advertised in the glossary as the place it is
# explained in full, so the term has to actually appear there. Without this,
# a promise can rot silently: the anchor still resolves and the wording is
# fine, but the reader who follows the link never meets the word again.
sys.path.insert(0, os.path.join(ROOT, "tools"))
from build import TERM_RE, HOME, path_of, DISPLAY  # noqa: E402

homeless = []
for anchor, rx in TERM_RE.items():
    home = HOME[anchor]
    prose = NAV.split(open(path_of(home)).read())[0]
    prose = re.sub(r"\*\*New to these terms\?\*\* .*\n", "", prose)
    if not re.search(rx, prose, re.I):
        homeless.append((anchor, home))
check("every glossary term appears in the question it is homed to", homeless,
      lambda x: "%s is homed at Q%02d but never appears there" % (DISPLAY[x[0]], x[1]))

# Glossary anchors referenced by questions must exist.
anchors = set(re.findall(r"^### (.+)$", open("docs/_glossary.md").read(), re.M))
slugs = {re.sub(r"[^a-z0-9]+", "-", a.lower()).strip("-") for a in anchors}
used = {m for n in nums for m in re.findall(r"_glossary\.md#([\w-]+)", body[n])}
check("glossary anchors exist", sorted(used - slugs), lambda a: "#%s not in glossary" % a)

print("\n%d questions checked. %s"
      % (total, "ALL PASS" if not failures else "%d FAILURES" % len(failures)))
sys.exit(1 if failures else 0)
