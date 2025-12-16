import gym # type: ignore
import numpy as np # type: ignore
import torch # type: ignore
import torch.nn as nn # type: ignore
import torch.optim as optim # type: ignore
from torch.distributions import Categorical # type: ignore

stat_sous_morpion = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]] # dans l'ordre de lecture // 1 : X ; 2 : 0 ; 3 : nul
couleur_IA = 1 # 1 si IA joue les X, 0 sinon


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
