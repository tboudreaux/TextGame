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
from colorama import Fore, Back, Style
import math
import names
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
    def __init__(self, velocity):
        """
        Initialize the player
        :param velocity: initial velocity of the player
        """
        WorldController.World.__init__(self)

        # Location Data
        start_loc = (0,0)   # bottom left corner of the world
        self.x = start_loc[0]
        self.y = start_loc[1]

        # Understood Commands (vocabulary)
        self.north = ['n', 'u', 'up', 'north', 'go north', 'move north']
        self.east = ['e', 'l', 'left', 'east', 'go east', 'move east']
        self.south = ['s', 'd', 'down', 'south', 'go south', 'move south']
        self.west = ['w', 'r', 'right', 'west', 'go west', 'move west']
        self.look = ['look around', 'look', 'whats around', 'near me', 'map', 'check around']
        self.supplies = ['backpack', 'what Do i have', 'inventory', 'i', 'supplies', 'check backpack']
        self.stats = ['stats', 'health', 'how am i doing', 'hp', 'standing', 'rep', 'reputation', 'status',
                      'money', 'bank', 'wallet', 'check stats', 'check status']

        # Player History / Interaction array
        index = np.linspace(0, self.size[1] - 1, self.size[1])
        columns = np.linspace(0, self.size[0] - 1 , self.size[1])
        self.PIA = pd.DataFrame(columns=columns, index=index)   # Player Interaction array (stores player world history)
        self.WOG[self.x][self.y] = 'Player'

        # Player meta data
        self.hold = []      # Store values of temporarily disabled grid point functions
        self.hold_here = False

        # Player Stats
        self.money = 1*10**9    # Starting money
        self.HP = 100   # Starting Hit Points
        self.inventory = {'A Strange Green thing': 12}     # Starts with an empty inventory
        self.reputation = 0

        # Player Physical Parameters
        self.width = 0.25  # meters
        self.velocity = velocity
        self.proper_time = 0    # seconds

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

    def coords(self):
        return [self.x, self.y]

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
                print Fore.RED + 'You cannot do that right now, sorry. You can move ' + possible + Style.RESET_ALL
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
        def stan_move():        # standard actions that need to be completed on each move
            self.hold_here = False  # pause the game
            self.turn_update(1)     # update the world turn counter
            self.time_update(self.velocity, self.grid_size)     # update the proper time of the player

        # Movement control
        if param in self.north:
            print 'You walk north'
            self.y += 1
            stan_move()
        elif param in self.south:
            print 'You walk south'
            self.y -= 1
            stan_move()
        elif param in self.east:
            print 'You walk east'
            self.x += 1
            stan_move()
        elif param in self.west:
            print 'You walk west'
            self.x -= 1
            stan_move()

        # Other Action controls
        elif param in self.look:
            self.look_around()
            self.turn_update(1, mod_prev=False)
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
        # print 'TIME: ', self.proper_time
        m, s = divmod(self.proper_time, 60)
        # print 'Minute:', m, 'second', s
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        w, d = divmod(d, 7)
        y, w = divmod(w, 52)
        de, y = divmod(y, 10)
        c, de = divmod(de, 10)
        mil, c = divmod(c, 10)
        print Fore.CYAN + 'It is ' + str(h) + ':' + str(m) + ':' + str(s).split('.')[0] + ' (hh:mm:ss) On day ' + \
              str(d) + Style.RESET_ALL
        if w > 1:
            print Fore.CYAN + 'It is week ' + str(w) + Style.RESET_ALL
        if y > 1:
            print Fore.CYAN + 'In year ' + str(y) + Style.RESET_ALL
        if de > 1:
            print Fore.CYAN + 'In decade ' + str(de) + Style.RESET_ALL
        if c > 1:
            print Fore.CYAN + 'In century ' + str(c) + Style.RESET_ALL
        if mil > 1:
            print Fore.CYAN + 'In millenium ' + str(mil) + Style.RESET_ALL

    def check_stats(self):
        print Back.WHITE + Fore.BLACK + 'CURRENT STATUS:' + '         ' + Style.RESET_ALL
        print Back.GREEN + Fore.BLACK + 'HEALTH: ' + str(self.HP) + '%' + '            ' + Style.RESET_ALL
        print Back.GREEN + Fore.BLACK + 'MONEY: $' + str(self.money) + '      ' + Style.RESET_ALL
        print Back.GREEN + Fore.BLACK + 'REPUTATION: ' + str(self.reputation) + ' rep points' + Style.RESET_ALL

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
        FunctionCall = 'IC.U_FUNC_' + str(self.x) + '_' + str(self.y) + '(' + send_string + ')'  # Build function call
        self.call_interact(FunctionCall)    # call the interaction function

    def time_update(self, vel, distance):
        """
        Function to update the proper time of the player based on velocity and time passed
        :param vel: velocity of the player in m/s
        :param distance: distance the player has moved in km
        :return: Updates the proper time of the player
        """
        distance *= 3.0*10**-5  # convert distance (read in in km) to SR units
        rel_vel = vel/(3.0*10**8)   # convert velocity (read in in m/s) to SR units
        time_passed_nr = distance / rel_vel  # coordinate time
        if vel >= 0.01:     # if velocity is greater than 1% the speed of light use the proper proper time equation
            self.proper_time += math.sqrt(1-rel_vel**2)*time_passed_nr
            # print 'UPDATING TIME BY: ' + str(math.sqrt(1-rel_vel**2)*time_passed_nr)
        else:       # use the binomial approximation
            self.proper_time += (1-(1/2.0)*rel_vel**2)*time_passed_nr
            # print 'UPDATING TIME BY: ' + str((1-(1/2.0)*rel_vel**2)*time_passed_nr)


