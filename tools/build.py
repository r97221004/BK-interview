#!/usr/bin/env python3
"""Rebuild the backend interview question set: stubs, glossary, and README."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from questions import Q, PARTS          # noqa: E402
from glossary import TERMS              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART_NAME = dict(PARTS)

BY_NUM = {q["num"]: q for q in Q}

# Importance 1-10, frequency-first: how often the question is actually asked,
# not how hard it is. A fundamental that opens most interviews outranks a
# subtle question that impresses on the rare occasion it appears.
IMPORTANCE = {
    1: 10, 11: 10, 21: 10,
    2: 9, 4: 9, 7: 9, 12: 9, 22: 9, 23: 9, 25: 9, 31: 9, 32: 9, 41: 9,
    3: 8, 5: 8, 6: 8, 8: 8, 13: 8, 14: 8, 24: 8, 26: 8, 27: 8, 33: 8,
    51: 8, 52: 8,
    9: 7, 15: 7, 34: 7, 42: 7,
}
assert set(IMPORTANCE) == set(BY_NUM), "importance must cover every question"

TOTAL = len(Q)

# How each glossary term is spelled in prose, for the "New to these terms?" line.
TERM_RE = {
    "endpoint": r"\bendpoints?\b", "rest": r"\bREST(ful)?\b", "resource": r"\bresources?\b",
    "idempotent": r"\bidempotenc?[ty]\b", "statelessness": r"stateless(ness)?",
    "status-code": r"status codes?", "persistent-connection": r"persistent connections?|keep-alive",
    "websocket": r"\bWebSockets?\b", "api-versioning": r"\bversioning\b",
    "breaking-change": r"breaking changes?", "presigned-url": r"presigned URLs?",
    "cookie": r"\bcookies?\b", "session": r"\bsessions?\b", "jwt": r"\bJWTs?\b",
    "same-origin-policy": r"same-origin policy", "cors": r"\bCORS\b",
    "preflight": r"\bpreflight\b", "csrf": r"\bCSRF\b", "samesite": r"\bSameSite\b",
    "xss": r"\bXSS\b", "csp": r"Content Security Policy|\bCSP\b",
    "output-encoding": r"output encoding", "sql-injection": r"SQL injection",
    "prepared-statement": r"prepared statements?|parameterized quer",
    "orm": r"\bORMs?\b", "least-privilege": r"least privilege",
    "acid": r"\bACID\b", "normalization": r"normaliz(ation|ed|e)\b",
    "denormaliz": r"denormaliz", "partitioning": r"partition(ing|s|ed)?\b",
    "sharding": r"shard(ing|s|ed)?\b", "index": r"\bindexe?s\b",
    "cache": r"\bcach(e|es|ing|ed)\b", "redis": r"\bRedis\b",
    "horizontal-scaling": r"horizontal(ly)? scal", "load-balancer": r"load balancers?",
    "cdn": r"\bCDN\b", "backpressure": r"backpressure|load shedding",
    "gil": r"\bGIL\b|Global Interpreter Lock", "event-loop": r"event loop",
    "hash-table": r"hash tables?", "dynamic-array": r"dynamic arrays?",
    "containerization": r"container(ization|s|ized)?\b",
    "multi-stage-build": r"multi-stage", "unit-test": r"unit tests?",
    "integration-test": r"integration tests?", "structured-logging": r"structured logging",
    "observability": r"observability", "tls": r"\bTLS\b|\bHTTPS\b",
    "rate-limiting": r"rate limit(ing|s|ed)?", "oauth2": r"OAuth ?2(\.0)?",
}
# "denormaliz" has no glossary entry of its own; it points at the normalization
# neighbourhood, so drop any regex key that is not a real term.
TERM_RE = {k: v for k, v in TERM_RE.items() if k in {t[0] for t in TERMS}}

HOME = {a: h for a, _, h, _ in TERMS}
DISPLAY = {a: d for a, d, _, _ in TERMS}


def slugify(heading):
    """Match GitHub's heading-to-anchor rule so links cannot drift from headings."""
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


