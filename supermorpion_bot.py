# Je ne garantis PAS que l'ensemble des fonctions est parfait, mais +100 000 parties ont été jouées.
# Voir le compte rendu du 15 septembre pour comprendre l'ensemble des modifications
# Merci de garder une lisibilité correcte du code


#======================Déclaration===========================
import tkinter as tk
from copy import deepcopy
import random
jeu = [[[[" ", " ", " "] for _ in range(3)] for _ in range(3)] for _ in range(3)]
eval_ = [[0 for _ in range(3)] for _ in range(3)]
force = [-1, -1]
diff = [[0, 1, 0], [1, 2, 1], [0, 1, 0]]
bot=""
couleurbot = "O" #nom un peu bizarre; plutot comprendre couleur associée à bot. couleur associée à bot2 en découle
bot2=""
boutons = {}
joueur_X = True
affichage = True
victoireX=0
victoireO=0
Nulle=0

#==============================Fonctions d'évaluation===========================

#Ce paragraphe date de MP2I et semble plutot fonctionnel. Cependant, je ne me souvient pas vraiment du fonctionnement exact de tout. A voir pour rendre le tout plus explicite

def eval_ssj(sous_jeu):
    # Lignes
    for i in range(3):
        if sous_jeu[i] == ["X"] * 3:
            return 1
        if sous_jeu[i] == ["O"] * 3:
            return -1
    # Colonnes
    for i in range(3):
        if sous_jeu[0][i] == sous_jeu[1][i] == sous_jeu[2][i] != " ":
            return 1 if sous_jeu[0][i] == "X" else -1
    # Diagonales
    if sous_jeu[0][0] == sous_jeu[1][1] == sous_jeu[2][2] != " ":
        return 1 if sous_jeu[0][0] == "X" else -1
    if sous_jeu[0][2] == sous_jeu[1][1] == sous_jeu[2][0] != " ":
        return 1 if sous_jeu[0][2] == "X" else -1
    # Cases vides
    for row in sous_jeu:
        if " " in row:
            return 0
    # Match nul
    return 42 # Si on remarque un bug dans totalite avec écrit 42, l'erreur vient d'ici. Normalement déjà réglé mais s'il y a des erreurs on peut s'intéresser à cette partie (pb régler avec la réinitialsation des variables)

def modif_eval_(jeu, eval_):
    for i in range(3):
        for j in range(3):
            eval_[i][j] = eval_ssj(jeu[i][j])

def est_fini(eval_):
    """
    Vérifie si la partie est finie
    """
    for i in range(3):
        if eval_[i] == [1]*3:
            return 1
        if eval_[i] == [-1]*3:
            return -1
    for i in range(3):
        if eval_[0][i] == eval_[1][i] == eval_[2][i] and eval_[0][i] != 0:
            return eval_[0][i]
    if eval_[0][0] == eval_[1][1] == eval_[2][2] and eval_[0][0] != 0:
        return eval_[0][0]
    if eval_[0][2] == eval_[1][1] == eval_[2][0] and eval_[0][2] != 0:
        return eval_[0][2]
    for i in range(3):
        for j in range(3):
            if eval_[i][j] == 0:
                return 0
    return 42  # match nul


def possible(i, j):
    """
    vérifie si un ssj n'est pas rempli
    """
    if i < 0 or j < 0 or i > 2 or j > 2:
        return None
    for k in range(3):
        for l in range(3):
            if jeu[i][j][k][l] == " ":
                return (k, l)
    return None

def gagne(a, b, x, y):
    """
    vérifie si le coup a b est gagnant #===A VERIFIER===
    """
    M = deepcopy(jeu)
    M[a][b][x][y] = couleurbot
    # lignes
    for i in range(3):
        if all(M[a][b][i][j] == couleurbot for j in range(3)):
            return True
    # colonnes
    for j in range(3):
        if all(M[a][b][i][j] == couleurbot for i in range(3)):
            return True
    # diagonales
    if all(M[a][b][i][i] == couleurbot for i in range(3)):
        return True
    if all(M[a][b][i][2 - i] == couleurbot for i in range(3)):
        return True
    return False


#==========================Fonctions de jeu======================================

