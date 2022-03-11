# Design

This is the design and plan of the game. The features described below are not fully implemented.

## Table of Contents
- [Design](#design)
  - [Table of Contents](#table-of-contents)
  - [Story](#story)
    - [Theme](#theme)
  - [Level Design](#level-design)
  - [Gameplay](#gameplay)
    - [Goals](#goals)
    - [Quests](#quests)
    - [Advancements](#advancements)
    - [Losing](#losing)
    - [Abilities](#abilities)
      - [Adaptive Abilities](#adaptive-abilities)
      - [Pawn Unique Abilities](#pawn-unique-abilities)
      - [Pawn Abilities](#pawn-abilities)
      - [King Abilities](#king-abilities)
  - [Art](#art)

## Story

You are a survivor of the last chess apocalypse. You can obtain chess piece variants with special abilities, play against wicked creatures, adventure the wild or crawl the dungeons, conquer the Chaos of Chess.

### Theme

The central theme of the game is light, but semi-horror style appear after mid-game. The game is also encouraging for the player to progress.

## Level Design

Player can grind for pieces, materials and coins at different regions in the game to choose difficulty.

ChessChaos includes the following gamemodes:
* Adventure: fight against mobs with random pieces and position.
* Dungeon: do multiple chess battle and lose hp upon losing a game, up to losing 3.
* Chaos: Starting pieces are randomized on the same rank.

## Gameplay

The player has a set of vanilla chess pieces. New pieces or variants can be obtained by doing quests, dungeons, or can be bought from NPCs. Abilities are sometimes applied when a piece is obtained, or can be added from doing quests or at the NPCs.

There are different regions the player can explore, each revealing unique NPCs, workstations, mobs and resources etc.

### Goals

Overall: Survive in the apocalypse and improve yourself to conquer the Chess Chaos.

Gameplay: Grind for better pieces, unlock new regions, beat tougher mobs.

### Quests

Use advancing quests to guide the player through progression and give them a sense of advancement.

### Advancements

### Losing

### Abilities

Piece abilities can be applied when obtained or added to a piece. **All the unique conflicts each other for game balance.**

**Every pawn can move 2 steps ahead in certain direction on the first move, and en passant rule is always applied.**

Piece type abbreviations are used to simplify the description. Each letter represents a piece type:

letter | piece type
------ | ----------
P      | pawn
N      | knight
B      | bishop
R      | rook
Q      | queen
K      | king

Partially inspired by [chess.com](https://www.chess.com/article/view/10-remarkable-chess-pieces-youve-never-seen)

#### Adaptive Abilities

- Leaper: Can leap like a Knight. (BRQK)
- Aimer: Capture only after leaping over one other piece. (BRQ)
- Spooky: Cannot be captured by enemy king. (NBRQ)
- Shadow: When moved, for the next enemy move, enemy king cannot move onto squares that the piece previously can move to. (NBRQ)
- Sneaker: Can move one square in any direction. (NBR)
- Ranger: Captures without moving onto the target square. (NBRQK)
- Rider: Moves/captures any number of unblocked steps as a knight in the same direction. (NBRQK)

#### Pawn Unique Abilities

- Charger: Moves/captures only one square forward.
- Drunkard: Moves one step diagonally forward, captures one square forward.
- Soldier: Moves/captures one step forward or horizontally.
- Sergeant: Moves/captures one step forward or diagonally.
- Berserker: Moves/captures one step forward, diagonally or horizontally.

#### Pawn Abilities

- Coward: Can always move 2 squares ahead.
- Expendable: Can be captured by alleys.
- Pacifist: Cannot capture pawns or be captured by pawns
- Explorer: Can be placed on the 3rd or 6th rank.
- Pioneer: Can be placed on the 3rd, 4th, 5th, or 6th rank.

#### King Abilities

- Commander: Allow backrank piece order to be customizable.
- Grimace: Can capture king on the same file without intervening pieces.
- Barterer: If exist a move to check opponent after checkmate, the game is drawn.
- Abomination: Can capture king on the same file or same rank without intervening pieces.
- Panic: Can make 2 moves when checked. The first move needn't move out of check.
- Teleporter: Can castle when checked or the crossing square is attacked.
- Ghost: Teleporter, and can castle infinitely in any direction even if king or rook is moved.

## Art

For the chess pieces, _Neo_ style is used as png assets. In the future, SVG chess assets will be used to implement visual abilities.

