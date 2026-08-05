from combat import owlbear_fight
from scenes import load_and_play    

def run_game():
    # intro scene
    load_and_play("data/scenes/intro.json", "intro_01")
    print("End of intro.")

    # combat begins
    owlbear_fight()

    # timeskip + funeral
    load_and_play("data/scenes/funeral.json", "funeral_01")

if __name__ == "__main__":
    run_game()