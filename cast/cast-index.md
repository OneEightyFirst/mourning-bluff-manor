# The Cast

The one-shot uses ten premade archetypes without fixed names, genders, or appearances. Table size is flexible: each player chooses a different one, up to all ten.

The spoiler-free player selection cards are in [`character-choice-cards.md`](character-choice-cards.md).

Each Cast member has:

- a background explaining why they would enter Mourning Bluff Manor;
- five Stats;
- a mechanical Weakness arising from an internal conflict;
- one Gift that manipulates their deck;
- one investigative Tool; and
- a blank Secret created by the player, which they must conceal from the rest of the group and which could create conflict if exposed.

1. [The Historical Archaeologist](historical-archaeologist.md)
2. [The Relative](missing-person-relative.md)
3. [The Fraudulent Medium](fraudulent-medium.md)
4. [The Paramedic](paramedic.md)
5. [The Psychic Researcher](psychic-researcher.md)
6. [The Psychiatrist](psychiatrist.md)
7. [The Detective](detective.md)
8. [The Priest](priest.md)
9. [The Dreamer](dreamer-of-the-manor.md)
10. [The Inheritor](inheritor.md)

## The Organizer

After the Cast members have been chosen, the players select one of them to be the **Organizer**. The Organizer is the person who contacted the others and assembled the group entering Mourning Bluff Manor.

The other characters need not know or trust one another before arriving, but each knows the Organizer. Being the Organizer does not replace that character's own reason for entering the manor. The Paramedic does not serve as the Organizer; they joined because one of the people entering the manor is their friend, but that relationship is not a character mechanic.

## The Cast profiles

Each character's completed profile, including Bio, Stats, Weakness, Gift, Tool, and (where written) the "What Is Established," "Make the Character Your Own," and "Decide Before Play" sections, lives entirely in its own file under `cast/`. The profiles are final; this index does not duplicate or draft their content.

Every build script (`build_booklet.py`, `build_character_profiles_pdf.py`, `build_character_reference_pdf.py`, `build_selected_character_packets.py`) parses this Cast structure directly from `cast/*.md`. There is no separate hardcoded copy anywhere; a file in `cast/` is always authoritative.
