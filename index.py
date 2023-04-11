from labyrinthe_generator import *
from algorithme_graphes import *
from tkinter import *
from tkinter.messagebox import *

# # route = search_path(graphe, '0,0', '9,0', 'BFS')
# # print("route from BFS '0,0' to '9,0' is :", route)
# # print('-'*15)
# # route = search_path(graphe, '0,9', '9,0', 'DFS')
# # print("route from DFS '0,0' to '9,0' is :", route)

"""----------------------------------------------------interface graphique----------------------------------------------------------"""

def main():
    default_resolution = '720x480'
    def show():
        labyrinthe.show()  

    def tool_window():
        def get_laby_graphe():
            laby_graphe  = get_graphe(labyrinthe)
            showinfo("Graphe",f"Voici le graphe de votre labyrinthe :\n\n {laby_graphe}")

        def laby_BFS():
            laby_graphe  = get_graphe(labyrinthe)
            BFS_parcours = laby_BFS_parcours(laby_graphe, labyrinthe.tab[0][labyrinthe.q-1].id)
            showinfo("parcours en BFS",f"Voici le resultat quand on parcours le labyrinthe en largeur :\n\n {BFS_parcours}")

        def laby_DFS():
            laby_graphe  = get_graphe(labyrinthe)
            DFS_parcours = laby_DFS_parcours(laby_graphe, labyrinthe.tab[0][labyrinthe.q-1].id)
            showinfo("parcours en BFS",f"Voici le resultat quand on parcours le labyrinthe en profondeur :\n\n {DFS_parcours}")

        def BFS_DFS_Case_route():
            BFS_Case_route_window = Tk()
            BFS_Case_route_window.geometry(default_resolution)
            BFS_Case_route_window.title("BFS case route") #affectation d'un titregen_window.title("Generateur") #affectation d'un titre
            Case_1_input = Entry(BFS_Case_route_window)
            Case_1_input.pack()
            Case_2_input =  Entry(BFS_Case_route_window)
            Case_2_input.pack()

            Choice = StringVar(BFS_Case_route_window, "BFS")

            values = {"BFS" : "BFS",
                    "DFS" : "DFS"}
            
            for (text, value) in values.items():
                Radiobutton(BFS_Case_route_window, text = text, variable = Choice,
                    value = value).pack(side = TOP, ipady = 5)
                
            def check_Case():
                laby_graphe  = get_graphe(labyrinthe)
                Case_1,Case_2 = Case_1_input.get(), Case_2_input.get()
                Button_choice = Choice.get()
                if "," in Case_1 and ',' in Case_2:
                    Case_1_index_separator,Case_2_index_separator = Case_1.index(','),Case_2.index(',')
                    Case_1_x = Case_1[:Case_1_index_separator]
                    Case_1_y = Case_1[1+Case_1_index_separator:]
                    Case_2_x = Case_2[:Case_2_index_separator]
                    Case_2_y = Case_2[1+Case_2_index_separator:]
                    if Case_1_x.isnumeric() and Case_1_y.isnumeric() and Case_2_x.isnumeric() and Case_2_y.isnumeric():
                        Case_1_x,Case_1_y = int(Case_1_x),int(Case_1_y)
                        Case_2_x,Case_2_y = int(Case_2_x),int(Case_2_y)
                        if  0 <= Case_1_x <=labyrinthe.p-1 and 0 <= Case_2_x <=labyrinthe.p-1 and 0 <= Case_1_y <=labyrinthe.q-1 and 0 <= Case_2_y <=labyrinthe.q-1:
                            route = get_path(laby_graphe, Case_1, Case_2, Button_choice)
                            showinfo("Chemin entre deux Case",f"voici le chemin trouver pour acceder de {Case_1} a {Case_2} en {Button_choice} : \n\n {route}")
                        else:
                            showerror("coordonnees incorrect", "les coordonnes x et y renter ne sont pas pas compris dans la taille du labyrinthe")
                    else:
                        showerror("coordonnees incorrect", "les coordonnes x et y ne sont pas numeriques")  
                else:
                    showerror("coordonnees incorrect", "Format invalide => format a respecter 'x,y'")   

            confirm_button = Button(BFS_Case_route_window, text='confirmer', command = check_Case)
            confirm_button.pack()

        def discover_cycles():
            laby_graphe = get_graphe(labyrinthe)
            matriceAdj = get_matrice_adj(laby_graphe, labyrinthe)
            if estCyclique(matriceAdj, 0) == True:
                showinfo("Detection de cycles", "Le graphe contient au moins un cycle")
                print("Le graphe contient un cycle")
            else:
                showinfo("Detection de cycles", "Le graphe est acyclique")
                print("Le graphe est acyclique")

        def get_matrice():
            nbl = 0
            keys = []
            laby_graphe = get_graphe(labyrinthe)
            for key in laby_graphe.keys(): keys.append(key)
            #affiche la matrice
            matriceAdj = get_matrice_adj(laby_graphe, labyrinthe)
            print('Case',keys)
            for k in range(len(matriceAdj)):
                print(keys[k],matriceAdj[k])
                nbl += 1
            print('nb ligne :',nbl,'nb column : ',len(matriceAdj[1]))            
            # showinfo("Matrice",f"Voici la Matrice d'adjacence de ce labyrinthe :\n\n {matriceAdj}")

        def get_optimal_path():
            optimal_window = Tk()
            optimal_window.geometry(default_resolution)
            optimal_window.title("BFS case route") #affectation d'un titregen_window.title("Generateur") #affectation d'un titre
            Case_1_input = Entry(optimal_window)
            Case_1_input.pack()
            Case_2_input =  Entry(optimal_window)
            Case_2_input.pack()
    
            def check_Case():
                laby_graphe  = get_graphe(labyrinthe)
                Case_1,Case_2 = Case_1_input.get(), Case_2_input.get()
                if "," in Case_1 and ',' in Case_2:
                    Case_1_index_separator,Case_2_index_separator = Case_1.index(','),Case_2.index(',')
                    Case_1_x = Case_1[:Case_1_index_separator]
                    Case_1_y = Case_1[1+Case_1_index_separator:]
                    Case_2_x = Case_2[:Case_2_index_separator]
                    Case_2_y = Case_2[1+Case_2_index_separator:]
                    if Case_1_x.isnumeric() and Case_1_y.isnumeric() and Case_2_x.isnumeric() and Case_2_y.isnumeric():
                        Case_1_x,Case_1_y = int(Case_1_x),int(Case_1_y)
                        Case_2_x,Case_2_y = int(Case_2_x),int(Case_2_y)
                        if  0 <= Case_1_x <=labyrinthe.p-1 and 0 <= Case_2_x <=labyrinthe.p-1 and 0 <= Case_1_y <=labyrinthe.q-1 and 0 <= Case_2_y <=labyrinthe.q-1:
                            all_routes = search_best_path(laby_graphe, Case_1, Case_2, labyrinthe)
                            print("all route : ",all_routes)
                            count = [] 
                            for i in range(len(all_routes)):
                                count.append(all_routes[i])
                            print(count)
                            print(count[0])
                            minimum = min(count)
                            index = count.index(minimum)
                            best_route = all_routes[index]
                            showinfo("Chemin entre deux Case",f"voici le chemin optimal pour aller de {Case_1} a {Case_2} : \n\n {best_route} \n\n avec un cout d'acces de {count[index]}")
                        else:
                            showerror("coordonnees incorrect", "les coordonnes x et y renter ne sont pas pas compris dans la taille du labyrinthe")
                    else:
                        showerror("coordonnees incorrect", "les coordonnes x et y ne sont pas numeriques")  
                else:
                    showerror("coordonnees incorrect", "Format invalide => format a respecter 'x,y'")   

            confirm_button = Button(optimal_window, text='confirmer', command = check_Case)
            confirm_button.pack()

        def cases_informations():
            print("coordinate = x,y")
            nb = 1
            for j in range(len(labyrinthe.tab)):
                for i in range(len(labyrinthe.tab[j])):
                    print('nb :',nb,'size :',labyrinthe.tab[j][i].size,'id = ',labyrinthe.tab[j][i].id,"==> N =",labyrinthe.tab[j][i].N,'/ W =',labyrinthe.tab[j][i].W,'/ E =',labyrinthe.tab[j][i].E,'/ S =',labyrinthe.tab[j][i].S)
                    nb += 1

            print('len x laby :',len(labyrinthe.tab))
            print('len y laby :',len(labyrinthe.tab[0]))


        tool_window = Tk()
        tool_window.geometry(default_resolution)
        tool_window.title("Tools") #affectation d'un titregen_window.title("Generateur") #affectation d'un titre
        button_show_laby  = Button(tool_window, text="Montrer le labyrinthe", command=show)
        button_show_laby.pack()

        button_laby_BFS = Button(tool_window, text="Parcours du labyrinth en BFS", command=laby_BFS)
        button_laby_BFS.pack()

        button_laby_DFS  = Button(tool_window, text="Parcours du labyrinth en DFS", command=laby_DFS)
        button_laby_DFS.pack()

        button_laby_graphe  = Button(tool_window, text="obtenir le graphe du labyrinth en DFS", command=get_laby_graphe)
        button_laby_graphe.pack()


        button_laby_BFS_route  = Button(tool_window, text="recherche chemin entre 2 case BFS ou DFS", command=BFS_DFS_Case_route)
        button_laby_BFS_route.pack()

        button_discover_cycle  = Button(tool_window, text="recherche d'existance de cycles", command=discover_cycles)
        button_discover_cycle.pack()

        button_get_matrice  = Button(tool_window, text="Obtenir la matrice d'adjacence", command=get_matrice)
        button_get_matrice.pack()

        button_find_best_path  = Button(tool_window, text="Obtenir le meilleur chemin existant", command=get_optimal_path)
        button_find_best_path.pack()

        button_all_case_infos  = Button(tool_window, text="infos sur chaque case du labyrinthe", command=cases_informations)
        button_all_case_infos.pack()

    def create_laby(x,y):
        global labyrinthe
        x_coordinate =  int(x)
        y_coordinate = int(y)
        labyrinthe = creation(x_coordinate,y_coordinate)
        tool_window()

    def generer():
        main_window.withdraw()
        gen_window = Tk()
        gen_window.geometry(default_resolution) #taille de la fenetre principale
        gen_window.title("Generateur") #affectation d'un titre
        x_input = Entry(gen_window)
        x_input.pack()
        y_input =  Entry(gen_window)
        y_input.pack()
        def check_x_y():
            x = x_input.get()
            y = y_input.get()
            if not x.isnumeric() or not y.isnumeric():
                showerror("coordonnees incorrect", "les coordonnes x et y renter ne sont pas valide")
            else:    
                create_laby(x,y)
                gen_window.withdraw()
                
        confirm_button = Button(gen_window, text='confirmer', command = check_x_y)
        confirm_button.pack()

    main_window = Tk()
    main_window.geometry(default_resolution) #taille de la fenetre principale
    main_window.title("The labyrinthe tools") #affectation d'un titre
    main_text = Label(main_window,anchor=CENTER, text =  "Bienvenu dans le generateur de labyrinthe") #text
    main_text.pack()
    generator_button=Button(main_window, text="Generer  un labyrinthe", command=generer) #creation d'un boutton pour ouvrir les fichier
    generator_button.pack(padx=(20),pady=(20))
    bouton_quit=Button(main_window, text="Quitter", command=quit) #creation d'un boutton pour quitter le programme
    bouton_quit.pack(padx=(20),pady=(20))
    main_window.mainloop() #affichage de la fenetre

main()
