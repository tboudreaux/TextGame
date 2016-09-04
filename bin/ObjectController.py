##############################
#      Object Controller     #
##############################
"""
Functionality: control objects in the game world
Dependencies: WorldController.py, IneractionController.py
References: N/A
"""
import random as r
import InteractionController as IC
import numpy as np
import pandas as pd

import WorldController


# Global Parameters


# Program Objects
class Player(WorldController.World):
    """
    Player Game object
    Stores all the player data including:
        Position
        Current Stats
        Past choices
    """
    def __init__(self):
        """
        Initialize the player
        """
        WorldController.World.__init__(self)

        # Location Data
        start_loc = (0,0)   # bottom left corner of the world
        self.x = start_loc[0]
        self.y = start_loc[1]

        # Understood Commands
        self.north = ['n', 'u', 'up', 'north', 'go north']
        self.east = ['e', 'l', 'left', 'east', 'go east']
        self.south = ['s', 'd', 'down', 'south', 'go south']
        self.west = ['w', 'r', 'right', 'west', 'go west']
        self.look = ['look around', 'look', 'whats around', 'near me', 'map', 'check around']
        self.supplies = ['backpack', 'what Do i have', 'inventory', 'i', 'supplies', 'check backpack']
        self.stats = ['stats', 'health', 'how am i doing', 'hp', 'standing', 'rep', 'reputation', 'status',
                      'money', 'bank', 'wallet', 'check stats', 'check status']

        # Player History / Interaction array
        index = np.linspace(0, self.size[1] - 1, self.size[1])
        columns = np.linspace(0, self.size[0] - 1 , self.size[1])
        self.PIA = pd.DataFrame(columns=columns, index=index)   # Player Interaction array (stores player world history)

        # Player meta data
        self.hold = []      # Store values of temporarily disabled grid point functions
        self.hold_here = False


        # Player Stats
        self.money = 1*10**9    # Starting money
        self.HP = 100   # Starting Hit Points
        self.inventory = {'A Strange Green thing': 12}     # Starts with an empty inventory
        self.reputation = 0

        # Initial Message Generator
        self.cont = True
        a = eval(self.WCG[self.x][self.y] + '()')
        a = a.split(',')
        for i in a:
            checksum = i[:3]    # function meta_data pass
            params = i[3:].split(':')   # function return data array first element
            if checksum == '/s/':  # auto run a look around at first birth
                eval('self.' + params[0])
            elif checksum == '/d/': # Store data about the first run
                self.PIA[self.x][self.y] = params[0]
        CAR = (0, 0)        # Coordinated on the world grid at last local function run

        # Limited Use Lambda Functions
        c = lambda a, b: b if a is True else 0

        # Variable Initilization
        self.holdcoords = 0
        self.holdvalue = 0

        # Main Player Control Loop
        while self.cont is True:
            if self.turn % 5 == 0:
                self.check_time()
            if self.HP <= 0:    # check health and if less than or 0 kill the player
                self.death()
            self.player_action()    # preform an action
            # os.system('clear')     # TODO: Make the clear work
            if self.cont is True:   # Control running function that player lands on
                self.wg_interact()   # Control World Grid interaction

    def read_input(self, prompt, valid=(None)):
        """
        General user input function for validating and getting input
        :param prompt: prompt displayed to the user asking for input (string)
        :param valid: valid responses to prompt (n type tuple)
        :return: from_user (string) -- user input validated against valid inputs
        """
        cont = False
        from_user = "//ERR"     # Default to an ERROR message
        all_valid = []
        for element in valid:       # Fill one array with all valid inputs passed into read_input
            for item in element:
                all_valid.append(item)
        while cont is False:        # force user to enter valid input
            from_user = raw_input(prompt)
            print from_user.lower()
            if from_user.lower() in all_valid:
                cont = True
            elif from_user.lower() == 'q':  # secret quit
                print 'QUIT'
                self.cont = False
                cont = True
            else:
                possible_direcitions = []
                try:
                    possible_direcitions.append(all_valid.index('north'))
                except ValueError:
                    pass
                try:
                    possible_direcitions.append(all_valid.index('east'))
                except ValueError:
                    pass
                try:
                    possible_direcitions.append(all_valid.index('south'))
                except ValueError:
                    pass
                try:
                    possible_direcitions.append(all_valid.index('west'))
                except ValueError:
                    pass
                for index, direction in enumerate(possible_direcitions):
                    if index == 0:
                        possible = all_valid[direction]
                    else:
                        possible += ' & ' + all_valid[direction]
                print 'You cannot do that right now, sorry. You can move ' + possible
        return from_user

    def player_action(self):
        """
        Move the player to a new coordinate on the world grid
        :return: Updates Player Position on the world grid
        """
        valid_move = [self.north, self.east, self.south, self.west]      # Do not change order of these!
        valid_action = [self.look, self.supplies, self.stats]
        prompt = 'What would you like to do: '     # TODO: Allow prompt to indicate legal actions

        # Movement Code
        if self.x == 0 and self.y == 0:     # Bottom Left Corner
            action = self.read_input(prompt, valid_move[:2] + valid_action)
            self.enact_action(action)
        elif self.x == 0 and self.y == self.size[1] - 1:      # Top Left Corner
            action = self.read_input(prompt, valid_move[1:3] + valid_action)
            self.enact_action(action)
        elif self.x == self.size[0] - 1 and self.y == self.size[1] - 1:     # Top Right Corner
            action = self.read_input(prompt, valid_move[2:] + valid_action)
            self.enact_action(action)
        elif self.x == self.size[0] - 1 and self.y == 0:       # Bottom Right Corner
            action = self.read_input(prompt, valid_move[:1] + valid_move[3:] + valid_action)
            self.enact_action(action)
        elif self.x == 0 and self.y != 0:   # Left y axis
            action = self.read_input(prompt,valid_move[:3] + valid_action)
            self.enact_action(action)
        elif self.x != 0 and self.y == self.size[1] - 1:    # Top X axis
            action = self.read_input(prompt, valid_move[1:] + valid_action)
            self.enact_action(action)
        elif self.x == self.size[0] - 1 and self.y == self.size[1] - 1:     # Right Y axis
            action = self.read_input(prompt, valid_move[:1] + valid_move[2:] + valid_action)
            self.enact_action(action)
        elif self.x != 0 and self.y == 0:       # Bottom X axis
            action = self.read_input(prompt, valid_move[:2] + valid_move[3:] + valid_action)
            self.enact_action(action)
        else:   # Rest of the world grid
            action = self.read_input(prompt, valid_move + valid_action)
            self.enact_action(action)

        # God Code

    def enact_action(self, param):
        """
        Run an action based on a user input
        :param param: the user input
        :return: N/A
        """

        # Movement control
        if param in self.north:
            print 'You walk north'
            self.y += 1
            self.hold_here = False
            self.turn_update(1)
        elif param in self.south:
            print 'You walk south'
            self.y -= 1
            self.hold_here = False
            self.turn_update(1)
        elif param in self.east:
            print 'You walk east'
            self.x += 1
            self.hold_here = False
            self.turn_update(1)
        elif param in self.west:
            print 'You walk west'
            self.x -= 1
            self.hold_here = False
            self.turn_update(1)

        # Other Action controls
        elif param in self.look:
            self.look_around()
            self.turn_update(1,mod_prev=False)
        elif param in self.supplies:
            self.check_inventory()
            self.turn_update(1, mod_prev=False)
        elif param in self.stats:
            self.check_stats()
            self.turn_update(1, mod_prev=False)

    def look_around(self):
        """
        Look around function
        :return: prints to screen whats around you
        """
        print 'You Look to your surroundings and get a sense of your position'
        edge_messages = ['The Edge of the world, it looks inviting',
                         "A fortuitously places large wall, you can't go there"]
        fog_messages = ['A Storm moving in and obsucuring your view',
                        'A dense fog which makes it hard to see', 'A large hippopotomus that is staring back at '
                        'you, you cannot see past']
        rand_message = lambda x: x[r.randint(0, len(x)-1)]
        m_choose = lambda a, b: a if not 'FUNC' in a else rand_message(b)  # hides defined grid functions
        # Try blocks are an implicit check for the edge of the world    TODO: Try to chancge to explicit checks
        try:
            whats_north = self.WCG[self.x][(self.y+1)][5:]   # grab the function, make it look better, print
        except KeyError as key:     # if you are at the edge inform the player
            whats_north = rand_message(edge_messages)
        try:
            whats_east = self.WCG[(self.x+1)][self.y][5:]
        except KeyError as key:
            whats_east = rand_message(edge_messages)
        try:
            whats_south = self.WCG[self.x][(self.y-1)][5:]
        except KeyError as key:
            whats_south = rand_message(edge_messages)
        try:
            whats_west = self.WCG[(self.x-1)][self.y][5:]
        except KeyError as key:
            whats_west = rand_message(edge_messages)

        # Consol Output
        print 'To your north you see:', m_choose(whats_north, fog_messages)
        print 'To your east you see:', m_choose(whats_east, fog_messages)
        print 'To your south you see:', m_choose(whats_south, fog_messages)
        print 'To your west you see:', m_choose(whats_west, fog_messages)

    def buy_good(self, good, cost):
        """
        buy a good and subtract the cost from your money
        :param good: good to buy (string)
        :param cost: cost of the good (float)
        :return: updates the amount of money that the player has
        """
        print 'you have just purchased a ' + str(good) + ' for the reasonable cost of ' + str(cost)
        self.money -= cost  # subtract the cost from wallet
        if good in self.inventory:
            self.inventory[good] += 1
        else:
            self.inventory[good] = 1
        print 'you have ' + str(self.money) + ' left in the bank'

    def hurt(self, damage):
        """
        Damage the player based on an amount of damage delt
        :param damage: amount of damaeg delt (int)
        :return:
        """
        print 'You took ' + str(damage) + ' points of damage'
        self.HP -= damage   # subtract the damage from HP

    def check_inventory(self):
        """
        Check the inventory of the player and print it out
        :return: Print inventory summery to the display
        """
        print 'In Your helpfully large pockets right now you have: '
        for i in self.inventory.items():
            print i[0], '-', i[1]

    def mod_standing(self, a):
        """
        Adjust the reputation of the player based on a reputation adjustment passed in
        :param a: the reputation adjustment (int or string castable to int)
        :return:
        """
        print 'Your reputation in the world has gone from: ' + str(self.reputation) + ' to: ' + str(self.reputation+a)
        self.reputation += int(a)

    def check_time(self):
        """
        Simple turn to time converter with 10 turns being equal to one day
        :return: N/A
        """
        time = self.turn/10.0   # 10 turns per day
        time = str(time)
        time = time.split('.')     # split at the decimal
        day = time[0]
        tempstr = '0.' + time[1]
        hour = float(tempstr)*24     # convert decimal to hours
        print 'It is day ' + str(1 + int(day)) + ' and hour ' + str(hour)

    def check_stats(self):
        print 'CURRENT STATUS:'
        print 'HEALTH: ' + str(self.HP) + '%'
        print 'MONEY: $' + str(self.money)
        print 'REPUTATION: ' + str(self.reputation) + ' rep points'

    def death(self):
        """
        Controls the players death cycle
        :return: resets values that could have changed for the player in the game to initial states and moves player
        """
        print 'GAME OVER | YOU FAILED | LOOOOOOOSER | Please send help because YOU JUST GOT BURNT'
        self.x = 0
        self.y = 0
        self.HP = 100
        self.money = 1*10**9
        self.hold_here = False
        self.inventory = {'A Strange Green thing': 12}
        self.hold = []
        self.reputation = 0
        index = np.linspace(0, self.size[1] - 1, self.size[1])
        columns = np.linspace(0, self.size[0] - 1 , self.size[1])
        self.PIA = pd.DataFrame(columns=columns, index=index)

    # META COMMAND FUNCTIONS
    def wg_interact(self):
        """
        World Grid Interaction Function -- controls how the world grid functions affect and interact with the player
        :return: N/A
        """
        # Lambda Functions:
        c = lambda a, b: b if a is True else 0

        # Interact Function
        indextopop = []
        for index, holdelement in enumerate(self.hold):
            if holdelement[2] > 0:
                if self.turn <= 1+self.prev_turn:
                    self.hold[index] = [holdelement[0], holdelement[1], holdelement[2] - 1]
            elif holdelement[2] <= 0:
                indextopop.append(index)
        for popelement in indextopop:
            self.hold.pop(popelement)
        for i, holdelement in enumerate(self.hold):
            if holdelement[0] == self.x and holdelement[1] == self.y:
                self.holdvalue = holdelement[2]
                self.hold_here = True
        if self.PIA[self.x][self.y] != 'off' and c(self.hold_here,
                                                   self.holdvalue) == 0:  # check if the function has been deactivated by the world
            FunctionCall = self.WCG[self.x][self.y] + '()'
            self.call_interact(FunctionCall)

    def call_interact(self, fcall):
        """
        Function to call the world grid functions and interprit their results
        :param fcall: Fully built function call (string)
        :return: N/A
        """
        a = eval(fcall)     # fun the actual called function
        try:  # Handel non value returning functions
            a = a.split(',')    # parse the returned value
            for i in a:  # read all of the values and specials returned by the function
                checksum = i[:3]    # Pull out the magic command
                params = i[3:].split(':')   # Pull out the parameters and split them apart
                try:  # Handel if a function does not return a string
                    if checksum == '/s/':  # check if local method magic word
                        function_call = ''
                        if len(params) == 1:  # special case for functions with no parameters imputed
                            function_call = params[0] + '()'
                        else:  # if the requested function does have parameters to input
                            for index, parameter in enumerate(params):  # generate function calls
                                if index == 0:  # populate function name and open (
                                    function_call = parameter + '('
                                elif index == len(params) - 1:  # populate final parameter and close )
                                    function_call += parameter + ')'
                                else:  # populare inbetween parameters and commas
                                    function_call += parameter + ', '
                        eval('self.' + function_call)  # evalute generated function sting
                    elif checksum == '/d/':  # check for data append magic word
                        self.PIA[self.x][self.y] = params[0]
                    elif checksum == '/h/':  # check for hold magic word
                        self.hold.append([self.x, self.y, int(params[0])])
                    elif checksum == '/0/':  # check for player death magic word
                        self.death()
                    elif checksum == '/a/':    # check for auto action indicator
                        self.enact_action(params[0])
                except TypeError:  # TODO: Change this to an explicitly handled error
                    pass
        except AttributeError as Ae:
            if str(Ae) == "'NoneType' object has no attribute 'split'" or str(Ae) == "'int' object has no attribute 'split'":  # Expected error
                pass
            else:  # Unexpected error
                print 'An Unknown Error has occurred | HARD FAIL'
                print str(Ae)
                exit()  # Hard fail, close the program

    def req_data(self, param_array):
        """
        data passer function from Player - interaction functions
        :param param_array: array of parameters of type unimportant that the world grid function has requested
        :return: N/A
        """
        send_string = '"'
        param_array = param_array.split('|')    # parse the request into its individual components
        for i, e, in enumerate(param_array):
            if 'PIA' in e:
                param_array[i] = param_array[i].split('-')  # grap the PIA coords in the split form -
        for i in param_array:
            if type(i) == str: # if the requested data is a single thing
                if i == 'rep':
                    send_string += str(self.reputation) + ':'   # build a string with the requested data
            else:   # if the requested data needs parameters to be specified
                if i[0] == 'PIA':   # Player interaction array check
                    xcoord = i[1]
                    ycoord = i[2]
                    send_string += str(self.PIA[int(xcoord)][int(ycoord)]) + ':'  # Build paremeter string
        send_string += '/o"' # terminate the string
        FunctionCall = 'IC.U_FUNC_' + str(self.x) + '_' + str(self.y) + '(' + send_string + ')' # Built function call
        self.call_interact(FunctionCall)    # call the interaction function


def game_init():
    """
    Main Game start
    :return: N/A
    """
    WorldController.world_init()       # Initialize the world
    Player()    # Call player into initilization routine


# Start from command line
if __name__=="__main__":
    game_init()
    print 'COMPLETE'
