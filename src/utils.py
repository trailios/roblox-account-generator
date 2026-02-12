from random  import randint, choice
from secrets import token_hex
from time    import time

class Utils:

    @staticmethod
    def generate_traceparent() -> str:
        return f"00-{token_hex(16)}-{token_hex(8)}-00"

    @staticmethod
    def generate_name() -> str:
        adjectives: list = [
            "Swift", "Bright", "Silent", "Golden", "Crystal", "Shadow", "Cosmic",
            "Mystic", "Blazing", "Frozen", "Electric", "Velvet", "Radiant", "Noble",
            "Savage", "Clever", "Lucky", "Mighty", "Gentle", "Wild", "Ancient",
            "Neon", "Iron", "Silver", "Crimson", "Azure", "Emerald", "Phantom",
            "Quantum", "Stellar", "Titan", "Primal", "Sonic", "Lunar", "Solar",
            "Toxic", "Feral", "Spectral", "Ethereal", "Mortal", "Divine", "Infernal",
            "Omega", "Alpha", "Zenith", "Apex", "Void", "Cyber", "Thunder",
            "Obsidian", "Platinum", "Jade", "Sapphire", "Topaz", "Onyx", "Opal"
        ]

        nouns: list = [
            "Wolf", "Phoenix", "Dragon", "Falcon", "Tiger", "Raven", "Serpent",
            "Knight", "Wizard", "Hunter", "Ghost", "Storm", "Blade", "Spark",
            "Viper", "Bear", "Hawk", "Lion", "Panther", "Fox", "Owl", "Shark",
            "Ninja", "Pilot", "Ranger", "Scout", "Warrior", "Voyager",
            "Titan", "Sphinx", "Kraken", "Pegasus", "Griffin", "Siren", "Bandit",
            "Mystic", "Paladin", "Samurai", "Daemon", "Avatar", "Sentinel", "Reaper",
            "Wraith", "Specter", "Chimera", "Leviathan", "Basilisk", "Hydra", "Golem",
            "Archer", "Assassin", "Guardian", "Sentinel", "Enforcer", "Vanguard"
        ]
        
        adjective: str = choice(adjectives)
        noun: str = choice(nouns)
        number: int = randint(100, 99999)
        
        return f"{adjective}{noun}{number}"[:20]
    
    @staticmethod
    def short_esync() -> str:
        current_time = time() * 1000
        
        return int(round(int(current_time), -2))