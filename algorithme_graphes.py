from typing import *
from Pile_File_class import *
import random

"""Creation Graphe"""
"""--------------------------------------------------------------------------------------------------------------"""
def get_graphe(laby:object) -> dict:
    """Fonction qui permet de generer un graphe a partir d'un labyrinthe
        - prend en argument un labyrinthe (object)
        - renvoie une graphe sour dorme de dict"""
    graphe = dict()
    for x in range(len(laby.tab)):
        for y in range(len(laby.tab[x])):
            linked_to = []
            if laby.tab[x][y].W: 
                linked_to.append(laby.tab[x-1][y].id)
                
            if laby.tab[x][y].E: 
                linked_to.append(laby.tab[x+1][y].id)

            if laby.tab[x][y].S: 
                linked_to.append(laby.tab[x][y-1].id)

            if laby.tab[x][y].N: 
                linked_to.append(laby.tab[x][y+1].id)

            graphe[laby.tab[x][y].id] = linked_to
    return graphe

def get_matrice_adj(graphe,laby):
    keys = []
    for key in graphe.keys(): keys.append(key)
    matrice = [[False for  i in range(len(keys))] for i in range(len(keys))]
    matrice_index = 0 
    for element in keys:
        linked_to = graphe[element]
        for value in linked_to:
            separator_index = value.index(',')
            c1 = int(value[:separator_index])
            c2 = int(value[1+separator_index:])
            change_index = laby.p * c1 + c2
            matrice[matrice_index][change_index] = True
        matrice_index  += 1
    return matrice

"""-------------------------------------------------------------------------------------------------------------"""
"""give all voisins for each sommet"""
def voisin(G:dict, sommet:str):
    """renvoie les differents voisins d'un sommet"""
    return G[sommet]

"""DFS NORAMAl"""
def laby_DFS_parcours(G,sommet):
    p=Pile()
    sommets_visites=[]
    p.empiler(sommet)
    while p.vide()==False:
        tmp=p.depiler()
        if tmp not in sommets_visites:
            sommets_visites.append(tmp)
            print(tmp,end=" ")
        voisins=[y for y in voisin(G,tmp) if y not in sommets_visites]
        for vois in voisins:
            p.empiler(vois)
    return sommets_visites

"""laby BFS"""
def laby_BFS_parcours(G, sommet):
    sommet_visite = []
    f = File()
    f.enfiler(sommet)
    while f.vide() == False:
        tmp = f.defiler()
        print(tmp)
        if tmp not in sommet_visite:
            sommet_visite.append(tmp)
        for vois in voisin(G,tmp):
            if vois not in sommet_visite and f.present(vois) == False:
                f.enfiler(vois)
    return sommet_visite


"""---------------------------------------------------------------------------------------------------------------"""
"""recherche chemin entre 2 case BFS ou DFS"""
def get_path(graphe, Begin_Case, End_Case, methode = 'BFS'):
    """BFS"""
    def parcours_BFS(G, depart):
        parents = dict()
        sommet_visite = []
        f = File()
        f.enfiler(depart)
        parents[depart] = None
        while f.vide() == False:
            tmp = f.defiler()
            if tmp not in sommet_visite:
                sommet_visite.append(tmp)
            for vois in voisin(G,tmp):
                if vois not in sommet_visite and f.present(vois) == False:
                    f.enfiler(vois)
                    parents[vois] = tmp
        print(parents)
        return parents

    """DFS"""
    def parcours_DFS(G,depart):
        sommets_visites = []
        parents = dict()
        p=Pile()
        p.empiler(depart)
        parents[depart] = None
        while p.vide()==False:
            depart = p.depiler()
            if depart not in sommets_visites:
                sommets_visites.append(depart)
                voisins=[y for y in voisin(G,depart) if y not in sommets_visites]
            for vois in voisins:
                p.empiler(vois)
                parents[vois] = depart
        return parents

    def Solution(end, parents):
        chemin = []
        courant = end
        while courant != None:
            chemin = [courant] + chemin
            courant = parents[courant]
        return chemin

    def search_path(graphe, Begin_Case, End_Case, set='BFS'):
        if set == 'BFS' or set == 'bfs': return Solution(End_Case ,parcours_BFS(graphe, Begin_Case))
        if set == 'DFS' or set == 'dfs': return Solution(End_Case ,parcours_DFS(graphe, Begin_Case))
        else: print('incorrect methode')
    return search_path(graphe, Begin_Case,End_Case,methode)
   
"""------------------------------------------------------------------------------------------------------"""

"""implementation recherche de cycle BFS ==> graphe non oriente"""
def estCyclique(matriceAdj, u):
    n = len(matriceAdj) # nombre de sommets
    file = []
    visites = [False] * n
    visites[u] = True
    # Pour mémoriser à partir de quel sommet on a découvert chaque commet du graphe
    parent = [-1] * n
    # Au départ le parent de u est u lui même
    parent[u] = u
    file.append(u)
    while file:
        courant = file.pop(0)
        visites[courant] = True
        for i in range(n): 
            if matriceAdj[courant][i] > 0 and visites[i] == False:
                file.append(i)
                visites[i] = True
                # Parent de i est le noeud courant
                parent[i] = courant
            # Si i est un noeud adjacent déjà visité et i n'est pas le parent de courant
            # donc il y a un cycle, retourner True
            elif matriceAdj[courant][i] > 0 and visites[i] == True and parent[courant] != i:
                return True
    # pas de chemin entre u et u
    return False


"""
def fonct_inconnue(G,sommet):
    sommets_visites=[]
    f=File()
    sommets_visites.append(sommet)
    f.enfiler((sommet,-1))
    while f.vide()==False:
        (tmp,parent)=f.defiler()
        voisins=voisin(G,tmp)
        for vois in voisins:
            if vois not in sommets_visites:
                sommets_visites.append(vois)
                f.enfiler((vois,tmp))
            elif vois!=parent:
                return True
    return False
"""

"""--------------------------------------------------------------------------------------------------------"""

"""implementation Dijstra"""
def search_best_path(graphe, Begin_Case, End_Case, laby):
    def current_path():
        current_path_found = get_path(graphe, Begin_Case, End_Case, 'DFS')
        current_size = 0
        for element in current_path_found: #calcule la taille du chemin
            # print('element : ',element,'type :', type(element))
            index_separator = element.index(',')
            # print('index separator : ',index_separator)
            index_x = int(element[:index_separator])
            index_y = int(element[1+index_separator:])
            current_size += laby.tab[index_x][index_y].size
        current = [current_size, current_path_found]
        return current
    path = current_path()
    return path

def get_best_path(graphe, Begin_Case, End_Case, laby):
    all_path = []
    for i in range(len(laby.tab)):
        path = search_best_path(graphe, Begin_Case, End_Case, laby)
        while not path in all_path:
            all_path.append(path)
    return all_path
    