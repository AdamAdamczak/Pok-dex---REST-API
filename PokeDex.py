import sqlite3
import requests
import sys
import json
import pandas as pd
def pokeapi_get(poke_name: str):
    url = "https://pokeapi.co/api/v2/pokemon/"+poke_name.lower()
    poke_info = requests.get(url).json()
    return poke_info
def stats_get(poke_info):
    types = poke_info['types']
    type_1 = types[0]['type']['name']
    if len(types)>1:
        type_2 = types[1]['type']['name']
    else:
        type_2 = None

    
    poke_stats={    
    'HP': [poke_info['stats'][0]['base_stat']],
    'Attack': [poke_info['stats'][1]['base_stat']],
    'Defense': [poke_info['stats'][2]['base_stat']],
    'SpecialAttack': [poke_info['stats'][3]['base_stat']],
    'SpecialDefense': [poke_info['stats'][4]['base_stat']],
    'Speed': [poke_info['stats'][5]['base_stat']],
    'Type_1': [type_1],
    'Type_2': [type_2]
    
    }
    return poke_stats

def attack_against(attacker: str, attacked: str, database: pd.DataFrame):
    attacked_type1 = database['Type_1']
    attacked_type2 = database['Type_2']
    conn = sqlite3.connect("pokemon_against.sqlite")
    c = conn.cursor()
    if attacked_type2[0]==None:
        effect = c.execute(f"SELECT against_{attacked_type1[0]} FROM against_stats WHERE name='{attacker}'").fetchone()
    else:
        effect = c.execute(f"SELECT against_{attacked_type1[0]},against_{attacked_type2[0]} FROM against_stats WHERE name='{attacker}'").fetchone()
    print(f"{attacker.upper()} attacked {attacked.upper()}... Effectiveness: {effect}" )



def main():
    database = stats_get(pokeapi_get('Ditto'))
    attack_against('Ditto','Ditto',database)
    
if __name__ == '__main__':
    sys.exit(main())  

