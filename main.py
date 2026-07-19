import json

def run_game():
    current_id = "intro_01"
    scene = {}
    with open("data/scenes/intro.json", 'r', encoding='utf-8') as f:
        scenes = json.load(f) # turns a list of dicts
        scene = {scene["id"]: scene for scene in scenes} # turn it into a dict with id as the key

    while current_id is not None:
        text = scene[current_id]["text"] # get the current line of text
        print(text)
        input("\n")
        current_id = scene[current_id]["next"] # get the next line of text
    print("End of intro.")

if __name__ == "__main__":
    run_game()