#---------------------------------------------------------------------------------------------------------
#                                        
#                                       Projet Théorie des graphes 
#                                                   2021
#
#---------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------
#                        Classes              
#----------------------------------------------------------------
class graphe :
    def __init__(self):
        self.nb_sommets = 0
        self.nb_arc = 0
        self.arc = []
        self.tab = [] # Stockera la matrice d'adjacence
        self.tab_valeurs = [] # Stockera la matrice d'adjacence avec les valeurs 
        self.tab_distance_init = []
        self.tab_distance = [] # Stockera de Floyd-Warshall la matrice des distances
        self.tab_chemin_init = []
        self.tab_chemin = [] # Stockera de Floyd-Warshall la matrice des chemins 
    
    def afficher(self):
        print("Nombre de sommets : ", self.nb_sommets, "\nNombre d'arcs : ", self.nb_arc)
        print("\nLes arcs : ")
        for i in range(int(self.nb_arc)):
            self.arc[i].afficher2()
    
class arc :     
    def __init__(self):
        self.extremite_init = 0
        self.extremite_term = 0
        self.valeur = 0
    
    def afficher2(self):
        print(self.extremite_init, self.extremite_term, self.valeur)

#----------------------------------------------------------------
#                        Fonctions              
#----------------------------------------------------------------


## Fonction permettant à l'utilisateur de choisir le graphe à analyser 
def choisir_graphe():
  numero = input("\nQuel est le numéro du graphe souhaité ? ")
  
  while numero.isdigit() == False or (int(numero) < 1 or int(numero) > 13):
    print("\nVotre saisie est invalide. Veuillez ressaisir un numéro entre 1 et 13.") 
    numero = input("Quel est votre choix ? ")
  return str(numero)


## Fonction permettant de récupérer un graphe donné en .txt grâce à son numéro
def lire_graphe(indice):
  fichier = "J3-graphe-" + indice + ".txt" 
  
  try :
    with open(fichier, "r") as fichier :
      temp = fichier.read().splitlines()
  except IOError :
    print("L'ouverture du fichier est impossible.\n")

  return temp


## Fonction permettant de créer un objet de la classe graphe à partir des éléments récupérés par la lecture du fichier .txt
def creer_graphe(tableau):
  gra.nb_sommets = tableau[0] # On rentre d'abord les éléments fixes, soit le nombre de sommet et d'arc
  gra.nb_arc = tableau[1]

  for i in range (2, len(tableau)): # Boucle qui permet de récupérer les arcs dans la classe graphe
    arc_temp = arc() # On utilise un arc temporaire que l'on remet ensuite dans gra une fois que les valeurs sont ajoutées
    temp = tableau[i].split() # On sépare une ligne en un tableau (chaque espace représente une nouvelle case)
    arc_temp.extremite_init = temp[0]
    arc_temp.extremite_term = temp[1]
    arc_temp.valeur = temp[2]
    gra.arc.append(arc_temp)
        

## Fonction permettant de créer la matrice d'adjacence
def creation_matrice_adj(gra):
  matrice_adj=[[0]*int(gra.nb_sommets) for k in range(int(gra.nb_sommets))] # Création matrice 2d ayant nb_sommets comme nombre de colonnes et de lignes
  ligne=0
  colonne=0
  
  # Boucle pour le parcours de la liste d'arcs du graphe
  for ligne in range (int(gra.nb_sommets)):
    for colonne in range (int(gra.nb_sommets)):
      for i in range(int(gra.nb_arc)):
        if int(gra.arc[i].extremite_init)==ligne and int(gra.arc[i].extremite_term)==colonne: # Condition pour vérifier si l'arc existe
          matrice_adj[ligne][colonne]=1  
  
  # Enregistrement des données dans notre classe graphe
  gra.tab = matrice_adj  
  return matrice_adj  


## Fonction permettant de créer la matrice d'adjacence avec les valeurs 
def creation_matrice_valeur(gra):
  matrice_valeur=[[0]*int(gra.nb_sommets) for k in range(int(gra.nb_sommets))] # Création matrice 2d ayant nb_sommets comme nombre de colonnes et de lignes
  ligne=0
  colonne=0

  # Boucle pour le parcours de la liste d'arcs du graphe
  for ligne in range (int(gra.nb_sommets)):
    for colonne in range (int(gra.nb_sommets)):
      for i in range(int(gra.nb_arc)):
        if int(gra.arc[i].extremite_init)==ligne and int(gra.arc[i].extremite_term)==colonne: # Condition pour vérifier si l'arc existe
          matrice_valeur[ligne][colonne]=int(gra.arc[i].valeur)  
  
  # Enregistrement des données dans notre classe graphe
  gra.tab_valeurs = matrice_valeur  
  return matrice_valeur


