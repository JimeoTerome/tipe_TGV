import tkinter as tk

#dans cette représentation jeu[i][j] accède au jeu de ligne i et de colonne j
jeu = [[[[" "," "," "], [" "," "," "], [" ", " ", " "]] for i in range(3)] for i in range(3)]

#Pour garder trace des sous parties gagnées 
eval_ = [[0,0,0],
        [0,0,0],
        [0,0,0]]

#Sur quel sous jeu le joueur actuel est forcé à jouer
force = [-1,-1]

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
        print(eval_)
        if(est_fini(eval_) == 1): 
            print("Les croix gagnent !")
        elif(est_fini(eval_) == -1): 
            print("Les ronds gagnent !")
        elif(est_fini(eval_) == 42):
            print("match nul !")
    else:
        if([i,j] != force):
            print("Vous êtes forcé à jouer sur le sous jeu de coordonées : " + str(force))
        elif(case != " "):
            print("Quelqu'un à déjà joué là !")
        else:
            print("Erreur")
            
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
        print(eval_)
        if(est_fini(eval_) == 1): 
            print("Les croix gagnent !")
        elif(est_fini(eval_) == -1): 
            print("Les ronds gagnent !")
        elif(est_fini(eval_) == 42):
            print("match nul !")
    else:
        if([i,j] != force):
            print("Vous êtes forcé à jouer sur le sous jeu de coordonées : " + str(force))
        elif(case != " "):
            print("Quelqu'un à déjà joué là !")
        else:
            print("Erreur")

#evaluation de sous jeu
def eval_ssj(sous_jeu):
    for i in range(3):
        if(sous_jeu[i] == ["X"]*3):
            return 1
        elif(sous_jeu[i] == ["O"]*3):
            return -1
    for i in range(3):
        if(sous_jeu[0][i] == sous_jeu[1][i] and sous_jeu[0][i] == sous_jeu[2][i] and sous_jeu[0][i] != " "):
            if(sous_jeu[0][i] == "X"):
                return 1
            else:
                return -1
    if(sous_jeu[0][0] == "X" and sous_jeu[1][1] == "X" and sous_jeu[2][2] == "X"):
        return 1
    elif(sous_jeu[0][0] == "O" and sous_jeu[1][1] == "O" and sous_jeu[2][2] == "O"):
        return -1
    else:
        for i in range(3):
            for j in range(3):
                if(sous_jeu[i][j] == " "):
                    return 0
        return 42
    
def modif_eval_(jeu, eval_):
    for i in range(3):
        for j in range(3):
            eval_[i][j] = eval_ssj(jeu[i][j])

def est_fini(eval_):
    for i in range(3):
        if(eval_[i] == [1]*3):
            return 1
        elif(eval_[i] == [-1]*3):
            return -1
    for i in range(3):
        if(eval_[0][i] == eval_[1][i] and eval_[0][i] == eval_[2][i]):
            if(eval_[0][i] == 1):
                return 1
            elif(eval_[0][i] == -1):
                return -1
    if(eval_[0][0] == 1 and eval_[1][1] == 1 and eval_[2][2] == 1):
        return 1
    elif(eval_[0][0] == -1 and eval_[1][1] == -1 and eval_[2][2] == -1):
        return -1
    else:
        for i in range(3):
            for j in range(3):
                if(eval_[i][j] == 0):
                    return 0
        return 42

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