def botj(n):
    """
    Déclenche les bots et compte le scrore
    glouton1 pour le glouton1
    alea1 pour aleatoire1
    c et d permettent de savoir qui doit jouer (du principe qu'on ne peut pas jouer et devoir jouer succesivement)
    la fonction est à adaptée au fur et à mesure des algo mis en place
    """
    global bot, couleurbot, bot2, victoireX, victoireO, Nulle, force

    fin = est_fini(eval_)
    if fin == 1:
        #print("Les X ont gagnés")
        victoireX += 1
        return
    elif fin == -1:
        #print("Les O ont gagnés")
        victoireO += 1
        return
    elif fin == 42:
        #print("Nul")
        Nulle += 1
        return

    # Si force pointe sur une sous-grille terminée, on la réinitialise
    if force != [-1, -1] and eval_[force[0]][force[1]] != 0:
        force = [-1, -1]

    c, d = (1, 0) if couleurbot == "X" else (0, 1)

    if bot == "glouton1" and c + n == 1:
        glouton1()
    elif bot == "alea1" and c + n == 1:
        aleatoire1()

    if bot2 == "glouton1" and d + n == 1:
        glouton1()
    elif bot2 == "alea1" and d + n == 1:
        aleatoire1()

def jouerX(i,j,k,l):
   """
   la fonction appelle elle même le glouton à jouer
   la fonction comporte une série de test assurant qu'aucun coup illégal est jouable
   """
   global force
   global boutons
   global joueur_X
   global eval_
   case = jeu[i][j][k][l]
   if(([i,j] == force or force == [-1,-1]) and (case == " ") and (eval_[i][j] == 0)):
        jeu[i][j][k][l] = "X"
        if (affichage):
            boutons[i, j, k, l].config(text="X", disabledforeground="blue")
            boutons[i, j, k, l].config(state="disabled")
        eval_[i][j] = eval_ssj(jeu[i][j])
        joueur_X = False
        if(eval_[k][l] != 0):
           force = [-1,-1]
        else:
           force = [k,l]
        botj(1)
   else:
    if([i,j] != force):
        print("Vous êtes forcé à jouer sur le sous jeu de coordonées : " + str(force))
    elif(case != " "):
        print("Quelqu'un à déjà joué là !")
    else:
        print("Erreur")

         
def jouerO(i,j,k,l):
    """
   la fonction appelle elle même le glouton à jouer
   la fonction comporte une série de test assurant qu'aucun coup illégal est jouable
    """
    global force
    global boutons
    global joueur_X
    case = jeu[i][j][k][l]
    if(([i,j] == force or force == [-1,-1]) and (case == " ") and (eval_[i][j] == 0)):
        jeu[i][j][k][l] = "O"
        if(affichage):
            boutons[i, j, k, l].config(text="O", disabledforeground="red")
            boutons[i, j, k, l].config(state="disabled")
        eval_[i][j] = eval_ssj(jeu[i][j])
        joueur_X = True
        if(eval_[k][l] != 0):
            force = [-1,-1]
        else:
            force = [k,l]
        botj(0)
    else:
        if([i,j] != force):
            print("Vous êtes forcé à jouer sur le sous jeu de coordonées : " + str(force))
        elif(case != " "):
            print("Quelqu'un à déjà joué là !")
        else:
            print("Erreur")


def totalite(n):
    """"
    fais des tests, non compatible avec affichage
    """
    global victoireX, victoireO, Nulle, joueur_X, eval_, force, diff, jeu
    for a in range(n):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        jeu = [[[[" ", " ", " "] for _ in range(3)] for _ in range(3)] for _ in range(3)]
                        eval_ = [[0 for _ in range(3)] for _ in range(3)]
                        force = [-1, -1]
                        diff = [[0, 1, 0], [1, 2, 1], [0, 1, 0]]
                        joueur_X=True
                        jouerX(i,j,k,l)
                        jeu = [[[[" ", " ", " "] for _ in range(3)] for _ in range(3)] for _ in range(3)]
                        eval_ = [[0 for _ in range(3)] for _ in range(3)]
                        force = [-1, -1]
                        diff = [[0, 1, 0], [1, 2, 1], [0, 1, 0]]
                        joueur_X=False
                        jouerO(i,j,k,l)
        if (a%20==0):
            print(a)
    print("Score:\n",bot," : ",victoireX,"\n", bot2, " : ",victoireO,"\nNulle:",Nulle,"\nTOTAL = ",n*81*2)
    victoireX=0
    victoireO=0
    Nulle=0



