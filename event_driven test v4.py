#!/usr/bin/env python3
"""
Event-Driven RPG System with LLM Integration
Uses smolagents library for LLM tool calling and character management
"""

import os
import json
import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from openai import OpenAI
from smolagents import ToolCallingAgent, OpenAIServerModel, tool
import copy
import datetime

# Import our character system
from character_class import Character, CharacterManager

@dataclass
class EventTemplate:
    """Event template structure"""
    id: str
    name: str
    description: str
    triggers: List[str]
    possible_outcomes: List[str]
    required_tools: List[str]
    context_hints: List[str]
    difficulty: str = "medium"  # easy, medium, hard
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class GameEvent:
    """Executed game event with context"""
    template_id: str
    template_name: str
    contextualized_description: str
    outcome: str
    character_changes: Dict[str, Any]
    timestamp: str
    player_action: str
    event_number: int

class EventManager:
    """Manages event templates and execution"""
    
    def __init__(self):
        self.templates_folder = Path("event_templates")
        self.templates_folder.mkdir(exist_ok=True)
        self.templates: Dict[str, EventTemplate] = {}
        self.load_all_templates()
    
    def load_all_templates(self):
        """Load all event templates from JSON files"""
        self.templates = {}
        for json_file in self.templates_folder.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    template = EventTemplate(**data)
                    self.templates[template.id] = template
            except Exception as e:
                print(f"Error loading template {json_file}: {e}")
    
    def save_template(self, template: EventTemplate):
        """Save an event template to JSON file"""
        filename = f"{template.id}.json"
        filepath = self.templates_folder / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(template), f, indent=2)
        
        self.templates[template.id] = template
    
    def get_random_template(self, tags: List[str] = None) -> Optional[EventTemplate]:
        """Get a random event template, optionally filtered by tags"""
        available_templates = list(self.templates.values())
        
        if tags:
            available_templates = [
                t for t in available_templates 
                if any(tag in t.tags for tag in tags)
            ]
        
        return random.choice(available_templates) if available_templates else None
    
    def get_template(self, template_id: str) -> Optional[EventTemplate]:
        """Get a specific template by ID"""
        return self.templates.get(template_id)

# Define tools for LLM character manipulation
@tool
def get_character_info(name: str) -> str:
    """Get full information about a character.
    
    Args:
        name: Name of the character
        
    Returns:
        Character information as formatted string
    """
    if hasattr(get_character_info, 'game_state') and name in get_character_info.game_state.characters:
        character = get_character_info.game_state.characters[name]
        return str(character)
    return f"Character '{name}' not found"

@tool
def modify_character_hp(name: str, change: int) -> str:
    """Modify a character's HP.
    
    Args:
        name: Name of the character
        change: Amount to change HP (positive for heal, negative for damage)
        
    Returns:
        Result of HP change
    """
    if hasattr(modify_character_hp, 'game_state') and name in modify_character_hp.game_state.characters:
        character = modify_character_hp.game_state.characters[name]
        old_hp = character.get_current_hp()
        
        if change > 0:
            healed = character.heal(change)
            return f"{name} healed {healed} HP. Current HP: {character.get_current_hp()}/{character.get_max_hp()}"
        else:
            died = character.take_damage(abs(change))
            death_msg = " and DIED!" if died else ""
            return f"{name} took {abs(change)} damage{death_msg}. Current HP: {character.get_current_hp()}/{character.get_max_hp()}"
    return f"Character '{name}' not found"

@tool
def modify_character_cash(name: str, change: int) -> str:
    """Modify a character's cash.
    
    Args:
        name: Name of the character
        change: Amount to change cash (positive to add, negative to subtract)
        
    Returns:
        Result of cash change
    """
    if hasattr(modify_character_cash, 'game_state') and name in modify_character_cash.game_state.characters:
        character = modify_character_cash.game_state.characters[name]
        old_cash = character.get_cash()
        new_cash = max(0, old_cash + change)
        character.set_cash(new_cash)
        
        action = "gained" if change > 0 else "lost"
        return f"{name} {action} ¥{abs(change)}. Current cash: ¥{new_cash}"
    return f"Character '{name}' not found"

@tool
def add_item_to_inventory(name: str, item: str) -> str:
    """Add an item to a character's inventory.
    
    Args:
        name: Name of the character
        item: Item to add
        
    Returns:
        Result of adding item
    """
    if hasattr(add_item_to_inventory, 'game_state') and name in add_item_to_inventory.game_state.characters:
        character = add_item_to_inventory.game_state.characters[name]
        character.add_item(item)
        return f"Added '{item}' to {name}'s inventory"
    return f"Character '{name}' not found"

