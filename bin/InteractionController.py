##############################
#   Interaction Controller   #
##############################
"""
Functionality: Stores the functions and classes to be run at individual world coords
Dependencies: N/A
References: WorldController.py
"""


def I_FUNC_0_0():
    print 'This is the start of your adventure, godspeed'
    return '/s/look_around(),/d/off'


def I_FUNC_1_0():
    buy = raw_input('A Merchant Approaches offering you water, What would you like to do[Buy/Decline/Attack/Flee]: ')
    cont = False
    while cont is False:
        if buy[0].upper() == 'Y' or buy[0].upper() == 'B' or buy[0].upper() == 'P' and buy.upper() != 'BYE' and buy.upper() != 'PUNCH' and len(buy) <= 10:
            cont = True
            return '/s/buy_good:"water":500,/h/10,/s/mod_standing:2'
        elif buy[0].upper() == 'N' or buy[0].upper() == 'D' and len(buy) <= 10:
            print 'The merchant is now sad because he has no money'
            print 'In a fit of rage the merchant attacks you using a old shoe filled with wasps'
            cont = True
            return '/s/hurt:100,/h/10'
        elif 'RUN' in buy.upper() or 'FLEE' in buy.upper():
            print 'The merchant manages to hit you over the head with a rock but takes pity becuase he has never sean' \
                  ' such a slow runner before in his life, I mean really this is a 78 year old merchant from a far off' \
                  ' land and you are young and from a very near land, the fact that you: a) got spooked enough by a ' \
                  'merchant to want to run and b) were so slow that he managed to hit you over the head with what was' \
                  ' a very poorly aimed rock (if we are being brutally honest here, which you know I always am) is ' \
                  'quite the embaressment in deed.'
            return '/s/hurt:35,/h/5,/a/north'
        elif buy[0].upper() == 'A' or buy.upper() == 'PUNCH':
            print 'You brutally attach the poor old merchant who wanted nothing but to sell some water to feed his ' \
                  'family, he has a daugter you know, now, because of you her father will no longer be around, yes ' \
                  'thats correct, in you unprovoked and uncalled for attach on the merchant you also convinced him' \
                  'to become a hermit, you monster.....'
            print 'You watch the poor merchant run off to his life of hermitage with a black eye, however as he is ' \
                  'going he happens into some quicksand and dies. At least it wasnt your fault you think'
            return '/s/hurt:5,/d/off,/s/mod_standing:-5'
        else:
            buy = raw_input('The Merchant does not speak your local tong well yet as he is from a far off land, '
                            'and he rudely asks you if you could repeat what you said: ')


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