#=============================Gloutons=============================

def glouton1():
    """
    Glouton O(1)
    priorités
    1. Coup gagnant
    2. Bloquer adversaire
    3. Centre
    4. Premier coup libre
    """
    global jeu, force, couleurbot, diff, joueur_X

    adv = "X" if couleurbot == "O" else "O"

    def coup_gagnant(i, j):
        for k in range(3):
            for l in range(3):
                if jeu[i][j][k][l] == " " and gagne(i, j, k, l):
                    return (k, l)
        return None

    def bloque_adv(i, j):
        for k in range(3):
            for l in range(3):
                if jeu[i][j][k][l] == " ":
                    M = deepcopy(jeu)
                    M[i][j][k][l] = adv
                    if eval_ssj(M[i][j]) == (1 if adv == "X" else -1):
                        return (k, l)
        return None

    # Sous-grilles possibles
    positions = []
    if force != [-1, -1] and eval_[force[0]][force[1]] == 0:
        positions = [force]
    else:
        positions = [(i, j) for i in range(3) for j in range(3) if eval_[i][j] == 0]

    if not positions:
        return  # Plus de coups possibles, partie finie

    # Trier par priorité diff
    positions.sort(key=lambda p: diff[p[0]][p[1]], reverse=True)

    for i, j in positions:
        # 1. Coup gagnant
        pos = coup_gagnant(i, j)
        if pos:
            if joueur_X:
                jouerX(i, j, pos[0], pos[1])
            else:
                jouerO(i, j, pos[0], pos[1])
            return
        # 2. Bloquer adversaire
        pos = bloque_adv(i, j)
        if pos:
            if joueur_X:
                jouerX(i, j, pos[0], pos[1])
            else:
                jouerO(i, j, pos[0], pos[1])
            return
        # 3. Centre
        if jeu[i][j][1][1] == " ":
            if joueur_X:
                jouerX(i, j, 1, 1)
            else:
                jouerO(i, j, 1, 1)
            return
        # 4. Premier coup libre
        pos = possible(i, j)
        if pos:
            if joueur_X:
                jouerX(i, j, pos[0], pos[1])
            else:
                jouerO(i, j, pos[0], pos[1])
            return


def aleatoire1():
    """
    joue aléatoirement parmis les coups disponibles
    """
    global jeu, force, bot, joueur_X, couleurbot
    sous_grilles = []
    if force != [-1, -1] and eval_[force[0]][force[1]] == 0:
        sous_grilles = [force]
    else:
        for i in range(3):
            for j in range(3):
                if eval_[i][j] == 0:
                    sous_grilles.append([i, j])
    i, j = random.choice(sous_grilles)
    cases_libres = [(k, l) for k in range(3) for l in range(3) if jeu[i][j][k][l] == " "]
    k, l = random.choice(cases_libres)
    if joueur_X == True:
        jouerX(i, j, k, l)
    else:
        jouerO(i, j, k, l)





#=============================Partie Tkinter=============================

if(affichage):

    fenetre = tk.Tk()
    fenetre.title("Super Morpion")
    fenetre.geometry("1000x1000")
    
    main_frame = tk.Frame(fenetre, bg="gray", width=60*9, height=60*9)
    main_frame.pack()
    
    
    
    def clic_case(i, j, k, l):
       global joueur_X
       print("Joueur courant :", "X" if joueur_X else "O")
       if joueur_X:
           jouerX(i,j,k,l)
       else:
           jouerO(i,j,k,l)
    
    
    for i in range(3):
       for j in range(3):
           sous_grille = tk.Frame(main_frame, bg="black", width=80*3, height=80*3)
           sous_grille.grid(row=i, column=j, padx=2, pady=2)
           for k in range(3):
               for l in range(3):
                   btn = tk.Button(
                       sous_grille,
                       text="",
                       font=("Helvetica", 18, "bold"),
                       width=4,
                       height=2,
                       command=lambda i=i, j=j, k=k, l=l: clic_case(i, j, k, l)
                   )
                   btn.grid(row=k, column=l, padx=1, pady=1)
                   boutons[i, j, k, l] = btn
    
    
    fenetre.mainloop()

print(jeu)