ANCHOR = {a: slugify(d) for a, d, _, _ in TERMS}


def path_of(num):
    q = BY_NUM[num]
    return "docs/%s/q%02d-%s.md" % (q["dir"], num, q["slug"])


def reading_order():
    """Question numbers in README order: importance first, then number.

    The prev/next footers follow this, so walking them is the same route as
    reading the README table top to bottom.
    """
    return [q["num"] for q in sorted(Q, key=lambda x: (-IMPORTANCE[x["num"]], x["num"]))]


def nav_footer(num):
    """Previous / home / next as one table. The chain is what makes every
    question reachable, so there is no separate Related section."""
    order = reading_order()
    i = order.index(num)
    here = path_of(num)

    def link(j):
        t = BY_NUM[order[j]]
        return "[Q%02d: %s](%s)" % (
            order[j], t["title"],
            os.path.relpath(path_of(order[j]), os.path.dirname(here)).replace(os.sep, "/"))

    prev = "*(first question)*" if i == 0 else link(i - 1)
    nxt = "*(last question)*" if i == len(order) - 1 else link(i + 1)
    home = "[All %d questions](%s)" % (
        len(order), os.path.relpath("README.md", os.path.dirname(here)).replace(os.sep, "/"))
    return ("---\n\n"
            "| ⬅ Previous | Home | Next ➡ |\n"
            "|---|---|---|\n"
            "| %s | %s | %s |\n" % (prev, home, nxt))


MAX_TERMS = 5


def terms_used(num, body):
    """Glossary terms this question uses but does not itself define.

    Only the prose counts, so two generated regions are stripped first. The
    navigation footer quotes the titles of the neighbouring questions, which
    would credit this question with every term those titles contain. And the
    terms line itself is made of term names: leaving it in makes the previous
    build's output an input to this one, which locks the line in place forever.
    """
    prose = body.split("---\n\n| ⬅ Previous")[0]
    prose = re.sub(r"\*\*New to these terms\?\*\* .*\n", "", prose)
    return {a for a, rx in TERM_RE.items()
            if HOME.get(a) not in (None, num) and re.search(rx, prose, re.I)}


def terms_line(used, freq, total):
    """Point at the terms a reader is least likely to know already.

    A term appearing in most questions is not news by the third page - linking
    it every time teaches readers to skip the line. So drop the ubiquitous ones,
    then keep the rarest few, which are the ones worth flagging.
    """
    used = [a for a in used if freq[a] <= total * 0.5]
    if not used:
        return None
    order = [t[0] for t in TERMS]
    used.sort(key=lambda a: (freq[a], order.index(a)))
    used = sorted(used[:MAX_TERMS], key=order.index)
    links = ", ".join("[%s](../_glossary.md#%s)" % (DISPLAY[a].split(" /")[0].lower(), ANCHOR[a])
                      for a in used)
    return "**New to these terms?** %s\n" % links


def linkify(text, self_anchor):
    """Link the first mention of each other glossary term inside a definition."""
    spans = []
    for a, rx in TERM_RE.items():
        if a == self_anchor:
            continue
        m = re.search(rx, text, re.I)
        if m:
            spans.append((m.start(), m.end(), a))
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    out, last = [], 0
    for start, end, a in spans:
        if start < last:
            continue  # overlaps an earlier link, such as "session" inside "session ID"
        out.append(text[last:start])
        out.append("[%s](#%s)" % (text[start:end], ANCHOR[a]))
        last = end
    out.append(text[last:])
    return "".join(out)


ANSWER_SHAPE = """## Answer Shape

<!-- TODO: describe the speaking order: direct answer, plain-language mechanism,
one concrete example or comparison, then the practical consequence. -->

<!-- TODO：說明口述順序：直接回答、白話機制、一個具體例子或比較，以及實務影響。 -->
"""