class NPC(WorldController.World):

    def __init__(self, char_type):
        """
        Initialize NPC
        :param char_type: Type of chat chosen from list of types (str)
        :return: Calls NPC into the world
        """
        WorldController.World.__init__(self)

        self.x = r.randint(2, self.size[0]-1)
        self.y = r.randint(2, self.size[0]-1)

        self.flag_array = [None, None, None, None]  # Flag arary for NPC (INVALID CHAR, TBD, TBD, TBD)
        types = ['Market Capitalists', 'Commies', 'speedy goer', 'Juggernauts', 'One of those supper dull people (Chemists)']
        if char_type in types:
            self.type = char_type
        else:
            self.type = 'General Citizen'
            self.flag_array[0] = 'INVALID TYPE'
        self.HP = 0  # NPC Health
        self.mood = 5   # NPC mood (5 is neutral, 0 is hostile 10 is happy)
        index = np.linspace(0, self.size[1] - 1, self.size[1])
        columns = np.linspace(0, self.size[0] - 1, self.size[1])
        self.NIA = pd.DataFrame(columns=columns, index=index)  # NPC interaction array (stores NPC interaction history)
        self.inventory = {'A speedy Quick Quick Maker': 2}     # Starts with an empty inventory
        self.reputation = 0
        self.money = 100    # Default money
        self.velocity = 0   # Default Velocity
        self.strength = 5   # NPC strength (5 is neutral, 0 is weak 10 is strong)
        self.assign_attribute()     # Auto assign attributes to NPC's
        self.gender = ['male', 'female'][r.randint(0, 1)]
        self.name = names.get_full_name(gender=self.gender)
        # self.action()

    def __str__(self):
        return Fore.MAGENTA + 'name: ' + self.name + '\n' + 'type: ' + self.type + '\n'\
               + 'Velocity: ' + str(self.velocity) + '\n' + 'Mood: ' + str(self.mood) + '\n' \
               + 'X Pos: ' + str(self.x) + '\n' + 'Y pos: ' + str(self.y) + '\n' + Style.RESET_ALL

    def coords(self):
        return [self.x, self.y]

    def assign_attribute(self):
        """
        Assign starting attributes of different NPC types
        :return: N/A
        """
        if self.type == 'Market Capitalists':
            self.accelerate(10)     # Accelerate the NPC (trader) by 10 m/s
            self.give_item('Goods', 10)     # TODO fill out trader good st. they are randomized
            self.give_money(900)    # Give the NPC 900 more credits
            self.play_with_emotions(3)
            self.mod_strength(-3)
        elif self.type == 'Commies':
            self.accelerate(100)    # Accelerate the NPC (fighter) by 100m/s
            self.play_with_emotions(-5)
            self.mod_strength(4)
        elif self.type == 'speedy goer':
            self.accelerate(2.5*10**8)  # Send the speedy goer to relativistic speeds
            self.give_item('break', 2)
            self.mod_strength(1)
        elif self.type == 'Juggernauts':
            self.mod_strength(5)
            self.give_item('The Jaws of Life', 1)
            self.give_item('Hammer', 2)
            self.play_with_emotions(-4)

    def give_money(self, amount):
        """
        Give Money to the NPC
        :param amount: amount of money to give to the NPC (float/int)
        :return: Updates the money in the NPC's wallet
        """
        self.money += amount

    def accelerate(self, dv):
        """
        Change the velocity of the NPC
        :param dv: Chage in velocity to add (float/int)
        :return: Update the velocity of the NPC
        """
        self.velocity += dv

    def give_item(self, item_name, item_amount):
        """
        Add an item and an amount of that item to NPC's inventory
        :param item_name: Name of the item to add (str)
        :param item_amount: amount of the item to add (int)
        :return: Updates the NPC's inventory with the new item and amount
        """
        self.inventory[item_name] = item_amount

    def play_with_emotions(self, de):
        """
        Modify the mood of the NPC
        :param de: change in emotional state (int)
        :return: Updates the NPCs Emotions
        """
        if self.mood + de < 0:  # makes sure mood can not go below 0
            self.mood = 0   # saddest possible
        elif self.mood + de > 10:   # makes sure mood cannot go above 10
            self.mood = 10  # Happiest possible
        else:
            self.mood += de     # for other cases just increment mood

    def mod_standing(self, dr):
        """
        Change the reputation of the NPC in the game world
        :param ds: Amount to change the reputation by
        :return: Update the reputation
        """
        if self.reputation + dr < 0:    # Don't let the NPC reputation go below 0
            self.reputation = 0
        else:   # else just incriment it
            self.reputation += dr

    def mod_strength(self, ds):
        """
        Modigy the strength of the NPC
        :param ds: Amount to modify strength by
        :return: Update to the NPC strength atribute
        """
        if self.strength + ds < 0:  # limit min strength
            self.strength = 0
        elif self.strength > 10:    # limit max strength
            self.strength = 10
        else:                       # else just increment based on parameter
            self.strength += ds

    def action(self, player_object, WOG):
        """
        NPC General Action
            If the player is within a 4x4 grid of the NPC the NPC will pathfind towards the player else the NPC will
            choose a random - legal movment
            If the NPC lands on another player or another NPC the NPC will preform a general action (id not a movement)
                The NPC will then automatically move on
        :param player_object: the player passed int the NPC
        :param WOG: World object grid
        :return: N/A
        """
        player = False
        player_loc = [0, 0]
        # print 'WOG is:\n', WOG
        if WOG[self.x].iloc[self.y] == 'Player':        # If the player is on the grid of an NPC then interact
            self.player_interact(player_object)
        else:       # Otherwise Check if the player is within a 4x4 grid, if so path find
            for i in xrange(-2, 2):
                for j in xrange(-2, 2):
                    if i+self.x < 0 or i+self.x >= self.size[0]:
                        add_x = 0
                    else:
                        add_x = i
                    if j + self.y < 0 or j+self.y >= self.size[1]:
                        add_y = 0
                    else:
                        add_y = j
                    if WOG[add_x+self.x].iloc[add_y+self.y] == 'Player':
                        player = True
                        player_loc[0] = i+self.x
                        player_loc[1] = j+self.y
        if player is True:      # Path find towards player
            movement = self.path_find(player_loc[0], player_loc[1])
            self.move(movement['x'], movement['y'])
        else:       # Random movement otherwise
            self.move(r.randint(-1, 1), r.randint(-1, 1))

    def path_find(self, x_goal, y_goal):
        """
        Path Find to the player or other NPC
        :param x_goal: location in the x to aim for (int)
        :param y_goal: Location in the y to aim for (int)
        :return: x amount to move and y amount to move (moves - dict)
        """
        moves = {}
        move_x = x_goal - self.x
        move_y = y_goal - self.y

        if move_x > 0:
            moves['x'] = 1
        elif move_x < 0:
            moves['x'] = -1
        else:
            moves['x'] = 0

        if move_y > 0:
            moves['y'] = 1
        elif move_y < 0:
            moves['y'] = -1
        else:
            moves['y'] = 0

        return moves

    def move(self, x, y):
        """
        Move the NPC
        :param x: x amount to move (int)
        :param y: y amount to move (int)
        :return: updates the NPC's position
        """
        if 0 < self.x + x < self.size[0]:       # Keep NPC on world grid (x)
            self.x += x
        if 0 < self.y + y < self.size[1]:       # Keep NPC on world grid (y)
            self.y += y

    def player_interact(self, player_object):
        """
        Player Interaction function that deals with how the NPC deals with the player
        :param player_object: Player object to pass into interaction routine
        :return:
        """
        player_object.hurt(100)
        return None


