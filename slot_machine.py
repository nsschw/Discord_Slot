import random
import pandas as pd


# Auszahlung für jede Kombination
payouts = {
    'shrek': 10,
    'drache': 7.5,
    'kater': 5,
    'esel': 3,
    'ass': 1,
    'koenig': 1,
    'koenigin': 0.5,
    'bube': 0.5,
    "10": 0.5}


symbols = ['shrek', 'drache', 'kater', 'esel', 'ass', 'koenig', 'koenigin', 'bube', "10"]
symbols_proba = [4, 5, 8, 10, 14, 14, 14, 15, 16]


# Funktion zum Drehen des Spielautomaten
def spin_field(x):
    return random.choices(symbols, weights=symbols_proba, k = 1)[0]

#Drehen von einer Spalte
def spin_col():
    x = 0
    col = []
    while x < 3:
        field = spin_field("_")        
        if field not in col:
            col.append(field)
            x += 1

    return col

# Drehen der 3 Reihen
def spin_bild():
    bild = pd.DataFrame(columns=["Col_1", "Col_2", "Col_3", "Col_4", "Col_5"], index=range(3))
    bild["Col_1"] = spin_col()
    bild["Col_2"] = spin_col()
    bild["Col_3"] = spin_col()
    bild["Col_4"] = spin_col()
    bild["Col_5"] = spin_col()
  
    return(bild)

#gets bild and calculates reward
def eval_bild(bild):

    reihen =[
        #Gerade linien
        [bild.at[0, "Col_1"], bild.at[0, "Col_2"], bild.at[0, "Col_3"], bild.at[0, "Col_4"], bild.at[0, "Col_5"]],
        [bild.at[1, "Col_1"], bild.at[1, "Col_2"], bild.at[1, "Col_3"], bild.at[1, "Col_4"], bild.at[1, "Col_5"]],
        [bild.at[2, "Col_1"], bild.at[2, "Col_2"], bild.at[2, "Col_3"], bild.at[2, "Col_4"], bild.at[2, "Col_5"]],         
    
        #Quere linien über das ganze Bild
        [bild.at[0, "Col_1"], bild.at[1, "Col_2"], bild.at[2, "Col_3"], bild.at[1, "Col_4"], bild.at[0, "Col_5"]],
        [bild.at[2, "Col_1"], bild.at[1, "Col_2"], bild.at[0, "Col_3"], bild.at[1, "Col_4"], bild.at[2, "Col_5"]],

        #halben queren linien
        [bild.at[1, "Col_1"], bild.at[0, "Col_2"], bild.at[0, "Col_3"], bild.at[0, "Col_4"], bild.at[1, "Col_5"]],
        [bild.at[1, "Col_1"], bild.at[2, "Col_2"], bild.at[2, "Col_3"], bild.at[2, "Col_4"], bild.at[1, "Col_5"]],

        #diagonale linien
        [bild.at[0, "Col_1"], bild.at[0, "Col_2"], bild.at[1, "Col_3"], bild.at[2, "Col_4"], bild.at[2, "Col_5"]],
        [bild.at[2, "Col_1"], bild.at[2, "Col_2"], bild.at[1, "Col_3"], bild.at[0, "Col_4"], bild.at[0, "Col_5"]],

        #Zickzack linie
        [bild.at[1, "Col_1"], bild.at[2, "Col_2"], bild.at[1, "Col_3"], bild.at[0, "Col_4"], bild.at[1, "Col_5"]]
    ]   


    #calculate rewards
    premium = ['shrek', 'drache', 'kater', 'esel']
    reward = 0
    scatter = 0
    hit_linien = []
    for nr_linie, reihe in enumerate(reihen):  


        #search for scatter
        for check in reihe:
            if check == "scatter":
                scatter += 1

        #get first symbol der reihe
        for i in range(5):
            if reihe[i] != "wild":
                symbol = reihe[i]
                break        

        #check how many in symbols in consecutive order are == symbol or == wild
        i = 0
        while i < 5:
            if (reihe[i] != symbol) and (reihe[i] != "wild"):
                break
            i += 1

        if (i == 2) and (symbol in premium):
            reward += payouts[symbol] * 0.5
            hit_linien.append(nr_linie)
        elif i == 3:
            reward += payouts[symbol] * 2
            hit_linien.append(nr_linie)
        elif i == 4:
            reward += payouts[symbol] * 4
            hit_linien.append(nr_linie)
        elif i == 5:
            reward += payouts[symbol] * 4
            hit_linien.append(nr_linie)

    if scatter > 2:
        freispiele = 1
    else:
        freispiele = 0

            

    return reward, hit_linien, freispiele


def play():

    bild = spin_bild()    
    reward, hit_linien, freispiele = eval_bild(bild)

    return bild, reward

    

if __name__ == "__main__":
    
    bild = spin_bild()    
    reward, hit_linien = eval_bild(bild)
    print(bild)
    print(hit_linien)