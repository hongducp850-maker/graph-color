from flask import Flask, render_template
import io, base64
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

def greedy_coloring(G_matrix, node_names):
    t_ = {node_names[i]: i for i in range(len(G_matrix))}
    degree = [sum(row) for row in G_matrix]
    availableColors = ["blue","red","yellow","green","orange","purple"]
    colorDict = {node_names[i]: availableColors.copy() for i in range(len(G_matrix))}
    deg_pairs = list(zip(node_names, degree))
    sortedNode = [x[0] for x in sorted(deg_pairs, key=lambda x: x[1], reverse=True)]
    theSolution = {}
    for n in sortedNode:
        chosenColor = colorDict[n][0]
        theSolution[n] = chosenColor
        idx = t_[n]
        for j in range(len(G_matrix[idx])):
            if G_matrix[idx][j] == 1:
                neighbor = node_names[j]
                if chosenColor in colorDict[neighbor]:
                    colorDict[neighbor].remove(chosenColor)
    return theSolution, degree

def plot_graph(G_matrix, node_names, coloring):
    G = nx.Graph()
    for n in node_names:
        G.add_node(n)
    for i in range(len(G_matrix)):
        for j in range(i+1, len(G_matrix)):
            if G_matrix[i][j] == 1:
                G.add_edge(node_names[i], node_names[j])
    colors = [coloring[n] for n in G.nodes()]
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6,5))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=900, edge_color='black', font_weight='bold')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()

DEFAULT_G = [
    [0,1,1,0,1,0],
    [1,0,1,1,0,1],
    [1,1,0,1,1,0],
    [0,1,1,0,0,1],
    [1,0,1,0,0,1],
    [0,1,0,1,1,0]
]
DEFAULT_NODE = "ABCDEF"

@app.route("/")
def index():
    coloring, degree = greedy_coloring(DEFAULT_G, DEFAULT_NODE)
    img_b64 = plot_graph(DEFAULT_G, list(DEFAULT_NODE), coloring)
    degree_map = {DEFAULT_NODE[i]: degree[i] for i in range(len(DEFAULT_NODE))}
    return render_template("index.html", coloring=coloring, degree_map=degree_map, img_b64=img_b64)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
