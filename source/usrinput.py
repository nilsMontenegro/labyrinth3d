import pygame

down  = False
moved = False

def process_raw_input():
    global down, moved

    generated_events = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            generated_events.append(["quit"])

        if event.type == pygame.MOUSEBUTTONDOWN:
            down  = True
            moved = False

        if event.type == pygame.MOUSEBUTTONUP:
            if down == True and moved == False:
                generated_events.append(["click", event.pos])
            down  = False
            moved = False

        if event.type == pygame.MOUSEMOTION:
            moved = True
            if down == True:
                generated_events.append(["move", event.pos, event.rel])

    return generated_events