@tool
def remove_item_from_inventory(name: str, item: str) -> str:
    """Remove an item from a character's inventory.
    
    Args:
        name: Name of the character
        item: Item to remove
        
    Returns:
        Result of removing item
    """
    if hasattr(remove_item_from_inventory, 'game_state') and name in remove_item_from_inventory.game_state.characters:
        character = remove_item_from_inventory.game_state.characters[name]
        success = character.remove_item(item)
        if success:
            return f"Removed '{item}' from {name}'s inventory"
        else:
            return f"{name} doesn't have '{item}' in inventory"
    return f"Character '{name}' not found"

@tool
def set_character_condition(name: str, condition: str) -> str:
    """Set a character's condition (status effect).
    
    Args:
        name: Name of the character
        condition: Condition to set (e.g., 'poisoned', 'sleeping', 'prone')
        
    Returns:
        Result of setting condition
    """
    if hasattr(set_character_condition, 'game_state') and name in set_character_condition.game_state.characters:
        character = set_character_condition.game_state.characters[name]
        character.set_condition(condition)
        return f"{name} is now {condition}"
    return f"Character '{name}' not found"

@tool
def clear_character_condition(name: str) -> str:
    """Clear a character's condition.
    
    Args:
        name: Name of the character
        
    Returns:
        Result of clearing condition
    """
    if hasattr(clear_character_condition, 'game_state') and name in clear_character_condition.game_state.characters:
        character = clear_character_condition.game_state.characters[name]
        character.clear_condition()
        return f"{name}'s condition has been cleared"
    return f"Character '{name}' not found"

@tool
def learn_character_skill(name: str, skill: str) -> str:
    """Teach a character a new skill.
    
    Args:
        name: Name of the character
        skill: Skill to learn
        
    Returns:
        Result of learning skill
    """
    if hasattr(learn_character_skill, 'game_state') and name in learn_character_skill.game_state.characters:
        character = learn_character_skill.game_state.characters[name]
        character.learn_skill(skill)
        return f"{name} learned the skill: {skill}"
    return f"Character '{name}' not found"

@tool
def get_all_characters() -> str:
    """Get a summary of all characters in the game.
    
    Returns:
        Summary of all characters
    """
    if hasattr(get_all_characters, 'game_state'):
        characters = get_all_characters.game_state.characters
        if not characters:
            return "No characters in the game"
        
        summary = "CHARACTERS IN GAME:\n" + "="*30 + "\n"
        for name, char in characters.items():
            summary += f"\n{char.get_symbol()} {name} ({char.get_archetype()})\n"
            summary += f"  HP: {char.get_current_hp()}/{char.get_max_hp()}\n"
            summary += f"  Cash: ¥{char.get_cash()}\n"
            summary += f"  Condition: {char.get_condition() or 'Normal'}\n"
            summary += f"  Control: {'Player' if char.get_player_control() else 'NPC'}\n"
        
        return summary
    return "No game state available"

@tool
def execute_event_template(template_id: str, player_action: str) -> str:
    """Execute an event template with context from player action.
    
    Args:
        template_id: ID of the event template to execute
        player_action: The action the player took that triggered this event
        
    Returns:
        Contextualized event description and outcome
    """
    if hasattr(execute_event_template, 'game_state'):
        game_state = execute_event_template.game_state
        template = game_state.event_manager.get_template(template_id)
        
        if not template:
            return f"Event template '{template_id}' not found"
        
        # Track this event execution
        import datetime
        event_number = len(game_state.event_history) + 1
        
        # Create game event record
        game_event = GameEvent(
            template_id=template_id,
            template_name=template.name,
            contextualized_description=template.description,
            outcome="",  # Will be filled in by LLM
            character_changes={},  # Will be tracked by other tools
            timestamp=datetime.datetime.now().isoformat(),
            player_action=player_action,
            event_number=event_number
        )
        
        # Add to history
        game_state.event_history.append(game_event)
        game_state.current_event = game_event
        
        # Update event statistics
        if template_id not in game_state.event_stats:
            game_state.event_stats[template_id] = {
                'name': template.name,
                'count': 0,
                'last_triggered': None
            }
        game_state.event_stats[template_id]['count'] += 1
        game_state.event_stats[template_id]['last_triggered'] = datetime.datetime.now().isoformat()
        
        # Create contextualized event description
        context = f"""
Player Action: {player_action}
Event Template: {template.description}
Context Hints: {', '.join(template.context_hints)}
Current Characters: {get_all_characters()}
        """
        
        return f"🎲 EVENT #{event_number}: {template.name} 🎲\n\n{template.description}\n\nUse the available character tools to resolve this event based on the player's action: {player_action}\n\nPossible outcomes: {', '.join(template.possible_outcomes)}"
    
    return "No game state available"

