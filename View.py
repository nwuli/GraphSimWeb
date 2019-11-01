import matplotlib.pyplot as plt
import networkx as nx


def showView(args):
    # 绘图的软
    G = args
    # draw=plt.subplot(1,length,i)
    pos = nx.circular_layout(G)
    nx.draw_circular(G, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, font_size=7, alpha=0.5, rotate=True)
    plt.axis('off')
    plt.show()