def stub(q, tl):
    n = q["num"]
    body = "\n".join([
        ANSWER_SHAPE,
        "## Full Spoken Answer\n",
        "<!-- TODO: English paragraph 1. -->\n\n"
        "<!-- TODO：繁體中文段落 1。 -->\n\n"
        "<!-- TODO: English paragraph 2. -->\n\n"
        "<!-- TODO：繁體中文段落 2。 -->\n\n"
        "<!-- TODO: English paragraph 3. -->\n\n"
        "<!-- TODO：繁體中文段落 3。 -->\n",
        nav_footer(n),
    ])
    head = ["# Q%02d: %s\n" % (n, q["title"]), "> %s\n" % q["tests"],
            "**Part:** %s | **Importance:** %d/10 | **Status:** Outline\n"
            % (PART_NAME[q["dir"]], IMPORTANCE[n])]
    if tl:
        head.append(tl)
    head += ["## In One Sentence\n",
             "<!-- TODO: one plain-language English sentence for someone meeting this topic "
             "for the first time. -->\n\n"
             "<!-- TODO：給第一次接觸這個主題的讀者，用一句繁體中文白話回答。 -->\n"]
    return "\n".join(head + [body])


def glossary_md():
    out = ["# Glossary\n",
           "> The vocabulary the answers assume. Every term links to the question that "
           "explains it properly.\n",
           "Questions link here on first use, so you can read in any order without hitting a "
           "term you have not met yet. If backend work is new to you, skimming this once first "
           "is worth the five minutes.\n"]
    for anchor, display, home, definition in TERMS:
        out.append("### %s\n" % display)
        out.append("%s\n" % linkify(definition, anchor))
        out.append("Explained in full: [Q%02d](%s).\n"
                   % (home, path_of(home).replace("docs/", "")))
    return "\n".join(out)


BADGES = """![Backend](https://img.shields.io/badge/Backend-Interview%20Prep-0F766E)
![Questions](https://img.shields.io/badge/Questions-29-2563EB)
![Format](https://img.shields.io/badge/Format-Q%26A-5D3FD3)
![Language](https://img.shields.io/badge/Language-EN%20%2B%20%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87-D97706)"""

