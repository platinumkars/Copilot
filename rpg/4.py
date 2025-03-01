import random

class GameException(Exception):
    """Custom exception class for game-specific errors"""
    pass
# List of actions and descriptions
ACTIONS = {
    'normal': {'type': 'physical', 'power': 1.0, 'accuracy': 1.0},  # Add normal attack
    'slash': {'type': 'physical', 'power': 1.2, 'accuracy': 0.9},
    'fireball': {'type': 'magical', 'power': 1.5, 'accuracy': 0.8},
    'heal': {'type': 'support', 'power': 0.3, 'accuracy': 1.0},
    'dodge': {'type': 'defense', 'power': 0.5, 'accuracy': 0.7}
}

# Combat modifiers
COMBAT_MODIFIERS = {
    'critical': 1.5,
    'miss': 0,
    'normal': 1.0,
    'weather_bonus': 1.2,
    'terrain_penalty': 0.8
}

# Status effects
STATUS_EFFECTS = {
    'poison': {'damage': 5, 'duration': 3},
    'burn': {'damage': 8, 'duration': 2},
    'freeze': {'damage': 0, 'duration': 2},
    'stun': {'damage': 0, 'duration': 1}
}

# Environment conditions
ENVIRONMENT = {
    'day': {'attack': 1.1, 'defense': 1.0},
    'night': {'attack': 0.9, 'defense': 1.1},
    'rain': {'speed': 0.8, 'accuracy': 0.9},
    'sunny': {'speed': 1.2, 'accuracy': 1.1}
}
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
        self.status_effects = []
        self.environment = 'day'
        self.stamina = 100
        self.mana = 100
        self.accuracy = 1.0  # Add accuracy attribute

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage, damage_type="physical"):
        # Apply environment modifiers
        env_mod = ENVIRONMENT[self.environment]
        defense_modifier = env_mod.get('defense', 1.0)
        
        # Calculate actual damage with modifiers
        actual_damage = max((damage - self.defense * defense_modifier), 0)
        self.hp -= actual_damage
        return actual_damage

    def attack_enemy(self, enemy, attack_type="normal"):
        # Check if stunned
        if any(effect.get('name') == 'stun' for effect in self.status_effects):
            print(f"{self.name} is stunned and cannot attack!")
            return

        # Get attack action from ACTIONS dictionary
        if attack_type not in ACTIONS:
            print(f"Unknown attack type: {attack_type}")
            return

        action = ACTIONS[attack_type]
        
        # Apply environment modifiers
        env_mod = ENVIRONMENT[self.environment]
        attack_modifier = env_mod.get('attack', 1.0)
        accuracy_modifier = env_mod.get('accuracy', 1.0)

        # Calculate base damage
        base_damage = self.attack * action['power']
        
        # Apply critical hit chance (20%)
        if random.random() < 0.2:
            base_damage *= COMBAT_MODIFIERS['critical']
            print("Critical hit!")

        # Check for accuracy
        if random.random() > (action['accuracy'] * accuracy_modifier):
            print(f"{self.name}'s attack missed!")
            return

        # Apply final modifiers
        final_damage = base_damage * attack_modifier
        print(f"{self.name} attacks {enemy.name} with {attack_type} for {final_damage:.1f} damage!")
        enemy.take_damage(final_damage)

    def add_status_effect(self, effect_name):
        effect = STATUS_EFFECTS[effect_name].copy()
        effect['name'] = effect_name
        self.status_effects.append(effect)
        print(f"{self.name} is affected by {effect_name}!")

    def update_status_effects(self):
        for effect in self.status_effects[:]:  # Create a copy to iterate
            if effect['name'] in STATUS_EFFECTS:
                self.hp -= effect.get('damage', 0)
                effect['duration'] -= 1
                if effect['duration'] <= 0:
                    self.status_effects.remove(effect)
                    print(f"{effect['name']} wore off from {self.name}")

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
        self.stamina += 10
        self.mana += 10
        self.experience = 0
        print(f"{self.name} levels up! Now at level {self.level}.")

    def special_ability(self):
        pass

    def display_stats(self):
        print(f"""
{self.name} Stats:
HP: {self.hp}/{self.max_hp}
Attack: {self.attack}
Defense: {self.defense}
Level: {self.level}
Stamina: {self.stamina}
Mana: {self.mana}
Status Effects: {[effect['name'] for effect in self.status_effects]}
""")

