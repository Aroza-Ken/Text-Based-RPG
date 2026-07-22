import json
import random

owlbearfight_alive = {"fursttryl": True, "ingot": True, "willow": True, "ilydia": True, "john": True, 
                      "mother_owlbear": True, "top_baby_owlbear": True, "bottom_baby_owlbear": True}

def win_scene():
    # add win scene here
    return

def postfight_scene():
    # add postfight scene here
    return

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
                    elif (character in enemy_HP):
                        alive_enemy.append(character)
            
            # loop through updated rotation
            for character in updated_rotation:
                if (character == "fursttryl"): # player-controlled character
                    turn_over = False
                    while (True):
                        toplevel_choice = ["1: Attack", "2: Assist", "3: Stats(Health)"]
                        for choice in toplevel_choice:
                            print(choice)
                        pick = input("\n")
                        if (pick == "1"): # Attack
                            while (True):
                                display_moves = [] # purely used to display the attack name with its representative number
                                player_attacks = {} # holds the actual attack data with its representative number
                                count_moves = 1

                                # fill in the above list and dict with the respective variables
                                for ability in party_lookup[character]["abilities"]:
                                    if (ability["type"] == "attack"):
                                        player_attacks.update({count_moves: ability})
                                        display_move = f"{count_moves}: {ability["name"]}"
                                        display_moves.append(display_move)
                                        count_moves += 1
                                
                                # add a return option (in both the list and dict)
                                return_toplevel = f"{count_moves}: Return"
                                display_moves.append(return_toplevel)
                                player_attacks.update({count_moves: "Return"})

                                for display_options in display_moves:
                                    print(display_options)
                                
                                select = input("\n")

                                try:
                                    number = int(select)
                                except ValueError:
                                    continue

                                # player chooses one of the attack abilities
                                if (int(select) in player_attacks and player_attacks[int(select)] != "Return"):
                                    while (True):
                                        display_enemies = [] # purely used to display the enemy name with its representative number
                                        current_enemies = {} # holds the actual enemy data with its representative number
                                        count_enemies = 1
                                        for enemy in alive_enemy:
                                            display_enemy = f"{count_enemies}: {enemy_lookup[enemy]["name"]}"
                                            display_enemies.append(display_enemy)
                                            current_enemies.update({count_enemies: enemy})
                                            count_enemies += 1
                                        
                                        # add a return option (in both the list and dict)
                                        return_attacks = f"{count_enemies}: Return"
                                        display_enemies.append(return_attacks)
                                        current_enemies.update({count_enemies: "Return"})

                                        for display_options in display_enemies:
                                            print(display_options)
                                        
                                        target = input("\n")

                                        try:
                                            number = int(target)
                                        except ValueError:
                                            continue

                                        # player chooses one of the alive targets, damage is randomized and target HP is updated
                                        if (int(target) in current_enemies and current_enemies[int(target)] != "Return"):
                                            min_damage = player_attacks[int(select)]["damage"]["min"]
                                            max_damage = player_attacks[int(select)]["damage"]["max"]
                                            damage = random.randint(min_damage, max_damage)
                                            chosen_target = current_enemies[int(target)]
                                            updated_HP = enemy_HP[chosen_target] - damage
                                            enemy_HP.update({chosen_target: updated_HP})

                                            if (updated_HP <= 0): # update character to dead if HP falls below 0
                                                owlbearfight_alive.update({chosen_target: False})
                                            # if the mother owlbear HP falls to the win condition
                                            if (chosen_target == "mother_owlbear" and updated_HP <= win_HP_boundary):
                                                fight_over = True
                                                win = True
                                            turn_over = True
                                        elif (int(target) in current_enemies): # player chooses return, goes back to pick ability
                                            break
                                        else:
                                            continue
                                elif (int(select) in player_attacks): # player chooses return, goes back to top level choice
                                    break
                                else:
                                    continue                     
                        elif (pick == "2"): # Assist
                            while (True):
                                display_moves = [] # purely used to display the assist name with its representative number
                                player_assists = {} # holds the actual assist data with its representative number
                                count_moves = 1

                                # fill in the above list and dict with the respective variables
                                for ability in party_lookup[character]["abilities"]:
                                    if (ability["type"] == "assist"):
                                        player_assists.update({count_moves: ability})
                                        display_move = f"{count_moves}: {ability["name"]}"
                                        display_moves.append(display_move)
                                        count_moves += 1
                                
                                # add a return option (in both the list and dict)
                                return_toplevel = f"{count_moves}: Return"
                                display_moves.append(return_toplevel)
                                player_assists.update({count_moves: "Return"})

                                for display_options in display_moves:
                                    print(display_options)
                                
                                select = input("\n")

                                try:
                                    number = int(select)
                                except ValueError:
                                    continue

                                # player chooses return, goes back to top level choice
                                if (int(select) in player_assists and player_assists[int(select)] == "Return"):
                                    break
                                # if not return, player chooses one of the assist abilities
                                elif (int(select) in player_assists and player_assists[int(select)]["name"] == "Guidance"):
                                    # to be implemented
                                    continue
                                elif (int(select) in player_assists and player_assists[int(select)]["name"] == "Cure Wounds"):
                                    while (True):
                                        display_party = [] # purely used to display the enemy name with its representative number
                                        current_party = {} # holds the actual enemy data with its representative number
                                        count_party = 1
                                        for member in alive_party:
                                            display_member = f"{count_party}: {party_lookup[member]["name"]}"
                                            display_party.append(display_member)
                                            current_party.update({count_party: member})
                                            count_party += 1
                                        
                                        # add player character to list and dict
                                        display_player = f"{count_party}: {party_lookup["fursttryl"]["name"]}"
                                        display_party.append(display_player)
                                        current_party.update({count_party: "fursttryl"})
                                        count_party += 1
                                        
                                        # add a return option (in both the list and dict)
                                        return_assists = f"{count_party}: Return"
                                        display_party.append(return_assists)
                                        current_party.update({count_party: "Return"})

                                        for display_options in display_party:
                                            print(display_options)
                                        
                                        target = input("\n")

                                        try:
                                            number = int(target)
                                        except ValueError:
                                            continue

                                        # player chooses one of the alive targets, damage is randomized and target HP is updated
                                        if (int(target) in current_party and current_party[int(target)] != "Return"):
                                            min_healing = player_assists[int(select)]["healing"]["min"]
                                            max_healing = player_assists[int(select)]["healing"]["max"]
                                            healing = random.randint(min_healing, max_healing)
                                            chosen_target = current_party[int(target)]
                                            updated_HP = party_HP[chosen_target] + healing
                                            # can only heal HP up to target's max HP
                                            if (updated_HP > party_lookup[chosen_target]["HP"]["child"]):
                                                updated_HP = party_lookup[chosen_target]["HP"]["child"]
                                            party_HP.update({chosen_target: updated_HP})
                                            turn_over = True
                                        elif (int(target) in current_party): # player chooses return, goes back to pick ability
                                            break
                                        else:
                                            continue
                                else:
                                    continue
                        elif (pick == "3"): # Stats(Health)
                            continue
                        else: # Prompt player again for valid input
                            continue

                        if (turn_over == True):
                            break
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