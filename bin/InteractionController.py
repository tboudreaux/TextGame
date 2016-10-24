##############################
#   Interaction Controller   #
##############################
"""
Functionality: Stores the functions and classes to be run at individual world coords
Dependencies: N/A
References: WorldController.py
"""
from colorama import Fore, Back, Style

def I_FUNC_0_0():
    print 'This is the start of your adventure, godspeed'
    return '/s/look_around(),/d/off'


def I_FUNC_1_0():
    print 'A strange orange thing comes before you blocking the way, you hesitate but eventually decide to try and ' \
          'to communicate with it via a yodal, it does not work, the orange beast approaches and engulfs you in its ' \
          'outer membrane. What is this then? You are inside the beast, its dark very dark....you hear a voice...'
    print Fore.GREEN + Back.RED + 'HELLO TRAVELER, I PRESENT UNTO YOU 12 ITEMS TO CHANGE YOUR MOVEMENT RELATIVE TO ' \
                                  'THE SENTINAL' + Style.RESET_ALL + '\nAt this point you are quite confused, really ' \
                                                                     'you only went out for a gallon of milk but okay' \
                                                                     ' sometimes one just has to, as they say role ' \
                                                                     'with it...' + Fore.GREEN + Back.RED + 'Stop' \
          'STOP THINKING TO YOURSELF IT IS QUITE DISTRACTING, REGARDLESS USE THESSE TO SELECT A VELOCITY, NOW GOOOOO'
    print Style.RESET_ALL
    print "The orange entity flys away in a flury of furbies, do not be fooed however the furbies are not the object" \
          "mearly an eccentricity of this orange glob, he like them don't judge, anyways he leaves behind 12 round" \
          "spheres and an oval one, the round spheres glow, the oval one was a figment of your imagination"
    pick_up = ('Would you like to pick up the objects: ')

    print 'As you ' + pick_up + 'the objetcs violently fly into your bag, apparently you had no choice in the matter ' \
          'to begin with'

    return '/s/give_item:"Acceleration Engine":12,/d/off'
def I_FUNC_2_0():
    return '/s/req_data:"rep|PIA-1-0|PIA-2-0"'
def U_FUNC_2_0(parameter_array):
    print 'You approach a giant roach'
    parameter_array = parameter_array.split(':')
    if parameter_array[2] != "KilledRoach":
        if int(parameter_array[0]) > 5:
            print 'The Roach sees that you are in good standing and lets you pass'
            return '/s/mod_standing:2,/d/rp'
        elif int(parameter_array[0]) == 5:
            print 'The Roach cannot make up its mind with you, it decides to eat you just to be on the safe side, you ' \
                  'know the old saying -- a roach always plays it safe '
            return '/s/hurt:100'
        elif int(parameter_array[0]) < 5:
            print 'The Roach is so appauled by your reputation (which let us be clear, precede you) that it has a cardiac' \
                  ' arrest, the towns people are so happy that this giant roach was killed (really a giant roach is gross)' \
                  'that they throw a party for you, it lasts for a long time'
            return '/s/mod_standing:100,/d/KilledRoach'
    else:
        print 'The roach body rots in the mud, gases are released and hurt you'
        return '/s/hurt:2,/h/2'

def I_FUNC_3_0():
    return '/s/req_data:"PIA-2-0"'
def U_FUNC_3_0(parameter_array):
    print 'You approach another giant roach'
    parameter_array = parameter_array.split(':')
    if parameter_array[0] == 'KilledRoach':
        print 'The roach shreaks at you "YOU KILLED MY MATE"'
        print 'Then the roach thinks, and says more gently, almost sensually "Thank god he was a real boar"'
        return '/s/mod_standing:10,/d/off'
    else:
        print 'The Roach has no interest in dealing with you, so eats you just to be on the safe side'
        return "/s/hurt:100"


def I_FUNC_0_24():
    print 'TEST'
    return 0


def I_FUNC_24_0():
    print 'TEST'
    return 0


def I_FUNC_13_0():
    print 'TEST'
    return 0


def I_FUNC_0_13():
    print 'TEST'
    return 0


def I_FUNC_13_24():
    print 'TEST'
    return 0

def I_FUNC_24_13():
    print 'TEST'
    return 0