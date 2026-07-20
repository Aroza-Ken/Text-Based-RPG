import json
import random

owlbearfight_alive = {"fursttryl": True, "ingot": True, "willow": True, "ilydia": True, "john": True, 
                      "mother_owlbear": True, "top_baby_owlbear": True, "bottom_baby_owlbear": True}

def win_scene():
    # add win scene here

def postfight_scene():
    # add postfight scene here

def owlbear_fight():
    with open("data/combat/owlbear_fight.json", 'r', encoding='utf-8') as f:
        encounter = json.load(f)
        party = encounter["party"]
        party_HP = {}
        enemy_HP = {}
        win_HP_boundary = encounter["win_hp_condition"]

        party_files = []

        # store HP for all party in a dict
        for member in party:
            path = f"data/characters/{member}.json"
            with open(path, 'r', encoding='utf-8') as file:
                character = json.load(file)
                party_HP.update({character["id"]: character["HP"]["child"]})
                party_files.append(character)

        party_files.sort(key=lambda x: x["id"])
        party_lookup = {member["id"]: member for member in party_files}
        
        # store HP for all enemies in a dict
        enemies = encounter["enemies"]
        for enemy in enemies:
            enemy_HP.update({enemy["id"]: enemy["HP"]})
        
        enemy_lookup = {enemy["id"]: enemy for enemy in enemies}

        # turn-based rotation loop
        while (True):
            initial_rotation = encounter["rotation"]
            updated_rotation = []
            alive_party = []
            alive_enemy = []
            fight_over = False
            win = False

            # check if character is alive
            for character in initial_rotation:
                if (owlbearfight_alive[character] == True):
                    updated_rotation.append(character)
                    if (character in party_HP and character != "fursttryl"):
                        alive_party.append(character)
                    else:
                        alive_enemy.append(character)
            
            # loop through updated rotation
            for character in updated_rotation:
                if (character == "fursttryl"): # player-controlled character
                    # do moves + update respective character HP (party or enemy)
                    # if attack kills enemy, update its alive status
                elif (character in enemy_HP): # enemy NPC
                    min_damage = enemy_lookup[character]["damage"]["min"]
                    max_damage = enemy_lookup[character]["damage"]["max"]
                    damage = random.randint(min_damage, max_damage) # random damage within bounds
                    # randomly attack other party member over player character
                    if (len(alive_party) > 0):
                        target = random.randint(0, len(alive_party) - 1)
                        chosen_target = alive_party[target]
                        updated_HP = party_HP[chosen_target] - damage
                        party_HP.update({chosen_target: updated_HP})
                        if (updated_HP <= 0): # update character to dead if HP falls below 0
                            owlbearfight_alive.update({chosen_target: False})
                    else:
                        updated_HP = party_HP["fursttryl"] - damage
                        party_HP.update({"fursttryl": updated_HP})
                        if (updated_HP <= 0): # update character to dead if HP falls below 0
                            owlbearfight_alive.update({"fursttryl": False})
                            fight_over = True
                else: # party NPC
                    attacks = []
                    assists = []
                    will_attack = True

                    # store attack and assist moves separately
                    for ability in party_lookup[character]["abilities"]:
                        if (ability["type"] == "attack"):
                            attacks.append(ability)
                        else:
                            assists.append(ability)
                    
                    # if character as assist moves, randomize whether to attack or assist
                    if (len(assists) > 0):
                        option = random.randint(0, 1)
                        if (option == 1):
                            will_attack = False
                    
                    # if attack, randomize attack ability, damage and target
                    # then update target current HP
                    if (will_attack == True):
                        move = random.randint(0, len(attacks) - 1)
                        chosen_move = attacks[move]
                        min_damage = chosen_move["damage"]["min"]
                        max_damage = chosen_move["damage"]["max"]
                        damage = random.randint(min_damage, max_damage)
                        
                        target = random.randint(0, len(alive_enemy) - 1)
                        chosen_target = alive_enemy[target]
                        updated_HP = enemy_HP[chosen_target] - damage
                        enemy_HP.update({chosen_target: updated_HP})
                        if (updated_HP <= 0): # update character to dead if HP falls below 0
                            owlbearfight_alive.update({chosen_target: False})
                        # if the mother owlbear HP falls to the win condition
                        if (chosen_target == "mother_owlbear" and updated_HP <= win_HP_boundary):
                            fight_over = True
                            win = True
                    # if assist, randomize healing effect and target
                    # then update target current HP
                    else:
                        min_healing = assists[0]["healing"]["min"]
                        max_healing = assists[0]["healing"]["max"]
                        healing = random.randint(min_healing, max_healing)
                        target = random.randint(0, len(alive_party) - 1)
                        chosen_target = alive_party[target]
                        updated_HP = party_HP[chosen_target] + healing
                        # can only heal HP up to target's max HP
                        if (updated_HP > party_lookup[chosen_target]["HP"]["child"]):
                            updated_HP = party_lookup[chosen_target]["HP"]["child"]
                        party_HP.update({chosen_target: updated_HP})

            # check if win or loss conditions are met
            if (fight_over == True):
                if (win == True):
                    win_scene()
                    break
                else:
                    postfight_scene()
                    break
                    

def run_game():
    # intro scene
    current_id = "intro_01"
    scene = {}
    with open("data/scenes/intro.json", 'r', encoding='utf-8') as f:
        scenes = json.load(f) # returns a list of dicts
        scene = {scene["id"]: scene for scene in scenes} # turn it into a dict with id as the key

    while current_id is not None:
        text = scene[current_id]["text"] # get the current line of text
        print(text)
        input("\n")
        current_id = scene[current_id]["next"] # get the next line of text
    print("End of intro.")

    # combat begins
    owlbear_fight()

if __name__ == "__main__":
    run_game()