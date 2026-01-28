import numpy as np # type: ignore
import torch # type: ignore
import torch.nn as nn # type: ignore
import torch.optim as optim # type: ignore
from torch.distributions import Categorical # type: ignore
import random

#================= La partie des autres sur Github  ================


#fonction qui est nulle
"""def printM(tab):
    print("================================")
    for i in range(9):
        chaine = ""
        for j in range(9):
            if tab[i*9+j] == 1:
                chaine += "X |"
            elif tab[i*9+j] == 0:
                chaine += "O |"
            else:
                chaine += "  |"
        print(chaine) """

def printM(tab):
    print("=" * 50)
    for ligne_grille in range(3):
        for ligne_case in range(3):
            ligne_affichage = ""
            for col_grille in range(3):
                sous_tableau = ligne_grille * 3 + col_grille
                for col_case in range(3):
                    case = ligne_case * 3 + col_case
                    indice = sous_tableau * 9 + case
                    if tab[indice] == 1:
                        ligne_affichage += "X "
                    elif tab[indice] == 0:
                        ligne_affichage += "O "
                    else:
                        ligne_affichage += ". "
                if col_grille < 2:
                    ligne_affichage += "| "
            print(ligne_affichage)
        if ligne_grille < 2:
            print("-" * 50)

class Stictactoe():

    def __init__(self):
        self.jeu = np.array([[-1 for i in range(9)] for i in range(9)])
        self.dernier_coup = None #None si l'utilisateur qui doit jouer peux jouer où il veut un entier entre 0 et 8 sinon

    def reset(self):
        self.jeu = np.array([[-1 for i in range(9)] for i in range(9)])
        self.dernier_coup = None
        #gagnant = qui_a_gagne(temp)
        return self.jeu.copy()
    
    def jouer_coup(self,action,symbole):
        """Joue un coup pour le symbole qui est 0 ou 1"""
        avant = self.jeu.copy()
        i1 = action//9 #le sous tableau où on joue
        j1 = action % 9 #la case dans ce sous tableau

        temp = qui_a_gagne_morpion(self.jeu[i1])
        if temp != -1:
            raise ValueError("Bug on peut pas jouer dans le sous tab " + str(i1))
        
        temp = qui_a_gagne_morpion(self.jeu[j1])

        self.jeu[i1][j1] = symbole

        if temp != -1:
            self.dernier_coup = None
        else:
            self.dernier_coup = j1

        apres = self.jeu.copy()
        recompense = calcule_recomp(avant,apres,symbole)
        
        return apres, recompense

    def stepIA(self,action,symbole):
        r = 0
        apres,recomp = self.jouer_coup(action,symbole)
        r += recomp

        resultat = qui_a_gagne(apres)

        if resultat == 0 or resultat == 1 or resultat == -2:
            #printM(self.jeu.flatten())
            return apres, r, True, 0
        
        #printM(self.jeu.flatten())
        return apres,r,False,0
    
    def stepRandom(self,symbole):
        r = 0
        coup_autorise = self.coup_autorise()
        if len(coup_autorise) == 0:
            print("Naaaaaan")
            printM(self.jeu.flatten())
            return self.jeu.copy(), r, True, 0
        
        k = random.choice(coup_autorise)
        apres,recomp = self.jouer_coup(k,symbole)
        r -= recomp
        resultat = qui_a_gagne(apres)
        if resultat == 0 or resultat == 1 or resultat == -2:
            #printM(self.jeu.flatten())
            return apres, r, True, 0 #je ne sais pas ce que doit être la dernière valeur
        
        #printM(self.jeu.flatten())
        return apres,r,False,0
    
    def coup_autorise(self): 
        #la fonction renvoie la liste TOUS des coups autorisées
        #càd si on peux jouer où on veux on renvoie toutes les cases où personne n'a joué
        retour = []
        temp = self.jeu.copy()
        temp = temp.flatten()
        if self.dernier_coup == None:
            for i in range(9):
                etat = qui_a_gagne_morpion(self.jeu[i])
                if etat == -1:
                    for j in range(9):
                        indice = i*9+j
                        if temp[indice] == -1:
                            retour.append(indice)
        else:
            etat = qui_a_gagne_morpion(self.jeu[self.dernier_coup])
            if etat == -1:
                for i in range(9):
                    indice = self.dernier_coup * 9 + i
                    if temp[indice] == -1:
                        retour.append(indice)
            else:
                for i in range(9):
                    etat_bis = qui_a_gagne_morpion(self.jeu[i])
                    if etat_bis == -1:
                        for j in range(9):
                            indice = i*9+j
                            if temp[indice] == -1:
                                retour.append(indice)
        return retour



