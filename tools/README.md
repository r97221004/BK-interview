# tools

Generators and checks for the question set. The README, the glossary, and every
navigation footer are generated - edit the data modules, not the output.

- `questions.py` - the questions themselves: number, part, slug, title, focus, and what the question really tests
- `glossary.py` - glossary terms and the question that owns each one
- `build.py` - importance ratings, the README prose, and the generator for stubs, `docs/_glossary.md`, and `README.md`
- `check.py` - verifies structure, links, numbering, bilingual paragraph shape, and README/file consistency

```bash
python3 tools/build.py
python3 tools/check.py
```

`build.py` never overwrites a question whose status has moved past `Outline`.
The guard reads each file's own `**Status:**` line, so finishing an answer
protects it automatically - there is no list to remember to update.

## Adding a question

1. Add it to `questions.py`, using the next free number **inside its part**.
   Parts are numbered in blocks of ten (1-9, 11-19, 21-29, ...) so a new
   question never forces a renumber. Numbers are permanent.
2. Add its importance to `IMPORTANCE` in `build.py`; the assertion there fails
   until every question has one.
3. Run `python3 tools/build.py` to write the stub and regenerate the README.
4. Write the answer, set `**Status:** Draft`, then run `python3 tools/check.py`.

## Sections

`check.py` enforces the section list and its order: **In One Sentence**,
**Answer Shape**, **Full Spoken Answer**, optionally **Quick Reference**, and
finally **Interview Version**.

The first three are bilingual prose and are checked paragraph by paragraph -
one English paragraph, then its Traditional Chinese counterpart, with three to
seven pairs in the spoken answer. Keep tables and code out of them, because the
paragraph count is what verifies the pairing.

**Quick Reference** is where that material goes instead. It is optional,
exempt from the language rules, and must contain a table or a fenced code
block - if it is prose, it belongs in the answer.

**Interview Version** is always the last section: the whole answer condensed
into one paragraph you could say end to end, then the one sentence worth
memorising - exactly two bilingual pairs, four paragraphs in all. It is the
last-minute revision pass, so it has to stand alone without the sections above.
