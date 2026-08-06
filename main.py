from combat import owlbear_fight
from scenes import load_and_play
import state  

def run_game():
    # intro scene
    load_and_play("data/scenes/intro.json", "intro_01")

    # combat begins
    owlbear_fight()

    # timeskip + funeral
    load_and_play("data/scenes/funeral.json", "funeral_01")

    # ingot interaction
    load_and_play("data/scenes/ingot_interaction01.json", "line_01")

    # illydia interaction
    load_and_play("data/scenes/illydia_interaction.json", "line_01")
    print(state.relationship) # temp print to check point system

if __name__ == "__main__":
    run_game()