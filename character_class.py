import json
import os
import random
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from table_character_generator import CharacterGenerator, Character as BaseCharacter

@dataclass
class Character:
    """Character class for RPG game"""
    name: str = ""
    symbol: str = "🤖"  # Default emoji
    max_hp: int = 6
    current_hp: int = field(init=False)
    cash: int = 0
    player_control: bool = False  # Default to computer controlled
    is_living: bool = True
    inventory: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    archetype: str = ""
    background: str = ""
    physical_description: str = ""
    condition: str = ""  # Temporary status like prone, sleeping, poisoned
    goals: str = ""
    contextualized: bool = False  # Flag for if character has been set into a story
    
    def __post_init__(self):
        """Initialize current_hp to max_hp after object creation"""
        if not hasattr(self, 'current_hp') or self.current_hp == 0:
            self.current_hp = self.max_hp
    
    # Getter methods
    def get_name(self) -> str:
        return self.name
    
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_max_hp(self) -> int:
        return self.max_hp
    
    def get_current_hp(self) -> int:
        return self.current_hp
    
    def get_cash(self) -> int:
        return self.cash
    
    def get_player_control(self) -> bool:
        return self.player_control
    
    def get_is_living(self) -> bool:
        return self.is_living
    
    def get_inventory(self) -> List[str]:
        return self.inventory.copy()
    
    def get_skills(self) -> List[str]:
        return self.skills.copy()
    
    def get_archetype(self) -> str:
        return self.archetype
    
    def get_background(self) -> str:
        return self.background
    
    def get_physical_description(self) -> str:
        return self.physical_description
    
    def get_condition(self) -> str:
        return self.condition
    
    def get_goals(self) -> str:
        return self.goals
    
    def get_contextualized(self) -> bool:
        return self.contextualized
    
    # Setter methods
    def set_name(self, name: str):
        self.name = name
    
    def set_symbol(self, symbol: str):
        self.symbol = symbol
    
    def set_max_hp(self, max_hp: int):
        self.max_hp = max_hp
        # Adjust current hp if it exceeds new max
        if self.current_hp > max_hp:
            self.current_hp = max_hp
    
    def set_current_hp(self, current_hp: int):
        self.current_hp = max(0, min(current_hp, self.max_hp))
        if self.current_hp <= 0:
            self.is_living = False
    
    def set_cash(self, cash: int):
        self.cash = max(0, cash)
    
    def set_player_control(self, player_control: bool):
        self.player_control = player_control
    
    def set_is_living(self, is_living: bool):
        self.is_living = is_living
    
    def set_inventory(self, inventory: List[str]):
        self.inventory = inventory
    
    def set_skills(self, skills: List[str]):
        self.skills = skills
    
    def set_archetype(self, archetype: str):
        self.archetype = archetype
    
    def set_background(self, background: str):
        self.background = background
    
    def set_physical_description(self, physical_description: str):
        self.physical_description = physical_description
    
    def set_condition(self, condition: str):
        self.condition = condition
    
    def set_goals(self, goals: str):
        self.goals = goals
    
    def set_contextualized(self, contextualized: bool):
        self.contextualized = contextualized
    
    def __str__(self):
        return self.generate_character_sheet()
    
    def generate_character_sheet(self) -> str:
        """Generate a formatted character sheet"""
        hp_bar = "█" * self.current_hp + "░" * (self.max_hp - self.current_hp)
        
        sheet = f"""
{self.symbol} CHARACTER SHEET {self.symbol}
═══════════════════════════════════════════

NAME: {self.name or 'Unknown'}
ARCHETYPE: {self.archetype or 'Unspecified'}

VITAL STATS
• HP: [{hp_bar}] {self.current_hp}/{self.max_hp}
• Cash: ¥{self.cash:,}
• Condition: {self.condition or 'Normal'}

BACKGROUND
{self.background or 'No background information available.'}

PHYSICAL DESCRIPTION
{self.physical_description or 'No physical description available.'}

GOALS
{self.goals or 'No specific goals defined.'}

INVENTORY [{len(self.inventory)} items]
{chr(10).join(f'• {item}' for item in self.inventory) if self.inventory else '• Empty'}

SKILLS [{len(self.skills)} skills]
{chr(10).join(f'• {skill}' for skill in self.skills) if self.skills else '• None learned'}
        """
        return sheet.strip()
    
    def take_damage(self, damage: int) -> bool:
        """Apply damage to character, returns True if character dies"""
        self.current_hp = max(0, self.current_hp - damage)
        if self.current_hp <= 0:
            self.is_living = False
            return True
        return False
    
    def heal(self, amount: int) -> int:
        """Heal character, returns actual amount healed"""
        if not self.is_living:
            return 0
        
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp
    
    def add_item(self, item: str):
        """Add item to inventory"""
        self.inventory.append(item)
    
    def remove_item(self, item: str) -> bool:
        """Remove item from inventory, returns True if successful"""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def learn_skill(self, skill: str):
        """Add skill if not already known"""
        if skill not in self.skills:
            self.skills.append(skill)
    
    def set_condition(self, condition: str):
        """Set temporary condition"""
        self.condition = condition
    
    def clear_condition(self):
        """Clear temporary condition"""
        self.condition = ""