def afficher_matrice(matrice):
  my_color= ["\033[0m", "\033[34m", "\033[32m", "\033[33m"] # On génère les couleurs - white + purple + green
  
  # Parcours de la matrice pour récupérer le plus grand nombre de digits dans un chiffre
  MaxLen = len(str(matrice[0][0])) 
  for i in range(len(matrice)):
    for j in range(len(matrice[0])):
      if int(MaxLen) < len(str(matrice[i][j])):
        MaxLen = len(str(matrice[i][j]))
  
  # Ajout des valeurs en colonne (extremité_terminale)  
  print("  ", end = " ")
  for k in range(len(matrice)):
    print(my_color[1], str(k) + int(MaxLen - len(str(k)) + 1) * " ", end = "")
  print(my_color[0], "\n")
  
  # Ajout des valeurs en ligne (extremité_initiale)
  for i in range(len(matrice)):
    print(my_color[1], i, end = "  ")    
    for j in range (len(matrice[i])):
      if matrice[i][j] == 0:
        print(my_color[2], end = "") 
      elif matrice[i][j] == -1 or str(matrice[i][j]) == 'inf':
        print(my_color[3], end = "")
      else: 
        print(my_color[2], end = "")
      print(str(matrice[i][j]) + int(MaxLen - len(str(matrice[i][j])) + 1) * " ", end = " ") # Permet de calculer le nombre d'espaces entre MaxLen - longueur du nombre actuel + 1
    print(my_color[0], "\n")
  return matrice


## Fonction permettant d'afficher les chemins les plus courts et leurs valeurs (coûts)
def aff_chemin(chemin,distance, sortie = None):
  N = len(chemin)
  for i in range(N) :
    for j in range(N) :
      if chemin[i][j] != -1 :
        print("Le chemin le plus court en partant de",i,"vers",j," : (",i,end = " ")
        print("Le chemin le plus court en partant de",i,"vers",j," : (",i,end = " ", file=sortie) #la variable "sortie" correspond au lieu d'écriture (console ou fichier)
        temp = j
        x=0
        tab=[]
        while chemin[i][temp] != i :
          tab.append(chemin[i][temp])
          temp = chemin[i][temp]
          x=x+1
        for y in reversed(tab):
           print(y,end = " ")
           print(y,end = " ", file=sortie) 
        print(j,")")
        print(j,")", file=sortie)


## Fonction exécutant l'algorithme de Floyd-Warshall 
def floydWarshall(matrice, gra):
  N = len(matrice)
  distance = matrice
  for i in range(N) :
    for j in range(N):
      if distance[i][j] == 0 :
        distance[i][j] = float('inf')
      if distance[i][i] == float('inf'): # Initialiser la diagonale
        distance[i][i] = 0
     
  print("Matrice Distance initiale : \n")
  afficher_matrice(distance)

  # Enregistrement des données dans notre classe graphe
  gra.tab_distance_init = distance

  chemin = [[-1 for x in range(N)] for y in range(N)]    # Initialiser tout à -1

  for i in range(N):
    for j in range(N):
      if i != j and distance[i][j] != float('inf') :
        chemin[i][j] = i
    chemin[i][i] = i
      
  print("\nMatrice Chemin initiale : \n")
  afficher_matrice(chemin)

  # Enregistrement des données dans notre classe graphe
  gra.tab_chemin_init = chemin

  # Voir k comme intermédiaire, j comme arrivé et i comme départ             
  for k in range(N):
    for i in range(N):
      for j in range(N):
        if distance[i][k] + distance[k][j] < distance[i][j]:
          distance[i][j] = distance[i][k] + distance[k][j]
          chemin[i][j] = chemin[k][j]
        
        if distance[i][i] < 0:  
          print("\n======= Itération numéro",k+1, "=======")
          print("\nMatrice Distance : \n")
          afficher_matrice(distance)
          gra.tab_distance = distance
          print("Circuit absorbant")
          trace_execution(indice, gra, k+1, "Algorithme de Floyd-Warshall", circuit = True, der_iter = True) # Si on a un cycle alors on sort directement de la fonction. Les matrices matrices initiales vont donc être affichées dans le fichier texte.
          return 0    
        
    print("\n======= Itération numéro",k+1, "=======")
    print("\nMatrice Distance : \n")
    afficher_matrice(distance)
    print("\nMatrice Chemin : \n")
    afficher_matrice(chemin)
    
    # Enregistrement des données dans notre classe graphe
    gra.tab_distance = distance
    gra.tab_chemin = chemin

    # Teste si on est à la dernière itération
    if (k == N-1):
      trace_execution(indice, gra, k+1, "Algorithme de Floyd-Warshall", der_iter = [chemin, distance])
    else : 
      trace_execution(indice, gra, k+1, "Algorithme de Floyd-Warshall")
          
  return 1  


