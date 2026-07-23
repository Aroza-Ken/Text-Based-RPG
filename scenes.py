import json

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
    # add win scene here
    return

def postfight_scene():
    # add postfight scene here
    return