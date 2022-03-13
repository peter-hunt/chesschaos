__all__ = [
    'ABILITY_CATEGORIES', 'FLAGS', 'B_NONE', 'S_NONE',
    'S_TYPE', 'S_UNIQUE_TYPE', 'B_TYPE', 'B_UNIQUE_TYPE',
]

ABILITY_CATEGORIES = (
    'adaptive', 'pawn_unique', 'pawn', 'king',
)

B_NONE = 0

S_NONE = ()
S_ADAPTIVE = (
    'cannon', 'sneaker', 'shock', 'leaper', 'shifty', 'chivalry', 'spooky',
    'ruthless', 'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow')
S_PAWN_UNIQUE = (
    'charger', 'drunkard', 'soldier', 'sergeant', 'berserker')
S_PAWN = ('coward', 'expendable', 'eagle', 'explorer', 'pacifist', 'pioneer')
S_KING = (
    'commander', 'grimace', 'barterer', 'sluggard',
    'abomination', 'panic', 'stubborn', 'ghost')
S_ALL = S_ADAPTIVE + S_PAWN_UNIQUE + S_PAWN + S_KING

S_TYPE = (
    S_PAWN,
    ('sneaker', 'shock', 'shifty', 'chivalry', 'spooky', 'ruthless',
     'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'sneaker', 'shock', 'leaper', 'chivalry', 'spooky', 'ruthless',
     'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'sneaker', 'shock', 'leaper', 'shifty', 'chivalry', 'spooky',
     'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'shock', 'leaper', 'chivalry', 'spooky',
     'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('ranger', 'nostalgic', 'poiscent') + S_KING,
)

S_UNIQUE_TYPE = (S_PAWN_UNIQUE, (), (), (), (), ())

FLAGS = {}
for i, name in enumerate(S_ALL):
    FLAGS[name] = 1 << i
    globals()[f'B_{name.upper()}'] = 1 << i

B_ALL = 2 ** len(FLAGS) - 1

for category in ABILITY_CATEGORIES:
    flag = 0
    for ability in globals()[f'S_{category.upper()}']:
        globals()[f'B_{ability.upper()}'] = FLAGS[ability]
        flag |= FLAGS[ability]
    globals()[f'B_{category.upper()}'] = flag
    __all__.append(f'B_{category.upper()}')
    __all__.append(f'S_{category.upper()}')

B_TYPE = [0, 0, 0, 0, 0, 0]
for i, abilities in enumerate(S_TYPE):
    for ability in abilities:
        B_TYPE[i] |= FLAGS[ability]

B_UNIQUE_TYPE = [0, 0, 0, 0, 0, 0]
for i, abilities in enumerate(S_UNIQUE_TYPE):
    for ability in abilities:
        B_UNIQUE_TYPE[i] |= FLAGS[ability]
