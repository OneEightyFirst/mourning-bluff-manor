# Core Rules

## What you need

One light-backed Tarot deck for each player, one contrasting dark-backed Tarot deck for the GM, a Cast sheet for each player, pencils, and six Grounding tokens per player. Glass beads in a bowl work well. No dice are used.

## Tone

Mourning Bluff Manor is exploratory horror, played together by one GM and however many players the table can hold, each one stepping into a different member of the Cast. Ten are written, and any number of them may be at the table on a given night. Nobody here is trying to win a fight: violence happens, but it is rarely the point, and it is never the solution. The real danger is the house itself, its stairs, its locks, its furniture, its memories, its etiquette, its architecture, and its ordinary accidents. There are no monsters waiting in the dark to leap out on cue. What makes Mourning Bluff Manor frightening is that it doesn't need one.

## Before play

Each player chooses one member of the Cast. Every character begins with six Grounding tokens.

**Prepare each player deck:**

1. Separate the 22 Major Arcana from the 56 Minor Arcana.
2. Shuffle the Major Arcana and draw two without looking at them.
3. Shuffle those two cards into the Minor Arcana.
4. Set the remaining Major Arcana aside, face down, out of play. They do not return to this character's deck this session; only the two drawn in step 2 can appear.
5. Place the deck face down and turn its top card face up.

The face-up top card is that character's **Premonition**. Everyone may see it. Whenever it is used or discarded, reveal the next card immediately. Routine actions do not consume cards; a Premonition is discarded only by a test, an ability, a Major effect, or an explicit consequence. Waiting does not make an unwanted future disappear. A character's own Gift or Weakness may change how this works for them specifically, keeping part of their deck hidden, held in reserve, or handled some other way; where a character's file in `cast/` describes something different, follow that instead.

Players may discuss their visible cards and coordinate around them. That is clairvoyance, not cheating. The limitation is fictional: the person taking the risk uses their own future, and a test cannot be transferred to whoever holds the strongest Premonition.

## Making a test

Use the visible Premonition, add the relevant Stat, and compare the total with the Difficulty.

| Difficulty | When to use |
| --- | --- |
| 8 | Favorable, but failure matters |
| 10 | Risky or uncertain |
| 12 | Severe danger or opposition |
| 14 | Extraordinary circumstances |

**Results:**

- Exceed the Difficulty by 3 or more: the character succeeds cleanly.
- Meet the Difficulty or exceed it by 1 or 2: the character succeeds, but a consequence follows.
- Miss the Difficulty: the action fails and the situation changes for the worse.

Consequences can cost time, separate the group, consume equipment, expose a secret, inflict harm, remove Grounding, attract attention, alter a route, or let the House insert a card. Never repeat the same test without a meaningful change.

A test's Difficulty number may be stated aloud or kept hidden, with only the Stat and the apparent danger named instead. Revealing it keeps the math transparent; withholding it keeps everyone guessing exactly how close a character came.

**A test happens only when** the outcome is uncertain, failure would change the situation, and the character is exposed to the consequence. A test is never called merely to inspect scenery, open an ordinary drawer, or confirm something the character would already know.

**Essential clues are never withheld behind a failed test.** A test may determine how safely, quickly, or completely a clue is obtained, or what notices the investigator in return, never whether the core clue exists at all.

Tests follow the character taking the action; the group cannot transfer a test after hearing the required Stat. Once a test's Stat and apparent danger are named, and the Difficulty is either stated or deliberately withheld, the action is committed and cannot be withdrawn.

**One action at a time.** When several people could act, each is asked what their character is doing before anyone's action resolves. Each character commits to one immediate action.

## Choosing a Stat

Choose the Stat according to the obstacle the character must overcome and how they confront it, not merely the broad action they are attempting. The same goal can require different Stats when approached differently. Opening a sealed door might use Vigor to force it, Reason to defeat its mechanism, or Notice to find its concealed release. When two Stats honestly apply, the player describes how the character approaches the problem, and the matching Stat and Difficulty follow from that.

### Notice

Notice is perception and awareness. It detects something present now but does not explain what that evidence means.

Examples:

1. Spot a tripwire before stepping through a doorway.
2. Hear movement inside a wall before whatever is there emerges.
3. Realize that a portrait's hands have changed position.
4. Catch someone slipping a key into their pocket.
5. Follow a faint trail of blood across a patterned carpet.

Use Reason, not Notice, when the important question is what the discovered evidence means.

### Reason

Reason is intelligence, learned knowledge, judgment, and willpower. It interprets evidence, applies expertise, solves problems, and resists attempts to override the character's conscious mind.

Examples:

1. Reconstruct the order of events from marks left in a disturbed room.
2. Stabilize a badly bleeding wound with limited supplies before the patient goes into shock.
3. Recognize the contradiction in a supernatural command and reject it as an intrusion.
4. Work out how to stop a clockwork lock without triggering it.
5. Identify the historical purpose of a symbol carved into a lintel.

Use Notice, not Reason, when the challenge is finding or sensing the evidence in the first place.

