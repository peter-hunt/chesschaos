__all__ = [
    'ABILITY_CATEGORIES', 'FLAGS', 'UNIQUE_FLAGS',
    'S_NONE', 'S_ALL', 'S_ALL_UNIQUE', 'S_TYPE', 'S_UNIQUE_TYPE',
    'S_ADAPTIVE', 'S_PAWN', 'S_KING', 'S_PAWN_UNIQUE',
    'B_NONE', 'B_ALL', 'B_TYPE', 'B_UNIQUE_TYPE',
    'B_ADAPTIVE', 'B_PAWN', 'B_KING',
    'B_CANNON', 'B_SNEAKER', 'B_SHOCK', 'B_LEAPER',
    'B_SHIFTY', 'B_CHIVALRY', 'B_SPOOKY', 'B_RUTHLESS',
    'B_RANGER', 'B_RIDER', 'B_NOSTALGIC', 'B_POISCENT',
    'B_SHADOW', 'B_COWARD', 'B_EXPENDABLE', 'B_EAGLE',
    'B_EXPLORER', 'B_PACIFIST', 'B_PIONEER', 'B_COMMANDER',
    'B_GRIMACE', 'B_BARTERER', 'B_SLUGGARD', 'B_ABOMINATION',
    'B_PANIC', 'B_STUBBORN', 'B_GHOST', 'B_RAPID',
    'B_CHARGER', 'B_DRUNKARD', 'B_SOLDIER', 'B_SERGEANT',
    'B_BERSERKER']

ABILITY_CATEGORIES = ('adaptive', 'pawn', 'king')
FLAGS = {
    'CANNON': 0x00000001,
    'SNEAKER': 0x00000002,
    'SHOCK': 0x00000004,
    'LEAPER': 0x00000008,
    'SHIFTY': 0x00000010,
    'CHIVALRY': 0x00000020,
    'SPOOKY': 0x00000040,
    'RUTHLESS': 0x00000080,
    'RANGER': 0x00000100,
    'RIDER': 0x00000200,
    'NOSTALGIC': 0x00000400,
    'POISCENT': 0x00000800,
    'SHADOW': 0x00001000,
    'COWARD': 0x00002000,
    'EXPENDABLE': 0x00004000,
    'EAGLE': 0x00008000,
    'EXPLORER': 0x00010000,
    'PACIFIST': 0x00020000,
    'PIONEER': 0x00040000,
    'COMMANDER': 0x00080000,
    'GRIMACE': 0x00100000,
    'BARTERER': 0x00200000,
    'SLUGGARD': 0x00400000,
    'ABOMINATION': 0x00800000,
    'PANIC': 0x01000000,
    'STUBBORN': 0x02000000,
    'GHOST': 0x04000000,
    'RAPID': 0x08000000}
UNIQUE_FLAGS = {
    'charger': 1,
    'drunkard': 2,
    'soldier': 3,
    'sergeant': 4,
    'berserker': 5}
S_NONE = ()
S_ALL = (
    'cannon', 'sneaker', 'shock', 'leaper',
    'shifty', 'chivalry', 'spooky', 'ruthless',
    'ranger', 'rider', 'nostalgic', 'poiscent',
    'shadow', 'coward', 'expendable', 'eagle',
    'explorer', 'pacifist', 'pioneer', 'commander',
    'grimace', 'barterer', 'sluggard', 'abomination',
    'panic', 'stubborn', 'ghost', 'rapid')
S_ALL_UNIQUE = (
    'charger', 'drunkard', 'soldier', 'sergeant',
    'berserker')
S_TYPE = (
    ('coward', 'expendable', 'eagle', 'explorer', 'pacifist', 'pioneer'),
    ('sneaker', 'shock', 'shifty', 'chivalry', 'spooky', 'ruthless', 'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'sneaker', 'shock', 'leaper', 'chivalry', 'spooky', 'ruthless', 'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'sneaker', 'shock', 'leaper', 'shifty', 'chivalry', 'spooky', 'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('cannon', 'shock', 'leaper', 'chivalry', 'spooky', 'ranger', 'rider', 'nostalgic', 'poiscent', 'shadow'),
    ('ranger', 'nostalgic', 'poiscent', 'commander', 'grimace', 'barterer', 'sluggard', 'abomination', 'panic', 'stubborn', 'ghost', 'rapid'))
S_UNIQUE_TYPE = (('charger', 'drunkard', 'soldier', 'sergeant', 'berserker'), (), (), (), (), ())
S_ADAPTIVE = (
    'cannon', 'sneaker', 'shock', 'leaper',
    'shifty', 'chivalry', 'spooky', 'ruthless',
    'ranger', 'rider', 'nostalgic', 'poiscent',
    'shadow')
S_PAWN = (
    'coward', 'expendable', 'eagle', 'explorer',
    'pacifist', 'pioneer')
S_KING = (
    'commander', 'grimace', 'barterer', 'sluggard',
    'abomination', 'panic', 'stubborn', 'ghost',
    'rapid')
S_PAWN_UNIQUE = (
    'charger', 'drunkard', 'soldier', 'sergeant',
    'berserker')
B_NONE = 0x00000000
B_ALL = 0x0fffffff
B_TYPE = [0x0007E000, 0x00001FF6, 0x00001FEF, 0x00001F7F, 0x00001F6D, 0x0FF80D00]
B_UNIQUE_TYPE = [5, 0, 0, 0, 0, 0]
B_ADAPTIVE = 0x00001fff
B_PAWN = 0x0007e000
B_KING = 0x0ff80000
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
B_RAPID = 0x08000000
B_CHARGER = 0x00000001
B_DRUNKARD = 0x00000002
B_SOLDIER = 0x00000003
B_SERGEANT = 0x00000004
B_BERSERKER = 0x00000005