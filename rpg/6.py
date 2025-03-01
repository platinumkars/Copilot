import random
import time

class Character:
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.level = 1
        self.exp = 0
        self.gold = 50
        self.inventory = {"Health Potion": 2, "Mana Potion": 2}
        self.weapons = {"Basic Sword": 8}
        self.current_weapon = "Basic Sword"
        self.abilities = {}
        self.status_effects = []
        self.armor = {"Basic Leather": 5}
        self.current_armor = "Basic Leather"
        
        # Initialize base abilities based on class
        self.update_abilities()
        
    def get_scaling_factor(self):
        """Calculate scaling factor based on level"""
        return 1 + (self.level - 1) * 0.15
        
    def update_abilities(self):
        """Update abilities based on level and class"""
        scaling = self.get_scaling_factor()
        
        if self.class_type.lower() in ["warrior", "1"]:
            self.health = 140 + (self.level - 1) * 25    # Increased health scaling
            self.max_health = self.health
            self.mana = 40 + (self.level - 1) * 8        # Reduced mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Rage": {"damage": int(25 * scaling), "mana_cost": 15, "description": "Strong attack with bonus damage"},
                "Shield Block": {"defense": int(15 * scaling), "duration": 2, "mana_cost": 10, "description": "Temporary defense boost"}
            }
            if self.level >= 3:
                base_abilities["Whirlwind"] = {"damage": int(18 * scaling), "hits": 3, "mana_cost": 25, "description": "Hit multiple times"}
            if self.level >= 5:
                base_abilities["Berserk"] = {"damage": int(40 * scaling), "mana_cost": 30, "description": "Powerful rage attack"}
                
        elif self.class_type.lower() in ["mage", "2"]:
            self.health = 80 + (self.level - 1) * 12     # Reduced health scaling
            self.max_health = self.health
            self.mana = 100 + (self.level - 1) * 20      # Increased mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Fireball": {"damage": int(20 * scaling), "duration": 3, "mana_cost": 15, "description": "Fire damage over time"},
                "Frost Bolt": {"damage": int(25 * scaling), "mana_cost": 20, "description": "Direct magic damage"}
            }
            if self.level >= 3:
                base_abilities["Lightning Strike"] = {"damage": int(35 * scaling), "mana_cost": 25, "description": "Powerful lightning attack"}
            if self.level >= 5:
                base_abilities["Meteor"] = {"damage": int(50 * scaling), "mana_cost": 40, "description": "Massive area damage"}

        elif self.class_type.lower() in ["paladin", "3"]:
            self.health = 120 + (self.level - 1) * 20    # Balanced health scaling
            self.max_health = self.health
            self.mana = 60 + (self.level - 1) * 12       # Balanced mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Holy Strike": {"damage": int(20 * scaling), "heal": int(10 * scaling), "mana_cost": 15, "description": "Holy damage with healing"},
                "Divine Shield": {"defense": int(20 * scaling), "duration": 3, "mana_cost": 20, "description": "Strong defensive barrier"}
            }
            if self.level >= 3:
                base_abilities["Consecration"] = {"damage": int(15 * scaling), "heal": int(15 * scaling), "mana_cost": 25, "description": "Area damage and healing"}
            if self.level >= 5:
                base_abilities["Divine Storm"] = {"damage": int(35 * scaling), "heal": int(20 * scaling), "mana_cost": 35, "description": "Powerful holy attack with healing"}

        elif self.class_type.lower() in ["necromancer", "4"]:
            self.health = 90 + (self.level - 1) * 15     # Low health scaling
            self.max_health = self.health
            self.mana = 90 + (self.level - 1) * 18       # High mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Death Bolt": {"damage": int(22 * scaling), "mana_cost": 15, "description": "Dark magic damage"},
                "Life Drain": {"damage": int(18 * scaling), "heal": int(15 * scaling), "mana_cost": 20, "description": "Drain life from enemy"}
            }
            if self.level >= 3:
                base_abilities["Curse"] = {"damage": int(12 * scaling), "duration": 4, "mana_cost": 25, "description": "Strong damage over time"}
            if self.level >= 5:
                base_abilities["Death Nova"] = {"damage": int(45 * scaling), "mana_cost": 40, "description": "Massive dark damage"}

        elif self.class_type.lower() in ["assassin", "5"]:
            self.health = 95 + (self.level - 1) * 14     # Medium-low health scaling
            self.max_health = self.health
            self.mana = 50 + (self.level - 1) * 10       # Medium mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Backstab": {"damage": int(30 * scaling), "mana_cost": 15, "description": "High damage from stealth"},
                "Poison Strike": {"damage": int(15 * scaling), "duration": 3, "mana_cost": 20, "description": "Poisoned weapon attack"}
            }
            if self.level >= 3:
                base_abilities["Shadow Step"] = {"damage": int(25 * scaling), "mana_cost": 25, "description": "Teleport behind enemy and strike"}
            if self.level >= 5:
                base_abilities["Death Mark"] = {"damage": int(45 * scaling), "duration": 2, "mana_cost": 35, "description": "Mark target for death"}

        elif self.class_type.lower() in ["druid", "6"]:
            self.health = 110 + (self.level - 1) * 18    # Medium-high health scaling
            self.max_health = self.health
            self.mana = 70 + (self.level - 1) * 15       # Medium-high mana scaling
            self.max_mana = self.mana
            base_abilities = {
                "Nature's Wrath": {"damage": int(20 * scaling), "mana_cost": 15, "description": "Nature damage"},
                "Regrowth": {"heal": int(25 * scaling), "duration": 3, "mana_cost": 20, "description": "Strong healing over time"}
            }
            if self.level >= 3:
                base_abilities["Entangling Roots"] = {"damage": int(18 * scaling), "duration": 2, "mana_cost": 25, "description": "Root and damage over time"}
            if self.level >= 5:
                base_abilities["Hurricane"] = {"damage": int(35 * scaling), "hits": 3, "mana_cost": 35, "description": "Multiple nature damage hits"}

        self.abilities = base_abilities