class CharacterManager:
    """Manager class for handling character operations"""
    
    def __init__(self):
        self.generator = CharacterGenerator()
        self.rendered_folder = "rendered_character"
        self.ensure_folder_exists()
        
        # Character symbols
        self.character_symbols = [
            "🤖", "💾", "🔌", "⚡", "🖥️", "📡", "🎭", "💀", "⚔️", "🔮",
            "💊", "🚁", "🌃", "🔥", "❄️", "⭐", "💰", "🎯", "🗲", "🔊"
        ]
    
    def ensure_folder_exists(self):
        """Create rendered_character folder if it doesn't exist"""
        if not os.path.exists(self.rendered_folder):
            os.makedirs(self.rendered_folder)
    
    def generate_character_with_background(self, name: str = "", **kwargs) -> Character:
        """Generate a character using the table generator for background"""
        # Generate base character for background information
        base_char = self.generator.generate_character()
        
        # Create character
        character = Character(
            name=name or f"Unknown_{random.randint(1000, 9999)}",
            symbol=random.choice(self.character_symbols),
            archetype=kwargs.get('archetype', base_char.archetype),
            background=base_char.generate_description(),
            **{k: v for k, v in kwargs.items() if k != 'archetype'}
        )
        
        return character
    
    def create_player_character(self, name: str, archetype: str = "", **kwargs) -> Character:
        """Create a player-controlled character"""
        return self.generate_character_with_background(
            name=name,
            player_control=True,
            archetype=archetype,
            **kwargs
        )
    
    def create_npc(self, name: str = "", archetype: str = "", **kwargs) -> Character:
        """Create an NPC (computer-controlled character)"""
        return self.generate_character_with_background(
            name=name,
            player_control=False,
            archetype=archetype,
            **kwargs
        )
    
    def export_character(self, character: Character, filename: str = None) -> str:
        """Export character to JSON file in rendered_character folder"""
        if filename is None:
            filename = f"{character.name.replace(' ', '_').lower()}.json"
        
        filepath = os.path.join(self.rendered_folder, filename)
        
        # Convert character to dictionary
        char_dict = {
            'name': character.name,
            'symbol': character.symbol,
            'max_hp': character.max_hp,
            'current_hp': character.current_hp,
            'cash': character.cash,
            'player_control': character.player_control,
            'is_living': character.is_living,
            'inventory': character.inventory,
            'skills': character.skills,
            'archetype': character.archetype,
            'background': character.background,
            'physical_description': character.physical_description,
            'condition': character.condition,
            'goals': character.goals,
            'contextualized': character.contextualized
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(char_dict, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_character(self, filename: str) -> Character:
        """Load character from JSON file in rendered_character folder"""
        filepath = os.path.join(self.rendered_folder, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Character file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            char_dict = json.load(f)
        
        # Handle current_hp separately since it's init=False
        current_hp = char_dict.pop('current_hp', None)
        
        # Create character object from dictionary
        character = Character(**char_dict)
        
        # Set current_hp after initialization
        if current_hp is not None:
            character.current_hp = current_hp
            
        return character
    
    def list_saved_characters(self) -> List[str]:
        """List all saved character files"""
        if not os.path.exists(self.rendered_folder):
            return []
        
        return [f for f in os.listdir(self.rendered_folder) if f.endswith('.json')]
    
    def delete_character(self, filename: str) -> bool:
        """Delete a character file"""
        filepath = os.path.join(self.rendered_folder, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

# Example usage and demonstration
if __name__ == "__main__":
    # Create character manager
    manager = CharacterManager()
    
    print("🤖 CHARACTER SYSTEM DEMO 🤖")
    print("═" * 60)
    
    # Create a player character
    print("\n--- Creating Player Character ---")
    player = manager.create_player_character(
        name="Zero Cool",
        cash=5000,
        physical_description="Lean hacker with chrome neural ports and glowing eyes",
        goals="Infiltrate Arasaka mainframe and expose corporate secrets"
    )
    
    # Add some items and skills
    player.add_item("Cyberdeck Model X")
    player.add_item("Encryption Software")
    player.add_item("Stim Pack")
    player.learn_skill("Hacking")
    player.learn_skill("Electronics")
    player.learn_skill("Stealth")
    
    print(player)
    
    # Create an NPC
    print("\n" + "═" * 60)
    print("--- Creating NPC ---")
    npc = manager.create_npc(
        name="Chrome Sally",
        cash=1200
    )
    npc.add_item("Katana")
    npc.add_item("Kevlar Vest")
    npc.learn_skill("Melee Combat")
    npc.learn_skill("Athletics")
    
    print(npc)
    
    # Demonstrate combat
    print("\n" + "═" * 60)
    print("--- Combat Simulation ---")
    print(f"NPC takes 3 damage...")
    npc.take_damage(3)
    print(f"NPC HP: {npc.current_hp}/{npc.max_hp}")
    
    print(f"NPC heals 2 HP...")
    healed = npc.heal(2)
    print(f"Healed {healed} HP. Current: {npc.current_hp}/{npc.max_hp}")
    
    # Export characters
    print("\n" + "═" * 60)
    print("--- Saving Characters ---")
    player_file = manager.export_character(player)
    npc_file = manager.export_character(npc)
    print(f"Player saved to: {player_file}")
    print(f"NPC saved to: {npc_file}")
    
    # List saved characters
    print(f"\nSaved characters: {manager.list_saved_characters()}")
    
    # Load a character
    print("\n--- Loading Character ---")
    loaded_player = manager.load_character("zero_cool.json")
    print(f"Loaded character: {loaded_player.name}")
    print(f"Archetype: {loaded_player.archetype}")
    print(f"Inventory: {loaded_player.inventory}")
    
    # Generate multiple random NPCs
    print("\n" + "═" * 60)
    print("--- Random NPC Generation ---")
    for i in range(2):
        random_npc = manager.create_npc()
        print(f"\nRandom NPC {i+1}: {random_npc.name}")
        print(f"Symbol: {random_npc.symbol}")
        print(f"Archetype: {random_npc.archetype}")
        print(f"Background snippet: {random_npc.background[:100]}...")