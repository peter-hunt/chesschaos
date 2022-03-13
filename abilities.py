__all__ = [
    'ABILITY_CATEGORIES', 'FLAGS', 'UNIQUE_FLAGS',
    'S_NONE', 'S_ALL', 'S_ALL_UNIQUE', 'S_TYPE', 'S_UNIQUE_TYPE',
    'S_ADAPTIVE', 'S_PAWN', 'S_KING', 'S_PAWN_UNIQUE',
    'B_NONE', 'B_ALL', 'B_TYPE', 'B_UNIQUE_TYPE', 'B_ADAPTIVE', 'B_PAWN', 'B_KING',
    'B_CANNON', 'B_SNEAKER', 'B_SHOCK', 'B_LEAPER', 'B_SHIFTY', 'B_CHIVALRY',
    'B_SPOOKY', 'B_RUTHLESS', 'B_RANGER', 'B_RIDER', 'B_NOSTALGIC', 'B_POISCENT',
    'B_SHADOW', 'B_COWARD', 'B_EXPENDABLE', 'B_EAGLE', 'B_EXPLORER', 'B_PACIFIST',
    'B_PIONEER', 'B_COMMANDER', 'B_GRIMACE', 'B_BARTERER', 'B_SLUGGARD',
    'B_ABOMINATION', 'B_PANIC', 'B_STUBBORN', 'B_GHOST', 'B_CHARGER', 'B_DRUNKARD',
    'B_SOLDIER', 'B_SERGEANT', 'B_BERSERKER']

ABILITY_CATEGORIES = ('adaptive', 'pawn', 'king')
FLAGS = {
    'cannon': 1, 'sneaker': 2, 'shock': 4, 'leaper': 8, 'shifty': 16, 'chivalry': 32,
    'spooky': 64, 'ruthless': 128, 'ranger': 256, 'rider': 512, 'nostalgic': 1024,
    'poiscent': 2048, 'shadow': 4096, 'coward': 8192, 'expendable': 16384,
    'eagle': 32768, 'explorer': 65536, 'pacifist': 131072, 'pioneer': 262144,
    'commander': 524288, 'grimace': 1048576, 'barterer': 2097152, 'sluggard': 4194304,
    'abomination': 8388608, 'panic': 16777216, 'stubborn': 33554432, 'ghost': 67108864}
UNIQUE_FLAGS = {'charger': 1, 'drunkard': 2,
                'soldier': 3, 'sergeant': 4, 'berserker': 5}
S_NONE = ()
S_ALL = ('cannon', 'sneaker', 'shock', 'leaper', 'shifty', 'chivalry', 'spooky',
         'ruthless', 'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow', 'coward',
         'expendable', 'eagle', 'explorer', 'pacifist', 'pioneer', 'commander',
         'grimace', 'barterer', 'sluggard', 'abomination', 'panic', 'stubborn', 'ghost')
S_ALL_UNIQUE = ('charger', 'drunkard', 'soldier', 'sergeant', 'berserker')
S_TYPE = (
    ('coward', 'expendable', 'eagle', 'explorer', 'pacifist', 'pioneer'),
    ('sneaker', 'shock', 'shifty', 'chivalry', 'spooky', 'ruthless', 'ranger', 'rider',
     'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'sneaker', 'shock', 'leaper', 'chivalry', 'spooky', 'ruthless', 'ranger',
     'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'sneaker', 'shock', 'leaper', 'shifty', 'chivalry', 'spooky', 'ranger',
     'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'shock', 'leaper', 'chivalry', 'spooky', 'ranger', 'rider', 'nostalgic',
     'poiscent', 'shadow'),
    ('ranger', 'nostalgic', 'poiscent', 'commander', 'grimace', 'barterer', 'sluggard',
     'abomination', 'panic', 'stubborn', 'ghost'))
S_UNIQUE_TYPE = (
    ('charger', 'drunkard', 'soldier', 'sergeant', 'berserker'), (), (), (), (), ())
S_ADAPTIVE = ('cannon', 'sneaker', 'shock', 'leaper', 'shifty', 'chivalry',
              'spooky', 'ruthless', 'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow')
S_PAWN = ('coward', 'expendable', 'eagle', 'explorer', 'pacifist', 'pioneer')
S_KING = ('commander', 'grimace', 'barterer', 'sluggard',
          'abomination', 'panic', 'stubborn', 'ghost')
S_PAWN_UNIQUE = ('charger', 'drunkard', 'soldier', 'sergeant', 'berserker')
B_NONE = 0x00000000
B_ALL = 0x07ffffff
B_TYPE = [516096, 8182, 8175, 8063, 8045, 133696768]
B_UNIQUE_TYPE = [5, 0, 0, 0, 0, 0]
B_ADAPTIVE = 0x00001fff
B_PAWN = 0x0007e000
B_KING = 0x07f80000
B_CANNON = 0x00000001
B_SNEAKER = 0x00000002
B_SHOCK = 0x00000004
B_LEAPER = 0x00000008
B_SHIFTY = 0x00000010
B_CHIVALRY = 0x00000020
B_SPOOKY = 0x00000040
B_RUTHLESS = 0x00000080
B_RANGER = 0x00000100
B_RIDER = 0x00000200
B_NOSTALGIC = 0x00000400
B_POISCENT = 0x00000800
B_SHADOW = 0x00001000
B_COWARD = 0x00002000
B_EXPENDABLE = 0x00004000
B_EAGLE = 0x00008000
B_EXPLORER = 0x00010000
B_PACIFIST = 0x00020000
B_PIONEER = 0x00040000
B_COMMANDER = 0x00080000
B_GRIMACE = 0x00100000
B_BARTERER = 0x00200000
B_SLUGGARD = 0x00400000
B_ABOMINATION = 0x00800000
B_PANIC = 0x01000000
B_STUBBORN = 0x02000000
B_GHOST = 0x04000000
B_CHARGER = 0x00000001
B_DRUNKARD = 0x00000002
B_SOLDIER = 0x00000003
B_SERGEANT = 0x00000004
B_BERSERKER = 0x00000005