# Specific Character Classes with special abilities and stats
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 120, 25, 10)
        self.rage = 50
        self.max_rage = 100
        self.special_moves = {
            'berserker': {'stamina_cost': 30, 'rage_required': 50},
            'shield_wall': {'stamina_cost': 20, 'rage_required': 30},
            'battle_cry': {'stamina_cost': 25, 'rage_required': 40}
        }

    def build_rage(self, amount):
        self.rage = min(self.max_rage, self.rage + amount)

    def special_ability(self, move_name):
        if move_name not in self.special_moves:
            print(f"Unknown move: {move_name}")
            return False

        move = self.special_moves[move_name]
        if self.stamina < move['stamina_cost']:
            print("Not enough stamina!")
            return False
        if self.rage < move['rage_required']:
            print("Not enough rage!")
            return False

        if move_name == 'berserker':
            self.attack *= 1.5
            self.defense *= 0.7
            print(f"{self.name} enters berserker rage!")
        elif move_name == 'shield_wall':
            self.defense *= 2
            print(f"{self.name} raises their shield wall!")
        elif move_name == 'battle_cry':
            self.attack *= 1.2
            self.defense *= 1.2
            print(f"{self.name} lets out a mighty battle cry!")

        self.stamina -= move['stamina_cost']
        self.rage -= move['rage_required']
        return True

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, 80, 35, 5)
        self.mana = 150  # Mages have more mana
        self.spellbook = {
            'fireball': {'mana_cost': 30, 'power': 1.8},
            'ice_bolt': {'mana_cost': 25, 'power': 1.5},
            'lightning': {'mana_cost': 40, 'power': 2.0}
        }

    def cast_spell(self, spell_name, target):
        if spell_name not in self.spellbook:
            print(f"Unknown spell: {spell_name}")
            return False

        spell = self.spellbook[spell_name]
        if self.mana < spell['mana_cost']:
            print("Not enough mana!")
            return False

        self.mana -= spell['mana_cost']
        damage = self.attack * spell['power']
        
        if spell_name == 'fireball':
            if random.random() < 0.3:
                target.add_status_effect('burn')
        elif spell_name == 'ice_bolt':
            if random.random() < 0.2:
                target.add_status_effect('freeze')
        elif spell_name == 'lightning':
            if random.random() < 0.25:
                target.add_status_effect('stun')

        target.take_damage(damage, "magical")
        print(f"{self.name} casts {spell_name} for {damage:.1f} damage!")
        return True

    def special_ability(self):
        if self.mana >= 50:
            self.mana -= 50
            self.attack *= 1.5
            print(f"{self.name} enters arcane concentration!")
            return True
        print("Not enough mana for special ability!")
        return False

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, 90, 30, 8)
        self.energy = 100
        self.max_energy = 100
        self.stealth = True
        self.abilities = {
            'backstab': {'energy_cost': 30, 'power': 2.0, 'requires_stealth': True},
            'poison_strike': {'energy_cost': 25, 'power': 1.5, 'poison_chance': 0.4},
            'vanish': {'energy_cost': 40, 'duration': 2},
            'swift_strike': {'energy_cost': 20, 'power': 1.3, 'hits': 2}
        }

    def attack_enemy(self, enemy, attack_type="normal"):
        if self.stealth and attack_type in self.abilities:
            damage_multiplier = 1.5
            print(f"{self.name} strikes from the shadows!")
            self.stealth = False
        else:
            damage_multiplier = 1.0
        
        if attack_type in self.abilities:
            ability = self.abilities[attack_type]
            if self.energy < ability['energy_cost']:
                print("Not enough energy!")
                return False
            if ability.get('requires_stealth', False) and not self.stealth:
                print("This ability requires stealth!")
                return False
            
            self.energy -= ability['energy_cost']
            
            if attack_type == 'swift_strike':
                for _ in range(ability['hits']):
                    super().attack_enemy(enemy, "slash")
            else:
                base_damage = self.attack * ability['power'] * damage_multiplier
                enemy.take_damage(base_damage)
                
                if attack_type == 'poison_strike' and random.random() < ability['poison_chance']:
                    enemy.add_status_effect('poison')
        else:
            super().attack_enemy(enemy, attack_type)

    def special_ability(self, ability_name='vanish'):
        if ability_name == 'vanish' and self.energy >= self.abilities['vanish']['energy_cost']:
            self.energy -= self.abilities['vanish']['energy_cost']
            self.stealth = True
            print(f"{self.name} vanishes into the shadows!")
            return True
        return False

    def update_status_effects(self):
        super().update_status_effects()
        self.energy = min(self.max_energy, self.energy + 10)  # Energy regeneration

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, hp=85, attack=28, defense=7)
        self.focus = 100
        self.max_focus = 100
        self.arrow_types = {
            'poison_arrow': {'focus_cost': 20, 'damage': 1.3, 'effect': 'poison'},
            'piercing_arrow': {'focus_cost': 30, 'damage': 1.8, 'penetration': True},
            'rapid_shot': {'focus_cost': 25, 'damage': 0.7, 'shots': 3},
            'frost_arrow': {'focus_cost': 35, 'damage': 1.4, 'effect': 'freeze'}
        }

    def attack_enemy(self, enemy, attack_type="normal"):
        if attack_type in self.arrow_types:
            arrow = self.arrow_types[attack_type]
            if self.focus < arrow['focus_cost']:
                print("Not enough focus!")
                return False

            self.focus -= arrow['focus_cost']
            
            if attack_type == 'rapid_shot':
                for _ in range(arrow['shots']):
                    damage = self.attack * arrow['damage']
                    enemy.take_damage(damage)
                    print(f"{self.name} fires a quick shot for {damage:.1f} damage!")
            else:
                damage = self.attack * arrow['damage']
                if arrow.get('penetration', False):
                    damage *= 2 if enemy.defense > 10 else 1.5
                enemy.take_damage(damage)
                
                if 'effect' in arrow:
                    if random.random() < 0.3:
                        enemy.add_status_effect(arrow['effect'])
                return True
        return super().attack_enemy(enemy, attack_type)