### Rapport

Rapport is charisma and social influence. It covers persuasion, empathy, reassurance, deception, intimidation, bargaining, and reading another person's emotional intent.

Examples:

1. Calm a panicking companion enough for them to follow instructions.
2. Persuade a hostile apparition to answer one question.
3. Convince a suspicious stranger that you belong in the house.
4. Recognize what subject a grieving spirit is refusing to discuss.
5. Negotiate terms with an entity offering safe passage.

Rapport influences another will. Reason or Nerve resists it, depending on how the character holds their ground.

### Nerve

Nerve is stamina, pain tolerance, courage, and sanity. It governs how long the character can endure physical or psychological strain without breaking down.

Examples:

1. Cross a nursery while something unseen whispers your name.
2. Keep moving after hours without sleep or safe rest.
3. Keep treating an injury while a corpse speaks beside you.
4. Remain functional through severe pain until immediate danger passes.
5. Resist a supernatural command through courage and raw refusal to break.

A mental command may use Reason if the character exposes its falsehood, or Nerve if they endure its pressure through sheer grit.

### Vigor

Vigor is strength, dexterity, agility, coordination, and athletics. It governs active physical performance rather than the stamina to endure prolonged strain.

Examples:

1. Force open a swollen wooden door before the corridor closes.
2. Climb a crumbling exterior wall in heavy rain.
3. Leap across a gap where the staircase has vanished.
4. Carry an injured companion away from a collapsing ceiling.
5. Pick a simple lock with improvised tools before approaching footsteps arrive.

Vigor handles active physical performance. Nerve handles prolonged exertion, pain, fear, and exhaustion.

Each Cast member has +4, +3, +2, +1, and +0 assigned once each across the five Stats (see `cast/` for exact assignments). The Stat measures capability; the card represents the future already waiting for them.

## Reading the Minor Arcana

| Card | Test value | Additional effect |
| --- | --- | --- |
| Ace | Critical success | Regain 1 Grounding |
| 2-10 | Printed value | None |
| Page | 11 | None |
| Knight | 12 | None |
| Queen | Automatic success | Lose 1 Grounding |
| King | Critical failure | Lose 1 Grounding |

An Ace succeeds cleanly regardless of Stat or Difficulty, no consequence, and returns one Grounding bead to the character, up to their starting maximum.

A Queen also succeeds cleanly regardless of Stat or Difficulty, no consequence, but the vision costs something vital: move one Grounding bead into the pool after resolving the action.

A King fails automatically, regardless of Stat or Difficulty. The action fails and the situation changes for the worse, exactly as with any missed test, and the character also moves one Grounding bead into the pool: an omen turning against them.

## The Four Suits

The suits are known to the players. They do not change the number or add a bonus. They tell everyone what kind of future surrounds the action and shape the benefits and consequences that follow. A suit is permission, not a command; its influence can be subtle, and players should gradually recognize the house's recurring symbolic vocabulary.

- **Cups, emotion and memory.** Relationships, grief, desire, empathy, family, spirits, dreams, and recollection.
- **Pentacles, the material house.** Objects, evidence, money, bargains, possessions, architecture, doors, and physical traces.
- **Swords, danger and truth.** Fear, conflict, pain, separation, difficult knowledge, accusation, and decisive harm.
- **Wands, action and change.** Instinct, movement, ambition, transformation, fire, supernatural power, and things set in motion.

## Major Arcana: House Layers

A Major Arcana is never used as a test value. The instant one becomes the active card, through revealing, an ability, or a House card, stop play and announce it.

An immediate change affects the whole house and establishes the card's ongoing Layer. Then every character's Premonition resets before play resumes: the character who revealed the Major discards it and reveals their next card; every other character discards their current Premonition without using it and reveals a new one. If another Major appears during the reset, everyone finishes resetting first, then that Major resolves normally.

Merely seeing a deeper Major through an ability does not activate it. It activates only when it reaches the top or is drawn for use.

A Layer usually lasts until another Major replaces it or until its fiction is resolved. It creates both danger and opportunity; unavoidable harm never lands without giving the players something meaningful to do.

**Repeated cards.** If a Major appears again, intensify or transform its earlier meaning. The house remembers. A second Hermit might extinguish even personal lights; a second Lovers might bind enemies rather than friends; a second World might close every route except one.

### Major Arcana I

- **The Fool.** Continuity is abandoned. Thresholds lead somewhere unexpected and new paths appear.
- **The Magician.** Tools and objects activate or perform impossible functions. Solutions demand deliberate use.
- **The High Priestess.** Silence and secrecy descend. Hidden things are easier to notice; speaking a truth may erase it.
- **The Empress.** Growth and hospitality become possessive. Roots spread, food freshens, and the house tries to nurture what it claims.
- **The Emperor.** Architecture imposes order. Doors lock, rooms acquire labels, and rank or rules suddenly matter.
- **The Hierophant.** Old customs resume. Etiquette, ritual, and household roles can protect those who obey them.

### Major Arcana II

