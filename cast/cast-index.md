# The Cast

The one-shot uses ten premade archetypes without fixed names, genders, or appearances. Five are chosen for play.

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

After the five Cast members have been chosen, the players select one of them to be the **Organizer**. The Organizer is the person who contacted the others and assembled the group entering Mourning Bluff Manor. Each eligible character will eventually have a short **If You Gathered the Group** prompt so that any combination of five characters makes sense.

The other characters need not know or trust one another before arriving, but each knows the Organizer. Being the Organizer does not replace that character's own reason for entering the manor. The Paramedic does not serve as the Organizer; they joined because one of the people entering the manor is their friend, but that relationship is not a character mechanic.

## The Historical Archaeologist

The completed character profile is in [`historical-archaeologist.md`](historical-archaeologist.md).

### Background

Someone anonymously sent you a box containing photographs, floor plans, correspondence, and property records from Mourning Bluff Manor. The material has never appeared in any archive. Together, the documents establish that a previously unknown inheritor is now the legal owner of the estate.

The inheritor hired you to examine the manor and put the stories surrounding it to rest. You enter expecting to expose tricks, identify environmental causes, authenticate or disprove the documents, and demonstrate that the house is not haunted.

### If You Gathered the Group

You selected people whose experience could help investigate the property, explain its supposed phenomena, and document the truth for the inheritor.

### Role

A specialist in historic sites, standing buildings, burials, material culture, and reconstructing events from physical evidence. The Historical Archaeologist studies construction layers, disturbed earth, human remains, discarded objects, alterations to the manor, and the relationship between physical evidence and surviving records.

This Cast member has an immediate connection to the Tower's buried foundation, the packed-earth floor of the Lower Circle, and anything the Fellows concealed beneath Mourning Bluff Manor.

Stats, Weakness, Gift, and Tool are finalized. The player creates the character's Secret.

Every build script (`build_booklet.py`, `build_character_profiles_pdf.py`, `build_character_reference_pdf.py`, `build_selected_character_packets.py`) parses this Cast structure directly from `cast/*.md`. There is no separate hardcoded copy anywhere; a file in `cast/` is always authoritative.
