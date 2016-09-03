##############################
#   Interaction Controller   #
##############################
"""
Functionality: Stores the functions and classes to be run at individual world coords
Dependencies: N/A
References: WorldController.py
"""


def I_FUNC_0_0(INFO):
    print 'This is the start of your adventure, godspeed'
    return '/s/look_around(),/d/off'


def I_FUNC_1_0(INFO):
    buy = raw_input('A Merchant Approaches offering you water, would you like to buy some?')
    cont = False
    while cont is False:
        if buy[0].upper() == 'Y' and len(buy) <= 5:
            cont = True
            return '/s/buy_good:"water":500,/d/t2a'
        elif buy[0].upper() == 'N' and len(buy) <= 5:
            print 'The merchant is now sad because he has no money'
            print 'In a fit of rage the merchant attacks you using a old shoe filled with wasps'
            cont = True
            return '/s/hurt:100'
        else:
            buy = raw_input('The Merchant does not speak your local tong well yet as he is from a far off land, '
                            'and he rudely asks you if you could repeat what you said: ')


def I_FUNC_10_14(INFO):
    print 'TEST'
    return 0


def I_FUNC_24_24(INFO):
    print 'TEST'
    return 0


def I_FUNC_0_24(INFO):
    print 'TEST'
    return 0


def I_FUNC_24_0(INFO):
    print 'TEST'
    return 0


def I_FUNC_13_0(INFO):
    print 'TEST'
    return 0


def I_FUNC_0_13(INFO):
    print 'TEST'
    return 0


def I_FUNC_13_24(INFO):
    print 'TEST'
    return 0

def I_FUNC_24_13(INFO):
    print 'TEST'
    return 0