- **The Lovers.** Bonds become literal. Paired people share sensations, choices, locations, or consequences.
- **The Chariot.** The house moves. Corridors travel, staircases change direction, and entire rooms shift position.
- **Strength.** Restrained things test their bonds. Force worsens the danger; patience or compassion creates leverage.
- **The Hermit.** Isolation and darkness spread. Personal lights reveal things the house ordinarily hides.
- **Wheel of Fortune.** Rooms and consequences repeat in altered form. Something lost may return, but never unchanged.

### Major Arcana III

- **Justice.** The house balances a debt with ancient, exacting fairness.
- **The Hanged Man.** Gravity or perspective overturns. Progress requires surrendering the obvious route.
- **Death.** Something ends and transforms. Death is not automatically physical or final.
- **Temperance.** Boundaries blend: rooms, times, people, and states of life overlap.
- **The Devil.** The house makes a tempting offer. Acceptance creates a bond or obligation.
- **The Tower.** Violent restructuring exposes what was concealed as routes and certainties collapse.

### Major Arcana IV

- **The Star.** Genuine clarity arrives. For a moment, the house cannot completely falsify what is learned.
- **The Moon.** Perception, geography, and identity become unreliable, but every falsehood contains a contradiction.
- **The Sun.** Merciless exposure reveals hidden things, including truths the characters hoped to keep private.
- **Judgement.** The living and dead are called to account through confession, accusation, or request.
- **The World.** The house briefly aligns into a comprehensible whole. A route toward the center or exit appears as side paths close.

## Helping and acting together

One character leads a test. A second character may help only by describing a concrete action that could change the outcome. The helper does not commit or reveal a card: add the helper's relevant Stat directly to the lead character's total for that test.

Helping does not cost the helper anything, no card, no consequence, no Grounding. What limits it is the fiction: the help only counts if the described action could plausibly change the outcome, and only one character may lead a given test.

**Group dangers.** When an event threatens everyone, do not ask one character to solve it for the table. Each endangered character tests the appropriate Stat, but their circumstances may differ: one holds the door, another guides someone through the dark, another resists the voice calling from upstairs.

## The House Deck

The GM keeps a complete dark-backed Tarot deck as the House Deck. Its cards may be inserted into player decks when the house gains influence. Because the backs differ, a player can see the contamination approaching without knowing its face.

**How close.** Insertion distance is tied to the target's current Grounding. At 5-6 Grounding, insert within the next six cards. At 3-4, within the next four. At 1-2, within the next two. At 0, place it directly beneath the active card. Do not count exact positions aloud.

**When revealed.** A dark Minor Arcana still resolves at its normal value and retains any Ace, Queen, or King rule. In addition, an intrusion follows based on its suit: Cups disturb memory or feeling; Pentacles alter an object or route; Swords bring threat or painful truth; Wands set an unnatural change in motion. After resolution, a dark card returns to the House Deck's discard pile rather than the player's discard pile.

**Dark Major Arcana.** A dark Major creates a House Layer like any other Major, but it is targeted at the character whose deck carried it. It may expose their Weakness, imitate an established personal detail, or reshape a room around something they brought into the house.

## Grounding

Grounding measures a character's ability to distinguish themselves from the house and the future pressing upon them. Each character begins with six counters. Keep them visible near the character sheet.

**Losing Grounding.** Move a counter into the central pool when a Queen is used, when a rule specifically requires it, or when Grounding loss is offered as a consequence appropriate to psychic strain, isolation, possession, or surrendering part of oneself.

**Regaining Grounding.** An Ace returns one of that character's counters from the pool, up to six. Certain discoveries, honest connections, safe rooms, or a meaningful personal turning point may also restore Grounding, when the moment genuinely calls for it.

**At zero: Unmoored.** An Unmoored character remains playable, but the boundary between character and house has opened. Turn their visible Premonition face down; they must now draw tests blindly. Whenever they fail a test or use a Queen, a House card may be inserted directly beneath the top card instead of removing another Grounding.

An Unmoored character can recover only by an Ace, or by accepting meaningful help in a place of safety.

## Physical harm

Physical harm is described specifically rather than tracked with points or boxes. A character might suffer a sprained ankle, a bleeding hand, a concussion, or broken ribs. The injury affects only actions it would reasonably hinder or prevent.

Failing a Vigor test does not automatically cause physical harm. The consequence follows the danger established before the test. Failing to lift a fallen beam may simply leave it blocking the way; failing to jump across a hole may cause a fall and an injury.

Another test happens only when an injury makes a later action dangerous or uncertain. Appropriate medical attention changes what the injury prevents or how it may worsen. Providing ordinary care does not require a test unless pressure, inadequate supplies, an unusual injury, or another meaningful uncertainty makes failure consequential.

## Tools

A Tool can be used in any way the physical object reasonably permits. Its description establishes what the character carries and any unusual qualities it possesses; it does not limit the Tool to one listed action. Using a Tool does not require a test when it makes the outcome safe and certain. A test happens only when meaningful danger or uncertainty remains.
