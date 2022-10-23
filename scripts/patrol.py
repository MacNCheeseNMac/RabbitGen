from random import choice, randint
from math import floor

from scripts.game_structure.game_essentials import *
from scripts.cat.names import *
from scripts.cat.cats import *
from scripts.cat.pelts import *

resource_directory = "resources/dicts/patrols/"
leaves_path = "leaves/"
biomes_path = "biomes/"

NEWLEAF = None
try:
    with open(f"{resource_directory}{leaves_path}newleaf.json", 'r') as read_file:
        NEWLEAF = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the newleaf.json file of patrols!'


GREENLEAF = None
try:
    with open(f"{resource_directory}{leaves_path}greenleaf.json", 'r') as read_file:
        GREENLEAF = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the greenleaf.json file of patrols!'

LEAF_FALL = None
try:
    with open(f"{resource_directory}{leaves_path}leaf-fall.json", 'r') as read_file:
        LEAF_FALL = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the leaf-fall.json file of patrols!'

LEAF_BARE = None
try:
    with open(f"{resource_directory}{leaves_path}leaf-bare.json", 'r') as read_file:
        LEAF_BARE = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the leaf-bare.json file of patrols!'

FOREST = None
try:
    with open(f"{resource_directory}{biomes_path}forest.json", 'r') as read_file:
        FOREST = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the forest.json file of patrols!'

PLAINS = None
try:
    with open(f"{resource_directory}{biomes_path}plains.json", 'r') as read_file:
        PLAINS = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the plains.json file of patrols!'

MOUNTAINOUS = None
try:
    with open(f"{resource_directory}{biomes_path}mountainous.json", 'r') as read_file:
        MOUNTAINOUS = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the mountainous.json file of patrols!'

SWAMP = None
try:
    with open(f"{resource_directory}{biomes_path}swamp.json", 'r') as read_file:
        SWAMP = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the swamp.json file of patrols!'

BEACH = None
try:
    with open(f"{resource_directory}{biomes_path}beach.json", 'r') as read_file:
        BEACH = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the beach.json file of patrols!'

DISASTER = None
try:
    with open(f"{resource_directory}disaster.json", 'r') as read_file:
        DISASTER = ujson.loads(read_file.read())
except:
    game.switches['error_message'] = 'There was an error loading the disaster.json file of patrols!'


# ---------------------------------------------------------------------------- #
#                              PATROL CLASS START                              #
# ---------------------------------------------------------------------------- #


