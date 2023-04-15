import pandas as pd
import pickle
import json

def check_win(zahl, reward):
    if zahl > reward:
        return 1
    else:
        return 0

#Returns Rarity of spin
def get_rarity(reward):
    df = pd.read_pickle("Daten/Proba_Spins.pickle")
    df = df["Gewinn"].apply(lambda x: check_win(x, reward))
    odds = df.value_counts()
    return round(odds[1] / len(df) * 100, 3)

#Checks whether spin this big has been already recorded
def get_daily_big_hit(reward):
    daten = [json.loads(line) for line in open("Daten/log.jsonl", "r", encoding="utf-8")]  

    max_reward_h = 0
    for spin in daten:
        max_reward_h = max(spin["reward"], max_reward_h)

    if reward > max_reward_h:
        return 1
    else:
        return 0


if __name__ == "__main__":
    x = get_daily_big_hit(2.1)
    print(x)