# Item Classes
class Item:
    def __init__(self, name, effects, rarity="common", durability=1):
        self.name = name
        self.effects = effects
        self.rarity = rarity
        self.durability = durability
        self.rarity_multipliers = {
            "common": 1.0,
            "rare": 1.5,
            "epic": 2.0,
            "legendary": 3.0
        }

    def apply_effect(self, character):
        multiplier = self.rarity_multipliers.get(self.rarity, 1.0)
        
        for effect_type, value in self.effects.items():
            if effect_type == 'heal':
                heal_amount = int(value * multiplier)
                character.hp = min(character.max_hp, character.hp + heal_amount)
                print(f"{character.name} heals for {heal_amount} HP. Total HP: {character.hp}")
            
            elif effect_type == 'buff':
                for stat, mod in value.items():
                    if stat == 'attack':
                        character.attack *= (1 + mod * multiplier)
                    elif stat == 'defense':
                        character.defense *= (1 + mod * multiplier)
                print(f"{character.name} gains {self.rarity} buff to {list(value.keys())}")
            
            elif effect_type == 'restore':
                if 'stamina' in value:
                    character.stamina = min(100, character.stamina + value['stamina'])
                if 'mana' in value:
                    character.mana = min(100, character.mana + value['mana'])
                print(f"{character.name} restores {value}")
            
            elif effect_type == 'status_cure':
                character.status_effects = [effect for effect in character.status_effects 
                                         if effect['name'] not in value]
                print(f"{character.name} is cured of {value}")

        self.durability -= 1
        if self.durability <= 0:
            print(f"{self.name} breaks after use!")

