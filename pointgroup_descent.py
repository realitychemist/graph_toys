import networkx as nx
from tkinter.filedialog import asksaveasfilename
from matplotlib import pyplot as plt
import matplotlib.patches as patches
plt.rcParams.update({"text.usetex": True,
                     "font.weight": "bold",
                     "text.latex.preamble": r"\usepackage{fourier} \boldmath"})

############
## GROUPS ##
############
hm_to_schoen = {r"$1$": "C1", r"$\bar{1}$": "Ci", r"$2$": "C2", r"$m$": "C1h", r"$3$": "C3", r"$4$": "C4",
                r"$\bar{4}$": "S4", r"$2/m$": "C2h", r"$222$": "D2", r"$mm2$": "C2v", r"$\bar{3}$": "C3i", r"$6$": "C6",
                r"$\bar{6}$": "C3h", r"$32$": "D3", r"$3m$": "C3v", r"$mmm$": "D2h", r"$4/m$": "C4h", r"$422$": "D4",
                r"$4mm$": "C4v", r"$\bar{4}2m$": "D2d", r"$6/m$": "C6h", r"$23$": "T", r"$\bar{3}m$": "D3d",
                r"$622$": "D6", r"$6mm$": "C6v", r"$\bar{6}m2$": "D3h", r"$4/mmm$": "D4h", r"$6/mmm$": "D6h",
                r"$m\bar{3}$": "Th", r"$432$": "O", r"$\bar{4}3m$": "Td", r"$m\bar{3}m$": "Oh"}
schoen_to_hm = dict(zip(hm_to_schoen.values(), hm_to_schoen.keys()))

# Crystal systems
cubic_schoen = {"T", "Th", "O", "Td", "Oh"}
cubic_hm = {schoen_to_hm[s] for s in cubic_schoen}
hex_schoen = {"C6", "C3h", "C6h", "D6", "C6v", "D3h", "D6h"}
hex_hm = {schoen_to_hm[s] for s in hex_schoen}
rhomb_schoen = {"C3", "C3i", "D3", "C3v", "D3d"}
rhomb_hm = {schoen_to_hm[s] for s in rhomb_schoen}
tet_schoen = {"C4", "S4", "C4h", "D4", "C4v", "D2d", "D4h"}
tet_hm = {schoen_to_hm[s] for s in tet_schoen}
ortho_schoen = {"D2", "C2v", "D2h"}
ortho_hm = {schoen_to_hm[s] for s in ortho_schoen}
mono_schoen = {"C2", "C1h", "C2h"}
mono_hm = {schoen_to_hm[s] for s in mono_schoen}
tric_schoen = {"C1", "Ci"}
tric_hm = {schoen_to_hm[s] for s in tric_schoen}

# Order
order_schoen = {"C1": 1, "Ci": 2, "C2": 2, "C1h": 2, "C2h": 4, "D2": 4, "C2v": 4, "D2h": 8, "C4": 4, "S4": 4,
                "C4h": 8, "D4": 8, "C4v": 8, "D2d": 8, "D4h": 16, "C3": 3, "C3i": 6, "D3": 6, "C3v": 6,
                "D3d": 12, "C6": 6, "C3h": 6, "C6h": 12, "D6": 12, "C6v": 12, "D3h": 12, "D6h": 24, "T": 12,
                "Th": 24, "O": 24, "Td": 24, "Oh": 48}
order_hm = {schoen_to_hm[sym]: order for sym, order in order_schoen.items()}

