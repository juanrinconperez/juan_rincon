from BinaryTree import *
from RedBlackTree import *
import random
import sys
sys.setrecursionlimit(15000000)

import networkx as nx
import matplotlib.pyplot as plt


def is_nil_node(node):
    if node is None:
        return True
    if hasattr(node, "is_nil") and callable(node.is_nil):
        return node.is_nil()
    return False


def get_node_color(node):
    if hasattr(node, "color"):
        if str(node.color).endswith("RED"):
            return "red"
        if str(node.color).endswith("BLACK"):
            return "black"
    return "lightblue"


def get_font_color(node):
    if hasattr(node, "color"):
        if str(node.color).endswith("RED") or str(node.color).endswith("BLACK"):
            return "white"
    return "black"


def get_node_label(node):
    if hasattr(node, "key"):
        return str(node.key)
    return str(node)


def hierarchy_pos(G, root, width=1.0, vert_gap=0.22, vert_loc=0):
    pos = {}

    def _hierarchy_pos(node, left, right, y):
        pos[node] = ((left + right) / 2, y)
        children = list(G.successors(node))

        if len(children) == 1:
            _hierarchy_pos(children[0], left, right, y - vert_gap)

        elif len(children) == 2:
            mid = (left + right) / 2
            _hierarchy_pos(children[0], left, mid, y - vert_gap)
            _hierarchy_pos(children[1], mid, right, y - vert_gap)

    _hierarchy_pos(root, 0, width, vert_loc)
    return pos


def build_graph(node, G, max_depth=3, current_depth=0):
    if is_nil_node(node) or current_depth > max_depth:
        return

    node_id = id(node)
    G.add_node(node_id, label=get_node_label(node), color=get_node_color(node), fontcolor=get_font_color(node))

    left = node.get_left()
    right = node.get_right()

    if not is_nil_node(left) and current_depth < max_depth:
        left_id = id(left)
        G.add_edge(node_id, left_id)
        build_graph(left, G, max_depth, current_depth + 1)

    if not is_nil_node(right) and current_depth < max_depth:
        right_id = id(right)
        G.add_edge(node_id, right_id)
        build_graph(right, G, max_depth, current_depth + 1)