README_HEAD = """# Backend Engineering Interview Questions

> A focused set of 29 high-frequency backend interview questions, answered bilingually and from the mechanism up.

%s

Backend interview questions are easy to answer badly. Most have a one-line answer that sounds right and reveals nothing, and the interviewer is listening for the layer underneath: what the protocol actually guarantees, where the state really lives, and what breaks first under load.

This repository is not a backend tutorial and not a framework reference. It is a set of questions selected for backend-engineering interviews. Each question carries a plain-language definition, a short speaking outline, and a complete spoken answer for follow-up - every paragraph in English and Traditional Chinese, because the interview may be in either.

## Why This Guide

Most material teaches the framework. Interviews test the model underneath it: why HTTP being stateless forces a design decision, why a prepared statement stops injection when escaping does not, why the database is the bottleneck before the application is.

That gap is why an engineer who ships APIs daily can still stall on "why does the browser send that cookie at all?" - the daily work never required the answer.

The list is deliberately not senior-only. Interviews open with fundamentals - what an endpoint is, what REST means, SQL versus NoSQL - and those are asked at every level, so they are the highest-frequency questions that exist. A senior candidate is expected to answer them crisply and then go one layer deeper than a junior would.

## If You Are New to Backend Work

The answers are written so you can start anywhere, and two things make that work:

- Every question opens with **In One Sentence** - a plain-language answer with no jargon, before any interview framing.
- Terms carry a link to the [glossary](docs/_glossary.md) the first time a question uses one it does not itself explain, so you never have to have read something else first.

### The Request Mental Model

Almost every question in this repository is about one of the arrows below. The rest of the guide explains what each one really does.

```mermaid
---
config:
  look: handDrawn
  theme: default
  themeVariables:
    fontFamily: '"Comic Sans MS", "Comic Sans", "Segoe Print", "Bradley Hand", cursive'
    lineColor: '#FFFFFF'
    edgeLabelBackground: '#475569'
  themeCSS: |
    .edgeLabel, .edgeLabel p, .edgeLabel span { color: #FFFFFF !important; }
---
flowchart LR
    client["Client"] -->|"HTTP request"| lb["Load balancer"]
    lb -->|"routes to an instance"| app["API server<br/>endpoint + handler"]
    app -->|"identify the caller"| auth["Session / JWT"]
    app -->|"read through"| cache[("Cache")]
    cache -->|"on a miss"| db[("Database")]
    app -->|"HTTP response"| client

    classDef edgeStyle fill:#0F172A,stroke:#2563EB,stroke-width:2px,color:#FFFFFF
    classDef svcStyle fill:#D97706,stroke:#92400E,stroke-width:3px,color:#FFFFFF
    classDef dataStyle fill:#0F172A,stroke:#16A34A,stroke-width:2px,color:#FFFFFF
    class client,lb,auth edgeStyle
    class app svcStyle
    class cache,db dataStyle
```

> **In plain language:** a request arrives, gets routed to one of many identical servers, proves who it is, reads data through a cache, and gets an answer back.

### A Beginner's Learning Order

Interview frequency and learning order are not the same. If backend work is new to you, follow the topics in this order, then use the links below to open a section.

```mermaid
---
config:
  look: handDrawn
  theme: default
  themeVariables:
    fontFamily: '"Comic Sans MS", "Comic Sans", "Segoe Print", "Bradley Hand", cursive'
    lineColor: '#FFFFFF'
    edgeLabelBackground: '#475569'
  themeCSS: |
    .edgeLabel, .edgeLabel p, .edgeLabel span { color: #FFFFFF !important; }
---
flowchart LR
    protocol["<b>1. The contract</b><br/>API &amp; HTTP"]
    state["<b>2. Where state lives</b><br/>Databases<br/>Security &amp; Auth"]
    operate["<b>3. Running it</b><br/>Architecture &amp; Scaling<br/>DevOps &amp; Deployment<br/>Testing &amp; Debugging"]
    protocol --> state --> operate

    classDef edgeStyle fill:#0F172A,stroke:#2563EB,stroke-width:2px,color:#FFFFFF
    classDef svcStyle fill:#D97706,stroke:#92400E,stroke-width:3px,color:#FFFFFF
    classDef workerStyle fill:#334155,stroke:#94A3B8,stroke-width:2px,color:#FFFFFF
    class protocol edgeStyle
    class state svcStyle
    class operate workerStyle
```

> **In plain language:** learn the conversation first, then where the data and the identity are kept, then how to keep the whole thing standing up.

%s

## What Each Question Covers

Each question file follows the same structure:

1. **In One Sentence** - the plain-language answer, for when you are meeting the topic for the first time.
2. **Answer Shape** - a short speaking order that moves from the direct answer to an example and a practical consequence.
3. **Full Spoken Answer** - the complete follow-up answer and a bank of details to select from, not a script to deliver in full.
4. **Quick Reference** - on some questions only: the comparison table or code sample worth revising from, kept out of the spoken sections because a table is not something you say out loud.
5. **Previous / Home / Next** - navigation through the interview-priority reading order.

### Which Layer to Answer With

The three sections are the same answer at increasing depth, so you can match the room. The Full Spoken Answer is deliberately longer than a good opening: select the relevant paragraphs when the interviewer follows up instead of reciting all of it.

| Layer | Reach for it when | Spoken length |
|---|---|---|
| **In One Sentence** | They only want to know whether you know the concept at all | about 8 seconds |
| **Answer Shape** | Your default opening. Follow the short speaking order, then stop | 30-50 seconds |
| **Full Spoken Answer** | They followed up, or clearly want the detail | select relevant detail; do not recite all of it |

The order is the point: lead with the answer, stop, and let the interviewer pull you deeper. A correct one-liner followed by silence beats a rambling explanation that never lands the answer.

### High-Frequency Shortcuts

Some interviewers combine several concepts into one question. These common wordings are already covered:

- **"How do you handle authentication?"** start with [Q21](docs/security-and-auth/q21-session-vs-jwt-authentication.md) for the trade-off, then use [Q24](docs/security-and-auth/q24-session-management.md) for the lifecycle and [Q22](docs/security-and-auth/q22-session-vs-cookie.md) if they ask what the cookie is actually carrying.
- **"What happens when I type a URL and hit enter?"** follow the request through [Q02](docs/api-and-http/q02-http-request-response-cycle.md), add routing from [Q03](docs/api-and-http/q03-what-is-an-api-endpoint.md), identity from [Q21](docs/security-and-auth/q21-session-vs-jwt-authentication.md), and the instance fan-out from [Q31](docs/architecture-and-scaling/q31-scaling-during-traffic-surge.md).
- **"Why is this endpoint slow?"** combine the diagnostic method in [Q52](docs/testing-and-debugging/q52-debugging-a-backend-application.md) with caching in [Q14](docs/databases/q14-redis-use-cases.md) and indexing in [Q15](docs/databases/q15-database-out-of-storage.md).
- **"XSS or CSRF?"** they are frequently asked back to back and confused: [Q25](docs/security-and-auth/q25-xss.md) is about your output, [Q26](docs/security-and-auth/q26-csrf.md) is about the browser's credentials.

## The 29 Questions

Ordered by importance, highest first. Read top to bottom and you cover the questions that actually decide interviews before the ones that rarely come up.

**Importance** is a 1-10 estimate of how often the question is asked, across junior and senior interviews alike. Frequency is the dominant factor - a fundamental that opens almost every interview scores higher than a subtle question that impresses when it appears but usually does not. It is not a difficulty rating.
"""

