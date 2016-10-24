import matplotlib.pyplot as plt
import random as r
import numpy as np
from tqdm import tqdm

from ObjectController import  Player, NPC
import WorldController


def game_run():
    """
    Main Game start
    :return: N/A
    """
    # count = 0
    # plt.axis([0,10,0,10])
    # plt.ion()
    # plt.show()
    # NPC_Count = 25  # Number of NPCs to Spawn into the world
    # NPCs = []
    # char_types = ['Market Capitalists', 'Commies', 'speedy goer', 'Juggernauts',
    #               'One of those supper dull people (Chemists)']
    W = WorldController.World()      # Initialize the world
    P = Player(3)  # Call player into initialization routine (default player speed 3 m/s)
    # W.update_world_object('Player', P.coords()[0], P.coords()[1])
    # for i in range(NPC_Count):      # Generate NPCs and place them on the world grid
    #     NPCs.append(NPC(char_types[r.randint(0, len(char_types)-1)]))       # Generate NPCs of semi-random class
    #     W.update_world_object('NPC_'+str(i), NPCs[i].coords()[0], NPCs[i].coords()[1])  # Place NPCs in world grid
    # W.world_object_to_csv()     # Debug code to see what is happening
    while P.cont is True:     # Game Loop
        if P.turn % 5 == 0:
            P.check_time()      # Check Player time
        if P.HP <= 0:    # check health and if less than or 0 kill the player
            W.reset_wog()       # Reset the world grid when the player dies
            # NPCs = []     # Kill all the NPCs in the world
            # for i in range(NPC_Count):      # Regenerate the NPCs
            #     NPCs.append(NPC(char_types[r.randint(0, len(char_types)-1)]))
            #     W.update_world_object('NPC_'+str(i), NPCs[i].coords()[0], NPCs[i].coords()[1])
            P.death()       # Kill the player
        # W.update_world_object(np.nan, P.coords()[0], P.coords()[1])
        P.player_action()    # preform an action
        # if type(W.query_wog()[P.coords()[0]][P.coords()[1]]) != float:  # Only look at non nan elements (non empty)
        #     if 'NPC' in W.query_wog()[P.coords()[0]][P.coords()[1]]:
        #         W.update_world_object('Player&'+W.query_wog()[P.coords()[0]][P.coords()[1]],
        #                               P.coords()[0], P.coords()[1])   # Update the Players Position on the WOG
        # else:
        #     W.update_world_object('Player', P.coords()[0], P.coords()[1])  # Update the Players Position on the WOG
        # print 'CALCULATING NON PLAYER MOVES',
        # for j, i in enumerate(NPCs):        # calculate NPC moves
        #     if type(W.query_wog()[i.coords()[0]][i.coords()[1]]) != float:   # Only look if there is something (not nan)
        #         if 'Player' in W.query_wog()[i.coords()[0]][i.coords()[1]]:
        #             W.update_world_object("Player", i.coords()[0], i.coords()[1])      # Reset the old world grid coord
        #         else:
        #             W.update_world_object("", i.coords()[0], i.coords()[1])
        #     i.action(P, W.query_wog())      # Preform Some action
        #     if type(W.query_wog()[i.coords()[0]][i.coords()[1]]) != float:
        #         if 'Player' in W.query_wog()[i.coords()[0]][i.coords()[1]]:
        #             W.update_world_object('Player&NPC_'+str(j), i.coords()[0],
        #                                   i.coords()[1])  # Add the NPC back into the WOG
        #         if 'NPC' in W.query_wog()[i.coords()[0]][i.coords()[1]]:
        #             W.update_world_object(W.query_wog()[i.coords()[0]][i.coords()[1]] + '&NPC_'+str(j), i.coords()[0],
        #                                   i.coords()[1])  # Add the NPC back into the WOG
        #     else:
        #         W.update_world_object('NPC_' + str(j), i.coords()[0],i.coords()[1])  # Add the NPC back into the WOG
        # W.world_object_to_csv()
        # plt.close()
        # for i in NPCs:
        #     if i.query_type() == char_types[0]:
        #         s = 'k'
        #     elif i.query_type() == char_types[1]:
        #         s = 'g'
        #     elif i.query_type() == char_types[2]:
        #         s = 'b'
        #     elif i.query_type() == char_types[3]:
        #         s = 'c'
        #     elif i.query_type() == char_types[4]:
        #         s = 'y'
        #
        #     if i.query_gender() == 'male':
        #         p = 'o'
        #     elif i.query_gender() == 'female':
        #         p = 'D'
        #     plt.plot([i.coords()[0]], [i.coords()[1]], p+s)
        # plt.plot([P.coords()[0]], [P.coords()[1]], 'or')
        # count += 1
        # plt.xlim(xmax=10)
        # plt.xlim(xmin=0)
        # plt.ylim(ymax=10)
        # plt.ylim(ymin=0)
        # plt.draw()
        # plt.pause(0.001)
        # # os.system('clear')     # TODO: Make the clear work
        if P.cont is True:   # Control running function that player lands on
            P.wg_interact()   # Control World Grid interaction


if __name__ == "__main__":
    game_run()
