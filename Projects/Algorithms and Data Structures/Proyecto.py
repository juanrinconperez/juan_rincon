from BinaryTree import *

letters = input("Escriba hasta un máximo de tres letras. Todas seguidas \n").lower().strip()
while len(letters) > 3 or len(letters) < 1:
    letters = input("Escriba entre una y tres letras. Todas seguidas \n").lower().strip()

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

with open("palabras_RAE.txt", "r", encoding = "utf-8") as words:
    for line in words:
        line = line.strip()
        first_letter = line[0]
        if first_letter == letter1:
            node = Node(len(line), line)
            if Tree1.root is None:
                node.key = 5 # len(letter) = 5 We try to find a balanced tree, because the first letter will be always the letter itself
                Tree1.root = node
            else:
                Tree1.insert_node(node)

        elif letter2 is not None and letter2 == first_letter:
            node = Node(len(line), line)
            if Tree2.root is None:
                node.key = 5 # len(letter) = 5 We try to find a balanced tree, because the first letter will be always the letter itself
                Tree2.root = node
            else:
                Tree2.insert_node(node)

        elif letter3 is not None and letter3 == first_letter:
            node = Node(len(line), line)
            if Tree3.root is None:
                node.key = 5 # len(letter) = 5 We try to find a balanced tree, because the first letter will be always the letter itself
                Tree3.root = node
            else:
                Tree3.insert_node(node)

print("Primera letra: \n")
print("\tLetra:", Tree1.root)
print("\tPalabra de la izquierda:", Tree1.root.get_left())
print("\tPalabra de la derecha:", Tree1.root.get_right())

if Tree2.root is not None:
    print("Second Letter: \n")
    print("\tLetra:", Tree2.root)
    print("\tPalabra de la izquierda:", Tree2.root.get_left())
    print("\tPalabra de la derecha:", Tree2.root.get_right())

if Tree3.root is not None:
    print("Third Letter: \n")
    print("\tLetra:", Tree3.root)
    print("\tPalabra de la izquierda:", Tree3.root.get_left())
    print("\tPalabra de la derecha:", Tree3.root.get_right())