class GameState:
    """Manages the current game state"""
    
    def __init__(self):
        self.characters: Dict[str, Character] = {}
        self.character_manager = CharacterManager()
        self.event_manager = EventManager()
        self.event_history: List[GameEvent] = []
        self.story_log: List[str] = []
        self.current_event: Optional[GameEvent] = None
        self.event_stats: Dict[str, Dict[str, Any]] = {}
        
        # Create some default event templates if none exist
        self.create_default_templates()
    
    def create_default_templates(self):
        """Create some default event templates if the folder is empty"""
        if not any(self.event_manager.templates_folder.glob("*.json")):
            default_templates = [
                EventTemplate(
                    id="treasure_find",
                    name="Treasure Discovery",
                    description="The party discovers a hidden cache of valuable items. The treasure could contain cash, equipment, or mysterious artifacts.",
                    triggers=["exploring", "searching", "investigating"],
                    possible_outcomes=["Find cash", "Find equipment", "Find magical item", "Trap triggers"],
                    required_tools=["modify_character_cash", "add_item_to_inventory", "modify_character_hp"],
                    context_hints=["Consider what the player was doing", "Match treasure to location", "Some treasures might be trapped"],
                    difficulty="easy",
                    tags=["exploration", "reward", "discovery"]
                ),
                EventTemplate(
                    id="combat_encounter",
                    name="Combat Encounter",
                    description="Hostile enemies appear and engage the party in combat. The outcome depends on the party's skills and tactics.",
                    triggers=["fighting", "attacking", "confronting"],
                    possible_outcomes=["Victory with no casualties", "Victory with injuries", "Retreat", "Defeat"],
                    required_tools=["modify_character_hp", "set_character_condition", "modify_character_cash"],
                    context_hints=["Consider party strength", "Match enemy to location", "Injuries should be realistic"],
                    difficulty="hard",
                    tags=["combat", "danger", "challenge"]
                ),
                EventTemplate(
                    id="skill_challenge",
                    name="Skill Challenge",
                    description="The party faces a challenge that requires specific skills or knowledge to overcome successfully.",
                    triggers=["attempting", "trying", "solving"],
                    possible_outcomes=["Success", "Partial success", "Failure with consequences", "Learn new skill"],
                    required_tools=["learn_character_skill", "modify_character_hp", "add_item_to_inventory"],
                    context_hints=["Match challenge to player action", "Reward creativity", "Failure should teach something"],
                    difficulty="medium",
                    tags=["challenge", "skill", "learning"]
                ),
                EventTemplate(
                    id="social_encounter",
                    name="Social Encounter",
                    description="The party meets NPCs who may become allies, enemies, or sources of information and opportunities.",
                    triggers=["talking", "negotiating", "meeting"],
                    possible_outcomes=["Gain ally", "Make enemy", "Get information", "Receive quest", "Trade opportunity"],
                    required_tools=["modify_character_cash", "add_item_to_inventory", "learn_character_skill"],
                    context_hints=["NPCs should have motivations", "Social outcomes depend on approach", "Information should be useful"],
                    difficulty="easy",
                    tags=["social", "npc", "roleplay"]
                )
            ]
            
            for template in default_templates:
                self.event_manager.save_template(template)
    
    def add_character(self, character: Character):
        """Add a character to the game"""
        self.characters[character.get_name()] = character
    
    def remove_character(self, name: str):
        """Remove a character from the game"""
        if name in self.characters:
            del self.characters[name]
    
    def get_event_statistics(self) -> str:
        """Get formatted event statistics"""
        if not self.event_stats:
            return "No events have been triggered yet."
        
        stats = "📊 EVENT STATISTICS 📊\n" + "="*40 + "\n"
        stats += f"Total Events Executed: {len(self.event_history)}\n\n"
        
        for template_id, data in self.event_stats.items():
            stats += f"• {data['name']} ({template_id}): {data['count']} times\n"
        
        if self.current_event:
            stats += f"\n🎯 Current Event: #{self.current_event.event_number} - {self.current_event.template_name}\n"
        
        return stats
    
    def save_state(self, filepath: str):
        """Save game state to file"""
        state_data = {
            "characters": {},
            "event_history": [],
            "story_log": self.story_log,
            "event_stats": self.event_stats,
            "current_event": asdict(self.current_event) if self.current_event else None
        }
        
        # Save characters
        for name, char in self.characters.items():
            char_dict = {
                'name': char.name,
                'symbol': char.symbol,
                'max_hp': char.max_hp,
                'current_hp': char.current_hp,
                'cash': char.cash,
                'player_control': char.player_control,
                'is_living': char.is_living,
                'inventory': char.inventory,
                'skills': char.skills,
                'archetype': char.archetype,
                'background': char.background,
                'physical_description': char.physical_description,
                'condition': char.condition,
                'goals': char.goals,
                'contextualized': char.contextualized
            }
            state_data["characters"][name] = char_dict
        
        # Save event history
        for event in self.event_history:
            state_data["event_history"].append(asdict(event))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2)
    
    def load_state(self, filepath: str):
        """Load game state from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        # Load characters
        self.characters = {}
        for name, char_dict in state_data.get("characters", {}).items():
            # Extract current_hp since it's not an init parameter
            current_hp = char_dict.pop('current_hp', None)
            
            # Create character with remaining parameters
            char = Character(**char_dict)
            
            # Set current_hp after creation if it was saved
            if current_hp is not None:
                char.current_hp = current_hp
            
            self.characters[name] = char
        
        # Load event history
        self.event_history = []
        for event_dict in state_data.get("event_history", []):
            event = GameEvent(**event_dict)
            self.event_history.append(event)
        
        # Load story log
        self.story_log = state_data.get("story_log", [])
        
        # Load event statistics
        self.event_stats = state_data.get("event_stats", {})
        
        # Load current event
        current_event_data = state_data.get("current_event")
        if current_event_data:
            self.current_event = GameEvent(**current_event_data)
        else:
            self.current_event = None

class RPGGameEngine:
    """Main game engine with LLM integration"""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1", api_key: str = "lm-studio"):
        self.game_state = GameState()
        
        # Initialize LLM and agent
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = OpenAIServerModel(
            model_id="local-model",
            api_base=base_url,
            api_key=api_key
        )
        
        # Set up tools with game state reference
        self.tools = [
            get_character_info, modify_character_hp, modify_character_cash,
            add_item_to_inventory, remove_item_from_inventory, set_character_condition,
            clear_character_condition, learn_character_skill, get_all_characters,
            execute_event_template
        ]
        
        # Attach game state to tools
        for tool in self.tools:
            tool.game_state = self.game_state
        
        self.agent = ToolCallingAgent(model=self.model, tools=self.tools)
    
    def process_player_action(self, player_input: str) -> str:
        """Process player input using LLM and return response"""
        
        # Get current game context
        characters_summary = get_all_characters()
        available_events = list(self.game_state.event_manager.templates.keys())
        
        prompt = f"""
