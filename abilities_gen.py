__all__ = [
    'ABILITY_CATEGORIES', 'FLAGS', 'UNIQUE_FLAGS', 'B_NONE', 'S_NONE',
    'S_ALL', 'S_ALL_UNIQUE', 'B_ALL',
    'S_ADAPTIVE', 'S_PAWN', 'S_PAWN_UNIQUE', 'S_KING',
    'S_TYPE', 'S_UNIQUE_TYPE', 'B_TYPE', 'B_UNIQUE_TYPE',
]

ABILITY_CATEGORIES = (
    'adaptive', 'pawn', 'king',
)

B_NONE = 0

S_NONE = ()
S_ADAPTIVE = (
    'cannon', 'sneaker', 'shock', 'leaper', 'shifty', 'chivalry', 'spooky',
    'ruthless', 'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow')
S_PAWN = ('coward', 'expendable', 'eagle', 'explorer', 'pacifist', 'pioneer')
S_KING = (
    'commander', 'grimace', 'barterer', 'sluggard',
    'abomination', 'panic', 'stubborn', 'ghost')

S_PAWN_UNIQUE = (
    'charger', 'drunkard', 'soldier', 'sergeant', 'berserker')

S_ALL = S_ADAPTIVE + S_PAWN + S_KING
S_ALL_UNIQUE = S_PAWN_UNIQUE

ADAPTIVES = (
    ('cannon', 'BRQ'),
    ('sneaker', 'NBR'),
    ('shock', 'NBRQ'),
    ('leaper', 'BRQ'),
    ('shifty', 'NR'),
    ('chivalry', 'NBRQ'),
    ('spooky', 'NBRQ'),
    ('ruthless', 'NB'),
    ('ranger', 'NBRQK'),
    ('rider', 'NBRQ'),
    ('nostalgic', 'NBRQK'),
    ('poiscent', 'NBRQK'),
    ('shadow', 'NBRQ'),
)

S_TYPE = (
    S_PAWN,
    tuple(adp[0] for adp in ADAPTIVES if 'N' in adp[1]),
    tuple(adp[0] for adp in ADAPTIVES if 'B' in adp[1]),
    tuple(adp[0] for adp in ADAPTIVES if 'R' in adp[1]),
    tuple(adp[0] for adp in ADAPTIVES if 'Q' in adp[1]),
    tuple(adp[0] for adp in ADAPTIVES if 'K' in adp[1]) + S_KING,
)

S_UNIQUE_TYPE = (S_PAWN_UNIQUE, (), (), (), (), ())

FLAGS = {}
for i, name in enumerate(S_ALL):
    FLAGS[name] = 1 << i
    globals()[f'B_{name.upper()}'] = 1 << i
    __all__.append(f'B_{name.upper()}')

UNIQUE_FLAGS = {}
for pt in range(6):
    for i, name in enumerate(S_UNIQUE_TYPE[pt], 1):
        UNIQUE_FLAGS[name] = i
        globals()[f'B_{name.upper()}'] = i
        __all__.append(f'B_{name.upper()}')

B_ALL = 2 ** len(FLAGS) - 1

for category in ABILITY_CATEGORIES:
    flag = 0
    for ability in globals()[f'S_{category.upper()}']:
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
    B_UNIQUE_TYPE[i] = len(abilities)


if __name__ == '__main__':
    _all_ = ['ABILITY_CATEGORIES', 'FLAGS', 'UNIQUE_FLAGS']
    _b_all_ = [name for name in __all__ if name.startswith('B_')]
    _b_special_ = ['B_NONE', 'B_ALL', 'B_TYPE', 'B_UNIQUE_TYPE',
                   'B_ADAPTIVE', 'B_PAWN', 'B_KING']
    _b_all_ = _b_special_ + sorted(
        {*_b_all_} - {*_b_special_},
        key=lambda name: (S_ALL + S_ALL_UNIQUE).index(name[2:].lower()))
    _s_all_ = ['S_NONE', 'S_ALL', 'S_ALL_UNIQUE', 'S_TYPE', 'S_UNIQUE_TYPE',
               'S_ADAPTIVE', 'S_PAWN', 'S_KING', 'S_PAWN_UNIQUE']
    _all_ += _s_all_ + _b_all_
    code = f'__all__ = {_all_}\n\n' + '\n'.join(
        f'{name} = 0x{value:08x}'
        if isinstance(value := globals()[name], int) and name.startswith('B_') else
        f'{name} = {value}'
        for name in _all_
    )
    with open('./abilities.py', 'w') as file:
        file.write(code)
