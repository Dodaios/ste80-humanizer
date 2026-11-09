# Humanizer STE80

[![skills.sh installs](https://skills.sh/b/Dodaios/humanizer-ste80)](https://skills.sh/Dodaios/humanizer-ste80) [![validate](https://github.com/Dodaios/humanizer-ste80/actions/workflows/validate.yml/badge.svg)](https://github.com/Dodaios/humanizer-ste80/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An agent skill that rewrites AI-sounding text so it reads like a clear, careful human wrote it. It does two things:

1. It removes the **tells** that people recognize as AI writing: "it's not just X, it's Y", one-line closers, forced triads, em dashes everywhere, "delve" and "seamless", "Great question!".
2. It rebuilds the **structure** with the method Andrej Karpathy shared: write **"80% of the way to ASD-STE100"**, the controlled English of aircraft maintenance manuals. The result has short sentences, one idea per sentence, active voice, simple tenses and plain words.

Most humanizers do only step 1. The text loses its stock phrases but keeps long, hedged, three-idea sentences, so it still reads like AI. STE80 fixes the layer below.

**Before:**
> Great question! Kubernetes liveness probes are a powerful mechanism that enables the kubelet to determine whether a container is healthy. When a liveness probe fails, the kubelet will automatically restart the container, which can help to ensure that your application remains available. However, it's important to note that misconfigured probes — for instance, ones with overly aggressive timeouts — can actually cause cascading restarts, so you should carefully tune parameters like `initialDelaySeconds` and `failureThreshold`. It's not just a health check, it's your first line of defense.

**After:**
> A liveness probe tells the kubelet if a container is healthy. If the probe fails, the kubelet restarts the container. This keeps the application available.
>
> A bad probe can also cause many restarts. For example, a timeout that is too short makes healthy containers fail the probe. To prevent this, set `initialDelaySeconds` and `failureThreshold` to values that fit your application.

The goal is text that people read easily. Getting past AI detectors is not a goal.

## Where the method comes from

On 2 October 2026, [Andrej Karpathy posted](https://x.com/karpathy/status/2105819303471976479) tips to make LLM output easier to understand. The first tip was about writing:

> Ask your LLM to explain something in ASD-STE100, it's a controlled language specification originally developed for aerospace maintenance documentation. LLMs well-versed in this language and it comes with heavy constraints on clean writing style that I often find a lot more readable. Sometimes I've tried to soften it a bit e.g. ask for "80% of the way to ASD-STE100" because the spec is quite stringent.

ASD-STE100 (Simplified Technical English, STE) came from European and US aerospace groups in the 1980s. Its purpose was to make maintenance manuals clear for mechanics whose first language is not English. A misread step on an aircraft can kill someone. So STE has hard rules:

- 20 words at most per instruction and 25 per description
- one instruction per sentence
- simple tenses and active voice
- one meaning per word, from a dictionary of about 900 approved words
- one topic per paragraph, with six sentences at most
- no noun stacks longer than three words
- no semicolons

The full standard is too strict for normal prose. For example, "check" and "test" are nouns only. "80% of the way" keeps all of the structure and only the parts of the vocabulary that sound natural. The current edition is Issue 9 (2025). It is [free from ASD](https://www.asd-ste100.org).

## Installation

Once installed, the skill answers to `/humanizer-ste80`. It also starts by itself when you ask to humanize, simplify or de-AI a text, or when you ask for STE.

### Any agent (skills.sh)

```bash
npx skills add Dodaios/humanizer-ste80
```

Install for all projects (global) and pick your agent:

```bash
npx skills add Dodaios/humanizer-ste80 --global --agent claude-code
npx skills add Dodaios/humanizer-ste80 --global --agent codex
npx skills add Dodaios/humanizer-ste80 --global --agent cursor
npx skills add Dodaios/humanizer-ste80 --global --agent '*'      # all detected agents
```

Without `--global`, the skill goes into the current project only. The [skills CLI](https://github.com/vercel-labs/skills) from Vercel works with Claude Code, Codex, Cursor, OpenCode and many more agents.

### Claude Code plugin

```
/plugin marketplace add Dodaios/humanizer-ste80
/plugin install humanizer-ste80@humanizer-ste80
```

### Claude.ai and Claude Desktop

Download this repo as a ZIP (Code → Download ZIP). Then upload it in Settings → Capabilities → Skills.

## Usage

```
/humanizer-ste80
<paste text>
```

Or just ask:

```
This sounds like ChatGPT wrote it. Make it sound like a person.
Rewrite this README 80% of the way to ASD-STE100.
Explain how TLS handshakes work in STE.
Light touch: just remove the AI stuff from docs/intro.md.
Convert docs/runbook.md to strict STE.
```

### Modes

| Mode | When | What it does |
|---|---|---|
| **Humanize (default)** | Normal requests | Removes every AI tell. Applies the STE structure at 80%. Keeps the writer's voice and warmth. |
| **Light** | "light touch", "just remove the AI stuff" | Removes the tells. Fixes only the worst sentences. |
| **Strict STE** | "strict", "full STE", procedures, safety notes | Every STE rule, including noun-only "check" and "test", no contractions, exact limits. |

### Match your voice

Give the skill a sample of your own writing. It then copies your rhythm, word choice and register, not a default voice.

### Fidelity first

Short sentences tempt a writer to drop facts. The skill has explicit rules against this:

- **Keep every fact.** "may" does not become "will".
- **Keep numbers, names and identifiers exact.**
- **Add nothing.**
- **Do not swap an exact word for a vaguer one.**
- **Flag a contradiction in the source** instead of resolving it silently.

## Part 1: the 23 AI tells

| Group | Tells |
|---|---|
| **A. Staging instead of stating** | 1. Not X but Y · 2. One-line closers · 3. Fake depth · 4. Run-up before the point · 5. Arguing with nobody |
| **B. Rhythm by rule** | 6. Forced triads (*weak alone*) · 7. Same sentence openings (*weak alone*) · 8. Em dashes everywhere · 9. Stacked hedges · 10. Passive voice and missing actors |
| **C. Inflation and borrowed authority** | 11. Stock AI words · 12. Inflated significance · 13. Shallow "-ing" riders · 14. Sales language · 15. Vague authority · 16. Avoiding "is" and "has" |
| **D. Formatting by rule** | 17. Bold as decoration · 18. Headings and bullets for short text · 19. Emoji and curly quotes in technical text |
| **E. Chat residue** | 20. Chatbot openers and closers · 21. Knowledge-limit hedges · 22. Writing about the text · 23. Re-explaining what the reader knows |

## Part 2: the 23 STE80 rules

| Group | Rules |
|---|---|
| **Sentences** | 1. One idea per sentence · 2. Short sentences (20/25 words) · 3. Condition first · 4. Do not drop words · 5. Lists for complex content · 6. Simple joints |
| **Verbs** | 7. Active voice · 8. Simple tenses · 9. Verbs, not nominalizations · 10. No "-ing" chains · 11. Honest modals · 12. Fewer phrasal verbs |
| **Words** | 13. One word, one meaning · 14. One term per thing · 15. The plain word · 16. No noun stacks · 17. Define technical names once |
| **Structure** | 18. One topic per paragraph · 19. General before specific · 20. Keep procedure and description apart · 21. Warnings first · 22. No semicolons · 23. Simple punctuation |

Details:

- [SKILL.md](SKILL.md) has every tell and rule.
- [references/ste80-rules.md](references/ste80-rules.md) has before and after examples for each STE rule.
- [references/word-swaps.md](references/word-swaps.md) has more than 100 plain-word swaps.
- [references/strict-mode.md](references/strict-mode.md) has the full strict rule set and a checklist.

## Checker

`scripts/ste_check.py` is a small linter with no dependencies. It flags:

- AI tells: not-X-but-Y, chatbot phrases, run-ups, fake depth, stacked hedges, vague authority, "-ing" riders, inflated claims, curly quotes
- stock AI words and heavy words, with plain swaps
- long sentences and long paragraphs
- semicolons and em dashes
- passive voice, perfect and progressive tenses, "-ing" forms and phrasal verbs
- in strict mode, also contractions and verb use of "check" and "test"

```bash
python scripts/ste_check.py README.md
python scripts/ste_check.py --strict docs/runbook.md
cat draft.txt | python scripts/ste_check.py -
python scripts/ste_check.py --json notes.md
```

It is a heuristic, not an AI detector and not a compliance checker. Use it to find places to look at.

## Tests

`evals/` has four test cases in the `claude plugin eval` format:

- a README rewrite
- a new explanation from scratch
- a strict-mode runbook
- a casual LinkedIn post that does not mention STE

Run them with:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash
```

## Limits

- **STE is for clear explanatory text.** For fiction, speeches or brand copy, the skill removes only the obvious tells and leaves the structure alone.
- **STE is an English standard.** For other languages, the skill applies the tells and the structure rules, but not the English word lists.
- **"STE style" is not "STE compliant."** Real compliance needs the official dictionary, trained writers and review.

## Sources and credits

- Andrej Karpathy on X, 2 October 2026: https://x.com/karpathy/status/2105819303471976479
- ASD-STE100 Issue 9 (2025): https://www.asd-ste100.org
- Wikipedia, [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup)
- [blader/humanizer](https://github.com/blader/humanizer) (MIT), which inspired the catalog of tells and the structure of this repo
- Hacker News discussion of STE skills (July 2026): https://news.ycombinator.com/item?id=49114639

## Disclaimer

This skill does not contain the ASD-STE100 specification or its dictionary. The rules are paraphrased and simplified. ASD-STE100 and Simplified Technical English are trademarks of ASD (AeroSpace, Security and Defence Industries Association of Europe). This project is not affiliated with or endorsed by ASD.

## License

[MIT](LICENSE)