class Patrol(object):

    def __init__(self):
        self.patrol_event = None
        self.patrol_leader = None
        self.patrol_cats = []
        self.patrol_names = []
        self.possible_patrol_leaders = []
        self.patrol_skills = []
        self.patrol_statuses = []
        self.patrol_traits = []
        self.patrol_total_experience = 0
        self.success = False
        self.patrol_random_cat = None
        self.patrol_other_cats = None
        self.patrol_stat_cat = None
        self.experience_levels = [
            'very low', 'low', 'slightly low', 'average', 'somewhat high',
            'high', 'very high', 'master', 'max'
        ]

    def add_patrol_cats(self):
        self.patrol_cats.clear()
        self.patrol_names.clear()
        self.possible_patrol_leaders.clear()
        self.patrol_skills.clear()
        self.patrol_statuses.clear()
        self.patrol_traits.clear()
        self.patrol_total_experience = 0
        for cat in game.switches['current_patrol']:
            name = str(cat.name)
            self.patrol_cats.append(cat)
            self.patrol_names.append(name)
            if cat.status != 'apprentice':
                self.possible_patrol_leaders.append(cat)
            self.patrol_skills.append(cat.skill)
            self.patrol_statuses.append(cat.status)
            self.patrol_traits.append(cat.trait)
            self.patrol_total_experience += cat.experience
            game.patrolled.append(cat)
        if self.possible_patrol_leaders:
            self.patrol_leader = choice(self.possible_patrol_leaders)
        elif not self.possible_patrol_leaders:
            self.patrol_leader = choice(self.patrol_cats)
        self.patrol_random_cat = choice(self.patrol_cats)
        """ idk, this wasn't working for some reason
        for self.patrol_names in self.patrol_cats:
            if self.patrol_random_cat != self.patrol_leader:
                continue
            else:
                self.patrol_random_cat = choice(self.patrol_cats)
        """
        if len(self.patrol_cats) >= 3:
            other_not_same = False
            if self.patrol_other_cats != self.patrol_leader and self.patrol_other_cats != self.patrol_random_cat:
                other_not_same = True
        else:
            self.patrol_other_cats = None

    def get_possible_patrols(self, current_season, biome, all_clans, game_setting_disaster):
        possible_patrols = []
        # general patrols, any number of cats
        # general hunting patrols
        possible_patrols.extend([
            PatrolEvent(
                1,
                'Your patrol comes across a mouse',
                'Your patrol catches the mouse!',
                'Your patrol narrowly misses the mouse',
                'Your patrol ignores the mouse',
                60,
                10,
                win_skills=['good hunter', 'great hunter', 'fantastic hunter']),
            PatrolEvent(
                2,
                'Your patrol comes across a large rat',
                'Your patrol catches the rat! More freshkill!',
                'Your patrol misses the rat, and their confidence is shaken',
                'Your patrol ignores the rat',
                50,
                10,
                win_skills=['great hunter', 'fantastic hunter']),
            PatrolEvent(
                3,
                'Your patrol comes across a large hare',
                'Your patrol catches the hare!',
                'Your patrol narrowly misses the hare',
                'Your patrol ignores the hare',
                40,
                20,
                win_skills=['fantastic hunter']),
            PatrolEvent(
                4,
                'Your patrol comes across a bird',
                'Your patrol catches the bird before it flies away!',
                'Your patrol narrowly misses the bird',
                'Your patrol ignores the bird',
                50,
                10,
                win_skills=['great hunter', 'fantastic hunter']),
            PatrolEvent(
                5,
                'Your patrol comes across a squirrel',
                'Your patrol catches the squirrel!',
                'Your patrol narrowly misses the squirrel',
                'Your patrol ignores the squirrel',
                50,
                10,
                win_skills=['good hunter', 'great hunter', 'fantastic hunter']),
            PatrolEvent(
                6,
                'Your patrol sees the shadow of a fish in a river',
                'r_c hooks the fish out of the water! More freshkill!',
                'Your patrol accidentally scares the fish away',
                'Your patrol ignores the fish',
                50,
                10,
                win_skills=['great hunter', 'fantastic hunter']),
            PatrolEvent(
                7,
                'r_c spots a rabbit up ahead but it seems to be acting strange',
                'r_c catches the rabbit and it is eaten as normal',
                'r_c catches the rabbit and later the cats who eat it become violently ill',
                'r_c avoids catching the rabbit and looks for other prey',
                40,
                10,
                win_skills=['smart', 'very smart', 'extremely smart']),
            PatrolEvent(
                8,
                'The patrol approaches a Twoleg nest while hunting',
                'The patrol has a successful hunt, avoiding any Twolegs',
                'Twoleg kits scare the patrol away',
                'The patrol decides to hunt elsewhere',
                40,
                10,
                win_skills=['great hunter', 'fantastic hunter'])
        ])

        # general/misc patrols
        possible_patrols.extend([
            PatrolEvent(
                100,
                'Your patrol doesn\'t find anything useful',
                'It was still a fun outing!',
                'How did you fail this??',
                'Your patrol decides to head home early',
                100,
                10),
            PatrolEvent(
                101, 'The patrol finds a nice spot to sun themselves',
                'The sunlight feels great and they have a pleasant patrol',
                'The patrol doesn\'t get much done because of that',
                'They decide to stay focused instead',
                80,
                10),
            PatrolEvent(
                102,
                'The patrol comes across a thunderpath',
                'Your patrol crosses the thunderpath and can hunt on the other side',
                'r_c is hit by a monster and debates retiring to the elder den',
                'They decide it is better not to cross',
                50,
                10,
                win_skills=['very smart', 'extremely smart']),
            PatrolEvent(
                106,
                'p_l finds a patch of herbs that they believe the medicine cat mentioned they needed',
                'The patrol brings the herbs back to camp and they are put to good use',
                'The herbs turn out to be useless weeds',
                'They decide to focus on the patrol instead and leave the herb collecting to the medicine cat',
                40,
                10,
                win_skills=['very smart', 'extremely smart']),
            PatrolEvent(
                107,
                'r_c goes missing during the patrol',
                'r_c is later found carrying loads of prey after a successful hunt',
                'r_c is found lying injured on the ground',
                'r_c eventually makes it back to camp',
                40,
                10,),
            PatrolEvent(
                108,
                'The smell of food lures r_c close to a Twoleg trap',
                'r_c grabs the food before the trap goes off',
                'r_c is caught in the trap and is taken by Twolegs shortly after',
                'r_c loses interest and walks back to the patrol',
                40,
                10,
                win_skills=['very smart', 'extremely smart']),
            PatrolEvent(
                110,
                'r_c spots a large rabbit, but it is just over the border',
                'r_c catches the rabbit without the enemy Clan noticing',
                'r_c is caught by an enemy Clan patrol and is sent on their way',
                'r_c decides against chasing the rabbit',
                50,
                10,
                win_skills=['fantastic hunter'])
        ])
        if len(self.patrol_cats) >= 2:
            possible_patrols.extend([
                PatrolEvent(
                    109,
                    'r_c notices a Clanmate trapped in some brambles',
                    'r_c frees their Clanmate',
                    'The patrol works all day to free their Clanmate and gets nothing else done',
                    'r_c runs back to camp to fetch help and rejoins the patrol later',
                    50,
                    10,
                    win_skills=['very smart', 'extremely smart'])
            ])

        # season patrols
        if current_season == 'Newleaf':
            possible_patrols.extend(self.generate_patrol_events(NEWLEAF))
        elif current_season == 'Greenleaf':
            possible_patrols.extend(self.generate_patrol_events(GREENLEAF))
        elif current_season == 'Leaf-fall':
            possible_patrols.extend(self.generate_patrol_events(LEAF_FALL))
        elif current_season == 'Leaf-bare':
            possible_patrols.extend(self.generate_patrol_events(LEAF_BARE))

        # biome specific patrols
        biome = biome.lower()
        if biome == 'forest':
            possible_patrols.extend(self.generate_patrol_events(FOREST))
        elif biome == 'plains':
            possible_patrols.extend(self.generate_patrol_events(PLAINS))
        elif biome == 'mountainous':
            possible_patrols.extend(self.generate_patrol_events(MOUNTAINOUS))
        elif biome == 'swamp':
            possible_patrols.extend(self.generate_patrol_events(SWAMP))
        elif biome == 'beach':
            possible_patrols.extend(self.generate_patrol_events(BEACH))


        # other_clan patrols
        if len(all_clans) > 0:
            1 == 1  # will add here

        # deadly patrols
        if game_setting_disaster == True:
            possible_patrols.extend(self.generate_patrol_events(DISASTER))
        # fighting patrols
        possible_patrols.extend([
            PatrolEvent(
                300,
                'Your patrol catches the scent of a fox',
                'Your patrol finds the fox and drives it away',
                'Your patrol fails to drive away to fox, but luckily there were no injuries',
                'Your patrol decides not to pursue the fox',
                40,
                20,
                win_skills=['good fighter', 'great fighter', 'excellent fighter']),
            PatrolEvent(
                301,
                'Your patrol comes catches the scent of a fox',
                'Your patrol drives away the fox and her cubs',
                'The mother fox fights to defend her cubs, and r_c is injured in the attack',
                'Your patrol decides not to pursue the fox',
                30,
                30,
                win_skills=['excellent fighter']),
            PatrolEvent(
                302,
                'Your patrol comes across a large dog',
                'Your patrol valiantly drives away the dog',
                'The dog is driven away, but not before injuring r_c',
                'Your patrol decides not to pursue the dog',
                40,
                20,
                win_skills=['excellent fighter']),
            PatrolEvent(
                303,
                'Your patrol comes across a small dog',
                'Your patrol drives away the dog',
                'The dog\'s barking scares away prey',
                'The patrol decides not to pursue the dog',
                20,
                60,
                win_skills=['good fighter', 'great fighter','excellent fighter']),
            PatrolEvent(
                305,
                'A gang of rogues confronts your patrol',
                'Your patrol drives away the rogues',
                'The rogues are bloodthirsty and kill r_c before they leave',
                'The patrol sprints back to camp',
                40,
                20,
                win_skills=['excellent fighter']),
            PatrolEvent(
                306,
                'There is a badger den up ahead',
                'Your patrol chases the badger off of the territory',
                'The badger is angered when the patrol nears its den and badly injures r_c',
                'The patrol avoids the badger den',
                40,
                20,
                win_skills=['excellent fighter']),
            PatrolEvent(
                307,
                'There is a badger den up ahead',
                'Your patrol chases the badger off of the territory',
                'The badger is furious when the patrol nears its den and kills r_c',
                'The patrol avoids the badger den',
                50,
                20,
                win_skills=['excellent fighter']),
            PatrolEvent(
                308,
                'While on patrol, r_c notices some suspicious pawprints in the ground',
                'The pawprints lead to a trespassing rogue and the patrol drives them off of the '
                'territory',
                'It turns out they were r_c\'s own pawprints... How embarrassing',
                'They decide not to investigate',
                60,
                20,
                win_skills=['good fighter', 'great fighter', 'excellent fighter']),
            PatrolEvent(
                309,
                'While on patrol, r_c notices some suspicious pawprints in the ground',
                'The pawprints lead to a trespassing rogue and the patrol drives them off of the '
                'territory',
                'The pawprints lead to a trespassing rogue who injures r_c before being driven away',
                'They decide not to investigate',
                60,
                20,
                win_skills=['good fighter', 'great fighter', 'excellent fighter'])
        ])

        if self.patrol_random_cat != None and self.patrol_random_cat.status == 'apprentice' and len(
                self.patrol_cats) > 1:
            possible_patrols.extend([
                PatrolEvent(
                    150,
                    'The patrol wants to hold a training session for r_c',
                    'r_c becomes more confident in their abilities after the training session',
                    'r_c is nervous and doesn\'t perform well',
                    'They decide to focus on the patrol instead',
                    50,
                    10),
                PatrolEvent(
                    116,
                    'While helping gathering herbs, r_c stumbles upon a bush of red berries',
                    'The patrol tells r_c to stay away from the deathberries just in time',
                    'r_c chews some of the deathberries and dies',
                    'r_c decides not to touch the berries',
                    50,
                    10,
                    win_skills=['very smart', 'extremely smart']),
                PatrolEvent(
                    116,
                    'While helping gathering herbs, r_c stumbles upon a bush of red berries',
                    'Yum! r_c recognizes them as strawberries and shares the tasty treat with the patrol',
                    'The patrol scolds r_c for wasting time munching on berries',
                    'r_c decides not to touch the berries',
                    50,
                    10,
                    win_skills=['very smart', 'extremely smart']),
            ])

        # new cat patrols
        possible_patrols.extend([
            PatrolEvent(
                500,
                'Your patrol finds a loner who is interested in joining the Clan',
                'The patrol convinces the loner to join the Clan',
                'The loner decides against joining',
                'Your patrol decides not to confront the loner',
                40,
                10,
                antagonize_text=
                'Your patrol drives the loner off of the territory',
                antagonize_fail_text=
                'The loner is taken aback by their hostility and decides that Clan life is not for them',
                win_skills=['great speaker', 'excellent speaker']),
            PatrolEvent(
                501,
                'Your patrol finds a loner who is interested in joining the Clan',
                'The patrol convinces the loner to join the Clan and they bring with '
                'them a litter of kits',
                'The loner decides against joining',
                'Your patrol decides not to confront the loner',
                40,
                10,
                antagonize_text=
                'Your patrol drives the loner off of the territory',
                antagonize_fail_text=
                'The loner is taken aback by their hostility '
                'and decides that Clan life is not for them',
                win_skills=['great speaker', 'excellent speaker']),
            PatrolEvent(
                502,
                'Your patrol finds a kittypet who is interested in joining the Clan',
                'The patrol convinces the kittypet to join the Clan',
                'The description of Clan life frightens the kittypet',
                'Your patrol decides not to confront the kittypet',
                40,
                10,
                antagonize_text=
                'Your patrol drives the kittypet off of the territory',
                antagonize_fail_text=
                'The kittypet is taken aback by their hostility '
                'and decides that Clan life is not for them',
                win_skills=['great speaker', 'excellent speaker']),
            PatrolEvent(
                503,
                'r_c finds a wounded cat near the thunderpath',
                'The patrol brings the cat back to camp. Once nursed back to health, '
                'the cat decides to join the Clan',
                'As r_c inspects the cat, they find that they are already hunting '
                'with their ancestors',
                'They leave the wounded cat alone',
                40,
                10,
                antagonize_text=
                'Your patrol drives the cat off of the territory',
                antagonize_fail_text=
                'The wounded cat is killed in an attempt to drive them off of the territory',
                win_skills=['smart', 'very smart', 'extremely smart']),
            PatrolEvent(
                504,
                'r_c finds an abandoned kit whose mother is nowhere to be found',
                'The kit is taken back to camp and nursed back to health',
                'The kit is taken back to camp, but grows weak and dies a few days later',
                'They leave the kit alone', 40, 10)
        ])


        # single cat patrol
        if len(self.patrol_cats) == 1:
            possible_patrols.extend([
                PatrolEvent(
                    400,
                    'r_c is nervous doing a patrol by themselves',
                    'They don\'t let their nerves get to them and continue the patrol successfully',
                    'They run back to camp, unable to continue',
                    'They continue the patrol but progress is slow',
                    40,
                    10,
                    win_skills=['very smart', 'extremely smart']),
                PatrolEvent(
                    401,
                    'Since r_c is alone, they debate taking a bite out of the freshkill they have just caught',
                    'They decide not to and end up catching extra prey for the kits and elders',
                    'They eat the freshkill; however, they do not catch more prey to make up for it and the kits and elders go hungry',
                    'They shake the thought from their mind',
                    30,
                    10,
                    win_skills=['smart', 'very smart', 'extremely smart']),
                PatrolEvent(
                    402,
                    'While alone on patrol, r_c thinks about life',
                    'They find peace within themselves and enjoy the rest of the patrol',
                    'Their thoughts are plagued with bad memories',
                    'r_c decides to focus on the patrol',
                    40,
                    10,)
            ])
            if self.patrol_cats[0].status == 'apprentice':
                possible_patrols.extend([
                    PatrolEvent(
                        450,
                        'r_c worries that an apprentice should not be out here alone',
                        'At least this is a good chance to learn the territory',
                        'r_c gets lost in the territory and doesn\'t learn anything',
                        'r_c turns back to camp, deciding that this is a bad idea',
                        40,
                        10,
                        win_skills=['very smart', 'extremely smart']),
                    PatrolEvent(
                        451,
                        'r_c\'s mentor assesses them by sending them on a solo hunt',
                        'r_c catches a lot of prey and passes their assessment',
                        'Hunting is poor and r_c\'s mentor is disappointed',
                        'r_c asks their mentor to do the assessment some other time',
                        40,
                        10,
                        win_skills=['good hunter', 'great hunter', 'fantastic hunter']),
                    PatrolEvent(
                        452,
                        'r_c\'s mentor assesses them by sending them on a solo border patrol',
                        'r_c successfully marks the Clan territory',
                        'r_c messes up the territory markings and almost starts a border skirmish',
                        'r_c asks their mentor to do the assessment some other time',
                        40,
                        10,)
                ])
                
        # two or more cats            
        # conversation patrols
        if len(self.patrol_cats) == 2 and self.patrol_leader != self.patrol_random_cat:
            # general relationship patrols
            if len(self.patrol_cats) == 2:
                possible_patrols.extend([
                    PatrolEvent(
                        1000,
                        'p_l playfully asks r_c to race',
                        'r_c accepts and wins, grinning mischieviously',
                        'r_c loses and gets annoyed',
                        'r_c politely declines',
                        50,
                        10),
                    PatrolEvent(
                        1001,
                        'p_l asks r_c if they can tell them a secret',
                        'p_l feels a huge weight lift from their shoulders as they tell their secret to r_c',
                        'r_c dismisses it rudely, leaving p_l heartbroken',
                        'r_c politely declines',
                        60,
                        10),
                    PatrolEvent(
                        1002,
                        'r_c has failed yet another hunting attempt and is feeling embarrassed',
                        'p_l gently instructs them what they could do better, and r_c catches a big squirrel!',
                        'p_l tries to tell them what they did wrong but r_c takes offense and stalks off',
                        'p_l says nothing',
                        60,
                        20),
                    PatrolEvent(
                        1004,
                        'p_l considers joking around with r_c to lighten up the mood',
                        'p_l makes r_c laugh the entire patrol',
                        'r_c scolds p_l for their lack of focus',
                        'p_l decides to stay quiet',
                        50,
                        10),
                    PatrolEvent(
                        1005,
                        'p_l points out an interesting cloud to r_c',
                        'r_c and p_l spend hours watching the sky together',
                        'r_c chides p_l for their childishness',
                        'p_l changes the subject',
                        50,
                        10),
                    PatrolEvent(
                        1006,
                        'r_c is thrilled that they were assigned to patrol with p_l today',
                        'The two spend the whole patrol chatting and laughing',
                        'Unfortunately, p_l doesn\'t seem to feel the same',
                        'Still, their duties to the clan come first',
                        50,
                        10),
                    PatrolEvent(
                        1007,
                        'p_l notices that r_c isn\'t acting like their usual self',
                        'r_c opens up to p_l over something that has been bothering them',
                        'r_c snaps at p_l to mind their own business',
                        'p_l decides not to interfere',
                        50,
                        10)
                    ])

                if current_season == 'Leaf-bare':
                    possible_patrols.extend([
                    PatrolEvent(
                        1003,
                        'p_l notices r_c shivering',
                        'p_l asks r_c if they want to walk closer for warmth',
                        'r_c says that they\'re fine',
                        'p_l decides not to mention it',
                        60,
                        20)
                    ])
                        
                # romantic patrols for two cats
                if cat_class.is_potential_mate(self.patrol_leader, self.patrol_random_cat):
                    possible_patrols.extend([
                    PatrolEvent(
                        1010,
                        'p_l casually brushes against r_c\'s flank',
                        'p_l and r_c enter camp together, tails entwined',
                        'r_c jerks away suddenly and almost trips',
                        'p_l immediately apologizes for doing so',
                        50,
                        10),
                    PatrolEvent(
                        1011,
                        'p_l thinks this might be the perfect chance to tell r_c how they feel',
                        'r_c listens intently, smiling a bit by the end of p_l\'s confession',
                        'r_c cuts them off, saying that they don\'t feel the same way',
                        'p_l\'s nerves seem to get the best of them and they say nothing',
                        50,
                        10),
                    
                    PatrolEvent(
                        1012,
                        'p_l asks r_c if they can talk on the patrol',
                        'r_c agrees. p_l and r_c end up talking until the sun starts to set',
                        'r_c agrees, but it\'s awkward and the rest of the patrol lasts way too long',
                        'p_l changes their mind',
                        50,
                        10),
                    PatrolEvent(
                        1013,
                        'p_l notices how pretty r_c looks with the sun on their pelt',
                        'p_l shares the compliment with r_c, who thanks them',
                        'r_c tells p_l to keep their eyes off of them',
                        'p_l decides to keep their feelings silent',
                        50,
                        10),
                    PatrolEvent(
                        1014,
                        'p_l notices r_c staring at them',
                        'p_l feels their heart flutter',
                        'p_l snaps at r_c to knock it off',
                        'p_l ignores r_c',
                        50,
                        10),
                    PatrolEvent(
                        1015,
                        'p_l thinks r_c\'s eyes are beautiful',
                        'p_l tells r_c and they love the compliment',
                        'p_l tells r_c and they feel awkward, ignoring p_l for the rest of the patrol',
                        'p_l shakes their head and focuses on the patrol',
                        50,
                        10)
                    ])
                    if current_season == 'Newleaf':
                        possible_patrols.extend([
                        PatrolEvent(
                            1012,
                            'p_l brings a flower to r_c, saying it matches their eyes',
                            'r_c smiles and takes the flower',
                            'r_c goes to take the flower and sneezes. The flower goes flying', 
                            'p_l drops the flower on the way over! Oh well',
                            50,
                            10),
                        ])
                elif self.patrol_random_cat.status == 'apprentice':
                    possible_patrols.extend([
                    PatrolEvent(
                        1020,
                        'p_l asks r_c how their training is going',
                        'r_c happily tells p_l all about the fighting move they just learned',
                        'r_c answers curtly, having been subjected to cleaning the elders\'s den recently',
                        'r_c doesn\t hear the question and p_l changes the subject',
                        50,
                        10),
                    PatrolEvent(
                        1021,
                        'p_l asks r_c if they would like to go to the training grounds to practice',
                        'The practice goes well and the apprentice learns a lot!',
                        'The apprentice can\'t seem to focus today',
                        'r_c declines the offer',
                        50,
                        10),
                    PatrolEvent(
                        1023,
                        'r_c doesn\'t feel totally comfortable around p_l just yet',
                        'p_l cracks a joke to make r_c feel more at ease',
                        'r_c forces themself to spend time with p_l but it doesn\'t help',
                        'r_c stays away from p_l',
                        50,
                        10)
                    ])
                if current_season == 'Leaf-fall':
                    possible_patrols.extend([
                    PatrolEvent(
                        1022,
                        'Leaf-fall gives new opportunities to train!',
                        'r_c pays close attention to how p_l stalks prey while walking on leaves and manages to catch a bird!',
                        'r_c can\'t seem to replicate p_l and scares off all the prey',
                        'p_l decides to hunt with r_c in an area with less leaves',
                        50,
                        10)
                        
                ])

                else:
                    possible_patrols.extend([
                    PatrolEvent(
                        200,
                        'Your patrol doesn\'t find anything useful',
                        'It was still a fun outing!',
                        'How did you fail this??',
                        'Your patrol decides to head home',
                        100,
                        10),
                    PatrolEvent(
                        201,
                        'The patrol finds a nice spot to sun themselves',
                        'The sunlight feels great and the cats have a successful patrol',
                        'The patrol doesn\'t get much done because of that',
                        'They decide to stay focused instead',
                        80,
                        10),
                    PatrolEvent(
                        204,
                        'Your patrol has a disagreement and look to p_l to settle the dispute',
                        'p_l manages to skillfully smooth over any disagreement',
                        'p_l stutters; they don\'t think they are fit to lead the patrol',
                        'Your patrol decides to head home',
                        50,
                        10,
                        win_skills=['great speaker', 'excellent speaker']),
                    PatrolEvent(
                        205,
                        'r_c admits that they had a vision from StarClan last night',
                        'The patrol talks them through the vision as they hunt',
                        'No one can make sense of the vision',
                        'The patrol doesn\'t talk about the vision',
                        50,
                        10,
                        win_skills=['strong connection to starclan']),
                    PatrolEvent(
                        202,
                        'The patrol quickly devolves into ghost stories and everyone is on edge',
                        'Despite the tense mood, the patrol is successful',
                        'A branch snaps and the whole patrol runs back to camp',
                        'p_l quickly silences any talk about ghosts',
                        50,
                        10),
                    PatrolEvent(
                        203, 'r_c is tempted to eat the prey they just caught',
                        'They eat the prey without anyone noticing',
                        'The patrol notices r_c eating the prey and reports them back at camp',
                        'r_c decides against breaking the warrior code',
                        50,
                        10),
                    PatrolEvent(
                        103,
                        'p_l suggests this might be a good chance for the cats to practice teamwork',
                        'Everyone has a nice practice session and their connection to their Clanmates grows stronger',
                        'Unfortunately, no one steps up to teach',
                        'They decide to focus on the patrol instead',
                        50,
                        10,
                        win_skills=['good teacher', 'great teacher', 'fantastic teacher']),
                    PatrolEvent(
                        104,
                        'p_l suggests this might be a good chance for the cats to practice new hunting techniques',
                        'Everyone has a nice practice session and their hunting skills grow stronger',
                        'Unfortunately, no one steps up to teach',
                        'They decide to focus on the patrol instead',
                        50,
                        10,
                        win_skills=['good teacher', 'great teacher', 'fantastic teacher']),
                    PatrolEvent(
                        105,
                        'p_l suggests this might be a good chance for the cats to practice new fighting techniques',
                        'Everyone has a nice practice session and their fighting skills grow stronger',
                        'Unfortunately, no one steps up to teach',
                        'They decide to focus on the patrol instead',
                        50,
                        10,
                        win_skills=['good teacher', 'great teacher', 'fantastic teacher'])
                ])

                # if self.patrol_random_cat.status == 'warrior' or self.patrol_random_cat.status == 'apprentice':
                #     possible_patrols.extend([
                #         PatrolEvent(
                #             250,
                #             'r_c admits that they have been training in the dark forest',
                #             'The patrol manages to convince r_c to stop',
                #             'The patrol isn\'t able to convince r_c to stop and a few nights later they are found dead in their nest',
                #             'The patrol decides not to advise r_c what they should do',
                #             50,
                #             10,
                #             win_skills=[
                #                 'great speaker', 'excellent speaker',
                #                 'strong connection to starclan'
                #             ]),
                #         PatrolEvent(
                #             251,
                #             'r_c admits that they have been training in the dark forest',
                #             'The patrol manages to convince r_c to stop',
                #             'The patrol isn\'t able to convince r_c to stop and a few nights later they wake up injured in their nest',
                #             'The patrol decides not to advise r_c what they should do',
                #             50,
                #             10,
                #             win_skills=[
                #                 'great speaker', 'excellent speaker',
                #                 'strong connection to starclan'
                #             ])
                #     ])

                if self.patrol_random_cat.status == 'deputy':
                    possible_patrols.extend([
                        PatrolEvent(
                            260,
                            'r_c admits that they don\'t think that they are a good deputy',
                            'The patrol tells r_c that the Clan wouldn\'t be the same without them, and r_c feels a sense of relief',
                            'The patrol secretly agrees with r_c',
                            'The patrol doesn\'t say anything about r_c\'s statement',
                            50,
                            10,
                            win_skills=['great speaker', 'excellent speaker']),
                        PatrolEvent(
                            251,
                            'The patrol starts to doubt r_c\'s ability as the Clan\'s deputy',
                            'r_c performs well on the patrol and all doubt is quelled',
                            'The patrol performs poorly and they blame r_c',
                            'The patrol decides to keep their thoughts to themselves',
                            50,
                            10)
                        ])
                # trait specific patrols
                if self.patrol_random_cat.trait == 'strange':
                    possible_patrols.extend([
                        PatrolEvent(
                            600,
                            'r_c tells the patrol to roll in a patch of garlic to diguise their scent while hunting',
                            'The plan works and their hunt goes well',
                            'The patrol finds no prey and blame r_c; it seems like all the prey was scared off because of their stench!',
                            'The patrol ignores r_c\'s odd instructions',
                            50,
                            10)
                        ])
                elif self.patrol_random_cat.trait == 'bloodthirsty':
                    possible_patrols.extend([
                        PatrolEvent(
                            605,
                            'r_c deliberately provokes a border patrol skirmish',
                            'The other cats in the patrol keep r_c from fighting and no one is hurt',
                            'r_c is injured by the enemy patrol',
                            'r_c decides to back down by themselves',
                            50,
                            10,
                            win_skills=['great speaker', 'fantastic speaker'])
                        ])


        # ---------------------------------------------------------------------------- #
        #                                 !!IMPORTANT!!                                #
        #                               currently in rework                            #
        #                     me (Lixxis) will make a solution later                   #
        # ---------------------------------------------------------------------------- #

        #if self.patrol_random_cat.skill == 'formerly a loner':
        #    possible_patrols.extend([
        #        PatrolEvent(
        #            510,
        #            'r_c finds an old friend of their\'s from when they were a loner',
        #            'r_c invites their friend to join the Clan',
        #            'r_c and their friend reminisce about old times',
        #            'r_c says farewell to their friend and rejoins the patrol', 40, 10)
        #    ])

        #if self.patrol_random_cat.status == 'formerly a kittypet':
        #    possible_patrols.extend([
        #        PatrolEvent(
        #            520,
        #            'r_c finds an old friend of their\'s from when they were a kittypet',
        #            'r_c invites their friend to join the Clan',
        #            'r_c and their friend reminisce about old times',
        #            'r_c says farewell to their friend and rejoins the patrol', 40, 10)
        #    ])            

        return possible_patrols

    def generate_patrol_events(self, patrol_dict):
        all_patrol_events = []
        for patrol in patrol_dict:
            patrol_event = PatrolEvent(
                patrol_id = patrol["patrol_id"],
                intro_text = patrol["intro_text"],
                success_text = patrol["success_text"],
                fail_text = patrol["fail_text"],
                decline_text = patrol["decline_text"],
                antagonize_text = patrol["antagonize_text"],
                antagonize_fail_text = patrol["antagonize_fail_text"],
                chance_of_success = patrol["chance_of_success"],
                exp = patrol["exp"],
                win_skills = patrol["win_skills"]
            )
            all_patrol_events.append(patrol_event)
        return all_patrol_events

    def calculate_success(self):
        if self.patrol_event is None:
            return
        # if patrol contains cats with autowin skill, chance of success is high
        # otherwise it will calculate the chance by adding the patrolevent's chance of success plus the patrol's total exp
        chance = self.patrol_event.chance_of_success + int(
            self.patrol_total_experience / 10)
        if self.patrol_event.patrol_id != 100:
            chance = min(chance, 80)
        if self.patrol_event.win_skills is not None:
            if set(self.patrol_skills).isdisjoint(
                    self.patrol_event.win_skills):
                chance = 90
        # change the chance based on the personality
        if self.patrol_event in range(1000, 1010):
            get_along = get_personality_compatibility(self.patrol_leader, self.patrol_random_cat)
            if get_along != None and get_along:
                chance = chance + 50
            if get_along != None and not get_along:
                chance = chance - 50
        c = randint(0, 100)
        if c < chance:
            self.success = True
            self.handle_exp_gain()
            self.add_new_cats()
            self.handle_relationships()
        else:
            self.success = False
            self.handle_deaths()
            self.handle_scars()
            self.handle_relationships()

    def handle_exp_gain(self):
        if self.success:
            for cat in self.patrol_cats:
                cat.experience = cat.experience + (
                    self.patrol_event.exp + 6 // len(self.patrol_cats)) // 5
                cat.experience = min(cat.experience, 80)
                cat.experience_level = self.experience_levels[floor(
                    cat.experience / 10)]

    def handle_deaths(self):
        if self.patrol_event.patrol_id in [
                108, 113, 114, 116, 120, 141, 250, 305, 307
        ]:
            if self.patrol_random_cat.status == 'leader':
                if self.patrol_event.patrol_id in [108, 113]:
                    game.clan.leader_lives -= 9 # taken by twolegs, fall into ravine
                else:
                    game.clan.leader_lives -= 1
            self.patrol_random_cat.die()
        elif self.patrol_event.patrol_id in [900, 901, 902]:
            for cat in self.patrol_cats:
                cat.experience += self.patrol_event.exp
                cat.experience = min(cat.experience, 80)
                if cat.status == 'leader':
                    game.clan.leader_lives -= 10
                cat.die()

    def handle_scars(self):
        if self.patrol_event.patrol_id in [107, 251, 301, 302, 304, 306, 309]:
            if self.patrol_random_cat.specialty is None:
                self.patrol_random_cat.specialty = choice(
                    [choice(scars1),
                     choice(scars2),
                     choice(scars4)])
            elif self.patrol_random_cat.specialty2 is None:
                self.patrol_random_cat.specialty2 = choice(
                    [choice(scars1),
                     choice(scars2),
                     choice(scars4)])
        elif self.patrol_event.patrol_id == 102:
            self.patrol_random_cat.skill = choice(
                ['paralyzed', 'blind', 'missing a leg'])
            if game.settings['retirement']:
                self.patrol_random_cat.status_change('elder')
        elif self.patrol_event.patrol_id == 904:
            if self.patrol_random_cat.specialty is None:
                self.patrol_random_cat.specialty = choice([choice(scars5)])
            elif self.patrol_random_cat.specialty2 is None:
                self.patrol_random_cat.specialty2 = choice([choice(scars5)])

    def handle_retirements(self):
        if self.patrol_event.patrol_id == 102 and game.settings.get(
                'retirement'):
            self.patrol_random_cat.status_change('elder')

    def handle_relationships(self):
        romantic_love = 0
        platonic_like = 0
        dislike = 0
        admiration = 0
        comfortable = 0
        jealousy = 0
        trust = 0

        # change the values
        if self.patrol_event.patrol_id in [
            1010, 1011, 1012, 1013, 1014, 1015
        ]:
            romantic_love = 10
        if self.patrol_event.patrol_id in [
                2, 3, 6, 100, 103, 140, 141, 200, 204, 605, 1000, 1001, 1002, 1003,
                1010, 1011, 1012, 1020, 1021, 1003, 1006
        ]:
            platonic_like = 10
        if self.patrol_event.patrol_id in [103, 110, 1000, 1001, 1002, 1010]:
            dislike = 5
        if self.patrol_event.patrol_id in [
                2, 3, 6, 104, 105, 108, 130, 131, 261, 300, 301, 302, 303, 305,
                307, 600, 1002, 1005
        ]:
            admiration = 10
        if self.patrol_event.patrol_id in [
                102, 120, 150, 202, 203, 250, 251, 260, 261, 1010, 1011, 1012, 1022,
                1004, 1023, 1007
        ]:
            comfortable = 5
        if self.patrol_event.patrol_id in []:
            jealousy = 5
        if self.patrol_event.patrol_id in [
                7, 8, 102, 107, 110, 114, 115, 141, 250, 251, 605, 1001, 1007
        ]:
            trust = 10

        # affect the relationship
        cat_ids = [cat.ID for cat in self.patrol_cats]
        for cat in self.patrol_cats:
            relationships = list(
                filter(lambda rel: rel.cat_to.ID in cat_ids,
                       cat.relationships))
            for rel in relationships:
                if self.success:
                    rel.romantic_love += romantic_love
                    rel.platonic_like += platonic_like
                    rel.dislike -= dislike
                    rel.admiration += admiration
                    rel.comfortable += comfortable
                    rel.jealousy -= jealousy
                    rel.trust += trust
                elif not self.success:
                    rel.romantic_love -= romantic_love
                    rel.platonic_like -= platonic_like
                    rel.dislike += dislike
                    rel.admiration -= admiration
                    rel.comfortable -= comfortable
                    rel.jealousy += jealousy
                    rel.trust -= trust

    def add_new_cats(self):
        if self.patrol_event.patrol_id in [504]:  # new kit
            kit = Cat(status='kitten', moons=0)
            #create and update relationships
            relationships = []
            for cat_id in game.clan.clan_cats:
                the_cat = Cat.all_cats.get(cat_id)
                if the_cat.dead or the_cat.exiled:
                    continue
                the_cat.relationships.append(Relationship(the_cat, kit))
                relationships.append(Relationship(kit, the_cat))
            kit.relationships = relationships
            game.clan.add_cat(kit)
            kit.skill = 'formerly a loner'
            kit.thought = 'Is looking around the camp with wonder'

        if self.patrol_event.patrol_id in [500, 501, 510]:  # new loner
            new_status = choice([
                'apprentice', 'warrior', 'warrior', 'warrior', 'warrior',
                'elder'
            ])
            if self.patrol_event.patrol_id == 501:
                new_status = 'warrior'
            kit = Cat(status=new_status)
            if (kit.status == 'elder'):
                kit.moons = randint(120, 150)
            #create and update relationships
            relationships = []
            for cat_id in game.clan.clan_cats:
                the_cat = Cat.all_cats.get(cat_id)
                if the_cat.dead or the_cat.exiled:
                    continue
                the_cat.relationships.append(Relationship(the_cat, kit))
                relationships.append(Relationship(kit, the_cat))
            kit.relationships = relationships
            game.clan.add_cat(kit)
            kit.skill = 'formerly a loner'
            kit.thought = 'Is looking around the camp with wonder'
            if (kit.status == 'elder'):
                kit.moons = randint(120, 150)
            if randint(0, 5) == 0:  # chance to keep name
                kit.name.prefix = choice(names.loner_names)
                kit.name.suffix = ''
            if self.patrol_event.patrol_id == 501:
                num_kits = choice([2, 2, 2, 2, 3, 4])
                for _ in range(num_kits):
                    kit2 = Cat(status='kitten', moons=0)
                    kit2.skill = 'formerly a loner'
                    kit2.parent1 = kit.ID
                    kit2.thought = 'Is looking around the camp with wonder'
                    #create and update relationships
                    relationships = []
                    for cat_id in game.clan.clan_cats:
                        the_cat = Cat.all_cats.get(cat_id)
                        if the_cat.dead or the_cat.exiled:
                            continue
                        if the_cat.ID in [kit2.parent1, kit2.parent2]:
                            the_cat.relationships.append(
                                Relationship(the_cat, kit2, False, True))
                            relationships.append(
                                Relationship(kit2, the_cat, False, True))
                        else:
                            the_cat.relationships.append(
                                Relationship(the_cat, kit2))
                            relationships.append(Relationship(kit2, the_cat))
                    kit2.relationships = relationships
                    game.clan.add_cat(kit2)

        elif self.patrol_event.patrol_id in [502, 503, 520]:  # new kittypet
            new_status = choice([
                'apprentice', 'warrior', 'warrior', 'warrior', 'warrior',
                'elder'
            ])
            kit = Cat(status=new_status)
            #create and update relationships
            relationships = []
            for cat_id in game.clan.clan_cats:
                the_cat = Cat.all_cats.get(cat_id)
                if the_cat.dead or the_cat.exiled:
                    continue
                the_cat.relationships.append(Relationship(the_cat, kit))
                relationships.append(Relationship(kit, the_cat))
            kit.relationships = relationships
            game.clan.add_cat(kit)
            if (kit.status == 'elder'):
                kit.moons = randint(120, 150)
            kit.skill = 'formerly a kittypet'
            kit.thought = 'Is looking around the camp with wonder'
            if (kit.status == 'elder'):
                kit.moons = randint(120, 150)
            if randint(0, 2) == 0:  # chance to add collar
                kit.accessory = choice(collars)
            if randint(0, 5) == 0:  # chance to keep name
                kit.name.prefix = choice(names.loner_names)
                kit.name.suffix = ''

    def check_territories(self):
        hunting_claim = str(game.clan.name) + 'Clan Hunting Grounds'
        self.hunting_grounds = []
        for y in range(44):
            for x in range(40):
                claim_type = game.map_info[(x, y)][3]
                if claim_type == hunting_claim:
                    self.hunting_claim_info[(x, y)] = game.map_info[(x, y)]
                    self.hunting_grounds.append((x, y))


class PatrolEvent(object):

    def __init__(self,
                 patrol_id,
                 intro_text,
                 success_text,
                 fail_text,
                 decline_text,
                 chance_of_success,
                 exp,
                 other_clan=None,
                 win_skills=None,
                 antagonize_text='',
                 antagonize_fail_text=''):
        self.patrol_id = patrol_id
        self.intro_text = intro_text
        self.success_text = success_text
        self.fail_text = fail_text
        self.decline_text = decline_text
        self.chance_of_success = chance_of_success  # out of 100
        self.exp = exp
        self.other_clan = other_clan
        self.win_skills = win_skills
        self.antagonize_text = antagonize_text
        self.antagonize_fail_text = antagonize_fail_text


patrol = Patrol()
