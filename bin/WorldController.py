##############################
#      World Controller      #
##############################
"""
Functionality: Generate the world and mediate interactions of objects with it
Dependencies: InteractionContoller.py
References: ObjectController.py
"""

# Library Dependencies
import random as r
import InteractionController as IC
import numpy as np
import pandas as pd

# ERROR STRINGS
INTERACTIONERROR = "UNABLE TO LOCATE ALL OR SOME INTERACTION FUNCTION(s) IN INTERACTION FILE \n -- CHECK FILE"


# World Data Structure
class WorldInfo:
    """
    Class to store more General information about the world
    """
    def __init__(self):
        self.size = (10, 10)    # world size x by y
        self.grid_size = 1
        self.gareas = ["self.river", "self.waterfall", "self.plains", "self.forest"]
        self.bioms = ["grassland", "wooded", "rivervalley", "beach"]

    def river(self):
        options = ['You are near a river, it babbles gently as you wander','A river if near you, you can hear the fish sing']
        print self.choose_text(options)

    def plains(self):
        print "PLAINS"

    def waterfall(self):
        print "WATERFALL"

    def forest(self):
        print "FOREST"

    def choose_text(self, opts):
        """
        Chooses semi-random text from a given option array
        :param opts: the text option array (string array)
        :return: choice (string)
        """
        choice = r.randint(0, len(opts)-1)
        return opts[choice]