class Enemy:
    def __init__(self, name, health, damage, exp_reward, gold_reward):
        self.name = name
        self.health = health * 1.2  # Increase base health by 20%
        self.max_health = self.health
        self.damage = int(damage * 0.8)  # Reduce base damage by 20%
        self.exp_reward = exp_reward * 1.5  # Increase exp reward by 50%
        self.gold_reward = int(gold_reward * 1.2)  # Increase gold reward by 20%
        self.status_effects = []
        self.abilities = {}
        self.is_boss = False
        
    def is_alive(self):
        """Check if enemy is still alive"""
        return self.health > 0
        
    def take_damage(self, amount):
        """Handle damage taken by enemy"""
        self.health = max(0, self.health - amount)
        return amount

def print_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.03)
    print()

def combat(player, enemy):
    print_slow(f"\nA {enemy.name} appears!")
    
    while enemy.health > 0 and player.health > 0:
        # Process status effects at start of turn
        process_status_effects(player)
        process_status_effects(enemy)
        
        # Display battle status
        print_slow(f"\n{'-'*40}")
        print_slow(f"Your HP: {player.health}/{player.max_health}")
        print_slow(f"Your MP: {player.mana}/{player.max_mana}")
        print_slow(f"Enemy HP: {enemy.health}")
        
        # Show active effects
        if player.status_effects:
            print_slow("\nYour status effects:")
            for effect in player.status_effects:
                print_slow(f"- {effect['name']} ({effect['duration']} turns)")
        
        # Combat options
        print_slow("\nWhat would you like to do?")
        print_slow("1. Attack")
        print_slow("2. Use Ability")
        print_slow("3. Use Item")
        print_slow("4. Run")
        
        choice = input("> ")
        
        # Process turn
        if choice == "1":
            damage = process_attack(player, enemy)
            enemy.health -= damage
            print_slow(f"You deal {damage} damage to the {enemy.name}!")
            
        elif choice == "2":
            show_abilities(player)
            ability = input("Choose ability (or 'back'): ")
            if ability in player.abilities and player.mana >= player.abilities[ability]["mana_cost"]:
                process_ability(player, enemy, ability)
            else:
                print_slow("Not enough mana or invalid ability!")
                continue

        elif choice == "3":
            print_slow("\nAvailable items:")
            if player.inventory.get("Health Potion", 0) > 0:
                print_slow("1. Health Potion")
            if player.inventory.get("Mana Potion", 0) > 0:
                print_slow("2. Mana Potion")
            
            item_choice = input("Choose item to use (or 'back'): ")
            
            if item_choice == "1" and player.inventory.get("Health Potion", 0) > 0:
                player.health = min(player.max_health, player.health + 30)
                player.inventory["Health Potion"] -= 1
                print_slow("You drink a health potion and recover 30 HP!")
            elif item_choice == "2" and player.inventory.get("Mana Potion", 0) > 0:
                player.mana = min(player.max_mana, player.mana + 25)
                player.inventory["Mana Potion"] -= 1
                print_slow("You drink a mana potion and recover 25 MP!")
            elif item_choice.lower() == "back":
                continue
            else:
                print_slow("Invalid item or not enough potions!")
                continue
                
        elif choice == "4":
            if random.random() < 0.5:
                print_slow("You successfully fled from combat!")
                return "fled"  # Changed return value to indicate fled status
            else:
                print_slow("You failed to run away!")
        
        # In combat function, replace enemy attack section
        if enemy.health > 0:
            damage_taken = process_enemy_attack(player, enemy)
            player.health -= damage_taken
            print_slow(f"The {enemy.name} attacks you for {damage_taken} damage! (Reduced by armor)")
            
    if player.health <= 0:
        print_slow("You have been defeated...")
        return False
    
    print_slow(f"You defeated the {enemy.name}!")
    player.exp += enemy.exp_reward
    player.gold += enemy.gold_reward
    print_slow(f"You gained {enemy.exp_reward} EXP and {enemy.gold_reward} gold!")
    
    # Add post-battle healing based on level
    heal_amount = int(player.max_health * (0.15 + (player.level * 0.01)))  # 15% + 1% per level
    mana_restore = int(player.max_mana * (0.1 + (player.level * 0.01)))   # 10% + 1% per level
    player.health = min(player.max_health, player.health + heal_amount)
    player.mana = min(player.max_mana, player.mana + mana_restore)
    print_slow(f"Victory healing: Recovered {heal_amount} HP and {mana_restore} MP!")
    
    # In combat function, modify level up section
    if player.exp >= 100 * (1 + (player.level * 0.1)):  # Scaling exp requirement
        player.level += 1
        player.exp = 0
        health_increase = 20 + (player.level * 5)  # Scaling health increase
        mana_increase = 10 + (player.level * 3)    # Scaling mana increase
        player.max_health += health_increase
        player.health = player.max_health
        player.max_mana += mana_increase
        player.mana = player.max_mana
        print_slow(f"Level up! You are now level {player.level}!")
        print_slow(f"Max HP increased by {health_increase}!")
        print_slow(f"Max MP increased by {mana_increase}!")
    
    return True