def qui_a_gagne_morpion(plateau):
    '''Cette fonction prend en argument 
    un plateau de format tableau de 9 cases 
    et renvoie 
    0 si les ronds ont gagné 
    1 si les croix ont gagné
    -2 si c'est un match nul (ou non terminé) -> à voir dans le futur pour séparer ces deux cas
    -1 si ce n'est pas terminé
    '''

    for i in range(3):
        indice = i*3
        if (plateau[indice] == plateau[indice+1]) and (plateau[indice+1] == plateau[indice+2]):
            if (plateau[indice] == 1) or (plateau[indice] == 0):
                return plateau[indice]

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
    
    for i in range(9):
        if plateau[i] == -1:
            return -1
        
    return -2

def qui_a_gagne(plateau):
    '''
    Sur le meme principe que qui_a_gagne_morpion,
    cette fonction renvoie qui a gagné sauf comportement
    indeterminé si c'est pas rond ou croix qui a gagné'''
    tempo = [-1 for i in range(9)]
    for i in range(9):
        tempo[i] = qui_a_gagne_morpion(plateau[i])
    return qui_a_gagne_morpion(tempo)

#================== Ma partie à mettre sur Github ==================

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

def entrainement(politique, environement, nb_ep, symbole,taux_appr=1e-3):
    recomps_episodes = []
    if symbole == 0:
        symbole_adv = 1
    else:
        symbole_adv = 0
    optimisateur = optim.Adam(politique.parameters(),lr = taux_appr)
    for episodes in range(nb_ep):
        etat = environement.reset()
        etat = torch.tensor(etat, dtype=torch.float32).flatten()
        log_probs =[]
        fini = False 
        recomp = []
        while not(fini):
            if symbole == 1:
                coup = choix_coup_IA(politique,environement,log_probs,etat)
                prochain_etat, r ,fini, _= environement.stepIA(coup,1)
                etat = torch.tensor(prochain_etat, dtype=torch.float32).flatten()
                if fini:
                    temp = qui_a_gagne(prochain_etat)
                    if temp == symbole :
                        r += 9
                    elif temp == symbole_adv:
                        r-= 9
                else:
                    prochain_etat,r2, fini, _ = environement.stepRandom(0)
                    r += r2 #r2 est négatif
                    etat = torch.tensor(prochain_etat, dtype=torch.float32).flatten()
                    if fini :
                        temp = qui_a_gagne(prochain_etat)
                        if temp == symbole:
                            r+=9
                        elif temp == symbole_adv:
                            r-=9
            else:
                prochain_etat,r, fini, _ = environement.stepRandom(1)
                etat = torch.tensor(prochain_etat, dtype=torch.float32).flatten()
                if fini:
                    temp = qui_a_gagne(prochain_etat)
                    if temp == symbole:
                        r += 9
                    elif temp == symbole_adv:
                        r -= 9
                else: 
                    coup = choix_coup_IA(politique,environement,log_probs,etat)
                    prochain_etat, r2 ,fini, _= environement.stepIA(coup,0)
                    r += r2
                    etat = torch.tensor(prochain_etat, dtype=torch.float32).flatten()
                    if fini:
                        temp = qui_a_gagne(prochain_etat)
                        if temp == symbole :
                            r += 9
                        elif temp == symbole_adv:
                            r-= 9
            recomp.append(r)
        recompense_final_ep = sum(recomp)
        recomps_episodes.append(recompense_final_ep)    
        perte = 0
        for log_prob in log_probs:
            perte += -log_prob * recompense_final_ep
        optimisateur.zero_grad()
        perte.backward()
        optimisateur.step()

    return recomps_episodes

def choix_coup_IA(politique, environement,log_probs,etat):
    valeurs = politique(etat) 

    actions = environement.coup_autorise()
    coup_legal = valeurs.clone()
    masque_coup_interdit =torch.ones_like(valeurs, dtype = torch.bool)
    masque_coup_interdit[actions] = False
    coup_legal[masque_coup_interdit] = - 1e9
    choix = Categorical(logits=coup_legal)
    action = choix.sample()

    log_probs.append(choix.log_prob(action))

    coup = action.item()
    return coup

reseau = PolitiqueSTicTacToe()
environement = Stictactoe()
nb_ep = 100
symbole = 0
print(entrainement(reseau,environement,nb_ep,symbole))
torch.save(reseau.state_dict(),"Poids_stictactoe.pth")