## Fonction qui enregistre les différentes procédures pour le graphe étudié
def trace_execution(indice, gra, numero, etape, der_iter = False, circuit = False): # Der_iter possède comme valeur de base = False et désigne la dernière itération du programme

  filename = 'J3-trace-graphe-' + indice +'.txt'    
  try : 
    with open(filename, "a") as file: # Ouverture du fichier en mode ajout à la fin du fichier 
      if etape == "Matrice d'Adjacence":
        file.write("\n--- " + etape + " --- \n") 
        for ligne in gra.tab:
          for element in ligne : 
            file.write(f"{element} ") # Le paramètre f"{} " permet d'écrire case par case la matrice et fonctionne comme la fonction str()
          file.write("\n")
                  
      elif etape == "Matrice d'Adjacence avec les valeurs":    
        file.write("\n--- " + etape + " --- \n") 
        for ligne in gra.tab_valeurs:
          for element in ligne : 
            file.write(f"{element} ") 
          file.write("\n")
        
      else : 
        # Première itération           
        if numero == 1 :
          file.write("\n--- " + etape + " --- \n")  

          # Affichage de la matrice distance initiale   
          file.write("Matrice Distance initiale : \n") 
          for ligne in gra.tab_distance_init:
            for element in ligne : 
              file.write(f"{element} ") 
            file.write("\n")    
          file.write("\n")   

          # Affichage de la matrice chemin initiale
          file.write("Matrice Chemin initiale : \n") 
          for ligne in gra.tab_chemin_init:
            for element in ligne : 
              file.write(f"{element} ") 
            file.write("\n")    
          file.write("\n")
          
        if circuit : 
          file.write(f"\n======= Iteration numero {numero}  =======\n")  
          
          # Affichage des distances   
          file.write("Matrice Distance : \n") 
          for ligne in gra.tab_distance:
            for element in ligne : 
              file.write(f"{element} ") 
            file.write("\n")    
          file.write("\n")   
            
          file.write("Presence d'un circuit absorbant.\n") 
                                  
        if not circuit: 
          file.write(f"\n======= Iteration numero {numero}  =======\n")        

          # Affichage des distances   
          file.write("Matrice Distance : \n") 
          for ligne in gra.tab_distance:
            for element in ligne : 
              file.write(f"{element} ") 
            file.write("\n")    
          file.write("\n")   

          # Affichage des chemins
          file.write("Matrice Chemin : \n")
          for ligne in gra.tab_chemin:
            for element in ligne : 
              file.write(f"{element} ") 
            file.write("\n")    
        
        # Dernière itération
        if der_iter :
          if der_iter is not True:
            file.write("\n")
            aff_chemin(der_iter[0], der_iter[1], sortie = file)
          file.write("\n--- Fin de l'etape " + etape + "--- \n")

  except IOError :
    print("L'ouverture du fichier est impossible.\n")

   
#---------------------------------------------------------------------------------------------------------
#                                               Main
#---------------------------------------------------------------------------------------------------------
commencer = True

while commencer == True :

  # Choix du graphe à analyser par l'utilisateur
  indice = choisir_graphe()
  print("Le graphe à analyser est le numéro",indice, ".")

  # On efface le contenu du fichier trace à traiter
  filename = 'J3-trace-graphe-' + indice +'.txt'    
  with open(filename, "w") as file : 
    pass

  # Lecture du contenu du fichier ouvert
  tableau = lire_graphe(indice)
  
  # Création du graphe et affichage
  gra = graphe() # On créé un objet de type graphe 
  creer_graphe(tableau)

  # Création de la matrice d'adjacence
  matrice_adj = creation_matrice_adj(gra)
  print("\nLa matrice adjacence : \n")
  afficher_matrice(matrice_adj)
  trace_execution(indice, gra, "A", "Matrice d'Adjacence")
  
  # Création de la matrice d'adjacence avec les valeurs 
  matrice_adj_val = creation_matrice_valeur(gra)
  print("\nLa matrice de valeur : \n")
  afficher_matrice(matrice_adj_val)
  trace_execution(indice, gra, "B", "Matrice d'Adjacence avec les valeurs")
    
  # Application de l'algorithme de Floyd-Warshall
  print("\n---- L'algorithme de Floyd-Warshall ----\n")
  floydWarshall(matrice_adj_val, gra)   

  continuer = int(input("\nSouhaitez-vous traiter un autre graphe ? 1 pour oui ou 0 pour quitter : "))
  if continuer == 0:
    commencer = False
  else : 
    commencer = True 