You are a game master for an RPG. The player has input: "{player_input}"

Current game state:
{characters_summary}

Available event templates: {', '.join(available_events)}

Your task:
1. Interpret the player's action in context
2. Decide if an event should be triggered based on the action
3. If triggering an event, use execute_event_template to select an appropriate one
4. Use the available character tools to resolve the consequences
5. Provide a narrative description of what happens

WHEN TO TRIGGER EVENTS:
- Actions that involve risk, discovery, or significant consequences
- Combat, exploration, social encounters with important NPCs
- Actions that match the triggers/themes of available templates

WHEN NOT TO TRIGGER EVENTS:
- Simple conversations between party members
- Basic equipment checks or maintenance
- Rest/idle actions without consequences
- Information gathering that doesn't involve risk

FOR NON-EVENT ACTIONS:
- Respond with engaging narrative description
- You may still use character tools if the action directly affects stats:
  * modify_character_hp for healing/damage
  * modify_character_cash for transactions
  * add/remove items for direct inventory changes
- Keep the story moving forward

Remember to:
- Match events to player actions logically
- Use character tools to apply consequences
- Create engaging narrative descriptions
- Consider the current state of all characters

Respond with a complete narrative of what happens as a result of the player's action.
        """
        
        try:
            response = self.agent.run(prompt)
            self.game_state.story_log.append(f"Player: {player_input}")
            self.game_state.story_log.append(f"GM: {response}")
            return response
        except Exception as e:
            return f"Error processing action: {str(e)}"
    
    def undo_last_event(self) -> str:
        """Undo the last event (basic implementation)"""
        if self.game_state.event_history:
            # Remove last event from history
            last_event = self.game_state.event_history.pop()
            
            # Update event statistics
            if last_event.template_id in self.game_state.event_stats:
                self.game_state.event_stats[last_event.template_id]['count'] -= 1
                if self.game_state.event_stats[last_event.template_id]['count'] <= 0:
                    del self.game_state.event_stats[last_event.template_id]
            
            # Clear current event if it was the one we just undid
            if (self.game_state.current_event and 
                self.game_state.current_event.event_number == last_event.event_number):
                self.game_state.current_event = None
            
            # Remove last two entries from story log (player action and GM response)
            if len(self.game_state.story_log) >= 2:
                self.game_state.story_log.pop()
                self.game_state.story_log.pop()
            
            return f"Undid event #{last_event.event_number}: {last_event.template_name}"
        return "No events to undo"

# GUI for Event Template Creator
class EventTemplateCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Event Template Creator")
        self.root.geometry("800x600")
        
        self.event_manager = EventManager()
        self.current_template = None
        
        self.setup_gui()
    
    def setup_gui(self):
        """Set up the GUI elements"""
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - form
        form_frame = ttk.LabelFrame(main_frame, text="Event Template", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right panel - template list
        list_frame = ttk.LabelFrame(main_frame, text="Existing Templates", padding=10)
        list_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Form fields
        row = 0
        
        # ID
        ttk.Label(form_frame, text="ID:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.id_var, width=40).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Name
        ttk.Label(form_frame, text="Name:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=40).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Difficulty
        ttk.Label(form_frame, text="Difficulty:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.difficulty_var = tk.StringVar(value="medium")
        difficulty_combo = ttk.Combobox(form_frame, textvariable=self.difficulty_var, 
                                       values=["easy", "medium", "hard"], width=37)
        difficulty_combo.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=row, column=0, sticky=tk.NW, pady=2)
        self.description_text = scrolledtext.ScrolledText(form_frame, width=50, height=4)
        self.description_text.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Triggers
        ttk.Label(form_frame, text="Triggers (one per line):").grid(row=row, column=0, sticky=tk.NW, pady=2)
        self.triggers_text = scrolledtext.ScrolledText(form_frame, width=50, height=3)
        self.triggers_text.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Possible Outcomes
        ttk.Label(form_frame, text="Possible Outcomes (one per line):").grid(row=row, column=0, sticky=tk.NW, pady=2)
        self.outcomes_text = scrolledtext.ScrolledText(form_frame, width=50, height=3)
        self.outcomes_text.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Required Tools
        ttk.Label(form_frame, text="Required Tools (one per line):").grid(row=row, column=0, sticky=tk.NW, pady=2)
        self.tools_text = scrolledtext.ScrolledText(form_frame, width=50, height=3)
        self.tools_text.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Context Hints
        ttk.Label(form_frame, text="Context Hints (one per line):").grid(row=row, column=0, sticky=tk.NW, pady=2)
        self.hints_text = scrolledtext.ScrolledText(form_frame, width=50, height=3)
        self.hints_text.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Tags
        ttk.Label(form_frame, text="Tags (comma separated):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.tags_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.tags_var, width=40).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Save Template", command=self.save_template).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Template", command=self.load_selected_template).pack(side=tk.LEFT, padx=5)
        
        # Template list
        self.template_listbox = tk.Listbox(list_frame, width=25, height=20)
        self.template_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        ttk.Button(list_frame, text="Refresh List", command=self.refresh_template_list).pack(pady=5)
        
        # Initial refresh
        self.refresh_template_list()
    
    def refresh_template_list(self):
        """Refresh the template list"""
        self.event_manager.load_all_templates()
        self.template_listbox.delete(0, tk.END)
        
        for template_id, template in self.event_manager.templates.items():
            self.template_listbox.insert(tk.END, f"{template_id}: {template.name}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.id_var.set("")
        self.name_var.set("")
        self.difficulty_var.set("medium")
        self.description_text.delete(1.0, tk.END)
        self.triggers_text.delete(1.0, tk.END)
        self.outcomes_text.delete(1.0, tk.END)
        self.tools_text.delete(1.0, tk.END)
        self.hints_text.delete(1.0, tk.END)
        self.tags_var.set("")
    
    def save_template(self):
        """Save the current template"""
        try:
            # Validate required fields
            template_id = self.id_var.get().strip()
            template_name = self.name_var.get().strip()
            
            if not template_id:
                messagebox.showerror("Error", "Template ID is required!")
                return
            
            if not template_name:
                messagebox.showerror("Error", "Template Name is required!")
                return
            
            # Get description
            description = self.description_text.get(1.0, tk.END).strip()
            if not description:
                messagebox.showerror("Error", "Description is required!")
                return
            
            # Parse list fields
            triggers_text = self.triggers_text.get(1.0, tk.END).strip()
            triggers = [t.strip() for t in triggers_text.split('\n') if t.strip()] if triggers_text else []
            
            outcomes_text = self.outcomes_text.get(1.0, tk.END).strip()
            outcomes = [o.strip() for o in outcomes_text.split('\n') if o.strip()] if outcomes_text else []
            
            tools_text = self.tools_text.get(1.0, tk.END).strip()
            tools = [t.strip() for t in tools_text.split('\n') if t.strip()] if tools_text else []
            
            hints_text = self.hints_text.get(1.0, tk.END).strip()
            hints = [h.strip() for h in hints_text.split('\n') if h.strip()] if hints_text else []
            
            tags_text = self.tags_var.get().strip()
            tags = [t.strip() for t in tags_text.split(',') if t.strip()] if tags_text else []
            
            # Create template
            template = EventTemplate(
                id=template_id,
                name=template_name,
                description=description,
                triggers=triggers,
                possible_outcomes=outcomes,
                required_tools=tools,
                context_hints=hints,
                difficulty=self.difficulty_var.get(),
                tags=tags
            )
            
            # Ensure templates folder exists
            self.event_manager.templates_folder.mkdir(exist_ok=True)
            
            # Save template
            self.event_manager.save_template(template)
            self.refresh_template_list()
            messagebox.showinfo("Success", f"Template '{template_id}' saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save template: {str(e)}")
            print(f"Debug - Save error: {e}")  # Debug output
    
    def load_selected_template(self):
        """Load the selected template into the form"""
        selection = self.template_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a template to load!")
            return
        
        selected_text = self.template_listbox.get(selection[0])
        template_id = selected_text.split(':')[0]
        
        template = self.event_manager.get_template(template_id)
        if template:
            self.id_var.set(template.id)
            self.name_var.set(template.name)
            self.difficulty_var.set(template.difficulty)
            
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(1.0, template.description)
            
            self.triggers_text.delete(1.0, tk.END)
            self.triggers_text.insert(1.0, '\n'.join(template.triggers))
            
            self.outcomes_text.delete(1.0, tk.END)
            self.outcomes_text.insert(1.0, '\n'.join(template.possible_outcomes))
            
            self.tools_text.delete(1.0, tk.END)
            self.tools_text.insert(1.0, '\n'.join(template.required_tools))
            
            self.hints_text.delete(1.0, tk.END)
            self.hints_text.insert(1.0, '\n'.join(template.context_hints))
            
            self.tags_var.set(', '.join(template.tags))
    
    def run(self):
        """Run the template creator GUI"""
        self.root.mainloop()

# Main Game GUI
class RPGGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RPG Game Engine")
        self.root.geometry("1200x800")
        
        try:
            self.game_engine = RPGGameEngine()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to LLM: {str(e)}")
            self.game_engine = None
        
        self.setup_gui()
        
        # Load some test characters
        self.load_test_characters()
    
    def setup_gui(self):
        """Set up the main game GUI"""
        
        # Main paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - game area
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=3)
        
        # Right panel - info panels
        right_paned = ttk.PanedWindow(main_paned, orient=tk.VERTICAL)
        main_paned.add(right_paned, weight=1)
        
        # Character info panel
        char_frame = ttk.LabelFrame(right_paned, text="Characters", padding=5)
        right_paned.add(char_frame, weight=1)
        
        # Event info panel
        event_frame = ttk.LabelFrame(right_paned, text="Events", padding=5)
        right_paned.add(event_frame, weight=1)
        
        # Game area - story display
        story_frame = ttk.LabelFrame(left_frame, text="Story", padding=5)
        story_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.story_text = scrolledtext.ScrolledText(story_frame, height=20, state=tk.DISABLED)
        self.story_text.pack(fill=tk.BOTH, expand=True)
        
        # Input area
        input_frame = ttk.LabelFrame(left_frame, text="Player Input", padding=5)
        input_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Player input
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_var, font=("Arial", 12))
        input_entry.pack(fill=tk.X, pady=(0, 5))
        input_entry.bind('<Return>', self.process_input)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Submit", command=self.process_input).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Undo", command=self.undo_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Game", command=self.save_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Game", command=self.load_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Story", command=self.clear_story).pack(side=tk.LEFT, padx=5)
        
        # Character display layout - horizontal
        char_content_frame = ttk.Frame(char_frame)
        char_content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Character text on the left
        self.character_text = scrolledtext.ScrolledText(char_content_frame, width=25, state=tk.DISABLED)
        self.character_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Character management buttons on the right
        char_button_frame = ttk.Frame(char_content_frame)
        char_button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(char_button_frame, text="Add\nCharacter", command=self.add_character, width=12).pack(pady=2)
        ttk.Button(char_button_frame, text="Refresh", command=self.refresh_characters, width=12).pack(pady=2)
        
        # Event display layout - horizontal
        event_content_frame = ttk.Frame(event_frame)
        event_content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Event text on the left
        self.event_text = scrolledtext.ScrolledText(event_content_frame, width=25, state=tk.DISABLED)
        self.event_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Event management buttons on the right
        event_button_frame = ttk.Frame(event_content_frame)
        event_button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(event_button_frame, text="Refresh\nEvents", command=self.refresh_events, width=12).pack(pady=2)
        ttk.Button(event_button_frame, text="Next Event\n(Random)", command=self.trigger_random_event, width=12).pack(pady=2)
        ttk.Button(event_button_frame, text="Force\nEvent", command=self.force_specific_event, width=12).pack(pady=2)
        ttk.Button(event_button_frame, text="Clear\nCurrent", command=self.clear_current_event, width=12).pack(pady=2)
        
        # Initial refreshes
        self.refresh_characters()
        self.refresh_events()
    
    def load_test_characters(self):
        """Load some test characters for demo"""
        if not self.game_engine:
            return
        
        # Create test player character
        player = self.game_engine.game_state.character_manager.create_player_character(
            name="Alex",
            cash=500,
            physical_description="A young adventurer with determination in their eyes",
            goals="Discover the truth about the ancient ruins"
        )
        player.add_item("Sword")
        player.add_item("Health Potion")
        player.learn_skill("Swordsmanship")
        
        # Create test NPC
        npc = self.game_engine.game_state.character_manager.create_npc(
            name="Sage Mentor",
            cash=100
        )
        npc.add_item("Ancient Tome")
        npc.learn_skill("Ancient Knowledge")
        
        # Add to game
        self.game_engine.game_state.add_character(player)
        self.game_engine.game_state.add_character(npc)
        
        self.refresh_characters()
    
    def add_story_text(self, text: str):
        """Add text to the story display"""
        self.story_text.config(state=tk.NORMAL)
        self.story_text.insert(tk.END, text + "\n\n")
        self.story_text.see(tk.END)
        self.story_text.config(state=tk.DISABLED)
    
    def process_input(self, event=None):
        """Process player input"""
        if not self.game_engine:
            messagebox.showerror("Error", "Game engine not initialized!")
            return
        
        player_input = self.input_var.get().strip()
        if not player_input:
            return
        
        self.input_var.set("")
        
        # Add player input to story
        self.add_story_text(f"> {player_input}")
        
        # Process with LLM
        try:
            response = self.game_engine.process_player_action(player_input)
            self.add_story_text(response)
        except Exception as e:
            self.add_story_text(f"Error: {str(e)}")
        
        # Refresh both displays
        self.refresh_characters()
        self.refresh_events()
    
    def undo_action(self):
        """Undo the last action"""
        if not self.game_engine:
            return
        
        result = self.game_engine.undo_last_event()
        self.add_story_text(f"[UNDO] {result}")
        self.refresh_characters()
        self.refresh_events()
    
    def refresh_characters(self):
        """Refresh the character display"""
        if not self.game_engine:
            return
        
        self.character_text.config(state=tk.NORMAL)
        self.character_text.delete(1.0, tk.END)
        
        characters_info = get_all_characters()
        self.character_text.insert(1.0, characters_info)
        
        self.character_text.config(state=tk.DISABLED)
    
    def refresh_events(self):
        """Refresh the event display"""
        if not self.game_engine:
            return
        
        self.event_text.config(state=tk.NORMAL)
        self.event_text.delete(1.0, tk.END)
        
        event_info = self.game_engine.game_state.get_event_statistics()
        self.event_text.insert(1.0, event_info)
        
        self.event_text.config(state=tk.DISABLED)
    
    def clear_current_event(self):
        """Clear the current event"""
        if not self.game_engine:
            return
        
        self.game_engine.game_state.current_event = None
        self.refresh_events()
        self.add_story_text("[SYSTEM] Current event cleared.")
    
    def trigger_random_event(self):
        """Trigger a random event"""
        if not self.game_engine:
            messagebox.showerror("Error", "Game engine not initialized!")
            return
        
        # Get available templates
        templates = list(self.game_engine.game_state.event_manager.templates.values())
        if not templates:
            messagebox.showwarning("Warning", "No event templates available!")
            return
        
        # Select random template
        random_template = random.choice(templates)
        
        # Trigger the event
        player_action = "[RANDOM EVENT TRIGGERED]"
        self.add_story_text(f"🎲 RANDOM EVENT: {random_template.name} 🎲")
        
        try:
            # Use the LLM to process the random event
            prompt = f"A random event has been triggered: {random_template.name}. Execute this event using execute_event_template with template_id '{random_template.id}' and player_action 'random event triggered'. Then use the appropriate character tools to resolve the event based on the template description and possible outcomes."
            
            response = self.game_engine.agent.run(prompt)
            self.add_story_text(response)
        except Exception as e:
            self.add_story_text(f"Error triggering random event: {str(e)}")
        
        # Refresh displays
        self.refresh_characters()
        self.refresh_events()
    
    def force_specific_event(self):
        """Show dialog to force a specific event"""
        if not self.game_engine:
            messagebox.showerror("Error", "Game engine not initialized!")
            return
        
        # Get available templates
        templates = self.game_engine.game_state.event_manager.templates
        if not templates:
            messagebox.showwarning("Warning", "No event templates available!")
            return
        
        # Create selection dialog
        self.show_event_selection_dialog(templates)
    
    def show_event_selection_dialog(self, templates):
        """Show dialog for selecting a specific event to force"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Force Event")
        dialog.geometry("450x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        ttk.Label(main_frame, text="Select an event template to force:", 
                  font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Event selection
        ttk.Label(main_frame, text="Event Template:").pack(anchor=tk.W)
        
        # Create combobox with template options
        template_options = []
        template_map = {}
        
        for template_id, template in templates.items():
            display_text = f"{template.name} ({template_id}) - {template.difficulty}"
            template_options.append(display_text)
            template_map[display_text] = template
        
        self.selected_template_var = tk.StringVar()
        template_combo = ttk.Combobox(main_frame, textvariable=self.selected_template_var, 
                                      values=template_options, state="readonly", width=50)
        template_combo.pack(fill=tk.X, pady=(5, 10))
        
        # Event preview
        ttk.Label(main_frame, text="Event Description:").pack(anchor=tk.W)
        description_text = scrolledtext.ScrolledText(main_frame, height=10, width=50, state=tk.DISABLED)
        description_text.pack(fill=tk.BOTH, expand=True, pady=(5, 15))
        
        def on_template_select(event=None):
            """Update description when template is selected"""
            selected = self.selected_template_var.get()
            if selected and selected in template_map:
                template = template_map[selected]
                description_text.config(state=tk.NORMAL)
                description_text.delete(1.0, tk.END)
                
                preview = f"Description: {template.description}\n\n"
                preview += f"Difficulty: {template.difficulty}\n\n"
                preview += f"Possible Outcomes:\n"
                for outcome in template.possible_outcomes:
                    preview += f"• {outcome}\n"
                preview += f"\nTriggers: {', '.join(template.triggers)}\n"
                preview += f"Tags: {', '.join(template.tags) if template.tags else 'None'}"
                
                description_text.insert(1.0, preview)
                description_text.config(state=tk.DISABLED)
        
        template_combo.bind('<<ComboboxSelected>>', on_template_select)
        
        # Buttons frame - Fixed layout
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0))
        
        def force_selected_event():
            """Force the selected event"""
            selected = self.selected_template_var.get()
            if not selected:
                messagebox.showwarning("Warning", "Please select an event template!")
                return
            
            if selected in template_map:
                template = template_map[selected]
                dialog.destroy()
                
                # Trigger the forced event
                self.add_story_text(f"⚡ FORCED EVENT: {template.name} ⚡")
                
                try:
                    # Use the LLM to process the forced event
                    prompt = f"A specific event has been forced: {template.name}. Execute this event using execute_event_template with template_id '{template.id}' and player_action 'forced event'. Then use the appropriate character tools to resolve the event based on the template description and possible outcomes."
                    
                    response = self.game_engine.agent.run(prompt)
                    self.add_story_text(response)
                except Exception as e:
                    self.add_story_text(f"Error forcing event: {str(e)}")
                
                # Refresh displays
                self.refresh_characters()
                self.refresh_events()
        
        def cancel_dialog():
            """Cancel the dialog"""
            dialog.destroy()
        
        # Create buttons with proper styling
        force_button = ttk.Button(button_frame, text="Force Event", command=force_selected_event)
        force_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_dialog)
        cancel_button.pack(side=tk.LEFT)
        
        # Set focus and default button
        template_combo.focus()
        dialog.bind('<Return>', lambda e: force_selected_event())
        dialog.bind('<Escape>', lambda e: cancel_dialog())
    
    def add_character(self):
        """Add a new character"""
        if not self.game_engine:
            return
        
        # Simple dialog for character name
        name = tk.simpledialog.askstring("Add Character", "Enter character name:")
        if name:
            new_char = self.game_engine.game_state.character_manager.create_npc(name=name)
            self.game_engine.game_state.add_character(new_char)
            self.refresh_characters()
            self.add_story_text(f"Added new character: {name}")
    
    def save_game(self):
        """Save the current game state"""
        if not self.game_engine:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.game_engine.game_state.save_state(filename)
                messagebox.showinfo("Success", "Game saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save game: {str(e)}")
    
    def load_game(self):
        """Load a game state"""
        if not self.game_engine:
            return
        
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.game_engine.game_state.load_state(filename)
                self.refresh_characters()
                self.refresh_events()
                
                # Display story log
                self.story_text.config(state=tk.NORMAL)
                self.story_text.delete(1.0, tk.END)
                for entry in self.game_engine.game_state.story_log:
                    self.story_text.insert(tk.END, entry + "\n")
                self.story_text.config(state=tk.DISABLED)
                
                messagebox.showinfo("Success", "Game loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load game: {str(e)}")
    
    def clear_story(self):
        """Clear the story display"""
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        self.story_text.config(state=tk.DISABLED)
        
        if self.game_engine:
            self.game_engine.game_state.story_log.clear()
    
    def run(self):
        """Run the main game GUI"""
        self.root.mainloop()

def main():
    """Main function to choose which GUI to run"""
    choice_root = tk.Tk()
    choice_root.title("RPG System Launcher")
    choice_root.geometry("300x150")
    
    ttk.Label(choice_root, text="Choose which application to run:", 
              font=("Arial", 12)).pack(pady=20)
    
    def run_template_creator():
        choice_root.destroy()
        creator = EventTemplateCreator()
        creator.run()
    
    def run_game():
        choice_root.destroy()
        game = RPGGameGUI()
        game.run()
    
    ttk.Button(choice_root, text="Event Template Creator", 
               command=run_template_creator).pack(pady=5)
    ttk.Button(choice_root, text="RPG Game Engine", 
               command=run_game).pack(pady=5)
    
    choice_root.mainloop()

if __name__ == "__main__":
    main()