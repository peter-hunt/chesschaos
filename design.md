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

The combat system is based on chess, which rules are explained on [Wikipedia](https://en.wikipedia.org/wiki/Rules_of_chess).

## Level Design

Player can grind for pieces, materials and coins at different regions in the game to choose difficulty. The game estimates the player's power from the pieces and placement, and generate random levels with enemy power based on the player power.

ChessChaos includes the following game modes:

- Adventure: fight against mobs with random pieces and position.
- Dungeon: do multiple chess battle and lose hp upon losing a game, up to losing 3.
- Chaos: Starting pieces are randomized on the same rank.

## Gameplay

The player has a set of vanilla chess pieces. New items or variants can be obtained by doing quests, dungeons, or can be bought from NPCs. Abilities are sometimes applied when a piece is obtained, or can be added from doing quests or at the NPCs.

There are different regions the player can explore, each revealing unique NPCs, workstations, mobs and resources etc.

## Goals

Overall: Survive in the apocalypse and improve yourself to conquer the Chess Chaos.

Gameplay: Grind for better items, unlock new regions, beat tougher mobs.

## Quests

Use advancing quests to guide the player through progression and give them a sense of advancement.

## Advancements

Use advancements to encourage the player to grind for unique items, beat certain levels, and collect things in endgame.

## Losing

When the player loses a level, the game gives the player a penalty of not receiving any loot on the next game, cumulatively. This is to make the player seek better items rather than trying to brute-force a level with starter gear, although it is still possible

## Abilities

Piece abilities can be applied when obtained or added to a piece. **All the unique conflicts each other for game balance.**

**Every pawn can move 2 steps ahead in certain direction on the first move, and en passant rule is always applied.**

Piece type abbreviations are used to simplify the description. Each letter represents a piece type:

| letter | piece type |
| ------ | ---------- |
| P      | pawn       |
| N      | knight     |
| B      | bishop     |
| R      | rook       |
| Q      | queen      |
| K      | king       |

Partially inspired by [chess.com](https://www.chess.com/article/view/10-remarkable-chess-pieces-youve-never-seen)

### Adaptive Abilities

- Cannon (BRQ)
- - Capture only after leaping over one other piece.
- Sneaker: (NBR)
- - Can move one square in any direction.
- Shock (NBRQ)
- - When moved, for the next enemy move, enemy king cannot capture this piece.
- Leaper (BRQ)
- - Can move like a Knight.
- Shifty (NR)
- - Can move like a Bishop.
- Chivalry (NBRQ)
- - When moved, for the next enemy move, enemy pawn cannot capture this piece.
- Spooky (NBRQ)
- - Cannot be captured by enemy king.
- Ruthless (NB)
- - Can move like a Rook.
- Ranger (NBRQK)
- - Can capture without moving onto the target square.
- Rider (NBRQ)
- - Can moves/capture on any number of unblocked steps as a knight in the same direction.
- Nostalgic (NBRQK)
- - Can capture by stepping on the enemy piece's last square.
- Poi-scent (NBRQK)
- - When moved, for the next enemy move, enemy piece cannot move onto your piece's last square.
- Shadow (NBRQ)
- - When moved, for the next enemy move, enemy king cannot move onto squares that the piece previously can move to.

### Pawn Unique Abilities

- Charger
- - Moves/captures only one square forward.
- Drunkard
- - Moves one step diagonally forward, captures one square forward.
- Soldier
- - Moves/captures one step forward or horizontally.
- Sergeant
- - Moves/captures one step forward or diagonally.
- Berserker
- - Moves/captures one step forward, diagonally or horizontally.

### Pawn Abilities

- Coward
- - Can always move 2 squares ahead.
- Expendable
- - Can be captured by alleys.
- Eagle
- - Promote on the 2nd or 7th rank.
- Explorer
- - Can be placed on the 3rd or 6th rank.
- Pacifist
- - Cannot capture pawns or be captured by pawns
- Pioneer
- - Can be placed on the 3rd, 4th, 5th, or 6th rank.

### King Abilities

- Commander
- - Allow back-rank piece order to be customizable.
- Grimace
- - Can capture king on the same file without intervening pieces.
- Barterer
- - If exist a move to check enemy after checkmate, the game is drawn.
- Sluggard
- - Can pass the move and force enemy to make a move.
- Abomination
- - Can capture king on the same file or same rank without intervening pieces.
- Panic
- - Can make 2 moves when checked. The first move needn't move out of check.
- Stubborn
- - Can castle when checked or the crossing square is attacked.
- Ghost
- - Stubborn, and can castle infinitely in any direction even if king or rook is moved.

## Art

For the chess pieces, _Neo_ style is used as PGN assets. In the future, SVG chess assets will be used to implement visual abilities.