#########################
## DESCENT CONNECTIONS ##
#########################
edgelist = [("Oh", "D4h"), ("Oh", "O"), ("Oh", "Td"), ("Oh", "Th"), ("Oh", "D3d"),
            ("D6h", "D2h"), ("D6h", "D6"), ("D6h", "C6v"), ("D6h", "C6h"), ("D6h", "D3h"), ("D6h", "D3d"),
            ("D4h", "C4v"), ("D4h", "C4h"), ("D4h", "D4"), ("D4h", "D2d"), ("D4h", "D2h"),
            ("O", "D4"), ("O", "D3"), ("O", "T"),
            ("Td", "D2d"), ("Td", "T"), ("Td", "C3v"),
            ("Th", "D2h"), ("Th", "T"), ("Th", "C3i"),
            ("D3d", "C2h"), ("D3d", "D3"), ("D3d", "C3v"), ("D3d", "C3i"),
            ("D2h", "C2v"), ("D2h", "D2"), ("D2h", "C2h"),
            ("D6", "D2"), ("D6", "C6"), ("D6", "D3"),
            ("C6v", "C2v"), ("C6v", "C6"), ("C6v", "C3v"),
            ("C6h", "C6"), ("C6h", "C2h"), ("C6h", "C3h"), ("C6h", "C3i"),
            ("D3h", "C2h"), ("D3h", "D3"), ("D3h", "C3h"), ("D3h", "C3v"), ("D3h", "C3i"),
            ("C4v", "C4"), ("C4v", "C2v"),
            ("C4h", "C4"), ("C4h", "S4"), ("C4h", "C2h"),
            ("D4", "C4"), ("D4", "D2"),
            ("D2d", "S4"), ("D2d", "C2v"), ("D2d", "D2"),
            ("D3", "C2"), ("D3", "C3"),
            ("T", "D2"), ("T", "C3"),
            ("C3v", "C1h"), ("C3v", "C3"),
            ("C3i", "C3"), ("C3i", "Ci"),
            ("C2h", "C2"), ("C2h", "C1h"), ("C2h", "Ci"),
            ("C2v", "C2"), ("C2v", "C1h"),
            ("D2", "C2"),
            ("C6", "C2"), ("C6", "C3"),
            ("C3h", "C1h"), ("C3h", "C3"),
            ("C4", "C2"),
            ("S4", "C2"),
            ("C2", "C1"),
            ("C3", "C1"),
            ("C1h", "C1"),
            ("Ci", "C1")]

####################
## BUILD AND PLOT ##
####################
g = nx.DiGraph()
g.add_edges_from(edgelist)

# Node colors
colors = {}
for node in g.nodes:
    if node in cubic_schoen:
        colors[node] = "#C01010"
    elif node in tet_schoen:
        colors[node] = "#E07000"
    elif node in ortho_schoen:
        colors[node] = "#7B9B2F"
    elif node in hex_schoen:
        colors[node] = "#1850E0"
    elif node in rhomb_schoen:
        colors[node] = "#00AAA7"
    elif node in mono_schoen:
        colors[node] = "#8020B0"
    elif node in tric_schoen:
        colors[node] = "#A02060"
    else:
        raise RuntimeError

legend = {"#C01010": r"\textbf{Cubic}",
          "#E07000": r"\textbf{Tetragonal}",
          "#7B9B2F": r"\textbf{Orthorhombic}",
          "#1850E0": r"\textbf{Hexagonal}",
          "#00AAA7": r"\textbf{Rhombohedral}",
          "#8020B0": r"\textbf{Monoclinic}",
          "#A02060": r"\textbf{Triclinic}"}
handles = [patches.Patch(color=color, label=label) for color, label in legend.items()]

pos = nx.nx_pydot.pydot_layout(g, "dot")
# Setting y by order directly highlights how much symmetry m-3m actually has compared with everything else
# ... but it's not very readable. Instead we'll use 10 equi-spaced y-values
order_to_yval = {48: 9, 24: 8, 16: 7, 12: 6, 8: 5, 6: 4, 4: 3, 3: 2, 2: 1, 1: 0}
for node in g.nodes:
    pos[node] = (pos[node][0], order_to_yval[order_schoen[node]])

nx.draw_networkx(g, pos=pos, node_color="none", node_size=1500,  # NOTE: I have hand-made a cleaner version of this
                 arrowstyle="->", edge_color="gray", with_labels=False)  # with much less ambiguous arrows
nx.draw_networkx_labels(g, pos=pos, labels=schoen_to_hm, font_color=colors, font_size=18)

plt.legend(handles=handles, loc="lower right", fontsize=12)
figure = plt.gcf()
plt.show()
figure.savefig(asksaveasfilename(defaultextension=".png"), dpi=300)