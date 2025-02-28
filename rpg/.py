class Character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def attack_enemy(self, enemy):
        print(f"{self.name} attacks {enemy.name} for {self.attack} damage.")
        enemy.take_damage(self.attack)


class Game:
    def __init__(self):
        self.player = Character("Hero", 100, 20)
        self.enemy = Character("Goblin", 50, 10)

    def play(self):
        print("Welcome to the RPG game!")
        while self.player.is_alive() and self.enemy.is_alive():
            action = input("Do you want to (A)ttack or (H)eal? ").lower()
            if action == "a":
                self.player.attack_enemy(self.enemy)
            elif action == "h":
                self.player.hp += 10
                print(f"{self.player.name} heals for 10 HP. Total HP: {self.player.hp}")
            else:
                print("Invalid action. Try again.")

            if self.enemy.is_alive():
                self.enemy.attack_enemy(self.player)

        if self.player.is_alive():
            print("You have defeated the enemy!")
        else:
            print("You have been defeated by the enemy.")


if __name__ == "__main__":
    game = Game()
    game.play()