# Update shop function's item handling
def shop(player):
    items = {
        # Potions
        "Health Potion": {"cost": 15, "effect": "Restore 40 HP"},
        "Mana Potion": {"cost": 20, "effect": "Restore 35 MP"},
        "Greater Health Potion": {"cost": 40, "effect": "Restore 80 HP"},
        "Greater Mana Potion": {"cost": 45, "effect": "Restore 70 MP"},
        
        # Basic Weapons
        "Iron Sword": {"cost": 80, "damage": 12},
        "Steel Sword": {"cost": 150, "damage": 20},
        "Magic Staff": {"cost": 120, "damage": 10, "mana_bonus": 25},
        
        # Advanced Weapons
        "Flame Sword": {"cost": 300, "damage": 35},
        "Frost Staff": {"cost": 280, "damage": 30, "mana_bonus": 40},
        "Shadow Dagger": {"cost": 250, "damage": 28},
        "Nature's Bow": {"cost": 270, "damage": 32},
        
        # Basic Armor
        "Leather Armor": {"cost": 100, "defense": 8},
        "Chain Mail": {"cost": 200, "defense": 15},
        
        # Advanced Armor
        "Plate Armor": {"cost": 400, "defense": 25},
        "Mage Robes": {"cost": 350, "defense": 12, "mana_bonus": 50},
        "Dragon Scale": {"cost": 500, "defense": 30}
    }
    
    while True:
        print_slow("\nWelcome to the shop!")
        print_slow(f"Your gold: {player.gold}")
        print_slow("\nAvailable items:")
        for item, details in items.items():
            desc = details.get('effect', 'Equipment')
            if 'damage' in details:
                desc = f"Damage: {details['damage']}"
            if 'defense' in details:
                desc = f"Defense: {details['defense']}"
            if 'mana_bonus' in details:
                desc += f", Mana Bonus: {details['mana_bonus']}"
            print_slow(f"{item}: {details['cost']} gold - {desc}")
        print_slow("\nEnter item name to buy (or 'exit' to leave):")
        
        choice = input("> ").title()
        if choice.lower() == "exit":
            break
        
        if choice in items:
            if player.gold >= items[choice]["cost"]:
                player.gold -= items[choice]["cost"]
                if "damage" in items[choice]:
                    player.weapons[choice] = items[choice]["damage"]
                elif "defense" in items[choice]:
                    player.armor[choice] = items[choice]["defense"]
                else:
                    player.inventory[choice] = player.inventory.get(choice, 0) + 1
                print_slow(f"Bought {choice}!")
            else:
                print_slow("Not enough gold!")
        else:
            print_slow("Invalid item!")

