# Mourning Bluff Manor (669 Gallows Way)

A Tarot-driven horror mystery RPG about clairvoyants exploring an ever-changing New England manor.

This repo was migrated from a working scratch folder into a proper, versioned project. History before the migration commit lived only as local Markdown edits with no git record; going forward, changes are tracked here and tagged as releases.

## Source of truth

- **`cast/*.md` is the single source of truth for every character.** The ten profiles (Bio, Stats, Weakness, Gift, Tool, Secret) are authoritative. If any generated PDF, script, or older draft disagrees with a file in `cast/`, the file in `cast/` is correct.
- **`rules/core-rules.md` and `rules/gm-guide.md` are the source of truth for mechanics and GM procedure.** These were reconciled from the original design notes plus the older rulebook draft, keeping what the older draft got right (Grounding, the House Deck, all 22 Major Arcana, Helping, the Four Suits) while removing anything that only applied to the discarded pre-Cast character set (the "Anchor" mechanic no longer exists; no current character has one).
- **`canon/known-background.md`, `canon/timeline.md`, `clues/clue-index.md`, and `decision-log.md`** track the mystery's underlying truth, what's locked, and what's still an open design question. See `decision-log.md`'s "Unresolved" section for what still needs to be decided before the central mystery can be finished, this is narrative work, not a rules gap.

## Project map

- [`canon/known-background.md`](canon/known-background.md) - Private GM truth behind the haunting. Not for players.
- [`canon/timeline.md`](canon/timeline.md) - Chronological reference for the manor, Miriam Bellweather, Lucius Ward, and the Fellows of the Rook.
- [`clues/clue-index.md`](clues/clue-index.md) - Working index connecting revelations to physical, documentary, spiritual, and psychic clues.
- [`rules/core-rules.md`](rules/core-rules.md) - Player- and GM-facing mechanics. Fully settled; this is what the rulebook PDF renders.
- [`rules/gm-guide.md`](rules/gm-guide.md) - GM procedure and tone: building a mystery, clue placement, room procedure, escape conditions, pacing.
- [`cast/cast-index.md`](cast/cast-index.md) - The ten premade character archetypes and the Organizer procedure.
- [`cast/*.md`](cast/) - One file per character. Source of truth for that character.
- [`house/rooms.md`](house/rooms.md) - Pointer to the room manuscript.
- [`669-gallows-hill-way.md`](669-gallows-hill-way.md) - The room-by-room manuscript.
- [`decision-log.md`](decision-log.md) - Locked decisions vs. open questions.
- [`assets/timeline/`](assets/timeline/) - In-fiction timeline photographs (handouts).
- [`assets/concept/`](assets/concept/) - Fellows of the Rook concept art.
- [`assets/reference/`](assets/reference/) - Real-world reference photography used while writing the Tower.
- [`output/pdf/`](output/pdf/) - Generated PDFs. Regenerate with the build scripts below; don't hand-edit.

## Canon rule

Material in `canon/known-background.md` is true unless explicitly labeled unresolved. Player-facing documents, testimony, rumors, and spirits may be incomplete or false, but the GM should know how each relates to the underlying truth. Do not put new ideas into established canon automatically, record uncertain ideas in `decision-log.md` until they're approved.

## Building the PDFs

Requires Python 3 with `reportlab` and `pypdf`:

```
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab pypdf
```

Then, from the repo root:

```
python3 build_booklet.py                     # rulebook: mechanics + roster, parsed from rules/ and cast/
python3 build_character_profiles_pdf.py       # all 10 full character dossiers
python3 build_character_reference_pdf.py      # 2-page condensed reference, all 10
python3 build_selected_character_packets.py   # individual print-and-play packets for the 7 currently offered characters
```

All four scripts parse their content live from `rules/` and `cast/*.md`. None of them should contain hardcoded character text; if one does, that's a bug, fix the Markdown and rerun the script, don't edit the PDF text in the script.

## Versioning

This repo uses git tags for releases (e.g. `v0.1.0`). A tagged release means: canon, rules, cast, and rooms are internally consistent as of that commit, and the PDFs in `output/pdf/` were regenerated from that exact commit. See `decision-log.md` for what changed and what's still open going into the next version.

## What's out of scope here

This repo contains Mourning Bluff Manor only. An unrelated Magic: the Gathering proxy/printing project that previously shared a working folder with this content was intentionally left behind during migration and is not part of this repo.
