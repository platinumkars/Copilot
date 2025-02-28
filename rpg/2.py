import random

# Character Classes
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

    def attack_enemy(self, enemy, attack_type):
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

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 120, 25, 10)

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, 80, 35, 5)

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, 90, 30, 8)

# Item Classes
class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def apply_effect(self, character):
        if self.effect['type'] == 'heal':
            character.hp += self.effect['value']
            print(f"{character.name} heals for {self.effect['value']} HP. Total HP: {character.hp}")

class HealingPotion(Item):
    def __init__(self):
        super().__init__("Healing Potion", {'type': 'heal', 'value': 20})

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

# Game Class with Quests and Storyline
class Game:
    def __init__(self):
        self.player = self.create_character()
        self.enemies = [Goblin(), Orc(), Dragon()]
        self.quests = ["Defeat the Goblin", "Retrieve the Magic Amulet", "Slay the Dragon"]
        self.current_quest = 0

    def create_character(self):
        print("Choose your class:\n1. Warrior\n2. Mage\n3. Rogue")
        choice = input("Enter the number of your choice: ")
        if choice == "1":
            return Warrior("Hero")
        elif choice == "2":
            return Mage("Hero")
        elif choice == "3":
            return Rogue("Hero")
        else:
            print("Invalid choice, defaulting to Warrior.")
            return Warrior("Hero")

    def play(self):
        print(f"Welcome to the RPG game, {self.player.name}!")
        while self.player.is_alive() and self.current_quest < len(self.quests):
            print(f"Current Quest: {self.quests[self.current_quest]}")
            action = input("Do you want to (A)ttack, (S)pecial Attack or (U)se Item? ").lower()
            if action == "a":
                self.battle(self.enemies[self.current_quest], "normal")
            elif action == "s":
                self.battle(self.enemies[self.current_quest], "special")
            elif action == "u":
                if self.player.inventory:
                    self.player.use_item(self.player.inventory[0])
                else:
                    print("No items in inventory.")
            else:
                print("Invalid action. Try again.")

        if self.player.is_alive():
            print("You have completed all the quests!")
        else:
            print("You have been defeated. Game Over.")

    def battle(self, enemy, attack_type):
        while self.player.is_alive() and enemy.is_alive():
            self.player.attack_enemy(enemy, attack_type)
            if enemy.is_alive():
                enemy.attack_enemy(self.player, random.choice(["normal", "special"]))

        if self.player.is_alive():
            print(f"You have defeated the {enemy.name}!")
            self.player.gain_experience(10)
            self.current_quest += 1
        else:
            print(f"You have been defeated by the {enemy.name}.")

if __name__ == "__main__":
    game = Game()
    game.play()
