#C:/Users/Elève/AppData/Local/Microsoft/WindowsApps/python3.10.exe
import tkinter as tk
from copy import deepcopy

# Initialisation du super morpion
jeu = [[[[" ", " ", " "] for _ in range(3)] for _ in range(3)] for _ in range(3)]
eval_ = [[0 for _ in range(3)] for _ in range(3)]
force = [-1, -1]

# Pour l’IA
couleurbot = "O"
diff = [[0, 1, 0], [1, 2, 1], [0, 1, 0]]

def eval_ssj(sous_jeu):
    for i in range(3):
        if sous_jeu[i] == ["X"] * 3:
            return 1
        if sous_jeu[i] == ["O"] * 3:
            return -1
    for i in range(3):
        if sous_jeu[0][i] == sous_jeu[1][i] == sous_jeu[2][i] and sous_jeu[0][i] != " ":
            return 1 if sous_jeu[0][i] == "X" else -1
    if sous_jeu[0][0] == sous_jeu[1][1] == sous_jeu[2][2] and sous_jeu[0][0] != " ":
        return 1 if sous_jeu[0][0] == "X" else -1
    if sous_jeu[0][2] == sous_jeu[1][1] == sous_jeu[2][0] and sous_jeu[0][2] != " ":
        return 1 if sous_jeu[0][2] == "X" else -1
    for row in sous_jeu:
        if " " in row:
            return 0
    return 42  # Match nul

def modif_eval_(jeu, eval_):
    for i in range(3):
        for j in range(3):
            eval_[i][j] = eval_ssj(jeu[i][j])

def est_fini(eval_):
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
    if i < 0 or j < 0 or i > 2 or j > 2:
        return None
    for k in range(3):
        for l in range(3):
            if jeu[i][j][k][l] == " ":
                return (k, l)
    return None

def gagne(a, b, x, y):
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

def glouton1():
    global jeu, force, couleurbot, diff


    pos = possible(force[0], force[1])
    if pos:
        jouerO(force[0],force[1],pos[0],pos[1])
    else:
        positions = [(i, j) for i in range(3) for j in range(3)]
        positions.sort(key=lambda p: diff[p[0]][p[1]], reverse=True)
        for i, j in positions:
            for k in range(3):
                for l in range(3):
                    if jeu[i][j][k][l] == " ":
                        jouerO(i,j,k,l)
                        return
                    
import tkinter as tk

boutons = {}

joueur_X = True

def jouerX(i,j,k,l):
   global force
   global boutons
   global joueur_X
   global eval_
   print(eval_)
   case = jeu[i][j][k][l]
   if(([i,j] == force or force == [-1,-1]) and (case == " ") and (eval_[i][j] == 0)):
        jeu[i][j][k][l] = "X"
        boutons[i, j, k, l].config(text="X", disabledforeground="blue")
        boutons[i, j, k, l].config(state="disabled")
        eval_[k][l] = eval_ssj(jeu[k][l])
        joueur_X = False
        print(eval_[k][l])
        if(eval_[k][l] != 0):
           force = [-1,-1]
        else:
           force = [k,l]
        glouton1()
   else:
    if([i,j] != force):
        print("Vous êtes forcé à jouer sur le sous jeu de coordonées : " + str(force))
    elif(case != " "):
        print("Quelqu'un à déjà joué là !")
    else:
        print("Erreur")
    print("glouton 1 a jouer")
         
def jouerO(i,j,k,l):
   global force
   global boutons
   global joueur_X
   case = jeu[i][j][k][l]
   if(([i,j] == force or force == [-1,-1]) and (case == " ") and (eval_[i][j] == 0)):
       jeu[i][j][k][l] = "O"
       boutons[i, j, k, l].config(text="O", disabledforeground="red")
       boutons[i, j, k, l].config(state="disabled")
       eval_[k][l] = eval_ssj(jeu[k][l])
       joueur_X = True
       if(eval_[k][l] != 0):
           force = [-1,-1]
       else:
           force = [k,l]
   else:
       if([i,j] != force):
           print("Vous êtes forcé à jouer sur le sous jeu de coordonées : " + str(force))
       elif(case != " "):
           print("Quelqu'un à déjà joué là !")
       else:
           print("Erreur")








#========================================================================


#=============================Partie Tkinter=============================

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
#========================================================================








print(jeu)





