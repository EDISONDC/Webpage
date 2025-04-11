import random

def explore(player_inventory):
    """Simulates exploring an area, potentially finding items or encountering minor events."""
    events = [
        "You find a small health potion!",
        "You discover a rusty dagger.",
        "You encounter Katherine the traveler who gives you some advice.",
        "Nothing interesting happens.","You discover a key",
    ]
    event = random.choice(events)
    print(f"You explore the area and... {event}")
    if "health potion" in event:
        print("You added a 'Health Potion' to your inventory.")
        player_inventory.append("Health Potion")
    elif "rusty dagger" in event:
        print("You added a 'Rusty Dagger' to your inventory.")
        player_inventory.append("Rusty Dagger")
    elif "key" in event:
        print("You added a 'Key' to your inventory.")
        player_inventory.append("Key")
        

def fight(player_health, player_attack):
    """Simulates a simple combat encounter."""
    enemy_health = random.randint(20, 50)
    enemy_attack = random.randint(5, 15)
    print("\nYou encounter Edison!")

    while player_health > 0 and enemy_health > 0:
        print(f"\nYour Health: {player_health}")
        print(f"Edison's Health: {enemy_health}")
        print("What do you do?")
        print("1. Attack")
        print("2. Try to flee (50% chance)")

        choice = input("Enter choice (1/2): ")

        if choice == "1":
            damage_dealt = random.randint(player_attack - 2, player_attack + 2)
            if damage_dealt < 0:
                damage_dealt = 0
            enemy_health -= damage_dealt
            print(f"You attack Edison for {damage_dealt} damage.")
            if enemy_health > 0:
                damage_taken = random.randint(enemy_attack - 2, enemy_attack + 2)
                if damage_taken < 0:
                    damage_taken = 0
                player_health -= damage_taken
                print(f"Edison attacks you for {damage_taken} damage.")
        elif choice == "2":
            if random.random() < 0.5:
                print("You successfully flee from Edison!")
                break
            else:
                damage_taken = random.randint(enemy_attack - 2, enemy_attack + 2)
                if damage_taken < 0:
                    damage_taken = 0
                player_health -= damage_taken
                print("You fail to flee and Edison attacks you for {damage_taken} damage.")
        else:
            print("Invalid choice.")

    if player_health <= 0:
        print("You have been defeated!")
    elif enemy_health <= 0:
        print("You defeated Edison!")

    return player_health

def check_inventory(inventory):
    """Displays the items in the player's inventory."""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory contains:")
        for item in inventory:
            print(f"- {item}")

def main_game_loop():
    """The main loop of the game."""
    print("Welcome to Vent-it-all-out!")
    player_name = input("Enter your character's name: ")
    player_health = 100
    player_attack = 10
    player_inventory = []

    print(f"\nHello, {player_name}!")

    while player_health > 0:
        print("\nWhat would you like to do?")
        print("1. Explore")
        print("2. Fight an enemy")
        print("3. Check Inventory")
        print("4. Exit Game")

        choice = input("Enter choice (1/2/3/4): ")

        if choice == "1":
            explore(player_inventory)
        elif choice == "2":
            player_health = fight(player_health, player_attack)
        elif choice == "3":
            check_inventory(player_inventory)
        elif choice == "4":
            print("Thank you for playing!")
            break
        else:
            print("Invalid choice. Try again.")

        if player_health <= 0:
            print("Game Over!")
            break

if __name__ == "__main__":
    main_game_loop()
