def afiicher_plateau (plateau):
  for i in range (0,2):
    for j in range (0,2):
      for k in range (0,2):
        for l in range (0,2):
          print (plateau[i+k][j+l])
          print (" ")
        print("| ")
      print ("\n")
