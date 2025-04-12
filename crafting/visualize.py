from json import load
from networkx import DiGraph
from pyvis.network import Network


data = load(open("data.json"))
G = DiGraph()

for k,v in data.items():
    G.add_node(k)
    for (frm, ing) in v:
        G.add_edge(frm, k, label=ing)

net = Network(notebook = False, cdn_resources = "remote",
                bgcolor = "#222222",
                font_color = "white",
                height = "1000px",
                width = "100%",
                directed=True,
)
net.from_nx(G.reverse())
# net.add_nodes(G.nodes)
# for (f,t),w in G.edges.items():
#     net.add_edge(t,f,weight=w["label"])
# net.add_edges(G.edges)
net.show("graph.html", notebook=False)