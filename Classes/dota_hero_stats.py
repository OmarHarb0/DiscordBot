import requests

HERO_BY_ID = {1: 'Anti-Mage', 2: 'Axe', 3: 'Bane',
    4: 'Bloodseeker', 5: 'Crystal Maiden', 6: 'Drow Ranger',
    7: 'Earthshaker', 8: 'Juggernaut', 9: 'Mirana', 10: 'Morphling',
    11: 'Shadow Fiend', 12: 'Phantom Lancer', 13: 'Puck', 14: 'Pudge',
    15: 'Razor', 16: 'Sand King', 17: 'Storm Spirit', 18: 'Sven',
    19: 'Tiny', 20: 'Vengeful Spirit', 21: 'Windranger', 22: 'Zeus',
    23: 'Kunkka', 25: 'Lina', 26: 'Lion', 27: 'Shadow Shaman',
    28: 'Slardar', 29: 'Tidehunter', 30: 'Witch Doctor', 31: 'Lich',
    32: 'Riki', 33: 'Enigma', 34: 'Tinker', 35: 'Sniper', 36: 'Necrophos',
    37: 'Warlock', 38: 'Beastmaster', 39: 'Queen of Pain', 40: 'Venomancer',
    41: 'Faceless Void', 42: 'Wraith King', 43: 'Death Prophet',
    44: 'Phantom Assassin', 45: 'Pugna', 46: 'Templar Assassin', 47: 'Viper',
    48: 'Luna', 49: 'Dragon Knight', 50: 'Dazzle', 51: 'Clockwerk',
    52: 'Leshrac', 53: 'Nature\'s Prophet', 54: 'Lifestealer', 55: 'Dark Seer',
    56: 'Clinkz', 57: 'Omniknight', 58: 'Enchantress', 59: 'Huskar',
    60: 'Night Stalker', 61: 'Broodmother', 62: 'Bounty Hunter', 63: 'Weaver',
    64: 'Jakiro', 65: 'Batrider', 66: 'Chen', 67: 'Spectre',
    68: 'Ancient Apparition', 69: 'Doom', 70: 'Ursa', 71: 'Spirit Breaker',
    72: 'Gyrocopter', 73: 'Alchemist', 74: 'Invoker', 75: 'Silencer',
    76: 'Outworld Devourer', 77: 'Lycan', 78: 'Brewmaster', 79: 'Shadow Demon',
    80: 'Lone Druid', 81: 'Chaos Knight', 82: 'Meepo', 83: 'Treant Protector',
    84: 'Ogre Magi', 85: 'Undying', 86: 'Rubick', 87: 'Disruptor',
    88: 'Nyx Assassin', 89: 'Naga Siren', 90: 'Keeper of the Light', 91: 'Io',
    92: 'Visage', 93: 'Slark', 94: 'Medusa', 95: 'Troll Warlord',
    96: 'Centaur Warrunner', 97: 'Magnus', 98: 'Timbersaw', 99: 'Bristleback',
    100: 'Tusk', 101: 'Skywrath Mage', 102: 'Abaddon', 103: 'Elder Titan',
    104: 'Legion Commander', 105: 'Techies', 106: 'Ember Spirit',
    107: 'Earth Spirit', 108: 'Underlord', 109: 'Terrorblade', 110: 'Phoenix',
    111: 'Oracle', 112: 'Winter Wyvern', 113: 'Arc Warden', 114: 'Monkey King',
    119: 'Dark Willow', 120: 'Pangolier', 121: 'Grimstroke', 123: 'Hoodwink',
    126: 'Void Spirit', 128: 'Snapfire', 129: 'Mars'}
BRACKETS = {0: 'All', 1: 'Immortal', 2: 'Divine', 3: 'Ancient', 4: 'Legend',
            5: 'Archon', 6: 'Crusader', 7: 'Guardian', 8: 'Herald',
            9: 'Unrated'}
WHICH_WEEK = {0: 'This Week', 1: 'Last Week'}


def parse_stats(stratzDict, when=''):  # Returns List of Dicts
    def pull_helper(pulledDict):  # Each Dict contains data for a hero
        def flat_helper(flatDict):
            return [{'HeroName': HERO_BY_ID[hero[0]],
                     f"PickRate": round(hero[1]['matchCount'] /
                                        stratzDict[
                                            f"match{when}PickCount"] * 1000,
                                        2),
                     f"BanRate": round(hero[2]['matchCount'] /
                                       stratzDict[
                                           f"match{when}BanCount"] * 1000, 2),
                     f"PickWinRate": round(hero[1]['wins'] * 100, 2),
                     f"BanWinRate": round(hero[2]['wins'] * 100, 2)}
                    for hero in flatDict]

        return flat_helper([(hero[0], hero[1][f"pick{when}"],
                             hero[1][f"ban{when}"]) for hero in pulledDict])

    return pull_helper([(hero['heroId'], hero['pickBan'])
                        for hero in stratzDict['heroes']])


def make_lists():  # Returns List of Tuples with current and last week data
    return [(parse_stats(apiResponse.json()),
             parse_stats(apiResponse.json(), when='LastWeek')) for apiResponse
            in
            [requests.get(
                f"https://api.stratz.com/api/v1/Hero/directory/simple",
                params=skill) for skill in
             [{0: None}, *[{'rank': f"{brak}"} for brak in range(8, -1, -1)]]]]


def spill_data(lists):  # Writes all data to herodata.csv
    with open('herodata.csv', 'w+') as output:
        for brakID, bracket in enumerate(lists):
            for weekID, week in enumerate(bracket):
                output.write(f"[{BRACKETS[brakID]}][{WHICH_WEEK[weekID]}]\n")
                output.write(f"{'Hero,':<20}{'Pick,':>8}{'Ban,':>8}"
                             f"{'PWin,':>8}{'BWin':>7}\n")
                for hero in week:
                    output.write(f"{hero['HeroName'] + ',':<20}"
                                 f"{hero['PickRate']:>7},{hero['BanRate']:>7},"
                                 f"{hero['PickWinRate']:>7},{hero['BanWinRate']:>7}\n")


if __name__ == "__main__":
    spill_data(make_lists())