def show_abilities(player):
    """Display available abilities and their descriptions"""
    print_slow("\nAvailable Abilities:")
    for ability, details in player.abilities.items():
        print_slow(f"{ability}: {details['description']} (Mana cost: {details['mana_cost']})")

def process_attack(player, enemy):
    """Calculate attack damage based on player's current weapon and enemy's attack"""
    # Player attacking enemy
    base_damage = player.weapons[player.current_weapon]
    damage_variation = random.randint(-2, 2)
    return max(0, base_damage + damage_variation)

def process_enemy_attack(player, enemy):
    """Calculate damage taken by player considering armor"""
    base_damage = enemy.damage
    armor_reduction = int(player.armor[player.current_armor] * 0.5)  # Armor reduces damage by 50%
    final_damage = max(1, base_damage - armor_reduction)  # Minimum 1 damage
    return final_damage

def process_ability(player, enemy, ability_name):
    """Process the use of a special ability"""
    ability = player.abilities[ability_name]
    player.mana -= ability["mana_cost"]
    total_damage = 0
    
    if "damage" in ability:
        damage = ability["damage"]
        if "hits" in ability:  # For multi-hit abilities
            for hit in range(ability["hits"]):
                hit_damage = damage + random.randint(-2, 2)  # Add variation per hit
                enemy.health -= hit_damage
                total_damage += hit_damage
                print_slow(f"Hit {hit + 1}: {hit_damage} damage!")
            print_slow(f"Total damage: {total_damage}")
        else:
            damage = damage + random.randint(-5, 5)  # Add variation for single hit
            enemy.health -= damage
            print_slow(f"You use {ability_name} and deal {damage} damage!")
    
    if "heal" in ability:
        heal = ability["heal"]
        original_health = player.health
        player.health = min(player.max_health, player.health + heal)
        actual_heal = player.health - original_health
        print_slow(f"You heal for {actual_heal} HP!")
    
    if "defense" in ability:
        defense_boost = {
            "name": ability_name,
            "defense": ability["defense"],
            "duration": ability["duration"]
        }
        # Remove any existing defense boost
        player.status_effects = [effect for effect in player.status_effects 
                               if effect["name"] != ability_name]
        player.status_effects.append(defense_boost)
        print_slow(f"Gained {ability['defense']} defense for {ability['duration']} turns!")
    
    if "duration" in ability and "damage" in ability:  # For damage over time effects
        effect_name = ability_name.lower()
        # Remove existing effect of same type
        enemy.status_effects = [effect for effect in enemy.status_effects 
                              if effect["name"] != effect_name]
        enemy.status_effects.append({
            "name": effect_name,
            "damage": int(ability["damage"] / 2),  # DoT deals half damage per tick
            "duration": ability["duration"]
        })
        print_slow(f"Applied {effect_name} effect for {ability['duration']} turns!")

def process_status_effects(entity):
    """Process status effects at the start of turn"""
    for effect in entity.status_effects[:]:  # Create a copy to modify during iteration
        if effect["name"] == "Poison":
            damage = effect["damage"]
            entity.health -= damage
            print_slow(f"{entity.name} takes {damage} poison damage!")
        elif effect["name"] == "Regeneration":
            heal = effect["heal"]
            entity.health = min(entity.max_health, entity.health + heal)
            print_slow(f"{entity.name} regenerates {heal} health!")
            
        effect["duration"] -= 1
        if effect["duration"] <= 0:
            entity.status_effects.remove(effect)
            print_slow(f"{effect['name']} effect has worn off!")