README_TAIL = """
## Progress Model

| Status | Meaning |
|---|---|
| Outline | The question exists and its scope is defined. |
| Draft | The answer has a complete first pass and can be read end to end. |
| Review | The answer is being checked for clarity, correctness, and interview usefulness. |
| Complete | The answer is polished and stable. |

## Who This Is For

- Backend engineers preparing for interviews, in English or in Traditional Chinese.
- Engineers who build APIs daily but have never had to explain them out loud.
- Anyone who can ship a working endpoint but would stall on why it works.
- Interviewers looking for questions that separate familiarity from understanding.

## Prerequisites

Comfort with one backend language and the shell. You should know what a function, a process, and an environment variable are. The Python-specific questions assume you have written Python, but the concepts behind them transfer.

Everything else is explained here or in the [glossary](docs/_glossary.md).

## How to Use This Guide

1. Read the table top to bottom. It is ordered by importance, so if you stop halfway you have still covered the half that matters most.
2. For a systematic pass instead, follow the learning-order map above - the contract first, then where state lives, because the later answers build on both.
3. Jump directly to a question when preparing for a specific topic, or when a real incident sent you here.
4. Practice out loud in the Answer Shape order: direct answer, plain-language explanation, example, practical consequence. Time yourself - a good opening is 30 to 50 seconds before the follow-up.
5. Then close the file and answer again without looking. The goal is natural delivery, not memorized wording.

## Tooling

The README, the glossary, and every navigation footer are generated. Edit the data, not the output:

```bash
python3 tools/build.py    # regenerate stubs, glossary, README, nav footers
python3 tools/check.py    # verify structure, links, numbering, bilingual shape
```

See [tools/README.md](tools/README.md) for what each module owns.
"""


def status_of(num):
    """The question's real status, so the README table cannot drift from the files."""
    p = os.path.join(ROOT, path_of(num))
    if os.path.exists(p):
        m = re.search(r"\*\*Status:\*\* (\w+)", open(p).read())
        if m:
            return m.group(1)
    return "Outline"


