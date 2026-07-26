import json
import state

def load_and_play(filepath, start):
    with open(filepath, 'r', encoding='utf-8') as f:
        scenes = json.load(f) # returns a list of dicts
        scene = {scene["id"]: scene for scene in scenes} # turn it into a dict with id as the key
    
    current_id = start
    while current_id is not None:
        text = scene[current_id]["text"] # get the current line of text
        print(text)
        input("\n")
        current_id = scene[current_id]["next"] # get the next line of text

def win_scene():
    load_and_play("data/scenes/owlbearfight_win.json", "line_01")

    with open("data/scenes/owlbearfight_win.json", 'r', encoding='utf-8') as f:
        scenes = json.load(f) # returns a list of dicts
        char_line = {line["speaker"]: line for line in scenes} # sort lines by the speaker

        ignore_chars = ["fursttryl", "mother_owlbear", "top_baby_owlbear", "bottom_baby_owlbear"]

        # play the party member's dialogue if they are alive
        for character in state.owlbearfight_alive:
            if (state.owlbearfight_alive[character] == True and character not in ignore_chars):
                load_and_play("data/scenes/owlbearfight_win.json", char_line[character]["id"])

        # count how many baby owlbears are alive
        count_babies = 0
        if (state.owlbearfight_alive["top_baby_owlbear"] == True and state.owlbearfight_alive["bottom_baby_owlbear"] == True):
            count_babies = 2
        elif (state.owlbearfight_alive["top_baby_owlbear"] == True or state.owlbearfight_alive["bottom_baby_owlbear"] == True):
            count_babies = 1

        # possibly play additional dialogue depending on count_babies
        if (count_babies == 1):
            load_and_play("data/scenes/owlbearfight_win.json", "line_10")
        elif (count_babies == 2):
            load_and_play("data/scenes/owlbearfight_win.json", "line_11")

    print("End")
    postfight_scene()

def postfight_scene():
    load_and_play("data/scenes/postfight.json", "line_01")

    with open("data/scenes/postfight.json", 'r', encoding='utf-8') as f:
            scenes = json.load(f) # returns a list of dicts
            char_line = {line["speaker"]: line for line in scenes} # sort lines by the speaker

            deaths = 0
            ignore_chars = ["mother_owlbear", "top_baby_owlbear", "bottom_baby_owlbear"]

            # count the number of dead party members
            for character in state.owlbearfight_alive:
                if (state.owlbearfight_alive[character] == False and character not in ignore_chars):
                    deaths += 1

            if (deaths > 0):
                load_and_play("data/scenes/postfight.json", "line_06")

            load_and_play("data/scenes/postfight.json", "line_08")

            # play the party member's dialogue if they are dead
            for character in state.owlbearfight_alive:
                if (state.owlbearfight_alive[character] == False and character not in ignore_chars):
                    load_and_play("data/scenes/postfight.json", char_line[character]["id"])

            load_and_play("data/scenes/postfight.json", "line_14")

            if (deaths > 0):
                load_and_play("data/scenes/postfight.json", "line_17")

            load_and_play("data/scenes/postfight.json", "line_23")
    