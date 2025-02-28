import random

# Base Character Class
class Character:
    def __init__(self, name, hp, attack, defense, level=1, experience=0, inventory=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = experience
        self.inventory = inventory if inventory else []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        actual_damage = max(damage - self.defense, 0)
        self.hp -= actual_damage
        return actual_damage

    def attack_enemy(self, enemy, attack_type="normal"):
        damage = self.attack * (1 if attack_type == "normal" else 1.5)
        print(f"{self.name} attacks {enemy.name} with {attack_type} attack for {damage} damage.")
        enemy.take_damage(damage)

    def use_item(self, item):
        if item in self.inventory:
            print(f"{self.name} uses {item.name}.")
            item.apply_effect(self)
            self.inventory.remove(item)
        else:
            print(f"{item.name} is not in inventory.")

    def gain_experience(self, exp):
        self.experience += exp
        print(f"{self.name} gains {exp} experience points.")
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 2
        self.defense += 1
        self.experience = 0
        print(f"{self.name} levels up! Now at level {self.level}.")

# Specific Character Classes
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 120, 25, 10)

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, 80, 35, 5)

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, 90, 30, 8)

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, 85, 28, 7)

# Item Classes
class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def apply_effect(self, character):
        if self.effect['type'] == 'heal':
            character.hp += self.effect['value']
            if character.hp > character.max_hp:
                character.hp = character.max_hp
            print(f"{character.name} heals for {self.effect['value']} HP. Total HP: {character.hp}")

class HealingPotion(Item):
    def __init__(self):
        super().__init__("Healing Potion", {'type': 'heal', 'value': 20})

class SuperHealingPotion(Item):
    def __init__(self):
        super().__init__("Super Healing Potion", {'type': 'heal', 'value': 50})

# Enemy Classes
class Goblin(Character):
    def __init__(self):
        super().__init__("Goblin", 60, 15, 5)

class Orc(Character):
    def __init__(self):
        super().__init__("Orc", 80, 20, 10)

class Dragon(Character):
    def __init__(self):
        super().__init__("Dragon", 200, 40, 20)

class Bandit(Character):
    def __init__(self):
        super().__init__("Bandit", 70, 18, 8)

# Game Class
class Game:
    def __init__(self):
        self.player = self.create_character()
        self.enemies = [Goblin(), Orc(), Bandit(), Dragon()]
        self.shop_items = [HealingPotion(), SuperHealingPotion()]
        self.quests = [
            {"name": "Defeat the Goblin", "enemy": self.enemies[0], "reward": 10},
            {"name": "Retrieve the Magic Amulet from the Orc", "enemy": self.enemies[1], "reward": 20},
            {"name": "Rescue the Villager from the Bandit", "enemy": self.enemies[2], "reward": 15},
            {"name": "Slay the Dragon", "enemy": self.enemies[3], "reward": 50}
        ]
        self.current_quest = 0

    def create_character(self):
        print("Choose your class:\n1. Warrior\n2. Mage\n3. Rogue\n4. Archer")
        choice = input("Enter the number of your choice: ")
        if choice == "1":
            return Warrior("Hero")
        elif choice == "2":
            return Mage("Hero")
        elif choice == "3":
            return Rogue("Hero")
        elif choice == "4":
            return Archer("Hero")
        else:
            print("Invalid choice, defaulting to Warrior.")
            return Warrior("Hero")

    def play(self):
        print(f"Welcome to the RPG game, {self.player.name}!")
        while self.player.is_alive() and self.current_quest < len(self.quests):
            self.show_status()
            self.show_quest()
            action = input("Do you want to (A)ttack, (S)pecial Attack, (U)se Item, or (V)isit Shop? ").lower()
            if action == "a":
                self.battle(self.quests[self.current_quest]["enemy"], "normal")
            elif action == "s":
                self.battle(self.quests[self.current_quest]["enemy"], "special")
            elif action == "u":
                if self.player.inventory:
                    self.player.use_item(self.player.inventory[0])
                else:
                    print("No items in inventory.")
            elif action == "v":
                self.visit_shop()
            else:
                print("Invalid action. Try again.")
        
        if self.player.is_alive():
            print("You have completed all the quests!")
        else:
            print("You have been defeated. Game Over.")

    def show_status(self):
        print(f"{self.player.name} - HP: {self.player.hp}/{self.player.max_hp}, Level: {self.player.level}, EXP: {self.player.experience}")

    def show_quest(self):
        quest = self.quests[self.current_quest]
        print(f"Current Quest: {quest['name']} - Reward: {quest['reward']} EXP")

    def battle(self, enemy, attack_type):
        while self.player.is_alive() and enemy.is_alive():
            self.player.attack_enemy(enemy, attack_type)
            if enemy.is_alive():
                enemy.attack_enemy(self.player, random.choice(["normal", "special"]))

        if self.player.is_alive():
            print(f"You have defeated the {enemy.name}!")
            self.player.gain_experience(self.quests[self.current_quest]["reward"])
            self.current_quest += 1
        else:
            print(f"You have been defeated by the {enemy.name}.")

    def visit_shop(self):
        print("Welcome to the shop! Available items:")
        for index, item in enumerate(self.shop_items):
            print(f"{index + 1}. {item.name} - Effect: {item.effect}")
        
        choice = input("Enter the number of the item to buy or 'q' to quit: ")
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(self.shop_items):
                self.player.inventory.append(self.shop_items[index])
                print(f"{self.player.name} buys a {self.shop_items[index].name}.")
            else:
                print("Invalid choice.")
        elif choice.lower() == 'q':
            print("Leaving the shop.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    game = Game()
    game.play()

# Additional Quests and Dialogue
def show_dialogue(text):
    print("\n" + text + "\n")

class SideQuest:
    def __init__(self, name, description, reward):
        self.name = name
        self.description = description
        self.reward = reward

    def complete_quest(self, player):
        print(f"Quest '{self.name}' completed! Reward: {self.reward} EXP")
        player.gain_experience(self.reward)

# Extending Game Class
class ExtendedGame(Game):
    def __init__(self):
        super().__init__()
        self.side_quests = [
            SideQuest("Find the Lost Ring", "A villager has lost a precious ring in the forest.", 5),
            SideQuest("Collect 10 Herbs", "Gather 10 healing herbs for the healer.", 5)
        ]

    def play(self):
        print(f"Welcome to the extended RPG game, {self.player.name}!")
        while self.player.is_alive() and (self.current_quest < len(self.quests) or self.side_quests):
            self.show_status()
            self.show_quest()
            action = input("Do you want to (A)ttack, (S)pecial Attack, (U)se Item, (V)isit Shop")