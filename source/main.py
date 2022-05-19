import time
import sys

import globalValues

if len(sys.argv) == 1:
    globalValues.i_am_server = True


if globalValues.i_am_server:
    # This call never returns.
    import server

import grafic
import waysegment
import labyrint
import player
import usrinput

import pygame
import OpenGL

own_player = player.Player()
other_players = []

print "connect to server      ",

own_player.connect_to_server(sys.argv[1], int(sys.argv[2]))

init_str = own_player.connection.recv(2048)
init_params = init_str.split("-")
own_player.ID = int(init_params[0])
labyrint.deserialize(init_params[2])

print "done"

while True:
    start_time = time.time()

    grafic.render_scene(labyrint)

    moved = False

    rotation_x = 0.0
    rotation_y = 0.0

    for event in usrinput.process_raw_input():
        if event[0] == "move":
            moved = True

            rotation_x += 1.0 * event[2][1]
            rotation_y += 1.0 * event[2][0]

        if event[0] == "click":
            grafic.position_check(event[1][0], event[1][1])
            #print "click at pos " + str(event[1]),
            #print "with color " + str(color)

        if event[0] == "quit":
            quit()

    if moved:
        grafic.update_rotation(rotation_x, rotation_y)



    end_time = time.time()
    #print "Time = " + str((end_time - start_time) * 1000) + " ms"
    time.sleep(0.001)
