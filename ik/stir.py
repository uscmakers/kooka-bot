from kooka_ik import kooka_ik
import matplotlib.pyplot as plt
import numpy as np

LINK1_LEN = 0.4
LINK2_LEN = 0.3

def main():
    # initialize kooka
    kooka = kooka_ik(LINK1_LEN, LINK2_LEN)
    kooka.print_status()
    coords = kooka.stir()

    # plot
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes(projection='3d')
    ax.set_xlim3d(-1,1)
    ax.set_ylim3d(-1,1)
    ax.set_zlim3d(0,1)
    i = 0

    print(coords)

    while(i<31):
        kooka.print_status()
        goals = np.array(coords[i])
        degrees = kooka.ik(goals)
        kooka.fk()
        
        plt.plot(kooka.pos_x,kooka.pos_y,kooka.pos_z)
        # plt.plot(kooka.traje_x, kooka.traje_y, kooka.traje_z)

        plt.pause(0.1)
        i+=1

        if(i == 30):
            i = 0


main()
