import os
from copy import copy

import pygame
import ujson

from scripts.game_structure.game_essentials import game


class Sprites:
    cat_tints = {}
    white_patches_tints = {}
    clan_symbols = []

    def __init__(self):
        """Class that handles and hold all spritesheets. 
        Size is normally automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.symbol_dict = None
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None

        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading Tints")
        #If you want less white patches, place hashtags below!
        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading White Patches Tints")

        #If you want less white patches, place hashtages above and remove below!
        #try:
            #with open("sprites/dicts/white_patches_lesstint.json", 'r') as read_file:
                #self.white_patches_tints = ujson.loads(read_file.read())
        #except IOError:
            #print("ERROR: Reading White Patches Less Tints")
        #If you want less white patches, remove hashtags above!

    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7,
                   no_index=False):  # pos = ex. (2, 3), no single pixels

        """
        Divide sprites on a spritesheet into groups of sprites that are easily accessible
        :param spritesheet: Name of spritesheet file
        :param pos: (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites
        :param name: Name of group being made
        :param sprites_x: default 3, number of sprites horizontally
        :param sprites_y: default 3, number of sprites vertically
        :param no_index: default False, set True if sprite name does not require cat pose index
        """

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                if no_index:
                    full_name = f"{name}"
                else:
                    full_name = f"{name}{i}"

                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )

                except ValueError:
                    # Fallback for non-existent sprites
                    print(f"WARNING: nonexistent sprite - {full_name}")
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite

                self.sprites[full_name] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart  # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50  # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and "
                  f"do a search for 'if width / 3 == height / 7:'")

        del width, height  # unneeded

        for x in [
            'lineart', 'lineartdf', 'lineartdead',
            'eyes', 'eyes2', 'skin', 'gilltongue', 'beagilltongue', 'horns', 'fancyskin', 
            'scars', 'missingscars',
            'medcatherbs',
            'collars', 'bellcollars', 'bowcollars', 'nyloncollars', 'rwlizards', 'drones', 'muddypaws', 
            'herbs2', 'insectwings', 'buddies', 'newaccs', 'bodypaint', 'implant', 'magic', 'necklaces',
            'newaccs2', 'drapery', 'eyepatches', 'pridedrapery', 'larsaccs', 'harleyaccs',
            'singlecolours', 'speckledcolours', 'tabbycolours', 'bengalcolours', 'marbledcolours',
            'rosettecolours', 'smokecolours', 'tickedcolours', 'mackerelcolours', 'classiccolours',
            'sokokecolours', 'agouticolours', 'singlestripecolours', 'maskedcolours', 'bananacolours',
            'centipedecolours', 'collaredcolours', 'concolours', 'gravelcolours', 'cyanlizardcolours',
            'slimemoldcolours', 'lanterncolours', 'vulturecolours', 'lizardcolours', 'leviathancolours',
            'fluffycolours', 'amoebacolours', 'seaslugcolours', 'yeekcolours', 'rustedcolours',
            'envoycolours', 'drizzlecolours', 'solacecolours', 'leafycolours', 'scaledcolours', 
            'dragonfruitcolours', 'necklacecolours', 'dreamercolours', 'duskdawncolours', 
            'seercolours', 'rottencolours', 'firecolours', 'countershadedcolours', 'cherrycolours',
            'oldgrowthcolours', 'sparklecatcolours', 'wolfcolours', 'sunsetcolours', 'hypnotistcolours',
            'ringedcolours', 'skinnycolours', 'sparsecolours', 'impishcolours', 'sportycolours', 
            'fizzycolours', 'skeletoncolours', 'shredcolours', 'glowingcolours', 'moldcolours', 'swingcolours',
            'raineyes', 'raineyes2', 'multieyes', 'multiraineyes', 'larseyes', 'multilarseyes', 'larseyes2', 'rivuleteyes', 'rivuleteyes2',
            'buttoneyes', 'buttoneyes2'
            'shadersnewwhite', 'lightingnew',
            'whitepatches', 'tortiepatchesmasks',
            'fademask', 'fadestarclan', 'fadedarkforest',
            'symbols'
        ]:
            if 'lineart' in x and game.config['fun']['april_fools']:
                self.spritesheet(f"sprites/aprilfools{x}.png", x)
            elif 'lineart' in x and game.settings['christmas_time']:
                self.spritesheet(f"sprites/christmas{x}.png", x)
            else:
                self.spritesheet(f"sprites/{x}.png", x)

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        for a, i in enumerate(
                ['YELLOW', 'AMBER', 'HAZEL', 'PALEGREEN', 'GREEN', 'BLUE', 
                'DARKBLUE', 'GREY', 'CYAN', 'EMERALD', 'HEATHERBLUE', 'SUNLITICE']):
            self.make_group('eyes', (a, 0), f'eyes{i}')
            self.make_group('eyes2', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['COPPER', 'SAGE', 'COBALT', 'PALEBLUE', 'BRONZE', 'SILVER',
                'PALEYELLOW', 'GOLD', 'GREENYELLOW', 'RED', 'PURPLE', 'MAUVE']):
            self.make_group('eyes', (a, 1), f'eyes{i}')
            self.make_group('eyes2', (a, 1), f'eyes2{i}')
        #rain's eyes
        for a, i in enumerate(
                ['ELECTRICBLUE', 'VIOLET', 'PINK', 'SNOW', 'ORANGE', 'CREAM', 'SEAFOAM', 'CRIMSON', 'NAVY', 'VOIDGOLD', 'COOLBROWN', 'PLUM']):
            self.make_group('raineyes', (a, 0), f'eyes{i}')
            self.make_group('raineyes2', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['INDIGO', 'LILAC']):
            self.make_group('raineyes', (a, 1), f'eyes{i}')
            self.make_group('raineyes2', (a, 1), f'eyes2{i}')
        #multieyes
        for a, i in enumerate(
                ['MULTIYELLOW', 'MULTIAMBER', 'MULTIHAZEL', 'MULTIPALEGREEN', 'MULTIGREEN', 'MULTIBLUE', 
                'MULTIDARKBLUE', 'MULTIGREY', 'MULTICYAN', 'MULTIEMERALD', 'MULTIHEATHERBLUE', 'MULTISUNLITICE']):
            self.make_group('multieyes', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['MULTICOPPER', 'MULTISAGE', 'MULTICOBALT', 'MULTIPALEBLUE', 'MULTIBRONZE', 'MULTISILVER',
                'MULTIPALEYELLOW', 'MULTIGOLD', 'MULTIGREENYELLOW', 'MULTIRED', 'MULTIPURPLE', 'MULTIMAUVE']):
            self.make_group('multieyes', (a, 1), f'eyes2{i}')
        #multieyes rain's colors
        for a, i in enumerate(
                ['MULTIELECTRICBLUE', 'MULTIVIOLET', 'MULTIPINK', 'MULTISNOW', 'MULTIORANGE',
                 'MULTICREAM', 'MULTISEAFOAM', 'MULTICRIMSON', 'MULTINAVY', 'MULTIVOIDGOLD',
                 'MULTICOOLBROWN', 'MULTIPLUM']):
            self.make_group('multiraineyes', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['MULTIINDIGO', 'MULTILILAC']):
            self.make_group('multiraineyes', (a, 1), f'eyes2{i}')

        #lars' eyes
        for a, i in enumerate(
                ['ALBA', 'ALBINO', 'ANGEL', 'APPLE', 'AQUA', 'ARID', 'BANANA', 'BLOOD', 'CARNI', 'CHAIN']):
            self.make_group('larseyes', (a, 0), f'eyes{i}')
            self.make_group('larseyes2', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['CREAMY', 'DAWN', 'ESES', 'EXILE', 'FAE', 'FALLSTAR', 'FIELD', 'FOAM', 'HOT', 'IRID']):
            self.make_group('larseyes', (a, 1), f'eyes{i}')
            self.make_group('larseyes2', (a, 1), f'eyes2{i}')
        for a, i in enumerate(
                ['KARMA', 'KIND', 'MARTI', 'MEISTALT', 'MHUNT', 'MELON', 'MESS', 'MEISTER', 'MINT', 'MINV']):
            self.make_group('larseyes', (a, 2), f'eyes{i}')
            self.make_group('larseyes2', (a, 2), f'eyes2{i}')
        for a, i in enumerate(
                ['MOON', 'MRIV', 'PEACH', 'PEBB', 'PELA', 'PEPPER', 'RETRO', 'RUNT', 'RUST', 'SIG']):
            self.make_group('larseyes', (a, 3), f'eyes{i}')
            self.make_group('larseyes2', (a, 3), f'eyes2{i}')
        for a, i in enumerate(
                ['SIXER', 'SPLIT', 'SUN', 'SWEET', 'TIDE', 'VIVID', 'WAVE', 'WINKS', 'ZENI', 'BEAST']):
            self.make_group('larseyes', (a, 4), f'eyes{i}')
            self.make_group('larseyes2', (a, 4), f'eyes2{i}')

        #lars' multi eyes
        for a, i in enumerate(
                ['MULTIALBA', 'MULTIALBINO', 'MULTIANGEL', 'MULTIAPPLE', 'MULTIAQUA', 'MULTIARID', 'MULTIBANANA', 'MULTIBLOOD', 'MULTICARNI', 'MULTICHAIN']):
            self.make_group('multilarseyes', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['MULTICREAMY', 'MULTIDAWN', 'MULTIESES', 'MULTIEXILE', 'MULTIFAE', 'MULTIFALLSTAR', 'MULTIFIELD', 'MULTIFOAM', 'MULTIHOT', 'MULTIIRID']):
            self.make_group('multilarseyes', (a, 1), f'eyes2{i}')
        for a, i in enumerate(
                ['MULTIKARMA', 'MULTIKIND', 'MULTIMARTI', 'MULTIMEISTALT', 'MULTIMHUNT', 'MULTIMELON', 'MULTIMESS', 'MULTIMEISTER', 'MULTIMINT', 'MULTIMINV']):
            self.make_group('multilarseyes', (a, 2), f'eyes2{i}')
        for a, i in enumerate(
                ['MULTIMOON', 'MULTIMRIV', 'MULTIPEACH', 'MULTIPEBB', 'MULTIPELA', 'MULTIPEPPER', 'MULTIRETRO', 'MULTIRUNT', 'MULTIRUST', 'MULTISIG']):
            self.make_group('multilarseyes', (a, 3), f'eyes2{i}')
        for a, i in enumerate(
                ['MULTISIXER', 'MULTISPLIT', 'MULTISUN', 'MULTISWEET', 'MULTITIDE', 'MULTIVIVID', 'MULTIWAVE', 'MULTIWINKS', 'MULTIZENI', 'MULTIBEAST']):
            self.make_group('multilarseyes', (a, 4), f'eyes2{i}')
                    
        #rivulet eyes
        for a, i in enumerate(
                ['RIVYELLOW', 'RIVAMBER', 'RIVHAZEL', 'RIVPALEGREEN', 'RIVGREEN', 'RIVBLUE', 
                'RIVDARKBLUE', 'RIVGREY', 'RIVCYAN', 'RIVEMERALD', 'RIVHEATHERBLUE', 'RIVSUNLITICE']):
            self.make_group('buttoneyes', (a, 0), f'eyes{i}')
            self.make_group('buttoneyes2', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['RIVCOPPER', 'RIVSAGE', 'RIVCOBALT', 'RIVPALEBLUE', 'RIVBRONZE', 'RIVSILVER',
                'RIVPALEYELLOW', 'RIVGOLD', 'RIVGREENYELLOW']):
            self.make_group('buttoneyes', (a, 1), f'eyes{i}')
            self.make_group('buttoneyes2', (a, 1), f'eyes2{i}')
      
        #button eyes (flamedash dev note - currently working at this!)
        for a, i in enumerate(
                ['BUTTONYELLOW', 'BUTTONAMBER', 'BUTTONHAZEL', 'BUTTONPALEGREEN', 'BUTTONGREEN', 'BUTTONBLUE', 
                'BUTTONDARKBLUE', 'BUTTONGREY', 'BUTTONCYAN', 'BUTTONEMERALD', 'BUTTONHEATHERBLUE', 'BUTTONSUNLITICE']):
            self.make_group('buttoneyes', (a, 0), f'eyes{i}')
            self.make_group('buttoneyes2', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['BUTTONCOPPER', 'BUTTONSAGE', 'BUTTONCOBALT', 'BUTTONPALEBLUE', 'BUTTONBRONZE', 'BUTTONSILVER',
                'BUTTONPALEYELLOW', 'BUTTONGOLD', 'BUTTONGREENYELLOW', 'BUTTONIRED', 'BUTTONPURPLE', 'BUTTONMAUVE']):
            self.make_group('buttoneyes', (a, 1), f'eyes{i}')
            self.make_group('buttoneyes2', (a, 1), f'eyes2{i}')
        for a, i in enumerate(
                ['BUTTONINDIGO', 'BUTTONLILAC']):
            self.make_group('buttoneyes', (a, 2), f'eyes2{i}')
            self.make_group('buttoneyes2', (a, 2), f'eyes2{i}')

        # white patches
        for a, i in enumerate(['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO',
            'MOON', 'PHANTOM', 'POWDER', 'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE']):
            self.make_group('whitepatches', (a, 0), f'white{i}')
        for a, i in enumerate(['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL', 
            'LIGHTSONG', 'VITILIGO', 'BLACKSTAR', 'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL']):
            self.make_group('whitepatches', (a, 1), f'white{i}')
        # ryos white patches
        for a, i in enumerate(['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO',
            'PAWS', 'MITAINE', 'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD']):
            self.make_group('whitepatches', (a, 2), f'white{i}')
        for a, i in enumerate(['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY',
            'FAROFA', 'DAMIEN', 'MISTER', 'BELLY', 'TAILTIP', 'TOES', 'TOPCOVER']):
            self.make_group('whitepatches', (a, 3), f'white{i}')
        for a, i in enumerate(
                ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW',
                'PANTS', 'REVERSEPANTS', 'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW']):
            self.make_group('whitepatches', (a, 4), f'white{i}')
        # beejeans white patches + perrio's point marks, painted, and heart2 + anju's new marks + key's blackstar
        for a, i in enumerate(['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT',
            'MAO', 'LUNA', 'CHESTSPECK', 'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER']):
            self.make_group('whitepatches', (a, 5), f'white{i}')
        # acorn's white patches + ryos' bub + fable lovebug + frankie trixie
        for a, i in enumerate(['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART',
            'SPARROW', 'VEST', 'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE']):
            self.make_group('whitepatches', (a, 6), f'white{i}')
        # acorn's white patches: the sequel
        for a, i in enumerate(['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE',
            'FADEBELLY', 'FRONT', 'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS']):
            self.make_group('whitepatches', (a, 7), f'white{i}')
        for a, i in enumerate(['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR',
            'BUSTER', 'SMOKEY', 'HAWKBLAZE', 'CAKE', 'ROSINA', 'PRINCESS']):
            self.make_group('whitepatches', (a, 8), f'white{i}')
        for a, i in enumerate(['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE']):
            self.make_group('whitepatches', (a, 9), 'white' + i)

        # single (solid)
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('singlecolours', (a, 0), f'single{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('singlecolours', (a, 1), f'single{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('singlecolours', (a, 2), f'single{i}')
        # tabby
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('tabbycolours', (a, 0), f'tabby{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('tabbycolours', (a, 1), f'tabby{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('tabbycolours', (a, 2), f'tabby{i}')
        # marbled
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('marbledcolours', (a, 0), f'marbled{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('marbledcolours', (a, 1), f'marbled{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('marbledcolours', (a, 2), f'marbled{i}')
        # rosette
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('rosettecolours', (a, 0), f'rosette{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('rosettecolours', (a, 1), f'rosette{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('rosettecolours', (a, 2), f'rosette{i}')
        # smoke
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('smokecolours', (a, 0), f'smoke{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('smokecolours', (a, 1), f'smoke{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('smokecolours', (a, 2), f'smoke{i}')
        # ticked
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('tickedcolours', (a, 0), f'ticked{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('tickedcolours', (a, 1), f'ticked{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('tickedcolours', (a, 2), f'ticked{i}')
        # speckled
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('speckledcolours', (a, 0), f'speckled{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('speckledcolours', (a, 1), f'speckled{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('speckledcolours', (a, 2), f'speckled{i}')
        # bengal
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('bengalcolours', (a, 0), f'bengal{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('bengalcolours', (a, 1), f'bengal{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('bengalcolours', (a, 2), f'bengal{i}')
        # mackerel
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('mackerelcolours', (a, 0), f'mackerel{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('mackerelcolours', (a, 1), f'mackerel{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('mackerelcolours', (a, 2), f'mackerel{i}')
        # classic
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('classiccolours', (a, 0), f'classic{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('classiccolours', (a, 1), f'classic{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('classiccolours', (a, 2), f'classic{i}')
        # sokoke
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('sokokecolours', (a, 0), f'sokoke{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('sokokecolours', (a, 1), f'sokoke{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('sokokecolours', (a, 2), f'sokoke{i}')
        # agouti
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('agouticolours', (a, 0), f'agouti{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('agouticolours', (a, 1), f'agouti{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('agouticolours', (a, 2), f'agouti{i}')
        # singlestripe
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('singlestripecolours', (a, 0), f'singlestripe{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('singlestripecolours', (a, 1), f'singlestripe{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('singlestripecolours', (a, 2), f'singlestripe{i}')
        # masked tabby
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('maskedcolours', (a, 0), f'masked{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('maskedcolours', (a, 1), f'masked{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('maskedcolours', (a, 2), f'masked{i}')
        # gravel
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('gravelcolours', (a, 0), f'gravel{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('gravelcolours', (a, 1), f'gravel{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('gravelcolours', (a, 2), f'gravel{i}')
        # collared
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('collaredcolours', (a, 0), f'collared{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('collaredcolours', (a, 1), f'collared{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('collaredcolours', (a, 2), f'collared{i}')
        # slimemold
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('slimemoldcolours', (a, 0), f'slimemold{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('slimemoldcolours', (a, 1), f'slimemold{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('slimemoldcolours', (a, 2), f'slimemold{i}')
        # cyan lizard
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('cyanlizardcolours', (a, 0), f'cyanlizard{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('cyanlizardcolours', (a, 1), f'cyanlizard{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('cyanlizardcolours', (a, 2), f'cyanlizard{i}')
        # vulture
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('vulturecolours', (a, 0), f'vulture{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('vulturecolours', (a, 1), f'vulture{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('vulturecolours', (a, 2), f'vulture{i}')
        # banana
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('bananacolours', (a, 0), f'banana{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('bananacolours', (a, 1), f'banana{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('bananacolours', (a, 2), f'banana{i}')
        # centipede
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('centipedecolours', (a, 0), f'centipede{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('centipedecolours', (a, 1), f'centipede{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('centipedecolours', (a, 2), f'centipede{i}')
        # conductor
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('concolours', (a, 0), f'conductor{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('concolours', (a, 1), f'conductor{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('concolours', (a, 2), f'conductor{i}')
        # lizard
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('lizardcolours', (a, 0), f'lizard{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('lizardcolours', (a, 1), f'lizard{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('lizardcolours', (a, 2), f'lizard{i}')
        # lantern
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('lanterncolours', (a, 0), f'lantern{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('lanterncolours', (a, 1), f'lantern{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('lanterncolours', (a, 2), f'lantern{i}')
        # leviathan
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('leviathancolours', (a, 0), f'leviathan{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('leviathancolours', (a, 1), f'leviathan{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('leviathancolours', (a, 2), f'leviathan{i}')
        # fluffy
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('fluffycolours', (a, 0), f'fluffy{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('fluffycolours', (a, 1), f'fluffy{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('fluffycolours', (a, 2), f'fluffy{i}')
        # amoeba
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('amoebacolours', (a, 0), f'amoeba{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('amoebacolours', (a, 1), f'amoeba{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('amoebacolours', (a, 2), f'amoeba{i}')
        # seaslug
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('seaslugcolours', (a, 0), f'seaslug{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('seaslugcolours', (a, 1), f'seaslug{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('seaslugcolours', (a, 2), f'seaslug{i}')
        # yeekpelt
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('yeekcolours', (a, 0), f'yeek{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('yeekcolours', (a, 1), f'yeek{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('yeekcolours', (a, 2), f'yeek{i}')
        # rusted
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('rustedcolours', (a, 0), f'rusted{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('rustedcolours', (a, 1), f'rusted{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('rustedcolours', (a, 2), f'rusted{i}')
        # envoy
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('envoycolours', (a, 0), f'envoy{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('envoycolours', (a, 1), f'envoy{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('envoycolours', (a, 2), f'envoy{i}')
        # drizzle
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('drizzlecolours', (a, 0), f'drizzle{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('drizzlecolours', (a, 1), f'drizzle{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('drizzlecolours', (a, 2), f'drizzle{i}')
        # solace
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('solacecolours', (a, 0), f'solace{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('solacecolours', (a, 1), f'solace{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('solacecolours', (a, 2), f'solace{i}')
        # leafy
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('leafycolours', (a, 0), f'leafy{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('leafycolours', (a, 1), f'leafy{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('leafycolours', (a, 2), f'leafy{i}')
        # scaled
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('scaledcolours', (a, 0), f'scaled{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('scaledcolours', (a, 1), f'scaled{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('scaledcolours', (a, 2), f'scaled{i}')
        # dragonfruit
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('dragonfruitcolours', (a, 0), f'dragonfruit{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('dragonfruitcolours', (a, 1), f'dragonfruit{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('dragonfruitcolours', (a, 2), f'dragonfruit{i}')
        # necklace
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('necklacecolours', (a, 0), f'necklace{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('necklacecolours', (a, 1), f'necklace{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('necklacecolours', (a, 2), f'necklace{i}')
        # dreamer
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('dreamercolours', (a, 0), f'dreamer{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('dreamercolours', (a, 1), f'dreamer{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('dreamercolours', (a, 2), f'dreamer{i}')
        # duskdawn
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('duskdawncolours', (a, 0), f'duskdawn{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('duskdawncolours', (a, 1), f'duskdawn{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('duskdawncolours', (a, 2), f'duskdawn{i}')
        # seer
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('seercolours', (a, 0), f'seer{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('seercolours', (a, 1), f'seer{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('seercolours', (a, 2), f'seer{i}')
        # rotten
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('rottencolours', (a, 0), f'rotten{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('rottencolours', (a, 1), f'rotten{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('rottencolours', (a, 2), f'rotten{i}')
        # fire
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('firecolours', (a, 0), f'fire{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('firecolours', (a, 1), f'fire{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('firecolours', (a, 2), f'fire{i}')
        # countershaded
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('countershadedcolours', (a, 0), f'countershaded{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('countershadedcolours', (a, 1), f'countershaded{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('countershadedcolours', (a, 2), f'countershaded{i}')
        # sunset
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('sunsetcolours', (a, 0), f'sunset{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('sunsetcolours', (a, 1), f'sunset{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('sunsetcolours', (a, 2), f'sunset{i}')
         # oldgrowth
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('oldgrowthcolours', (a, 0), f'oldgrowth{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('oldgrowthcolours', (a, 1), f'oldgrowth{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('oldgrowthcolours', (a, 2), f'oldgrowth{i}')
         # sparklecat
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('sparklecatcolours', (a, 0), f'sparklecat{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('sparklecatcolours', (a, 1), f'sparklecat{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('sparklecatcolours', (a, 2), f'sparklecat{i}')
         # wolf
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('wolfcolours', (a, 0), f'wolf{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('wolfcolours', (a, 1), f'wolf{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('wolfcolours', (a, 2), f'wolf{i}')
         # cherry
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('cherrycolours', (a, 0), f'cherry{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('cherrycolours', (a, 1), f'cherry{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('cherrycolours', (a, 2), f'cherry{i}')
          # hypnotist
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('hypnotistcolours', (a, 0), f'hypnotist{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('hypnotistcolours', (a, 1), f'hypnotist{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('hypnotistcolours', (a, 2), f'hypnotist{i}')
            # ringed
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('ringedcolours', (a, 0), f'ringed{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('ringedcolours', (a, 1), f'ringed{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('ringedcolours', (a, 2), f'ringed{i}')
            # skinny !NOTE THIS HAS 2 ROWS OF 7 AND ONE 5!
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('skinnycolours', (a, 0), f'skinny{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA', 'LIGHTBROWN']):
            self.make_group('skinnycolours', (a, 1), f'skinny{i}')
        for a, i in enumerate(['LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('skinnycolours', (a, 2), f'skinny{i}')
            # sparse !NOTE THIS HAS 2 ROWS OF 7 AND ONE 5!
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('sparsecolours', (a, 0), f'sparse{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA', 'LIGHTBROWN']):
            self.make_group('sparsecolours', (a, 1), f'sparse{i}')
        for a, i in enumerate(['LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('sparsecolours', (a, 2), f'sparse{i}')
            # impish
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('impishcolours', (a, 0), f'impish{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('impishcolours', (a, 1), f'impish{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('impishcolours', (a, 2), f'impish{i}')
            # sporty
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('sportycolours', (a, 0), f'sporty{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('sportycolours', (a, 1), f'sporty{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('sportycolours', (a, 2), f'sporty{i}')
            # fizzy
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('fizzycolours', (a, 0), f'fizzy{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('fizzycolours', (a, 1), f'fizzy{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('fizzycolours', (a, 2), f'fizzy{i}')
            # skeleton
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('skeletoncolours', (a, 0), f'skeleton{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('skeletoncolours', (a, 1), f'skeleton{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('skeletoncolours', (a, 2), f'skeleton{i}')
            # shred
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('shredcolours', (a, 0), f'shred{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('shredcolours', (a, 1), f'shred{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('shredcolours', (a, 2), f'shred{i}')
            # glowing
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('glowingcolours', (a, 0), f'glowing{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('glowingcolours', (a, 1), f'glowing{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('glowingcolours', (a, 2), f'glowing{i}')
            # mold
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('moldcolours', (a, 0), f'mold{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('moldcolours', (a, 1), f'mold{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('moldcolours', (a, 2), f'mold{i}')
            # swing
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('swingcolours', (a, 0), f'swing{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('swingcolours', (a, 1), f'swing{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('swingcolours', (a, 2), f'swing{i}')

        

        # new new torties
        for a, i in enumerate(['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE']):
            self.make_group('tortiepatchesmasks', (a, 0), f"tortiemask{i}")
        for a, i in enumerate(['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL', 'GRUMPYFACE']):
            self.make_group('tortiepatchesmasks', (a, 1), f"tortiemask{i}")
        for a, i in enumerate(['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE']):
            self.make_group('tortiepatchesmasks', (a, 2), f"tortiemask{i}")
        for a, i in enumerate(['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY']):
            self.make_group('tortiepatchesmasks', (a, 3), f"tortiemask{i}")
        for a, i in enumerate(['SHILOH', 'FRECKLED', 'HEARTBEAT']):
            self.make_group('tortiepatchesmasks', (a, 4), f"tortiemask{i}")

        # Empty skin
        for a, i in enumerate(['BLACK', 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN', "RED"]):
            self.make_group('skin', (a, 0), f"skin{i}")
        for a, i in enumerate(['DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH']):
            self.make_group('skin', (a, 1), f"skin{i}")
        for a, i in enumerate(['DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE']):
            self.make_group('skin', (a, 2), f"skin{i}")

        # Gills, Tongues, Quills
        for a, i in enumerate(['PINKGILLS', 'BLUEGILLS', 'REDGILLS', 'LIMEGILLS', 'YELLOWGILLS', 'WHITEGILLS']):
            self.make_group('gilltongue', (a, 0), f"skin{i}")
        for a, i in enumerate(['RAINBOWGILLS', 'FUCHSIATONGUE', 'PASTELTONGUE', 'KOBITONGUE', 'REDTONGUE', 'GREYTONGUE']):
                self.make_group('gilltongue', (a, 1), f"skin{i}")
        for a, i in enumerate(['ORANGETONGUE', 'WHITESPOTS', 'BLACKSPOTS', 'MIXSPOTS', 'RAINBOWSPOTS', 'BLACKCLAWS']):
            self.make_group('gilltongue', (a, 2), f"skin{i}")
        if game.settings["bea_gilltongue"]:
            for a, i in enumerate(['WHITETENNA', 'REDTENNA', 'PINKTENNA', 'ORANGETENNA', 'YELLOWTENNA', 'BLUETENNA']):
                self.make_group('beagilltongue', (a, 3), f"skin{i}")
            for a, i in enumerate(['GREENTENNA', 'WHITEGLOWSPOTS', 'REDGLOWSPOTS', 'PINKGLOWSPOTS', 'ORANGEGLOWSPOTS', 'YELLOWGLOWSPOTS']):
                self.make_group('beagilltongue', (a, 4), f"skin{i}")
            for a, i in enumerate(['BLUEGLOWSPOTS', 'GREENGLOWSPOTS']):
                self.make_group('beagilltongue', (a, 5), f"skin{i}")
        else:
            for a, i in enumerate(['WHITETENNA', 'REDTENNA', 'PINKTENNA', 'ORANGETENNA', 'YELLOWTENNA', 'BLUETENNA']):
                self.make_group('gilltongue', (a, 3), f"skin{i}")
            for a, i in enumerate(['GREENTENNA', 'WHITEGLOWSPOTS', 'REDGLOWSPOTS', 'PINKGLOWSPOTS', 'ORANGEGLOWSPOTS', 'YELLOWGLOWSPOTS']):
                self.make_group('gilltongue', (a, 4), f"skin{i}")
            for a, i in enumerate(['BLUEGLOWSPOTS', 'GREENGLOWSPOTS']):
                self.make_group('gilltongue', (a, 5), f"skin{i}")

        #Horns
        for a, i in enumerate(['WHITEHORNSRAM', 'BLACKHORNSRAM', 'REDHORNSRAM', 'YELLOWHORNSRAM', 'GREENHORNSRAM', 'BLUEHORNSRAM', 'ORANGEHORNSRAM', 'BROWNHORNSRAM']):
            self.make_group('horns', (a, 0), f"skin{i}")
        for a, i in enumerate(['WHITEHORNSSCAV', 'BLACKHORNSSCAV', 'REDHORNSSCAV', 'YELLOWHORNSSCAV', 'GREENHORNSSCAV', 'BLUEHORNSSCAV', 'ORANGEHORNSSCAV', 'BROWNHORNSSCAV']):
            self.make_group('horns', (a, 1), f"skin{i}")
        for a, i in enumerate(['WHITEHORNSELITE', 'BLACKHORNSELITE', 'REDHORNSELITE', 'YELLOWHORNSELITE', 'GREENHORNSELITE', 'BLUEHORNSELITE', 'ORANGEHORNSELITE', 'BROWNHORNSELITE']):
            self.make_group('horns', (a, 2), f"skin{i}")
        for a, i in enumerate(['WHITEHORNSSHARP', 'BLACKHORNSSHARP', 'REDHORNSSHARP', 'YELLOWHORNSSHARP', 'GREENHORNSSHARP', 'BLUEHORNSSHARP', 'ORANGEHORNSSHARP', 'BROWNHORNSSHARP']):
            self.make_group('horns', (a, 3), f"skin{i}")
        for a, i in enumerate(['WHITEHORNSDRAGON', 'BLACKHORNSDRAGON', 'REDHORNSDRAGON', 'YELLOWHORNSDRAGON', 'GREENHORNSDRAGON', 'BLUEHORNSDRAGON', 'ORANGEHORNSDRAGON', 'BROWNHORNSDRAGON']):
            self.make_group('horns', (a, 4), f"skin{i}")
        for a, i in enumerate(['WHITEHORNSLANCER', 'BLACKHORNSLANCER', 'REDHORNSLANCER', 'YELLOWHORNSLANCER', 'GREENHORNSLANCER', 'BLUEHORNSLANCER', 'ORANGEHORNSLANCER', 'BROWNHORNSLANCER']):
            self.make_group('horns', (a, 5), f"skin{i}")

        #fancyskin spritesheet
        for a, i in enumerate(['WHITEMOTH', 'BLACKMOTH', 'REDMOTH', 'YELLOWMOTH', 'GREENMOTH', 'BLUEMOTH', 'ORANGEMOTH', 'BROWNMOTH']):
            self.make_group('fancyskin', (a, 0), f"skin{i}")
        for a, i in enumerate(['WHITEWHISKERS', 'BLACKWHISKERS', 'REDWHISKERS', 'YELLOWWHISKERS', 'GREENWHISKERS', 'BLUEWHISKERS', 'ORANGEWHISKERS', 'BROWNWHISKERS']):
            self.make_group('fancyskin', (a, 1), f"skin{i}")
        for a, i in enumerate(['PINKFINS', 'BLUEFINS', 'REDFINS', 'GREENFINS', 'YELLOWFINS', 'WHITEFINS', 'BLACKNEEDLES', 'WHITENEEDLES']):
            self.make_group('fancyskin', (a, 2), f"skin{i}")
        for a, i in enumerate(['WHITECYAN', 'ORANGECYAN', 'BROWNCYAN', 'PINKCYAN', 'PINKERCYAN', 'TEALCYAN', 'GREENCYAN', 'BLOODYCYAN']):
            self.make_group('fancyskin', (a, 3), f"skin{i}")
        for a, i in enumerate(['LAVENDERCYAN', 'PURPLECYAN', 'CYANCYAN', 'BLUECYAN', 'DARKBLUECYAN', 'DARKPURPLECYAN', 'BLACKCYAN', 'EGGCYAN']):
            self.make_group('fancyskin', (a, 4), f"skin{i}")
        for a, i in enumerate(['YELLOWCYAN', 'RAINBOWNEEDLES', 'CYANWINGS']):
            self.make_group('fancyskin', (a, 5), f"skin{i}")

        self.load_scars()
        self.load_symbols()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """

        # Define scars
        scars_data = [
            ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
             "BOTHBLIND", "BURNPAWS", "BURNTAIL"],
            ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE", "FROSTFACE", "FROSTTAIL",
             "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"],
            ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE", "LEGBITE",
             "NECKBITE", "FACE"],
            ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR", 
             "ROTMARKED", "ROTRIDDEN", "TOPSURGERY"],
            ["CUTOPEN", "LABRATFACE", "VIVISECTION", "LABRATCHEST", "LABRATLIMBS", "NEUTRINO", "MANGLEDARM", 
             "ENVOYCHEST", "HALFFACELEFT", "FULLBODYBURNS", "BESIEGED", "HALFFACERIGHT"],
            ["STARBURN", "ARMBURN", "DOUBLEBITE", "DANGEROUS", "SMOKINGFACE", "NIBBLEDIDIOT", "X-FACE",
             "NIBBEDAGAIN", "MESSIAH", "EXTRACTIONTWO", "RESTITCHEDUPPER", "RESTITCHEDLOWER"],
            ["STITCHEDHEAD", "BURNTLEG", "BURNTARM"],
        ]

        # define missing parts
        missing_parts_data = [
            ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW"]
        ]

        # scars 
        for row, scars in enumerate(scars_data):
            for col, scar in enumerate(scars):
                self.make_group('scars', (col, row), f'scars{scar}')

        # missing parts
        for row, missing_parts in enumerate(missing_parts_data):
            for col, missing_part in enumerate(missing_parts):
                self.make_group('missingscars', (col, row), f'scars{missing_part}')

        # accessories
        medcatherbs_data = [
            ["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "LAUREL"],
            ["BLUEBELLS", "NETTLE", "POPPY", "LAVENDER", "HERBS", "PETALS"],
            [],  # Empty row because this is the wild data, except dry herbs.
            ["OAK LEAVES", "CATMINT", "MAPLE SEED", "JUNIPER", "SAKURA"]
        ]

        wild_data = [
            ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "MOTH WINGS", "CICADA WINGS"]
        ]

        collars_data = [
            ["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"],
            ["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"],
            ["PINK", "PURPLE", "MULTI", "INDIGO"]
        ]

        bellcollars_data = [
            ["CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL", "LIMEBELL"],
            ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"],
            ["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]
        ]

        bowcollars_data = [
            ["CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW", "LIMEBOW"],
            ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"],
            ["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]
        ]

        nyloncollars_data = [
            ["CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON", "LIMENYLON"],
            ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"],
            ["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]
        ]
        drones_data = [
            ["CRIMSONDRONE", "BLUEDRONE", "YELLOWDRONE", "CYANDRONE", "REDDRONE", "LIMEDRONE"],
            ["GREENDRONE", "RAINBOWDRONE", "BLACKDRONE", "SPIKESDRONE", "WHITEDRONE"],
            ["PINKDRONE", "PURPLEDRONE", "MULTIDRONE", "INDIGODRONE"]
        ]
        rwlizards_data = [
            ["BLUESKY", "BLUESEA", "PINKMAGENTA", "PINKPURPLE", "GREENEMERALD", "GREENLIME", "WHITEHIDDEN", "WHITEREVEALED"], 
            ["BLACKNEUTRAL", "BLACKALERT", "YELLOWORANGE", "YELLOWLEMON", "REDTOMATO", "CYANBLUE", "CYANGREEN"],
            ["ALBISALAFUSHIA", "ALBISALARED", "MELASALARED", "MELASALAFUSHIA", "MELASALAPURPLE"]
        ]
        muddypaws_data = [
            ["MUDDYPAWS"]
        ]
        herbs2_data = [
            ["SPEAR", "PEARLEAR", "KARMAFLOWER", "LILCENTI", "PEARLNECK", "REDBATNIP"], 
            ["LILFLY","BATNIP", "FLASHFRUIT", "REDFLASHFRUIT", "GREENKELP", "REDKELP"], 
            ["VULTMASK", "KINGMASK", "SCAVMASK", "TREESEED", "GLOWSTONE", "BROWNKELP"], 
            ["LILBEETLE", "EXPLOSPEAR", "GREENDRAGFLY", "BLUEDRAGFLY", "ELESPEAR"]
        ]
        insectwings_data = [
            ["DEATHSHEAD", "BLUEBORDERED", "BLOODVEIN", "LARGEEMERALD", "CINNABAR", "LUNA", "ROSYMAPLE"],
            ["ATLAS", "HERCULES", "SUNSET", "PURPLEEMPEROR", "WHITEADMIRAL", "SWALLOWTAIL"]
        ]
        drones_data = [
            ["CRIMSONDRONE", "BLUEDRONE", "YELLOWDRONE", "CYANDRONE", "REDDRONE", "LIMEDRONE"],
            ["GREENDRONE", "RAINBOWDRONE", "BLACKDRONE", "SPIKESDRONE", "WHITEDRONE"],
            ["PINKDRONE", "PURPLEDRONE", "MULTIDRONE", "INDIGODRONE"]
        ]
        buddies_data = [
            ["MOUSEBLUE", "MOUSEYEL", "MOUSEPINK", "MOUSERED", "YEEKRED", "YEEKBLUE"], 
            ["VULTGRUB", "GRAPPLE", "SNAILGREEN", "SNAILBLUE", "SNAILRED", "SNAILPURPLE"],
            ["NOODLERED", "NOODLEPURPLE", "NOODLEGREY", "NOODLEBLUE", "NOODLEWHITE", "NOODLEPINK"],
            ["IGGYYELLOW", "IGGYPURPLE", "IGGYWHITE", "IGGYGREEN", "IGGYRED", "IGGYBLUE"],
            ["SQUIDBLACK", "SQUIDWHITE", "BUBBLE", "WORMGRASSPOT", "POLEPLANTPOT"]
        ]
        newaccs_data = [
            ["BATFLY", "BLUEFRUIT", "EMPTYBAG", "HERBSBAG", "INVEGG", "VOIDSPAWN"],
            ["REDARMOR", "OVERSEEREYE", "SPIDEREAR", "NEURONBLUE", "NEURONRED", "NEURONGREEN"],
            ["NEURONWHITE", "KARMAONE", "KARMATWO", "KARMATHREE", "KARMAFOUR", "SCROLL"],
            ["NECKLACESILVER", "NECKLACEGOLD", "TAILWRAP", "RAINCOAT", "LACESCARF", "TOLLMASK"],
            ["FLOWEREDMOSS", "MOSS", "MUSHROOMS", "MUSHROOMHAT", "GRENADE", "SANTAHAT"],
            ["EYEPATCH", 'INVMOUTH', "MOUSEYELPLUSH", "MOUSEREDPLUSH", "MOUSEBLUEPLUSH", "MOUSEPINKPLUSH"]
        ]
        newaccs2_data = [
            ["GLITCHING", "ROBOTARM", "ROBOTLEG"]
        ]
        bodypaint_data = [
            ["REDPAINT", "PINKPAINT", "VOIDPAINT", "YELLOWPAINT", "GREENPAINT", "PALEPAINT"],
            ["CYANPAINT", "BLUEPAINT", "PURPLEPAINT", "MAGENTAPAINT", "BLACKPAINT", "WHITEPAINT"]
        ]
        implant_data = [
            ["IMPLANTWHITE", "IMPLANTPURPLE", "IMPLANTGREEN", "IMPLANTYELLOW", "IMPLANTBLUE"],
            ["EYEIMPLANTWHITE", "EYEIMPLANTRED", "EYEIMPLANTGREEN", "EYEIMPLANTYELLOW", "EYEIMPLANTBLUE"],
            ["GLOWWHITE", "GLOWPURPLE", "GLOWGREEN", "GLOWYELLOW", "GLOWBLUE"],
            ["CELLIMPLANT"]
        ]
        magic_data = [
            ["ORANGEFIRE", "GREENFIRE", "BLUEFIRE", "YELLOWFIRE", "WHITEFIRE", "PINKFIRE", "REDFIRE"],
            ["GREENRING", "CYANRING", "SILVERRING", "WHITERING", "YELLOWRING", "VOIDRING", "GOLDRING"],
            ["PETPEBBLE", "PETCLAY", "PETLAPIS", "PETAMETHYST", "PETJADE", "PETGRANITE", "PETSANDSTONE"]
        ]
        necklaces_data = [
            ["NECKLACEWHITE", "NECKLACEPINK", "NECKLACEPURPLE", "NECKLACEYELLOW", "NECKLACECYAN"],
            ["NECKLACEGREEN", "NECKLACERED", "NECKLACEORANGE", "NECKLACEBLUE", "NECKLACEBLACK"]
        ]
        drapery_data = [
            ["DRAPERYWHITE", "DRAPERYORANGE", "DRAPERYTAN", "DRAPERYPALEYELLOW", "DRAPERYYELLOW", "DRAPERYLIGHTMINT", "DRAPERYMINT", "DRAPERYGREEN", "DRAPERYLIGHTAQUA"],
            ["DRAPERYAQUA", "DRAPERYCYAN", "DRAPERYLIGHTGRAY", "DRAPERYPURPLE", "DRAPERYLIGHTINDIGO", "DRAPERYBLUE", "DRAPERYLAVENDER", "DRAPERYLIGHTPINK", "DRAPERYPINK"],
            ["DRAPERYHOTPINK", "DRAPERYGRAY", "DRAPERYDARKGRAY", "DRAPERYPALEPINK", "DRAPERYLIGHTRED", "DRAPERYRED", "DRAPERYPEACH", "DRAPERYLIGHTORANGE"]
        ]
        pridedrapery_data = [
            ["ORIGINALGAYDRAPERY", "TRANSDRAPERY", "GENDERQUEERDRAPERY", "AGENDERDRAPERY", "NONBINARYDRAPERY", "POLYAMDRAPERY", "GENDERFLUIDDRAPERY"],
            ["GENDERFLUXDRAPERY", "GAYDRAPERY", "OMNISEXUALDRAPERY", "OBJECTUMDRAPERY", "RAINBOWDRAPERY", "PHILIDRAPERY", "BISEXUALDRAPERY"],
            ["PANSEXUALDRAPERY", "POLYSEXUALDRAPERY", "ASEXUALDRAPERY", "LESBIANDRAPERY", "INTERSEXDRAPERY", "AROACEDRAPERY", "DEMIGIRLDRAPERY"],
            ["DEMIBOYDRAPERY", "DEMIGENDERDRAPERY", "DEMIFLUIDDRAPERY", "DEMIFLUXDRAPERY", "ABRODRAPERY", "ARODRAPERY", "DEMISEXDRAPERY"],
            ["DEMIRODRAPERY", "ACHILLEANDRAPERY", "SAPPHICDRAPERY", "DIAMORICDRAPERY", "UNLABELEDDRAPERY", "TRANSFEMDRAPERY", "TRANSMASCDRAPERY"],
            ["BIGENDERDRAPERY", "MULTISEXDRAPERY", "ACESPECDRAPERY", "AROSPECDRAPERY"]
        ]
        eyepatch_data = [
            ["EYEPATCHWHITE", "EYEPATCHGREEN", "EYEPATCHAQUA", "EYEPATCHTURQUOISE", "EYEPATCHCYAN", "EYEPATCHBLUE", "EYEPATCHINDIGO"],
            ["EYEPATCHPURPLE", "EYEPATCHMAGENTA", "EYEPATCHPINK", "EYEPATCHROSE", "EYEPATCHLIGHTGRAY", "EYEPATCHDARKGRAY", "EYEPATCHBLACK"],
            ["EYEPATCHRED", "EYEPATCHORANGE", "EYEPATCHAMBER", "EYEPATCHYELLOW", "EYEPATCHLIME"]
        ]
        larsaccs_data = [
            ["ALLSEEINGGOLD", "ALLSEEINGSILVER", "BESIEGEDMASKOG", "BESIEGEDMASKBLUE", "BESIEGEDMASKCYAN"],
            ["BESIEGEDMASKGRAY", "BESIEGEDMASKGREEN", "BESIEGEDMASKINDIGO", "BESIEGEDMASKORANGE", "BESIEGEDMASKPINK"],
            ["BESIEGEDMASKPURPLE", "BESIEGEDMASKRED", "BESIEGEDMASKROSE", "BESIEGEDMASKAQUA", "BESIEGEDMASKYELLOW"],
            ["HANDPEARLBLANK", "HANDPEARLBLUE", "HANDPEARLGREEN", "HANDPEARLORANGE", "HANDPEARLPURPLE"],
            ["HANDPEARLRED", "HANDPEARLYELLOW", "PEARLDRAPERY", "STRAIGHTGOLD", "STRAIGHTSILVER"]
        ]
    
        harleyaccs_data = [
            ["FALLENSTARMASK", "TORNCLOAKFALL", "FALLENSTARPAWS", "TORNCLOAKWINTER"],
            ["TORNCLOAKNIGHT", "TORNCLOAKSHADOW", "TORNCLOAKSILVER", "FAUXMANE"]
        ]

        # medcatherbs
        for row, herbs in enumerate(medcatherbs_data):
            for col, herb in enumerate(herbs):
                self.make_group('medcatherbs', (col, row), f'acc_herbs{herb}')
        self.make_group('medcatherbs', (5, 2), 'acc_herbsDRY HERBS')

        # wild
        for row, wilds in enumerate(wild_data):
            for col, wild in enumerate(wilds):
                self.make_group('medcatherbs', (col, 2), f'acc_wild{wild}')

        # collars
        for row, collars in enumerate(collars_data):
            for col, collar in enumerate(collars):
                self.make_group('collars', (col, row), f'collars{collar}')

        # bellcollars
        for row, bellcollars in enumerate(bellcollars_data):
            for col, bellcollar in enumerate(bellcollars):
                self.make_group('bellcollars', (col, row), f'collars{bellcollar}')

        # bowcollars
        for row, bowcollars in enumerate(bowcollars_data):
            for col, bowcollar in enumerate(bowcollars):
                self.make_group('bowcollars', (col, row), f'collars{bowcollar}')

        # nyloncollars
        for row, nyloncollars in enumerate(nyloncollars_data):
            for col, nyloncollar in enumerate(nyloncollars):
                self.make_group('nyloncollars', (col, row), f'collars{nyloncollar}')
        # rw lizards     
        for a, i in enumerate(
                ["BLUESKY", "BLUESEA", "PINKMAGENTA", "PINKPURPLE", "GREENEMERALD", "GREENLIME", "WHITEHIDDEN", "WHITEREVEALED", "BLACKNEUTRAL", "BLACKALERT"]):
            self.make_group('rwlizards', (a, 0), f'lizards{i}')
        for a, i in enumerate(["YELLOWORANGE", "YELLOWLEMON", "REDTOMATO", "CYANBLUE", "CYANGREEN", "ALBISALAFUSHIA", "ALBISALARED", "MELASALARED", "MELASALAFUSHIA", "MELASALAPURPLE"]):
            self.make_group('rwlizards', (a, 1), f'lizards{i}')

        # drones
        for row, drones in enumerate(drones_data):
            for col, drone in enumerate(drones):
                self.make_group('drones', (col, row), f'collars{drone}')

        #sey's accs
        for row, muddypaws in enumerate(muddypaws_data):
            for col, muddypaws in enumerate(muddypaws):
                self.make_group('muddypaws', (col, row), f'muddypaws{muddypaws}')
                
        for a, i in enumerate(
                ["DEATHSHEAD", "BLUEBORDERED", "BLOODVEIN", "LARGEEMERALD", "CINNABAR", "LUNA", "ROSYMAPLE"]):
            self.make_group('insectwings', (a, 0), f'insectwings{i}')
        for a, i in enumerate(["ATLAS", "HERCULES", "SUNSET", "PURPLEEMPEROR", "WHITEADMIRAL", "SWALLOWTAIL"]):
            self.make_group('insectwings', (a, 1), f'insectwings{i}')
            
        #herbs 2
        for row, herbs2 in enumerate(herbs2_data):
            for col, herbs2 in enumerate(herbs2):
                self.make_group('herbs2', (col, row), f'herbs2{herbs2}')
                
        #buddies
        for row, buddies in enumerate(buddies_data):
            for col, buddies in enumerate(buddies):
                self.make_group('buddies', (col, row), f'buddies{buddies}')
                
        #newaccs
        for row, newaccs in enumerate(newaccs_data):
            for col, newaccs in enumerate(newaccs):
                self.make_group('newaccs', (col, row), f'newaccs{newaccs}')
                
        #newaccs2
        for row, newaccs2 in enumerate(newaccs2_data):
            for col, newaccs2 in enumerate(newaccs2):
                self.make_group('newaccs2', (col, row), f'newaccs2{newaccs2}')

        #bodypaint
        for row, bodypaint in enumerate(bodypaint_data):
            for col, bodypaint in enumerate(bodypaint):
                self.make_group('bodypaint', (col, row), f'bodypaint{bodypaint}')

        #implant
        for row, implant in enumerate(implant_data):
            for col, implant in enumerate(implant):
                self.make_group('implant', (col, row), f'implant{implant}')

        #magic
        for row, magic in enumerate(magic_data):
            for col, magic in enumerate(magic):
                self.make_group('magic', (col, row), f'magic{magic}')

        #necklaces
        for row, necklaces in enumerate(necklaces_data):
            for col, necklaces in enumerate(necklaces):
                self.make_group('necklaces', (col, row), f'necklaces{necklaces}')
        #drapery
        for row, drapery in enumerate(drapery_data):
            for col, drapery in enumerate(drapery):
                self.make_group('drapery', (col, row), f'drapery{drapery}')
        #pridedrapery
        for row, pridedrapery in enumerate(pridedrapery_data):
            for col, pridedrapery in enumerate(pridedrapery):
                self.make_group('pridedrapery', (col, row), f'pridedrapery{pridedrapery}')
        #eyepatches
        for row, eyepatches in enumerate(eyepatch_data):
            for col, eyepatches in enumerate(eyepatches):
                self.make_group('eyepatches', (col, row), f'eyepatches{eyepatches}')
        #larsaccs
        for row, larsaccs in enumerate(larsaccs_data):
            for col, larsaccs in enumerate(larsaccs):
                self.make_group('larsaccs', (col, row), f'larsaccs{larsaccs}')
        #harleyaccs
        for row, harleyaccs in enumerate(harleyaccs_data):
            for col, harleyaccs in enumerate(harleyaccs):
                self.make_group('harleyaccs', (col, row), f'harleyaccs{harleyaccs}')

    def load_symbols(self):
        """
        loads clan symbols
        """

        if os.path.exists('resources/dicts/clan_symbols.json'):
            with open('resources/dicts/clan_symbols.json') as read_file:
                self.symbol_dict = ujson.loads(read_file.read())

        # U and X omitted from letter list due to having no prefixes
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "V", "W", "Y", "Z"]

        # sprite names will format as "symbol{PREFIX}{INDEX}", ex. "symbolSPRING0"
        y_pos = 1
        for letter in letters:
            for i, symbol in enumerate([symbol for symbol in self.symbol_dict if
                                        letter in symbol and self.symbol_dict[symbol]["variants"]]):
                x_mod = 0
                for variant_index in range(self.symbol_dict[symbol]["variants"]):
                    x_mod += variant_index
                    self.clan_symbols.append(f"symbol{symbol.upper()}{variant_index}")
                    self.make_group('symbols',
                                    (i + x_mod, y_pos),
                                    f"symbol{symbol.upper()}{variant_index}",
                                    sprites_x=1, sprites_y=1, no_index=True)

            y_pos += 1

    def dark_mode_symbol(self, symbol):
        """Change the color of the symbol to dark mode, then return it
        :param Surface symbol: The clan symbol to convert"""
        dark_mode_symbol = copy(symbol)
        var = pygame.PixelArray(dark_mode_symbol)
        var.replace((87, 76, 45), (239, 229, 206))
        del var
        # dark mode color (239, 229, 206)
        # debug hot pink (255, 105, 180)

        return dark_mode_symbol

# CREATE INSTANCE
sprites = Sprites()