def game_init():
    """
    Main Game start
    :return: N/A
    """
    NPC_Count = 25  # Number of NPCs to Spawn into the world
    NPCs = []
    char_types = ['Market Capitalists', 'Commies', 'speedy goer', 'Juggernauts',
                  'One of those supper dull people (Chemists)']
    W = WorldController.World()      # Initialize the world
    P = Player(3)  # Call player into initialization routine (default player speed 3 m/s)
    W.update_world_object('Player', P.coords()[0], P.coords()[1])
    for i in range(NPC_Count):
        NPCs.append(NPC(char_types[r.randint(0, len(char_types)-1)]))
    for j, i in enumerate(NPCs):
        W.update_world_object('NPC_'+str(j), i.coords()[0], i.coords()[1])
    W.world_object_to_csv()
    while P.cont is True:     # Game Loop
        if P.turn % 5 == 0:
            P.check_time()      # Check Player time
        if P.HP <= 0:    # check health and if less than or 0 kill the player
            P.death()       # Kill the player
        W.update_world_object(np.nan, P.coords()[0], P.coords()[1])
        P.player_action()    # preform an action
        if type(W.query_wog()[P.coords()[0]][P.coords()[1]]) != float:
            test = W.query_wog()[P.coords()[0]][P.coords()[1]]
            print 'THIS IS: ', W.query_wog()[P.coords()[0]][P.coords()[1]]
            if NPC in W.query_wog()[P.coords()[0]][P.coords()[1]]:
                W.update_world_object('Player&'+W.query_wog()[P.coords()[0]][P.coords()[1]],
                                      P.coords()[0], P.coords()[1])   # Update the Players Position on the WOG
        else:
            W.update_world_object('Player', P.coords()[0], P.coords()[1])  # Update the Players Position on the WOG
        for j, i in enumerate(NPCs):        # calculate NPC moves
            if type(W.query_wog()[i.coords()[0]][i.coords()[1]]) != float:
                if 'Player' in W.query_wog()[i.coords()[0]][i.coords()[1]]:
                    W.update_world_object("Player", i.coords()[0], i.coords()[1])      # Reset the old world grid coord
                else:
                    W.update_world_object("", i.coords()[0], i.coords()[1])
            i.action(P, W.query_wog())      # Preform Some action
            if type(W.query_wog()[i.coords()[0]][i.coords()[1]]) != float:
                if 'Player' in W.query_wog()[i.coords()[0]][i.coords()[1]]:
                    W.update_world_object('Player&NPC_'+str(j), i.coords()[0],
                                          i.coords()[1])  # Add the NPC back into the WOG
            else:
                W.update_world_object('NPC_' + str(j), i.coords()[0],i.coords()[1])  # Add the NPC back into the WOG
        W.world_object_to_csv()
        # os.system('clear')     # TODO: Make the clear work
        if P.cont is True:   # Control running function that player lands on
            P.wg_interact()   # Control World Grid interaction


# Start from command line
if __name__ == "__main__":
    game_init()
