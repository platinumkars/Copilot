import random

class Character:
    def __init__(self, name, hp, attack, defense, inventory=None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
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

class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def apply_effect(self, character):
        if self.effect['type'] == 'heal':
            character.hp += self.effect['value']
            print(f"{character.name} heals for {self.effect['value']} HP. Total HP: {character.hp}")

class Game:
    def __init__(self):
        self.player = Character("Hero", 100, 20, 5, [Item("Healing Potion", {'type': 'heal', 'value': 20})])
        self.enemy = Character("Goblin", 50, 15, 3)

    def play(self):
        print("Welcome to the RPG game!")
        while self.player.is_alive() and self.enemy.is_alive():
            action = input("Do you want to (A)ttack, (S)pecial Attack or (U)se Item? ").lower()
            if action == "a":
                self.player.attack_enemy(self.enemy, "normal")
            elif action == "s":
                self.player.attack_enemy(self.enemy, "special")
            elif action == "u":
                if self.player.inventory:
                    self.player.use_item(self.player.inventory[0])
                else:
                    print("No items in inventory.")
            else:
                print("Invalid action. Try again.")

            if self.enemy.is_alive():
                attack_type = random.choice(["normal", "special"])
                self.enemy.attack_enemy(self.player, attack_type)

        if self.player.is_alive():
            print("You have defeated the enemy!")
        else:
            print("You have been defeated by the enemy.")

if __name__ == "__main__":
    game = Game()
    game.play()
