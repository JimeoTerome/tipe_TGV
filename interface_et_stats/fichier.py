couleur_IA = 1 # 1 si IA joue les X, 0 sinon

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

stat_sous_morpion = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]] # dans l'ordre de lecture // 1 : X ; 2 : 0 ; 3 : nul
