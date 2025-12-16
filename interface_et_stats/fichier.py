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
