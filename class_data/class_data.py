from ability import create_ability_from_data
from ability import *



# PSIONIC MAGE STATS AND ABILITIES
psionic_mage_abilities = [create_ability_from_data("Levitate"),
                          create_ability_from_data("Dash"),
                          create_ability_from_data("Fireball")]
psionic_mage_default_stats = {
    'health': 100,
    'mana': 100,
    'mana_color': 'purple',
    'mana_regen': 0.2,
    'gravity' : 0.1,
    'abilities': psionic_mage_abilities,
}

# BLOOD MAGE STATS AND ABILITIES
blood_mage_default_stats = {
    'health': 130,
    'mana': 0,
    'mana_color': 'black',
    'mana_regen': 0,
    'abilities': [BloodBurst, CrimsonPact, SanguineChains, Hemorrhage, ArcaneMissile, LightningStrike],
}

# TECHNO MAGE STATS AND ABILITIES
techno_mage_abilities = [create_ability_from_data("Teleport"),
                         create_ability_from_data("Invisibility"),
                         create_ability_from_data("Shield"),
                         create_ability_from_data("Lightning_Wall") ]
techno_mage_default_stats = {
    'health': 100,
    'mana': 100,
    'mana_color': 'blue',
    'mana_regen': 0,
    'abilities': techno_mage_abilities
}

# BRUISER STATS AND ABILITIES
bruiser_abilities = [create_ability_from_data("Heal")]
bruiser_default_stats = {
    'health': 130,
    'mana': 75,
    'mana_color': 'blue',
    'mana_regen': 0,
    'abilities': bruiser_abilities
}

# HUNTER STATS AND ABILITIES
hunter_abilities = [create_ability_from_data("Heal")]
hunter_default_stats = {
    'health': 130,
    'mana': 75,
    'mana_color': 'blue',
    'mana_regen': 0,
    'abilities': hunter_abilities
}

# DUELIST STATS AND ABILITIES
duelist_abilities = [create_ability_from_data("Heal")]
duelist_default_stats = {
    'health': 130,
    'mana': 75,
    'mana_color': 'blue',
    'mana_regen': 0,
    'abilities': duelist_abilities
}

game_classes = {
    "Psionic Mage": psionic_mage_default_stats,
    "Blood Mage": blood_mage_default_stats,
    "Techno Mage": techno_mage_default_stats,
    "Bruiser": bruiser_default_stats,
    "Hunter": hunter_default_stats,
    "Duelist": duelist_default_stats
}
