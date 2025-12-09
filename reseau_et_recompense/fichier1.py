import gym # type: ignore
import numpy as np # type: ignore
import torch # type: ignore
import torch.nn as nn # type: ignore
import torch.optim as optim # type: ignore
from torch.distributions import Categorical # type: ignore

class PolitiqueSTicTacToe(nn.Module):
    def __init__(self):
        super(PolitiqueSTicTacToe, self).__init__()
        #fc veut dire fully connected
        self.fc1 = nn.Linear(81,256)
        self.fc2 = nn.Linear(256,512)
        self.fc3 = nn.Linear(512,256)
        self.fc4 = nn.Linear(256,81)

        self.relu = nn.ReLU()

    def forward(self,x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.fc4(x)

        return x 

def calcule_recomp(etat_avant,etat_apres,symbole):
    '''etat_avant -> l'etat avant que l'IA ai joué
        etat_apres -> l'etat après que l'IA ai joué
        symbole -> le symbole joué par l'IA 0 pour les ronds et 1 pour les croix
        effet : calcule la recompense càd renvoie 1 si un grille a été gagné, -1 si une a été perdu et 0 sinon'''
    tab1 = [-1 for i in range(9)]
    tab2 = [-1 for i in range(9)]
    for i in range(9):
        tab1[i] = qui_a_gagne_morpion(etat_avant[i])   
        tab2[i] = qui_a_gagne_morpion(etat_apres[i])
    for i in range(9): 
        if tab1[i] != tab2[i]:
            if tab2[i] == symbole:
                return 1
            else: 
                return -1
    return 0


#Cette fonction ne marche pas
def entrainement(politique, environement, nb_ep, symbole,taux_appr=10**(-3)):
    recomps_episodes = []
    optimisateur = optim.Adam(politique.parameters(),lr = taux_appr)
    if symbole == 0:
        opp_symbole = 1
    else:
        opp_symbole = 0
    for episodes in range(nb_ep):
        etat = environement.reset()
        etat = torch.tensor(etat, dtype=torch.float32).flatten()
        log_probs =[]
        fini = False 
        recomp = []
        while not(fini): 
            valeurs = politique(etat) 

            actions = environement.coup_autorise()
            coup_legal = valeurs.clone()
            masque_coup_interdit =torch.ones_like(valeurs, dtype = torch.bool)
            masque_coup_interdit[actions] = False
            coup_legal[masque_coup_interdit] = - 1e9

            choix = Categorical(logits=coup_legal)
            action = choix.sample()

            log_probs.append(choix.log_prob(action))

            prochain_etat, r ,fini, _= environement.step(action) #celle-ci aussi puisque on a pas la fonction step
            recomp.append(r)
            etat = torch.tensor(prochain_etat, dtype=torch.float32).flatten()
            if fini:
                temp = qui_a_gagne(etat)
                if temp == symbole :
                    recomp.append(9)
                else:
                    recomp.append(-3)
        recompense_final_ep = sum(recomp)
        recomps_episodes.append(recompense_final_ep)    
        perte = 0
        for log_prob in log_probs:
            perte += -log_prob * recompense_final_ep
        optimisateur.zero_grad()
        perte.backward()
        optimisateur.step()
    return recomps_episodes
