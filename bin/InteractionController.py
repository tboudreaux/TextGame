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
            return '/s/hurt:100/h/10'
        elif 'RUN' in buy.upper() or 'FLEE' in buy.upper():
            print 'The merchant manages to hit you over the head with a rock but takes pity becuase he has never sean' \
                  ' such a slow runner before in his life, I mean really this is a 78 year old merchant from a far off' \
                  ' land and you are young and from a very near land, the fact that you: a) got spooked enough by a ' \
                  'merchant to want to run and b) were so slow that he managed to hit you over the head with what was' \
                  ' a very poorly aimed rock (if we are being brutally honest here, which you know I always am) is ' \
                  'quite the embaressment in deed.'
            return '/s/hurt:35,/h/5'
        elif buy[0].upper() == 'A' or buy.upper() == 'PUNCH':
            print 'You brutally attach the poor old merchant who wanted nothing but to sell some water to feed his ' \
                  'family, he has a daugter you know, now, because of you her father will no longer be around, yes ' \
                  'thats correct, in you unprovoked and uncalled for attach on the merchant you also convinced him' \
                  'to become a hermit, you monster'
            return '/s/hurt:5,/d/off,/s/mod_standing:-5'
        else:
            buy = raw_input('The Merchant does not speak your local tong well yet as he is from a far off land, '
                            'and he rudely asks you if you could repeat what you said: ')


def I_FUNC_10_14():
    print 'TEST'
    return 0


def I_FUNC_24_24():
    print 'TEST'
    return 0


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