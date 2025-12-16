import gym # type: ignore
import numpy as np # type: ignore
import torch # type: ignore
import torch.nn as nn # type: ignore
import torch.optim as optim # type: ignore
from torch.distributions import Categorical # type: ignore
import matplotlib.pyplot as plt

stat_sous_morpion = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]] # dans l'ordre de lecture // 1 : X ; 2 : 0 ; 3 : nul
victoireX=0
victoireO=0
victoireNulle=0
tab_des_goat=[]

class Stictactoe(gym.Env):

    def __init__(self):
        self.jeu = np.array([[-1 for i in range(9)] for i in range(9)])
        self.dernier_coup = None #à modifier

        self.actions = gym.spaces.Discrete(81)

    def reset(self):
        temp = self.jeu
        self.jeu = np.array([[-1 for i in range(9)] for i in range(9)])
        self.dernier_coup = None

        #gagnant = qui_a_gagne(temp)

        return self.jeu.copy()
    
    def step(self, action):
        return None
    
    def coup_autorise(self): 
        #la fonction renvoie la liste TOUS des coups autorisées
        #càd si on peux jouer où on veux on renvoie toutes les cases où personne n'a joué
        pass

def qui_a_gagne_morpion(plateau):
    '''Cette fonction prend en argument 
    un plateau de format tableau de 9 cases 
    et renvoie 
    0 si les ronds ont gagné 
    1 si les croix ont gagné
    -1 si c'est un match nul (ou non terminé) -> à voir dans le futur pour séparer ces deux cas
    '''

    for i in range(3):
        if (plateau[i] == plateau[i+1]) and (plateau[i+1] == plateau[i+2]):
            if (plateau[i] == 1) or (plateau[i] == 0):
                return plateau[i]

    for i in range(3):
        if (plateau[i] == plateau[i+3]) and (plateau[i+3] == plateau[i+6]):
            if (plateau[i] == 1) or (plateau[i] == 0):
                return plateau[i]
    
    if (plateau[0] == plateau[4]) and (plateau[4] == plateau[8]):
        if (plateau[0] == 1) or (plateau[0] == 0):
            return plateau[0]
        
    if (plateau[2] == plateau[4]) and (plateau[4] == plateau[6]):
        if (plateau[2] == 1) or (plateau[2] == 0):
            return plateau[2]
        
    return -1

def qui_a_gagne(plateau):
    '''
    Sur le meme principe que qui_a_gagne_morpion,
    cette fonction renvoie qui a gagné'''
    tempo = [-1 for i in range(9)]
    for i in range(9):
        tempo[i] = qui_a_gagne_morpion(plateau[i])
    return qui_a_gagne_morpion(tempo)

def afficher_plateau(plateau):
  for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if plateau[i][j] == 1:
                print("X", end=" ")
            elif plateau[i][j] == -1:
                print("O", end=" ")
            else:
                print("·", end=" ")
        print()


def fin_de_partie(plateau):
    global stat_sous_morpion
    global victoireX
    global victoireO
    global victoireNulle
    global tab_des_goat
    #pour faire une répartition de qui gagne quoi
    for i in range (9):
        if (qui_a_gagne_morpion(plateau[i])==0):
            stat_sous_morpion[i][1] +=1
        elif (qui_a_gagne_morpion(plateau[i])==0):
            stat_sous_morpion[i][0] +=1
        else:
            stat_sous_morpion[i][2] +=1
    #pour faire une stat de l'évolution des victoires
    if (qui_a_gagne(plateau)=0):
        victoireO +=1
        tab_des_goat.append(0)
    elif (qui_a_gagne(plateau)=1):
        victoireX +=1
        tab_des_goat.append(1)
    else :
        victoireNulle +=1
        tab_des_goat.append(-1)

def faire_des_stats(plateau):
    global stat_sous_morpion
    global victoireX
    global victoireO
    global victoireNulle
    global tab_des_goat
    total_par_sous_morpion = [sum(s) for s in stat_sous_morpion]
    plt.figure()
    plt.bar(range(1, 10), total_par_sous_morpion)
    plt.xlabel("Sous-morpion (1 à 9)")
    plt.ylabel("Nombre de parties")
    plt.title("Sous-morpions les plus joués/gagnés")
    plt.show()
    
    #
    
    plt.figure()
    plt.pie(
        [victoireX, victoireO, victoireNulle],
        labels=["X", "O", "Nul"],
        autopct="%1.1f%%"
    )
    plt.title("Répartition des résultats")
    plt.show()
    
    #
    
    x_cum = []
    o_cum = []
    n_cum = []
    
    cx = 0
    co = 0
    cn = 0
    
    for r in tab_des_goat:
        if r == "X":
            cx += 1
        elif r == "O":
            co += 1
        else:
            cn += 1
    
        x_cum.append(cx)
        o_cum.append(co)
        n_cum.append(cn)
    
    plt.figure()
    plt.plot(x_cum, label="X")
    plt.plot(o_cum, label="O")
    plt.plot(n_cum, label="Nul")
    plt.xlabel("Nombre de parties")
    plt.ylabel("Victoires cumulées")
    plt.title("Évolution des résultats dans le temps")
    plt.legend()
    plt.show()
    
