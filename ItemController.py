#####################
#  Item Controller  #
#####################
import random as r
c = 299792458    # Speed of light


def route_use(Player_name, item):
    if item == 'a_strange_green_thing':
        a_strange_green_thing(Player_name)
    elif item == 'acceleration_engine':
        acceleration_engine(Player_name)


def a_strange_green_thing(Player_name):
    print 'NOTHING HAPPENS ASIDE FROM YOU GETTING MORE GREEN STUFF ON YOUR FACE, IT IS MILDLY ENTERING THO'
    Player_name.inventory['A Strange Green thing'] -= 1


def acceleration_engine(Player_name):
    dv = raw_input('Please enter desired velocity relative to the sentinel: ')
    if dv < c:
        Player_name.velocity = dv
    else:
        print 'You start moving, faster, faster, faster, however it is getting harder, faster...faster.........' \
              '...faster.............................................................................faster' \
              ' much to everyones suprise you did not make it to the speed of light, that was sarcastic, no one' \
              ' was suprised, do you not know basic physics, anyways you are moving pretty fast now'
        vel_min = r.uniform(0.1, 10)
        Player_name.velocity = c - vel_min
        print 'VELOCCITY IS: ' + str(Player_name.velocity)
        print 'THAT IS ' + str((Player_name.velocity/c)*100) + ' % the speed of light'
