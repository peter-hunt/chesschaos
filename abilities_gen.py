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
    'abomination', 'panic', 'stubborn', 'ghost', 'rapid')

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
    def chunks(lst, size):
        return [lst[i:i + size] for i in range(0, len(lst), size)]

    names = [
        ['ABILITY_CATEGORIES', 'FLAGS', 'UNIQUE_FLAGS'],
        ['S_NONE', 'S_ALL', 'S_ALL_UNIQUE', 'S_TYPE', 'S_UNIQUE_TYPE'],
        ['S_ADAPTIVE', 'S_PAWN', 'S_KING', 'S_PAWN_UNIQUE'],
        ['B_NONE', 'B_ALL', 'B_TYPE', 'B_UNIQUE_TYPE'],
        ['B_ADAPTIVE', 'B_PAWN', 'B_KING'],
    ]
    specials = sum(names, start=[])
    bit_names = [name for name in __all__ if name.startswith('B_')]
    bit_names = sorted(
        {*bit_names} - {*specials},
        key=lambda name: (S_ALL + S_ALL_UNIQUE).index(name[2:].lower()))
    names.extend(chunks(bit_names, 4))
    all_vars = {name: globals()[name] for name in sum(names, start=[])}

    builder = ['__all__ = [']
    for group in names:
        builder.append('\n    ' + ', '.join(f'{name!r}' for name in group) + ',')
    builder[-1] = builder[-1][:-1] + ']\n\n'
    vars = '\n'.join(
        f'{name} = ' +
        ('{\n    ' + f',\n    '.join(f'{flag!r}: 0x{num:08x}'.upper().replace('0X', '0x')
                                     for flag, num in value.items()) + '}'
         if name == 'FLAGS' else
         '[' + f', '.join(f'0x{num:08x}'.upper().replace('0X', '0x')
                          for num in value) + ']'
         if name == 'B_TYPE' else
         '{\n    ' + f',\n    '.join(f'{flag!r}: {num}' for flag, num in value.items()) + '}'
         if name == 'UNIQUE_FLAGS' else
         '(\n    ' + f',\n    '.join(f'{item}' for item in value) + ')'
         if name in {'S_TYPE'} else
         '(\n    ' + f',\n    '.join(', '.join(f'{item!r}' for item in group)
                                     for group in chunks(value, 4)) + ')'
         if name in {'S_ALL', 'S_ADAPTIVE', 'S_PAWN', 'S_KING', 'S_PAWN_UNIQUE', 'S_ALL_UNIQUE'} else
         f'0x{value:08x}'
         if isinstance(value, int) and name.startswith('B_') else
         f'{value}') for name, value in all_vars.items()
    )
    builder.append(vars)
    code = ''.join(builder)

    with open('./abilities.py', 'w') as file:
        file.write(code)