# World Object
class World(WorldInfo):
    """
    World Object class, stores the populated world grid and world variables such as anything related to a time
    cycle or multi player interactionary objects
    """
    def __init__(self):
        WorldInfo.__init__(self)
        self.funcpos = 0
        self.gen()
        self.turn = 0
        self.prev_turn = 0
        self.clock = 0

    def gen(self):
        """
        Generates World Grid
        :return: World Grid
        """
        index = np.linspace(0, self.size[1] - 1, self.size[1])
        columns = np.linspace(0, self.size[0] - 1 , self.size[1])
        self.WCG = pd.DataFrame(columns=columns, index=index)    # Generate the World Coordiate Grid and inililize it to zero
        self.WOG = pd.DataFrame(columns=columns, index=index)    # Generate the World Object Grid and inililize it to zero

        """FUNCTION TO READ IN FROM INTERACTION"""
        self.read_interact()

    def read_interact(self):
        """
        Assigns functions from either the interaction controller or general functions from the WorldInfo class
        to coordinated on the world grid
        :return: populated world grid
        """
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                FuncToAssign = 'IC.I_FUNC_' + str(i) + '_' + str(j)
                try:
                    eval(FuncToAssign)      # Check if the function is valid
                    self.WCG[i][j] = FuncToAssign      # Assign each Grid array a function to run
                except AttributeError as e:     # If all interaction functions are not present
                    if str(e) == "'module' object has no attribute 'I_FUNC_" + str(i) + "_" + str(j) + "'":   # If error correct use general Interaction function
                        self.WCG[i][j] = self.random_gen(i, j)
                    else:       # else raise hard fail error
                        print INTERACTIONERROR
                        exit()  # hard fail
        self.WCG.to_csv('World.csv', sep=',', encoding='utf-8')

    def random_gen(self, i, j):
        """
        Generates the semi-random parts of the world grid
        :param i: x coordiate (integer)
        :param j: y coordiate (integer)
        :return: WORDGRIDELEMENT - the interaction function to assign to the world grid at the give coords
        """
        WORLDGRIDELEMENT = 'river'
        if i == 0 and j == 0:  # if there is no defined first action define a set first without a random check:
            FuncToAssign = 'river'
            self.WCG[i][j] = FuncToAssign
        elif i == self.size[0] - 1 and j == 0:  # Generate world for lower right corrner
            funcs = (str(self.WCG[i - 1][j]).strip('<').strip('>').split(' ')[self.funcpos],
                        str(self.WCG[i][j + 1]).strip('<').strip('>').split(' ')[self.funcpos])
            a = 9  # probabability cutoff
            b = 1
            left_prob, up_prob, rand_prob = (r.randint(0, 19), r.randint(0, 19), r.randint(0,19))
            tup = (self.is_go(left_prob, a), self.is_go(up_prob, a), self.is_go(rand_prob, b))
            WORLDGRIDELEMENT = self.det_rand(tup, funcs)
        elif i == self.size[0] - 1 and j == self.size[1] - 1:  # Generate world for upper right corrner
            funcs = (str(self.WCG[i][j - 1]).strip('<').strip('>').split(' ')[self.funcpos],
                          str(self.WCG[i - 1][j]).strip('<').strip('>').split(' ')[self.funcpos])
            a = 9  # probabability cutoff
            b = 1
            down_prob, left_prob, rand_prob = (r.randint(0, 19), r.randint(0, 19), r.randint(0, 19))
            tup = (self.is_go(down_prob, a), self.is_go(left_prob, a), self.is_go(rand_prob, b))
            WORLDGRIDELEMENT = self.det_rand(tup, funcs)
        elif i == 0 and j == self.size[1] - 1:  # Generate world for upper left corrner
            funcs = (str(self.WCG[i + 1][j]).strip('<').strip('>').split(' ')[self.funcpos],
                           str(self.WCG[i][j - 1]).strip('<').strip('>').split(' ')[self.funcpos])
            a = 9  # probabability cutoff
            b = 1
            right_prob, down_prob, rand_prob = (r.randint(0, 19), r.randint(0, 19), r.randint(0, 19))
            tup = (self.is_go(right_prob, a), self.is_go(down_prob, a), self.is_go(rand_prob, b))
            WORLDGRIDELEMENT = self.det_rand(tup, funcs)
        elif i == 0 and j != 0:  # Generate the left yaxis of the world
            funcs = (str(self.WCG[i][j + 1]).strip('<').strip('>').split(' ')[self.funcpos],
                               str(self.WCG[i + 1][j]).strip('<').strip('>').split(' ')[self.funcpos],
                               str(self.WCG[i][j - 1]).strip('<').strip('>').split(' ')[self.funcpos])
            a = 3  # probabability cutoff
            b = 1
            up_prob, right_prob, down_prob, rand_prob = (r.randint(0, 9), r.randint(0, 9), r.randint(0, 9),
                                                         r.randint(0, 9))
            tup = (self.is_go(up_prob, a), self.is_go(right_prob, a), self.is_go(down_prob, a),
                   self.is_go(rand_prob, b))
            WORLDGRIDELEMENT = self.det_rand(tup, funcs)
        elif i != 0 and j == 0:  # Genete the bottom xaxis of the world
            funcs = (str(self.WCG[i - 1][j]).strip('<').strip('>').split(' ')[self.funcpos],
                               str(self.WCG[i][j + 1]).strip('<').strip('>').split(' ')[self.funcpos],
                               str(self.WCG[i + 1][j]).strip('<').strip('>').split(' ')[self.funcpos])
            a = 3  # probabability cutoff
            b = 1
            left_prob, up_prob, right_prob, rand_prob = (r.randint(0, 9), r.randint(0, 9), r.randint(0, 9),
                                                         r.randint(0, 9))
            tup = (self.is_go(left_prob, a), self.is_go(up_prob, a), self.is_go(right_prob, a),
                   self.is_go(rand_prob, b))
            WORLDGRIDELEMENT = self.det_rand(tup, funcs)
        elif i != 0  and j == self.size[1] - 1:  # Genete the top xaxis of the world
            funcs = (str(self.WCG[i + 1][j]).strip('<').strip('>').split(' ')[self.funcpos],
                                 str(self.WCG[i][j - 1]).strip('<').strip('>').split(' ')[self.funcpos],
                                 str(self.WCG[i - 1][j]).strip('<').strip('>').split(' ')[self.funcpos])
            a = 3  # probabability cutoff
            b = 1
            right_prob, down_prob, left_prob, rand_prob = (r.randint(0, 9), r.randint(0, 9), r.randint(0, 9),
                                                           r.randint(0, 9))
            tup = (self.is_go(right_prob, a), self.is_go(down_prob, a), self.is_go(left_prob, a),
                   self.is_go(rand_prob, b))
            WORLDGRIDELEMENT = self.det_rand(tup, funcs)
        elif i == self.size[0] - 1 and j != 0:  # Generate the right yaxis of the world
            funcs = (str(self.WCG[i][j - 1]).strip('<').strip('>').split(' ')[self.funcpos],
                               str(self.WCG[i - 1][j]).strip('<').strip('>').split(' ')[self.funcpos],
                               str(self.WCG[i][j + 1]).strip('<').strip('>').split(' ')[self.funcpos])
            a = 3  # probabability cutoff
            b = 1
            down_prob, left_prob, up_prob, rand_prob = (r.randint(0, 9), r.randint(0, 9), r.randint(0, 9),
                                                        r.randint(0, 9))
            tup = (self.is_go(down_prob, a), self.is_go(left_prob, a), self.is_go(up_prob, a), self.is_go(rand_prob, b))
            WORLDGRIDELEMENT = self.det_rand(tup, funcs)
        else:  # Generate rest of world
            funcs = (str(self.WCG[i][j + 1]).strip('<').strip('>').split(' ')[self.funcpos],
                                     str(self.WCG[i + 1][j]).strip('<').strip('>').split(' ')[self.funcpos],
                                     str(self.WCG[i][j - 1]).strip('<').strip('>').split(' ')[self.funcpos],
                                     str(self.WCG[i - 1][j]).strip('<').strip('>').split(' ')[self.funcpos])
            a = 9  # probabability cutoff
            b = 1
            up_prob, right_prob, down_prob, left_prob, rand_prob = (
            r.randint(0, 39), r.randint(0, 39), r.randint(0, 39), r.randint(0, 39), r.randint(0, 39))
            tup = (self.is_go(up_prob, a), self.is_go(right_prob, a), self.is_go(down_prob, a),
                   self.is_go(left_prob, a), self.is_go(rand_prob, b))
            WORLDGRIDELEMENT = self.det_rand(tup, funcs)
        return WORLDGRIDELEMENT

    @staticmethod
    def is_go(value, cut_off):
        """
        check if a value is below a curoff level and if so respond
        :param value: value to check (should be same type as cut_off)
        :param cut_off: value to compare against (should be same type as value)
        :return: true if value is less than cutoff false if anything else
        """
        if value < cut_off:
            return True
        else:
            return False

    @staticmethod
    def prob_check(ttc):
        """
        Picks from true values in a boolean tuple a single true boolean
        :param ttc: tuple to check (n element tuple made up of booleans)
        :return: element_number (int) -- index in the tuple which was choosen
        """
        true_array = []
        for index, element in enumerate(ttc):
            if element is False:
                pass
            else:
                true_array.append([index, element])     # Generate an array with the origional index and bool values
        if len(true_array) > 0:
            element_number = true_array[r.randint(0, len(true_array)-1)][0]     # Picks semi-random element to go with
        else:       # If all have failed then default to the first element in the function array
            element_number = 0
        return element_number

    def r_area(self):
        """
        returns a random area for the world grid
        :return: random area function
        """
        return self.gareas[r.randint(0, len(self.gareas)-1)]

    def det_rand(self, ttc, func):
        """
        checks between general area and random generation
        :param ttc: tuple to check
        :param func:
        :return:
        """
        prob_element = self.prob_check(ttc)
        if prob_element < len(func) - 1:
            if 'FUNC' in func[prob_element]:
                return self.r_area()
            if func[prob_element] == 'nan':
                return self.r_area()
            return func[prob_element]
        else:
            return self.r_area()

    def turn_update(self, amount, mod_prev=True):
        """
        Update the turn and prev turn by an amount
        :param amount: amount to update turn and prev turn by (float)
        :param mod_prev: boolean to modify or not to modify the previous turn
        :return:N/A
        """
        if mod_prev is True:
            self.prev_turn = self.turn
        self.turn += amount

    def update_world_object(self, Object, x, y):
        """
        Updates the World Object Grid
        :param Object: Object to add to the Grid (str)
        :param x: X coord (int)
        :param y: y Coord (int)
        :return:N/A
        """
        self.WOG[x][y] = Object

    def world_object_to_csv(self):
        """
        Write out the World Object array to a csv
        :return: N/A
        """
        self.WOG.to_csv('TextNPC.csv', sep='\t')

    def query_wog(self):
        """
        Query the World object array
        :return: the World Object grid
        """
        return self.WOG

    def reset_wog(self):
        """
        Run the reset parameters on the world
        :return: Rests WOG
        """
        index = np.linspace(0, self.size[1] - 1, self.size[1])
        columns = np.linspace(0, self.size[0] - 1 , self.size[1])
        self.WOG = pd.DataFrame(columns=columns, index=index)


# Initialize the world
def world_init():
    """
    Begin World init
    :return: N/A
    """
    World()


# Start the program from the command line
if __name__ == "__main__":
    world_init()