class HealingPotion(Item):
    def __init__(self, rarity="common"):
        effects = {
            'heal': 20,
            'buff': {'defense': 0.1},
            'restore': {'stamina': 15, 'mana': 15},
            'status_cure': ['poison', 'burn']
        }
        durability = {
            'common': 1,
            'rare': 2,
            'epic': 3,
            'legendary': 5
        }
        super().__init__(
            f"{rarity.capitalize()} Healing Potion",
            effects,
            rarity=rarity,
            durability=durability.get(rarity, 1)
        )

class SuperHealingPotion(Item):
    def __init__(self, rarity="rare"):
        effects = {
            'heal': 50,  # More healing than regular potion
            'buff': {
                'attack': 0.15,
                'defense': 0.15
            },
            'restore': {
                'stamina': 30,
                'mana': 30
            },
            'status_cure': ['poison', 'burn', 'freeze', 'stun']  # Cures all status effects
        }
        durability = {
            'rare': 2,
            'epic': 4,
            'legendary': 6
        }
        super().__init__(
            f"{rarity.capitalize()} Super Healing Potion",
            effects,
            rarity=rarity,
            durability=durability.get(rarity, 2)
        )

# Enemy Classes
class Goblin(Character):
    def __init__(self):
        super().__init__("Goblin", 60, 15, 5)
        self.agility = 20
        self.pack_bonus = False

    def special_ability(self):
        if not self.pack_bonus and self.hp < self.max_hp * 0.5:
            print("Goblin calls for pack support!")
            self.attack *= 1.3
            self.defense *= 1.2
            self.pack_bonus = True
            return True
        return False

class Orc(Character):
    def __init__(self):
        super().__init__("Orc", 80, 20, 10)
        self.rage = 0
        self.berserk_mode = False

    def take_damage(self, damage, damage_type="physical"):
        actual_damage = super().take_damage(damage, damage_type)
        self.rage += int(actual_damage * 0.5)
        return actual_damage

    def special_ability(self):
        if self.rage >= 30 and not self.berserk_mode:
            print("Orc enters berserk mode!")
            self.attack *= 1.5
            self.defense *= 0.7
            self.berserk_mode = True
            self.rage = 0
            return True
        return False

class Dragon(Character):
    def __init__(self):
        super().__init__("Dragon", 200, 40, 20)
        self.breath_cooldown = 0
        self.flying = False
        self.elemental_mode = "fire"

    def special_ability(self):
        if self.breath_cooldown == 0:
            print(f"Dragon uses {self.elemental_mode} breath attack!")
            self.breath_cooldown = 3
            self.attack *= 2
            if random.random() < 0.4:
                return "burn"
        elif not self.flying and random.random() < 0.3:
            print("Dragon takes to the sky!")
            self.flying = True
            self.defense *= 1.5
        return False

    def update_status_effects(self):
        super().update_status_effects()
        if self.breath_cooldown > 0:
            self.breath_cooldown -= 1

class Bandit(Character):
    def __init__(self):
        super().__init__("Bandit", 70, 18, 8)
        self.stealth = False
        self.stolen_items = []
        self.combo_counter = 0

    def special_ability(self):
        if not self.stealth and random.random() < 0.3:
            print("Bandit disappears into the shadows!")
            self.stealth = True
            return True
        elif self.combo_counter >= 2:
            print("Bandit unleashes devastating combo attack!")
            self.attack *= (1.2 + (self.combo_counter * 0.1))
            self.combo_counter = 0
            return True
        return False

    def attack_enemy(self, enemy, attack_type="normal"):
        if self.stealth:
            self.attack *= 1.5
            self.stealth = False
        super().attack_enemy(enemy, attack_type)
        self.combo_counter += 1

