# tools

Generators and checks for the question set. The README, the glossary, and every
navigation footer are generated - edit the data modules, not the output.

- `questions.py` - the 29 questions: number, part, slug, title, focus, and what the question really tests
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
