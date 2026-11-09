# Guide for agents

This repo is one agent skill, `humanizer-ste80`. `SKILL.md` at the root is the skill. Part 1 lists AI tells. Part 2 lists the STE80 structure rules. Follow these rules when you change it.

- **Write in the style the skill teaches.** Short sentences, active voice, simple tenses, one term per thing.
- **Keep the version in sync** in four places: `SKILL.md` (`metadata.version`), the first heading in `CHANGELOG.md`, `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`.
- **Keep SKILL.md under 500 lines.** Put long material in `references/`.
- **Keep SKILL.md and README.md in sync** when you add, remove or rename a tell or a rule.
- **Keep `scripts/ste_check.py` in sync** with the tells and words in SKILL.md where a regex can find them.
- **Do not copy the ASD-STE100 specification or dictionary.** ASD owns the copyright. Paraphrase rules in your own words. Cite only single word pairs.
- **Do not claim compliance.** The skill and the checker give "STE style", not certified STE.
- **Before you publish**, run:

```bash
python scripts/ste_check.py --help
npx skills add . --list
claude plugin validate .
```