# Update show_inventory_menu function
def show_inventory_menu(player):
    """Show inventory menu with weapon and armor switching options"""
    while True:
        print_slow("\n=== Inventory Menu ===")
        print_slow("1. View Items")
        print_slow("2. Change Weapon")
        print_slow("3. Change Armor")
        print_slow("4. Back")
        
        choice = input("> ")
        
        if choice == "1":
            print_slow("\nInventory:")
            for item, quantity in player.inventory.items():
                print_slow(f"{item}: {quantity}")
            print_slow("\nWeapons:")
            for weapon, damage in player.weapons.items():
                print_slow(f"{weapon} (Damage: {damage})")
            print_slow(f"Currently equipped weapon: {player.current_weapon}")
            print_slow("\nArmor:")
            for armor, defense in player.armor.items():
                print_slow(f"{armor} (Defense: {defense})")
            print_slow(f"Currently equipped armor: {player.current_armor}")
            
        elif choice == "2":
            print_slow("\nAvailable Weapons:")
            weapons = list(player.weapons.keys())
            for i, weapon in enumerate(weapons, 1):
                damage = player.weapons[weapon]
                print_slow(f"{i}. {weapon} (Damage: {damage})")
                if weapon == player.current_weapon:
                    print_slow("   *Currently Equipped*")
            
            try:
                weapon_choice = int(input("\nChoose weapon number (0 to cancel): "))
                if 0 < weapon_choice <= len(weapons):
                    new_weapon = weapons[weapon_choice - 1]
                    if new_weapon != player.current_weapon:
                        player.current_weapon = new_weapon
                        print_slow(f"Equipped {new_weapon}!")
                    else:
                        print_slow("That weapon is already equipped!")
                elif weapon_choice != 0:
                    print_slow("Invalid weapon number!")
            except ValueError:
                print_slow("Invalid input!")
                
        elif choice == "3":
            print_slow("\nAvailable Armor:")
            armors = list(player.armor.keys())
            for i, armor in enumerate(armors, 1):
                defense = player.armor[armor]
                print_slow(f"{i}. {armor} (Defense: {defense})")
                if armor == player.current_armor:
                    print_slow("   *Currently Equipped*")
            
            try:
                armor_choice = int(input("\nChoose armor number (0 to cancel): "))
                if 0 < armor_choice <= len(armors):
                    new_armor = armors[armor_choice - 1]
                    if new_armor != player.current_armor:
                        player.current_armor = new_armor
                        print_slow(f"Equipped {new_armor}!")
                    else:
                        print_slow("That armor is already equipped!")
                elif armor_choice != 0:
                    print_slow("Invalid armor number!")
            except ValueError:
                print_slow("Invalid input!")
                
        elif choice == "4":
            break

def main():
    print_slow("Welcome to the Text RPG!")
    name = input("Enter your character's name: ")
    class_type = input("Choose your class (Warrior, Mage, Paladin, Necromancer, Assassin, Druid ): ")
    player = Character(name, class_type)
    
    while True:
        print_slow(f"\n{player.name} - Level {player.level}")
        print_slow(f"HP: {player.health}/{player.max_health}")
        print_slow(f"Gold: {player.gold}")
        print_slow("\nWhat would you like to do?")
        print_slow("1. Fight monsters")
        print_slow("2. Visit shop")
        print_slow("3. Check inventory")
        print_slow("4. Quit")
        
        choice = input("> ")
        
        if choice == "1":
            enemies = []
            spawn_table = [
                (Enemy("Rat", 20, 3, 15, 10), 40),          # Weak enemy, high spawn rate
                (Enemy("Goblin", 35, 5, 25, 20), 30),       # Basic enemy
                (Enemy("Wolf", 45, 7, 35, 30), 15),         # Medium enemy
                (Enemy("Bandit", 60, 9, 45, 40), 10),       # Strong enemy
                (Enemy("Troll", 100, 12, 60, 50), 5),       # Mini-boss, rare spawn
            ]
            
            # Select enemy based on probability
            roll = random.uniform(0, 100)
            cumulative = 0
            for enemy, chance in spawn_table:
                cumulative += chance
                if roll <= cumulative:
                    enemies = [enemy]
                    break
            enemy = random.choice(enemies)
            
            result = combat(player, enemy)
            if result == "fled":
                continue  # Continue game loop if fled
            elif not result:
                break    # End game if defeated
                
        elif choice == "2":
            shop(player)
            
        elif choice == "3":
            show_inventory_menu(player)  # Replace the old inventory display
            
        elif choice == "4":
            print_slow("Thanks for playing!")
            break

if __name__ == "__main__":
    main()