def topic_nav():
    """A compact generated topic grid beside the learning-order map."""
    links = []
    for i, (d, name) in enumerate(PARTS, 1):
        ns = [q["num"] for q in Q if q["dir"] == d]
        links.append("**%d.** [%s](docs/%s/) · %d question%s"
                     % (i, name, d, len(ns), "" if len(ns) == 1 else "s"))
    rows = ["| %s | %s | %s |" % tuple(links[i:i + 3]) for i in range(0, len(links), 3)]
    return "\n".join(["**Open a topic:**", "", "| | | |", "|---|---|---|"] + rows)


def readme():
    out = [README_HEAD % (BADGES, topic_nav())]
    ranked = sorted(Q, key=lambda x: (-IMPORTANCE[x["num"]], x["num"]))
    for score in sorted(set(IMPORTANCE.values()), reverse=True):
        rows = [q for q in ranked if IMPORTANCE[q["num"]] == score]
        out.append("### Importance %d/10 (%d question%s)\n"
                   % (score, len(rows), "" if len(rows) == 1 else "s"))
        out.append("| Question | Part | Focus | Status |")
        out.append("|---|---|---|---|")
        for q in rows:
            out.append("| [%s](%s) | %s | %s | %s |"
                       % (q["title"], path_of(q["num"]), PART_NAME[q["dir"]],
                          q["focus"], status_of(q["num"])))
        out.append("")
    out.append(README_TAIL)
    return "\n".join(out).rstrip() + "\n"


def written(num):
    """True once a question has real prose in it.

    Derived from the file's own Status line rather than a list kept here, so
    that finishing an answer protects it automatically. A hand-maintained list
    is one forgotten edit away from a rebuild silently deleting a written
    answer, and the deletion looks exactly like a normal regeneration.
    """
    return os.path.exists(os.path.join(ROOT, path_of(num))) and status_of(num) != "Outline"


def main():
    for d, _ in PARTS:
        os.makedirs(os.path.join(ROOT, "docs", d), exist_ok=True)

    # Pass one: which terms does each question use, and how common is each term
    # across the whole set? The second question can only be answered globally,
    # which is why the terms line cannot be decided while rendering one stub.
    bodies = {q["num"]: stub(q, None) for q in Q}
    for q in Q:
        p = os.path.join(ROOT, path_of(q["num"]))
        if written(q["num"]):
            bodies[q["num"]] = open(p).read()
    used = {n: terms_used(n, b) for n, b in bodies.items()}
    freq = {a: sum(1 for s in used.values() if a in s) for a in TERM_RE}

    kept = []
    for q in Q:
        n = q["num"]
        p = os.path.join(ROOT, path_of(n))
        if written(n):
            kept.append(n)
            current = open(p).read()
            current = re.sub(
                r"---\n\n\| ⬅ Previous \| Home \| Next ➡ \|\n"
                r"\|---\|---\|---\|\n\|.*\|\s*$",
                nav_footer(n), current, flags=re.S)
            # The terms line is generated metadata, not prose: which terms are
            # rare enough to be worth linking only becomes known once every
            # answer is written, so it is recomputed on each build rather than
            # frozen at the moment the stub was created.
            current = re.sub(r"\*\*New to these terms\?\*\* .*\n\n", "", current)
            tl = terms_line(used[n], freq, TOTAL)
            if tl:
                current = re.sub(r"(\*\*Status:\*\* \w+\n\n)", r"\1" + tl + "\n",
                                 current, count=1)
            open(p, "w").write(current)
            continue
        open(p, "w").write(stub(q, terms_line(used[n], freq, TOTAL)))

    open(os.path.join(ROOT, "docs", "_glossary.md"), "w").write(glossary_md())
    open(os.path.join(ROOT, "README.md"), "w").write(readme())
    print("wrote %d stubs, kept %d written answers (%s) + glossary + README"
          % (TOTAL - len(kept), len(kept),
             ", ".join("Q%02d" % n for n in sorted(kept)) or "none"))


if __name__ == "__main__":
    main()
