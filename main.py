import json

def run_game():
    current_id = "intro_01"
    scene = {}
    with open("data/scenes/intro.json", 'r', encoding='utf-8') as f:
        scenes = json.load(f)
        scene = {scene["id"]: scene for scene in scenes}

    while current_id is not None:
        print(scene[current_id]["text"])
        input("\n")
        current_id = scene[current_id]["next"]
    print("End of intro.")

if __name__ == "__main__":
    run_game()