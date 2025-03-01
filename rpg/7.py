import random
import time

class AmongUsGame:
    def __init__(self):
        self.players = ["Red", "Blue", "Green", "Yellow", "White", "Black"]
        self.impostor = random.choice(self.players)
        self.alive_players = self.players.copy()
        self.game_over = False

    def emergency_meeting(self):
        print("\n🚨 EMERGENCY MEETING! 🚨")
        print(f"Alive players: {', '.join(self.alive_players)}")
        vote = input("Who do you think is the impostor? ")
        
        if vote == self.impostor:
            print("Victory! You found the impostor!")
            self.game_over = True
        else:
            print("Wrong! The game continues...")
            self.alive_players.remove(random.choice([p for p in self.alive_players if p != self.impostor]))

    def sabotage(self):
        print("\n💥 SABOTAGE! 💥")
        victim = random.choice([p for p in self.alive_players if p != self.impostor])
        self.alive_players.remove(victim)
        print(f"{victim} was eliminated!")

    def play(self):
        print("Welcome to Text Among Us!")
        print("There is 1 impostor among us...")
        
        while not self.game_over and len(self.alive_players) > 2:
            time.sleep(1)
            action = input("\nWhat would you like to do? (1: Call meeting, 2: Wait): ")
            
            if action == "1":
                self.emergency_meeting()
            else:
                self.sabotage()
        
        if not self.game_over:
            print(f"\nGame Over! The impostor ({self.impostor}) won!")

if __name__ == "__main__":
    game = AmongUsGame()
    game.play()