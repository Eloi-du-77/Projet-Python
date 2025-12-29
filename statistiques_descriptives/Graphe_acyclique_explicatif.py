import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

def graphe_acyclique_explicatif(df) :
    """Trace le graphe acyclique explicatif de la démarche

    Prend en argument la df
    """
    corr_jo_jp = (
        df[['score_olympique', 'score_paralympique']]
        .dropna()
        .corr()
        .loc['score_olympique', 'score_paralympique']
    )

    print(f"Corrélation score JO et JP : {corr_jo_jp:.3f}")
    G = nx.DiGraph()

    main_nodes = ["Pays", "JO", "JP"]
    jo_vars = ["Score_olympique"]
    jp_vars = ["Score_paralympique"]
    pays_vars = [
        "idh",
        "pib_habitant",
        'moy_education_2008',
        'moy_loisirs_2008',
        'moy_amenagement_2008',
        'moy_maladie_2008'
    ]

    G.add_nodes_from(main_nodes + jo_vars + jp_vars + pays_vars)

    edges_jo = [("JO", v) for v in jo_vars]
    edges_jp = [("JP", v) for v in jp_vars]
    edges_pays = [("Pays", v) for v in pays_vars]

    #Dire ou seront placés les noeuds du graphe
    pos = {
        "Pays": np.array([0, 0]),
        "JO": np.array([4, 2]),
        "JP": np.array([4, -2])
    }

    for i, v in enumerate(jo_vars):
        pos[v] = np.array([8, 2 + 0.8 - i*1.0])
    for i, v in enumerate(jp_vars):
        pos[v] = np.array([8, -1.2 - i*1.0])
    for i, v in enumerate(pays_vars):
        pos[v] = np.array([-4, 2 + 0.8 - i*1.0])


    plt.figure(figsize=(24, 16))
    ax = plt.gca()

    #Tracé des arrêtes pour les variables pas "principales" (celles hors de pays, score olympique et paralympique)
    nx.draw_networkx_edges(G, pos, edgelist=edges_jo + edges_jp + edges_pays,
                        arrows=True, arrowstyle='-|>', arrowsize=20, width=1.5, edge_color="black")

    #Tracer les cercles principaux (ceux avec les scores et pays)
    node_size_main = 4500
    nx.draw_networkx_nodes(G, pos, nodelist=main_nodes, node_color="salmon",
                        node_shape="o", node_size=node_size_main, edgecolors="black")
    nx.draw_networkx_labels(G, pos, labels={n: n for n in main_nodes}, font_size=14)

    #Tracer les rectangles des sous-variables
    def draw_box(label, xy):
        ax.text(xy[0], xy[1], label, ha="center", va="center",
                fontsize=14,
                bbox=dict(boxstyle="round,pad=0.8", facecolor="lightblue",
                        edgecolor="black", linewidth=1.5))
    for v in jo_vars + jp_vars + pays_vars:
        draw_box(v, pos[v])


    #On trace les flèches principales
    def draw_arrow(src, dst, rad=0, color='black'):
        #On fait en sorte que les flèches touchent le bord des cases
        start = pos[src]
        end = pos[dst]
        vec = end - start
        length = np.linalg.norm(vec)
        r = np.sqrt(node_size_main)/200
        start_adj = start + vec*(r/length)
        end_adj = end - vec*(r/length)
        arrow = FancyArrowPatch(start_adj, end_adj,
                                connectionstyle=f"arc3,rad={rad}",
                                arrowstyle='-|>', mutation_scale=25,
                                color=color, linewidth=2)
        ax.add_patch(arrow)

    #On trace les flèches

    #Pays vers JO et JP
    draw_arrow("Pays", "JO")
    draw_arrow("Pays", "JP")

    #Double flèche entre JO et JP
    draw_arrow("JO", "JP", rad=0.2)
    draw_arrow("JP", "JO", rad=-0.2)

    #Ecrire la corrélation des deux
    ax.text((pos["JO"][0] + pos["JP"][0])/2 + 0.2,
            (pos["JO"][1] + pos["JP"][1])/2,
            f"corr = {corr_jo_jp:.2f}",
            fontsize=14,
            bbox=dict(facecolor="white", edgecolor="black", pad=0.3))

    plt.title("DAG : Liens entre nos variables", fontsize=18)
    plt.axis("off")
    plt.show()
