import random

ADJECTIVES = [
    "Silent", "Cosmic", "Brave", "Curious", "Electric",
    "Hidden", "Swift", "Crimson", "Icy", "Golden",
    "Midnight", "Urban", "Quantum", "Wild", "Calm",
    "Ancient", "Mystic", "Dark", "Radiant", "Fierce",
    "Lunar", "Solar", "Neon", "Frozen", "Burning",
    "Savage", "Noble", "Rapid", "Clever", "Arcane",
    "Phantom", "Iron", "Obsidian", "Stormy", "Glacial",
    "Shadowy", "Thunderous", "Velvet", "Vivid", "Shattered",
    "Cursed", "Blessed", "Savory", "Atomic", "Binary",
    "Digital", "Turbo", "Retro", "Cyber", "Astral",
    "Grim", "Emerald", "Scarlet", "Azure", "Silver",
    "Bronze", "Frosty", "Mighty", "Wicked", "Chill",
    "Infernal", "Divine", "Chaotic", "Epic", "Stealthy",
    "Rogue", "Viral", "Epic", "Daring", "Fearless",
    "Savvy", "Majestic", "Prime", "Ultra", "Hyper"
]

NOUNS = [
    "Cobra", "Falcon", "River", "Wolf", "Tiger",
    "Orion", "Phoenix", "Panther", "Shadow", "Comet",
    "Viper", "Eagle", "Fox", "Dragon", "Hawk",
    "Raven", "Shark", "Leopard", "Jaguar", "Cyclone",
    "Blaze", "Storm", "Nova", "Galaxy", "Meteor",
    "Hunter", "Knight", "Samurai", "Ninja", "Wizard",
    "Rider", "Sniper", "Voyager", "Nomad", "Gladiator",
    "Sentinel", "Titan", "Warden", "Rogue", "Ghost",
    "Specter", "Reaper", "Pirate", "Berserker", "Guardian",
    "Monarch", "Sphinx", "Oracle", "Tempest", "Vortex",
    "Phantom", "Machine", "Golem", "Serpent", "Kraken",
    "Falconer", "Alchemist", "Scholar", "Commander", "Captain",
    "Drifter", "Assassin", "Outlaw", "Ranger", "Prophet",
    "Marauder", "Warlord", "Seeker", "Champion", "Architect"
]


def generate_random_username():
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    number = random.randint(10, 999)

    return f"{adjective}-{noun}-{number}"