def draw_tree(root, max_levels=5):
    if is_nil_node(root):
        print("Empty tree")
        return

    G = nx.DiGraph()
    build_graph(root, G, max_depth=max_levels - 1)

    pos = hierarchy_pos(G, id(root))
    labels = nx.get_node_attributes(G, "label")
    node_colors = [G.nodes[node]["color"] for node in G.nodes]

    plt.figure(figsize=(16, 9))

    nx.draw_networkx_edges(G, pos, arrows=False, width=1.5)
    nx.draw_networkx_nodes(G, pos, node_size=5000, node_color=node_colors, edgecolors="black", linewidths=1.5)

    for node, (x, y) in pos.items():
        plt.text(x, y, labels[node], ha="center", va="center", fontsize=10, fontweight="bold", color=G.nodes[node]["fontcolor"])

    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    letters = input("Escriba hasta un máximo de tres letras. Todas seguidas \n").lower().strip()
    while len(letters) > 3 or len(letters) < 1:
        letters = input("Escriba entre una y tres letras. Todas seguidas \n").lower().strip()

    order = input("Desea que se ordenen alfabeticamente (A) o aleatoriamente (B)").upper().strip()
    while order not in ("A", "B"):
        order = input("Desea que se ordenen alfabeticamente (A) o aleatoriamente (B)").upper().strip()

    letter1 = letters[0]
    letter2 = letters[1] if len(letters) > 1 else None
    letter3 = letters[2] if len(letters) > 2 else None

    # Checking if some letter is repeated, if it occurs, we set the last one as None
    if letter1 == letter2 and letter3 is None:
        letter2 = None
    elif letter1 == letter2 and letter3 is not None:
        if letter1 == letter3:
            letter3 = None
        letter2, letter3 = letter3, None

    if letter1 == letter3:
        letter3 = None

    if letter2 == letter3:
        letter3 = None

    Tree1 = BinaryTree()
    Tree2 = BinaryTree()
    Tree3 = BinaryTree()
    RBTree1 = RedBlackTree()
    RBTree2 = RedBlackTree()
    RBTree3 = RedBlackTree()

    words1 = []
    words2 = []
    words3 = []
    with open("palabras_RAE.txt", "r", encoding = "utf-8") as words:
        for line in words:
            line = line.strip()
            first_letter = line[0]
            if order == "A":
                if first_letter == letter1:
                    node = Node(line, line)
                    rbnode = RBNode(line, line)

                    Tree1.insert_node(node)
                    RBTree1.insert(rbnode)

                elif letter2 is not None and first_letter == letter2:
                    node = Node(line, line)
                    rbnode = RBNode(line, line)

                    Tree2.insert_node(node)
                    RBTree2.insert(rbnode)

                elif letter3 is not None and first_letter == letter3:
                    node = Node(line, line)
                    rbnode = RBNode(line, line)

                    Tree3.insert_node(node)
                    RBTree3.insert(rbnode)
            else:
                if first_letter == letter1:
                    words1.append(line)
                elif letter2 is not None and letter2 == first_letter:
                    words2.append(line)
                elif letter3 is not None and letter3 == first_letter:
                    words3.append(line)

    if order == "B":
        random.shuffle(words1)
        while len(words1) > 0:
            word = words1.pop()
            Tree1.insert_node(Node(word, word))
            RBTree1.insert(RBNode(word, word))

        if len(words2) > 0:
            random.shuffle(words2)
            while len(words2) > 0:
                word = words2.pop()
                Tree2.insert_node(Node(word, word))
                RBTree2.insert(RBNode(word, word))

        if len(words3) > 0:
            random.shuffle(words3)
            while len(words3) > 0:
                word = words3.pop()
                Tree3.insert_node(Node(word, word))
                RBTree3.insert(RBNode(word, word))

    print(f"\n--- INFORMACION DEL ARBOL DE LA LETRA {letter1.upper()} (Binario)---\n")
    print("Primera palabra:", Tree1.root)
    print("Palabra de la izquierda:", Tree1.root.get_left())
    print("Palabra de la derecha:", Tree1.root.get_right())
    print("Numero de nodos:", Tree1.count_nodes_tree())
    print("Numero de hojas:", Tree1.count_leafs())
    print("Camino mas largo:", Tree1.longest_path())
    print("Caminos de longitud 3:", Tree1.paths_to_leaf_with_length(Tree1.root, 3))
    draw_tree(Tree1.root, max_levels=5)

    print(f"\n--- INFORMACION DEL ARBOL DE LA LETRA {letter1.upper()} (Rojo-Negro)---\n")
    print("Primera palabra:", RBTree1.root)
    print("Palabra de la izquierda:", None if RBTree1.is_NIL(RBTree1.root.get_left()) else RBTree1.root.get_left())
    print("Palabra de la derecha:", None if RBTree1.is_NIL(RBTree1.root.get_right()) else RBTree1.root.get_right())
    print("Numero de nodos:", RBTree1.count_nodes_tree())
    print("Numero de hojas:", RBTree1.count_leafs())
    print("Camino mas largo:", RBTree1.longest_path())
    print("Caminos de longitud 3:", RBTree1.paths_to_leaf_with_length(RBTree1.root, 3))
    draw_tree(RBTree1.root, max_levels=5)

    if Tree2.root is not None:
        print(f"\n--- INFORMACION DEL ARBOL DE LA LETRA {letter2.upper()} (Binario)---\n")
        print("Primera palabra:", Tree2.root)
        print("Palabra de la izquierda:", Tree2.root.get_left())
        print("Palabra de la derecha:", Tree2.root.get_right())
        print("Numero de nodos:", Tree2.count_nodes_tree())
        print("Numero de hojas:", Tree2.count_leafs())
        print("Camino mas largo:", Tree2.longest_path())
        print("Caminos de longitud 3:", Tree2.paths_to_leaf_with_length(Tree2.root, 3))
        draw_tree(Tree2.root, max_levels=5)

    if not RBTree2.is_NIL(RBTree2.root):
        print(f"\n--- INFORMACION DEL ARBOL DE LA LETRA {letter2.upper()} (Rojo-Negro)---\n")
        print("Primera palabra:", RBTree2.root)
        print("Palabra de la izquierda:", None if RBTree2.is_NIL(RBTree2.root.get_left()) else RBTree2.root.get_left())
        print("Palabra de la derecha:", None if RBTree2.is_NIL(RBTree2.root.get_right()) else RBTree2.root.get_right())
        print("Numero de nodos:", RBTree2.count_nodes_tree())
        print("Numero de hojas:", RBTree2.count_leafs())
        print("Camino mas largo:", RBTree2.longest_path())
        print("Caminos de longitud 3:", RBTree2.paths_to_leaf_with_length(RBTree2.root, 3))
        draw_tree(RBTree2.root, max_levels=5)

    if Tree3.root is not None:
        print(f"\n--- INFORMACION DEL ARBOL DE LA LETRA {letter3.upper()} (Binario)---\n")
        print("Primera palabra:", Tree3.root)
        print("Palabra de la izquierda:", Tree3.root.get_left())
        print("Palabra de la derecha:", Tree3.root.get_right())
        print("Numero de nodos:", Tree3.count_nodes_tree())
        print("Numero de hojas:", Tree3.count_leafs())
        print("Camino mas largo:", Tree3.longest_path())
        print("Caminos de longitud 3:", Tree3.paths_to_leaf_with_length(Tree3.root, 3))
        draw_tree(Tree3.root, max_levels=5)

    if not RBTree3.is_NIL(RBTree3.root):
        print(f"\n--- INFORMACION DEL ARBOL DE LA LETRA {letter3.upper()} (Rojo-Negro)---\n")
        print("Primera palabra:", RBTree3.root)
        print("Palabra de la izquierda:", None if RBTree3.is_NIL(RBTree3.root.get_left()) else RBTree3.root.get_left())
        print("Palabra de la derecha:", None if RBTree3.is_NIL(RBTree3.root.get_right()) else RBTree3.root.get_right())
        print("Numero de nodos:", RBTree3.count_nodes_tree())
        print("Numero de hojas:", RBTree3.count_leafs())
        print("Camino mas largo:", RBTree3.longest_path())
        print("Caminos de longitud 3:", RBTree3.paths_to_leaf_with_length(RBTree3.root, 3))
        draw_tree(RBTree3.root, max_levels=5)