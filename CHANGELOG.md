# Changelog

## 2.0.0

- Renamed from `ste80` to `humanizer-ste80`. The skill is now a general humanizer that uses STE80 as its method.
- New Part 1: 23 AI tells in five groups (staging, rhythm, inflation, formatting, chat residue), inspired by Wikipedia's "Signs of AI writing" and blader/humanizer.
- Part 2: the 23 STE80 structure rules, now in compact form. The full rules with before and after examples moved to `references/ste80-rules.md`.
- New modes: Humanize (default), Light, Strict STE.
- New sections: Voice (match a writing sample), "Human quirks" to keep, contradiction flag in the fidelity rules.
- `ste_check.py` now also flags AI tells: not-X-but-Y, chatbot openers and closers, run-ups, fake depth, stacked hedges, vague authority, "-ing" riders, inflated significance and curly quotes.
- New eval case: `humanize-linkedin-post`.

## 1.0.0

- First release.
- 80% mode (default) and strict mode.
- 23 rules in six groups (sentences, verbs, words, structure, punctuation, what 80% relaxes), with before and after examples.
- Fidelity rules: keep every fact, keep uncertainty at its strength, add nothing.
- `references/word-swaps.md`: plain alternatives in ten groups, including typical LLM vocabulary.
- `references/strict-mode.md`: paraphrased ASD-STE100 Issue 9 rule sections and a final checklist.
- `scripts/ste_check.py`: dependency-free heuristic linter.
