# STE80

[![skills.sh installs](https://skills.sh/b/Dodaios/ste80)](https://skills.sh/Dodaios/ste80) [![validate](https://github.com/Dodaios/ste80/actions/workflows/validate.yml/badge.svg)](https://github.com/Dodaios/ste80/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An agent skill that makes your AI write **"80% of the way to ASD-STE100"**. ASD-STE100 is the controlled English of aircraft maintenance manuals. The result is short sentences, one idea per sentence, active voice, plain words and no filler. It reads like a careful engineer wrote it, not a chatbot.

**Before:**
> Great question! Kubernetes liveness probes are a powerful mechanism that enables the kubelet to determine whether a container is healthy. When a liveness probe fails, the kubelet will automatically restart the container, which can help to ensure that your application remains available. However, it's important to note that misconfigured probes — for instance, ones with overly aggressive timeouts — can actually cause cascading restarts, so you should carefully tune parameters like `initialDelaySeconds` and `failureThreshold`.

**After:**
> A liveness probe tells the kubelet if a container is healthy. If the probe fails, the kubelet restarts the container. This keeps the application available.
>
> A bad probe configuration can cause many restarts. For example, a timeout that is too short makes healthy containers fail the probe. To prevent this, set `initialDelaySeconds` and `failureThreshold` to values that fit your application.

## Where the idea comes from

On 2 October 2026, [Andrej Karpathy posted](https://x.com/karpathy/status/2105819303471976479) a list of tips to make LLM output easier to understand. The first tip was about writing:

> Ask your LLM to explain something in ASD-STE100, it's a controlled language specification originally developed for aerospace maintenance documentation. LLMs well-versed in this language and it comes with heavy constraints on clean writing style that I often find a lot more readable. Sometimes I've tried to soften it a bit e.g. ask for "80% of the way to ASD-STE100" because the spec is quite stringent.

The full standard is very strict. It has a fixed dictionary, and words like "check" and "test" are nouns only. The 80% version keeps what helps the reader and drops what makes normal prose sound strange. This skill packs that idea into rules an agent can follow every time, with a clear default and a strict mode.

## What ASD-STE100 is

ASD-STE100 (Simplified Technical English, STE) is a controlled language. European and US aerospace industry groups created it in the 1980s. Its purpose was to make maintenance manuals clear for mechanics whose first language is not English. A misread step on an aircraft can kill someone. So STE has hard rules:

- **Short sentences:** 20 words at most for instructions and 25 for descriptions.
- **One instruction per sentence.**
- **Simple tenses only:** simple present, simple past, simple future and the imperative.
- **Active voice.**
- **One word, one meaning:** a dictionary of about 900 approved words.
- **One topic per paragraph,** and six sentences at most.
- **No noun stacks** longer than three words.
- **No semicolons.**
- **Warnings and cautions** come before the step they protect.

The same rules remove the habits that make LLM text tiring: long sentences that carry three ideas, "leverage" and "utilize", "it should be noted that", hedged tenses, synonym cycling and walls of text.

The current edition is Issue 9 (2025). It is [free from ASD](https://www.asd-ste100.org).

## Installation

Once installed, the skill answers to `/ste80`. It also starts by itself when you ask for plain, clear or STE-style writing.

### Any agent (skills.sh)

```bash
npx skills add Dodaios/ste80
```

Install for all projects (global) and pick your agent:

```bash
npx skills add Dodaios/ste80 --global --agent claude-code
npx skills add Dodaios/ste80 --global --agent codex
npx skills add Dodaios/ste80 --global --agent cursor
npx skills add Dodaios/ste80 --global --agent '*'      # all detected agents
```

Without `--global`, the skill goes into the current project only. The `skills` CLI ([vercel-labs/skills](https://github.com/vercel-labs/skills)) works with Claude Code, Codex, Cursor, OpenCode and many more.

### Claude Code plugin

```
/plugin marketplace add Dodaios/ste80
/plugin install ste80@ste80
```

### Claude.ai and Claude Desktop

Download this repo as a ZIP (Code → Download ZIP). Then upload it in Settings → Capabilities → Skills.

### Manual

Copy this folder to `~/.claude/skills/ste80/` (Claude Code) or to the skills folder of your agent.

## Usage

```
/ste80
<paste text>
```

Or just ask:

```
Rewrite this README 80% of the way to ASD-STE100.
Explain how TLS handshakes work in STE.
Make this email shorter and clearer.
Convert docs/runbook.md to strict STE.
```

### Two modes

| Mode | When | What it does |
|---|---|---|
| **80% (default)** | Normal requests | All structure rules (sentence length, one idea per sentence, active voice, simple tenses, short paragraphs, one term per thing). Plain words, but no fixed dictionary. Contractions OK in casual text. |
| **Strict** | "strict", "full STE", "100%", procedures, safety notes | Every rule, including noun-only "check" and "test", modal verbs limited to can, must and will, no contractions, and exact word limits. |

### Fidelity first

Short sentences tempt a writer to drop facts. The skill has explicit rules against this:

- **Keep every fact.**
- **Keep uncertainty at its strength.** "may" does not become "will".
- **Keep identifiers exact:** code, commands, paths and numbers.
- **Add nothing.**
- **Flag a source that contradicts itself,** instead of resolving it silently.

## The rules

| Group | Rules |
|---|---|
| **A. Sentences** | 1. One idea per sentence · 2. Keep sentences short (20/25 words) · 3. Condition first · 4. Do not drop words · 5. Lists for complex text · 6. Link related sentences |
| **B. Verbs** | 7. Active voice · 8. Simple tenses only · 9. Verbs, not nouns made from verbs · 10. Avoid "-ing" verb forms · 11. Avoid modal hedging · 12. No phrasal verbs |
| **C. Words** | 13. One word, one meaning · 14. One term per thing · 15. Use the plain word · 16. No noun stacks · 17. Define technical names once |
| **D. Structure** | 18. One topic per paragraph (6 sentences max) · 19. Give information in steps · 20. Separate procedure from description · 21. Warnings first |
| **E. Punctuation** | 22. No semicolons · 23. Simple punctuation, no em dash glue |

All of these, with before and after examples, are in [SKILL.md](SKILL.md). [references/strict-mode.md](references/strict-mode.md) has the full strict rule set and a checklist. [references/word-swaps.md](references/word-swaps.md) has more than 100 plain-word swaps, including typical LLM vocabulary ("delve", "robust", "seamless", "leverage").

## Checker

`scripts/ste_check.py` is a small linter with no dependencies. It flags:

- long sentences and long paragraphs
- semicolons and em dashes
- likely passive voice
- perfect and progressive tenses
- "-ing" verb forms and phrasal verbs
- words from the swap list
- contractions and verb use of "check" and "test" (strict mode only)

```bash
python scripts/ste_check.py README.md
python scripts/ste_check.py --strict docs/runbook.md
cat draft.txt | python scripts/ste_check.py -
python scripts/ste_check.py --json notes.md
```

It is a heuristic. Use it to find places to look at, not as proof of compliance.

## Tests

`evals/` has three test cases in the `claude plugin eval` format:

- a README rewrite
- a new explanation from scratch
- a strict-mode runbook

Each case has a prompt and graders. Run them with:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash
```

In our first run, the base model already did well when the prompt named ASD-STE100. The skill made the difference in fidelity: it kept "may need to" hedged and flagged a contradiction in the source. Without the skill, the hedge became a firm instruction.

## Limits

- **STE is for technical and explanatory text.** It removes voice on purpose. Do not use it for fiction, marketing or speeches.
- **It is an English standard.** For other languages, the skill applies only the structure rules.
- **"STE style" is not "STE compliant."** Real compliance needs the official dictionary, trained writers and review.

## Sources

- Andrej Karpathy on X, 2 October 2026: https://x.com/karpathy/status/2105819303471976479
- ASD-STE100 Issue 9 (2025): https://www.asd-ste100.org
- Hacker News discussion of STE skills (July 2026): https://news.ycombinator.com/item?id=49114639
- Structure of this repo inspired by [blader/humanizer](https://github.com/blader/humanizer)

## Disclaimer

This skill does not contain the ASD-STE100 specification or its dictionary. The rules are paraphrased and simplified. ASD-STE100 and Simplified Technical English are trademarks of ASD (AeroSpace, Security and Defence Industries Association of Europe). This project is not affiliated with or endorsed by ASD.

## License

[MIT](LICENSE)
