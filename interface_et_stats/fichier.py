def afiicher_plateau (plateau):
  for i in range (0,2):
    for j in range (0,2):
      for k in range (0,2):
        for l in range (0,2):
          if (plateau[i+k][j+l]==1) :
            print("X")
          if (plateau[i+k][j+l]==-1) :
            print("O")
          else print ("·")
          print (" ")
        print("| ")
      print ("\n")