# Extending Game Class
class Game:
    def __init__(self):
        self.initialize_game_systems()
        self.player = None  # Initialize player before character creation
        self.current_quest = 0
        self.gold = 100
        self.turns = 0
        self.time_of_day = 'day'
        self.player = self.create_character()  # Create character after systems init

    def upgrade_to_extended(self):
        """Upgrade basic game to extended version"""
        extended_game = ExtendedGame()
        # Transfer basic game data to extended game
        extended_game.player = self.player
        extended_game.gold = self.gold
        extended_game.current_quest = self.current_quest
        extended_game.turns = self.turns
        extended_game.time_of_day = self.time_of_day
        return extended_game

    def save_game_state(self):
        """Save the current game state"""
        try:
            # For now, just print a message
            print("Game state saved!")
        except Exception as e:
            print(f"Failed to save game state: {e}")

    def initialize_game_systems(self):
        """Initialize all game systems"""
        self.settings = {
            'difficulty': 'normal',
            'permadeath': False,
            'show_tutorials': True,
            'auto_save': True
        }
        self.active_buffs = []
        self.quest_log = []
        self.achievement_tracker = {}
        self.quests = [
            {
                "name": "The First Trial",
                "enemy": Goblin(),
                "required_level": 1,
                "reward": 50,
                "environment": "day"
            }
        ]
        self.current_location = "Starting Village"
        self.turns = 0
        self.time_of_day = 'day'
        self.gold = 100
        self.shop_items = [
            HealingPotion("common"),
            HealingPotion("rare"),
            SuperHealingPotion("rare")
        ]
        self.item_prices = {
            "common": 50,
            "rare": 100,
            "epic": 200,
            "legendary": 500
        }
        
    def create_character(self):
        print("Choose your class:")
        print("1. Warrior - High HP and defense")
        print("2. Mage - Powerful spells")
        print("3. Rogue - Stealth and critical strikes")
        print("4. Archer - Ranged attacks")
        
        while True:
            try:
                choice = input("Enter the number of your choice (1-4): ")
                name = input("Enter your character's name: ")
                
                if choice == "1":
                    self.player = Warrior(name)
                    return self.player
                elif choice == "2":
                    self.player = Mage(name)
                    return self.player
                elif choice == "3":
                    self.player = Rogue(name)
                    return self.player
                elif choice == "4":
                    self.player = Archer(name)
                    return self.player
                else:
                    print("Invalid choice, please try again.")
            except Exception as e:
                print(f"Error creating character: {e}")

    def play(self):
        try:
            print(f"Welcome to the RPG game, {self.player.name}!")
            while self.player.is_alive() and self.current_quest < len(self.quests):
                try:
                    self.update_game_state()
                    self.show_status()
                    choice = self.get_player_choice()
                    if choice == "upgrade":
                        return self.upgrade_to_extended()
                    self.process_player_choice(choice)
                except GameException as e:
                    print(f"Game error: {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    if input("Continue playing? (y/n): ").lower() != 'y':
                        break
        finally:
            self.save_game_state()

    def update_game_state(self):
        """Update basic game state"""
        self.turns += 1
        if self.turns % 5 == 0:
            self.time_of_day = random.choice(list(ENVIRONMENT.keys()))
            print(f"\nEnvironment changed to: {self.time_of_day}")
            self.player.environment = self.time_of_day
        
        self.player.update_status_effects()

    def show_status(self):
        """Display basic game status"""
        print(f"\n{'='*50}")
        print(f"Time of Day: {self.time_of_day}")
        print(f"Gold: {self.gold}")
        self.player.display_stats()
        print(f"{'='*50}")

    def show_quest(self):
        quest = self.quests[self.current_quest]
        if self.player.level < quest["required_level"]:
            print(f"WARNING: This quest requires level {quest['required_level']}!")
        print(f"\nCurrent Quest: {quest['name']}")
        print(f"Recommended Environment: {quest['environment']}")
        print(f"Reward: {quest['reward']} EXP + {quest['reward'] * 10} Gold")
        print(f"Enemy: {quest['enemy'].name} (HP: {quest['enemy'].hp}/{quest['enemy'].max_hp})")

    def battle(self, enemy, attack_type):
        """Handle the battle between player and enemy"""
        if self.player.level < self.quests[self.current_quest]["required_level"]:
            print("Warning: You are underleveled for this quest!")
        
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
            # Display battle status
            print(f"\n{self.player.name} HP: {self.player.hp}/{self.player.max_hp}")
            print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
            
            # Player's turn
            print("\nYour turn!")
            if attack_type == "special":
                if isinstance(self.player, Mage):
                    spell = input("Choose spell (fireball/ice_bolt/lightning): ")
                    self.player.cast_spell(spell, enemy)
                elif isinstance(self.player, Warrior):
                    move = input("Choose move (berserker/shield_wall/battle_cry): ")
                    self.player.special_ability(move)
                elif isinstance(self.player, Archer):
                    arrow = input("Choose arrow type (poison_arrow/piercing_arrow/rapid_shot/frost_arrow): ")
                    self.player.attack_enemy(enemy, arrow)
                elif isinstance(self.player, Rogue):
                    ability = input("Choose ability (backstab/poison_strike/swift_strike): ")
                    self.player.attack_enemy(enemy, ability)
            else:
                # Use the normal attack from ACTIONS
                self.player.attack_enemy(enemy, "normal")
            
            # Enemy's turn
            if enemy.is_alive():
                print(f"\n{enemy.name}'s turn!")
                enemy.attack_enemy(self.player, "normal")  # Enemy uses normal attack
            
            # Update status effects
            self.player.update_status_effects()
            enemy.update_status_effects()
        
        # Battle conclusion
        if self.player.is_alive():
            quest_reward = self.quests[self.current_quest]["reward"]
            gold_reward = quest_reward * 10
            
            # Environment bonus
            if self.time_of_day == self.quests[self.current_quest]["environment"]:
                quest_reward = int(quest_reward * 1.5)
                gold_reward = int(gold_reward * 1.5)
                print("\nEnvironment bonus applied!")
            
            print(f"\nVictory! You defeated the {enemy.name}!")
            print(f"Earned {quest_reward} EXP and {gold_reward} Gold!")
            self.player.gain_experience(quest_reward)
            self.gold += gold_reward
            self.current_quest += 1
        else:
            print(f"\nDefeat! You were slain by the {enemy.name}.")

    def visit_shop(self):
        while True:
            print(f"\nWelcome to the shop! Your gold: {self.gold}")
            print("\nAvailable items:")
            for index, item in enumerate(self.shop_items):
                price = self.item_prices[item.rarity]
                print(f"{index + 1}. {item.name} - {price} gold")
            
            choice = input("\nEnter item number to buy or 'q' to quit: ")
            if choice.lower() == 'q':
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(self.shop_items):
                    item = self.shop_items[index]
                    price = self.item_prices[item.rarity]
                    
                    if self.gold >= price:
                        self.gold -= price
                        self.player.inventory.append(item)
                        print(f"\nBought {item.name} for {price} gold!")
                    else:
                        print("\nNot enough gold!")
                else:
                    print("\nInvalid item number!")
            except ValueError:
                print("\nInvalid input!")

    def use_inventory_item(self):
        if not self.player.inventory:
            print("\nNo items in inventory!")
            return
        
        print("\nInventory:")
        for index, item in enumerate(self.player.inventory):  # Use enumerate instead
            print(f"{index + 1}. {item.name}")
        
        try:
            choice = int(input("\nEnter item number to use or 0 to cancel: ")) - 1
            if 0 <= choice < len(self.player.inventory):
                self.player.use_item(self.player.inventory[choice])
        except ValueError:
            print("\nInvalid input!")

    def rest(self):
        heal_amount = self.player.max_hp * 0.3
        self.player.hp = min(self.player.max_hp, self.player.hp + heal_amount)
        self.player.stamina = min(100, self.player.stamina + 30)
        self.player.mana = min(100, self.player.mana + 30)
        print(f"\n{self.player.name} rests and recovers some HP, stamina, and mana.")
        self.turns += 2  # Resting takes time

    def show_inventory(self):
        if not self.player.inventory:
            print("\nInventory is empty!")
            return
        
        print("\nInventory:")
        for item in self.player.inventory:
            print(f"- {item.name} ({item.rarity})")

    def get_player_choice(self):
        """Get the player's choice of action"""
        print("\nActions:")
        print("1. Normal Attack")
        print("2. Special Attack")
        print("3. Use Item")
        print("4. Show Status")
        print("5. Upgrade to Extended Game")  # Add upgrade option
        print("6. Quit")
        return input("Choose your action (1-6): ")

    def process_player_choice(self, choice):
        """Process the player's choice"""
        if choice == "1":
            self.battle(self.quests[self.current_quest]["enemy"], "normal")
        elif choice == "2":
            self.battle(self.quests[self.current_quest]["enemy"], "special")
        elif choice == "3":
            self.use_inventory_item()
        elif choice == "4":
            self.show_status()
        elif choice == "5":
            return "upgrade"  # Signal to upgrade
        elif choice == "6":
            raise GameException("Player quit")
        else:
            print("Invalid choice!")

    def confirm_exit(self):
        """Confirm if player wants to exit"""
        return input("\nAre you sure you want to exit? (y/n): ").lower() == 'y'

    def handle_critical_error(self, error):
        """Handle critical game errors"""
        print(f"\nCritical Error: {error}")
        try:
            self.save_game_state()
            print("Game state saved successfully")
            return True
        except Exception as e:
            print(f"Failed to save game state: {e}")
            return False

class ExtendedGame(Game):
    def __init__(self):
        super().__init__()  # Call parent class init first
        self.initialize_extended_systems()
        self.current_weather = 'clear'
        self.faction_relations = {
            'village': 0,
            'guild': 0,
            'kingdom': 0
        }

    def play(self):
        """Main game loop for extended game"""
        try:
            print(f"\n{'='*60}")
            print(f"Welcome to the Enhanced RPG Game, {self.player.name}!")
            print(f"Current Location: {self.current_location}")
            print(f"{'='*60}\n")

            while self.player.is_alive():
                try:
                    self.update_game_state()
                    self.process_world_events()
                    self.check_environmental_hazards()
                    self.update_faction_relations()
                    self.show_enhanced_status()
                    
                    choice = self.get_extended_player_choice()
                    if choice == 'x':
                        if self.confirm_exit():
                            break
                    else:
                        self.process_extended_choice(choice)
                    
                    if self.settings.get('auto_save', True):
                        self.save_game_state()
                        
                except GameException as e:
                    print(f"Game error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    if not self.recover_game_state():
                        break
        finally:
            self.cleanup_game_resources()
            self.show_final_statistics()

    def generate_random_event(self):
        """Generate a random world event"""
        events = [
            {'type': 'combat', 'description': 'Ambush!', 'enemy': Bandit()},
            {'type': 'treasure', 'description': 'Found a chest!', 'gold': 50},
            {'type': 'weather', 'description': 'Storm approaching!', 'effect': 'storm'}
        ]
        return random.choice(events)

    def handle_world_event(self, event):
        """Handle a world event"""
        print(f"\nWorld Event: {event['description']}")
        if event['type'] == 'combat':
            self.enhanced_battle(event['enemy'], "normal")
        elif event['type'] == 'treasure':
            self.gold += event['gold']
            print(f"Found {event['gold']} gold!")
        elif event['type'] == 'weather':
            self.current_weather = event['effect']
            print(f"Weather changed to {event['effect']}!")

    def initialize_extended_systems(self):
        """Initialize extended game specific systems"""
        self.current_weather = 'clear'
        self.weather_duration = 0
        self.reputation = {
            'village': {'value': 0, 'title': 'Stranger'},
            'guild': {'value': 0, 'title': 'Initiate'},
            'kingdom': {'value': 0, 'title': 'Unknown'}
        }
        self.combat_combo = 0
        self.max_combo = 5
        self.combo_multiplier = 0.1
        self.materials = {'wood': 0, 'iron': 0, 'crystal': 0, 'herb': 0}
        self.initialize_crafting()

if __name__ == "__main__":
    try:
        game = Game()
        while True:
            if isinstance(game, Game) and not isinstance(game, ExtendedGame):
                result = game.play()
                if result == "upgrade":
                    game = game.upgrade_to_extended()
                    continue
                break
            elif isinstance(game, ExtendedGame):
                game.play()
                break
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if hasattr(game, 'save_game_state'):
            game.save_game_state()
        print("\nThanks for playing!")

# Additional Quests and Dialogue
def show_dialogue(text):
    print("\n" + text + "\n")

class SideQuest:
    def __init__(self, name, description, requirements=None):
        self.name = name
        self.description = description
        self.requirements = requirements or {}
        self.progress = 0
        self.stages = []
        self.rewards = {
            'exp': 0,
            'gold': 0,
            'items': [],
            'stats': {}
        }
        self.completed = False
        self.failed = False
        self.time_limit = None

    def add_stage(self, description, objective_count=1, special_condition=None):
        self.stages.append({
            'description': description,
            'required': objective_count,
            'current': 0,
            'completed': False,
            'special_condition': special_condition
        })

    def set_rewards(self, exp=0, gold=0, items=None, stats=None):
        self.rewards['exp'] = exp
        self.rewards['gold'] = gold
        self.rewards['items'] = items or []
        self.rewards['stats'] = stats or {}

    def update_progress(self, stage_index, amount=1, condition_met=False):
        if stage_index < len(self.stages):
            stage = self.stages[stage_index]
            if stage['special_condition'] and not condition_met:
                return False
            
            stage['current'] = min(stage['current'] + amount, stage['required'])
            if stage['current'] >= stage['required']:
                stage['completed'] = True
                print(f"Stage completed: {stage['description']}")
                
            self.check_completion()
            return True
        return False

    def check_completion(self):
        if all(stage['completed'] for stage in self.stages):
            self.completed = True
            return True
        return False

    def complete_quest(self, player):
        if not self.check_requirements(player):
            print("Requirements not met to complete quest!")
            return False

        if not self.completed:
            print("Quest not yet completed!")
            return False

        # Apply rewards
        player.gain_experience(self.rewards['exp'])
        player.gold += self.rewards['gold']
        
        for item in self.rewards['items']:
            player.inventory.append(item)
            print(f"Received item: {item.name}")

        for stat, value in self.rewards['stats'].items():
            if hasattr(player, stat):
                current_value = getattr(player, stat)
                setattr(player, stat, current_value + value)
                print(f"{stat.capitalize()} increased by {value}")

        print(f"Quest '{self.name}' completed!")
        print(f"Rewards: {self.rewards['exp']} EXP, {self.rewards['gold']} Gold")
        return True

    def check_requirements(self, player):
        if 'level' in self.requirements and player.level < self.requirements['level']:
            return False
        if 'items' in self.requirements:
            for item in self.requirements['items']:
                if item not in player.inventory:
                    return False
        if 'stats' in self.requirements:
            for stat, value in self.requirements['stats'].items():
                if getattr(player, stat, 0) < value:
                    return False
        return True

    def fail_quest(self):
        self.failed = True
        print(f"Quest '{self.name}' failed!")



        # Game cleanup and final stats
        self.cleanup_game_resources()
        self.show_final_statistics()
        self.save_player_achievements()
        print("\nThanks for playing! Your legend will be remembered.")
        self.initialize_game_systems()

