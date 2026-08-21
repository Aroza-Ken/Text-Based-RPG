import json
import state

def check_relationship(character):
    # for the respective characters, set the flag depending if the relationship is positive or negative
    if (character == "ingot" or character == "willow"):
        if state.relationship[character] == -3:
            state.scene_flags[character] = True
    if (character == "illydia" or character == "john"):
        if state.relationship[character] == 3:
            state.scene_flags[character] = True

def load_and_play(filepath, start):
    with open(filepath, 'r', encoding='utf-8') as f:
        scenes = json.load(f) # returns a list of dicts
        scene = {scene["id"]: scene for scene in scenes} # turn it into a dict with id as the key
    
    current_id = start
    while current_id is not None:
        if ("options" in scene[current_id]):
            choices = {}
            while (True):
                count = 1

                print(scene[current_id]["text"]) # print the current line of text

                # store all the options in a dict
                for options in scene[current_id]["options"]:
                    choices.update({count: options})
                    print(options["label"])
                    count += 1

                choice = input("\n")
                try:
                    number = int(choice)
                except ValueError:
                    continue

                # state of character relationship and next dialogue depending on player's choice
                if (choice == "1"):
                    if (options["target"] != None):
                        state.relationship[options["target"]] += choices[int(choice)]["points"]
                    next_text = choices[int(choice)]["next"]
                    # if the next text branches, check the relationship status and proceed to the respective scene
                    if (next_text == "check_status"):
                        check_relationship(options["target"])
                        if (state.scene_flags[options["target"]] == True):
                            current_id = choices[int(choice)]["scene_A"]
                        else:
                            current_id = choices[int(choice)]["scene_B"]
                    else:
                        current_id = choices[int(choice)]["next"]
                    break
                elif (choice == "2"):
                    if (options["target"] != None):
                        state.relationship[options["target"]] += choices[int(choice)]["points"]
                    next_text = choices[int(choice)]["next"]
                    # if the next text branches, check the relationship status and proceed to the respective scene
                    if (next_text == "check_status"):
                        check_relationship(options["target"])
                        if (state.scene_flags[options["target"]] == True):
                            current_id = choices[int(choice)]["scene_A"]
                        else:
                            current_id = choices[int(choice)]["scene_B"]
                    else:
                        current_id = choices[int(choice)]["next"]
                    break
                elif (choice == "3"):
                    if (options["target"] != None):
                        state.relationship[options["target"]] += choices[int(choice)]["points"]
                    next_text = choices[int(choice)]["next"]
                    # if the next text branches, check the relationship status and proceed to the respective scene
                    if (next_text == "check_status"):
                        check_relationship(options["target"])
                        if (state.scene_flags[options["target"]] == True):
                            current_id = choices[int(choice)]["scene_A"]
                        else:
                            current_id = choices[int(choice)]["scene_B"]
                    else:
                        current_id = choices[int(choice)]["next"]
                    break
                else:
                    continue
        # if there is no next field, check the relationship status and proceed to the respective scene branch
        elif ("next" not in scene[current_id]):
            check_relationship(scene[current_id]["target"])
            if (state.scene_flags[scene[current_id]["target"]] == True):
                current_id = scene[current_id]["scene_A"]
            else:
                current_id = scene[current_id]["scene_B"]
        else:
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