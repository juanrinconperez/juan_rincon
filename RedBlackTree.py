from enum import Enum


class Color(Enum):
    RED = 0
    BLACK = 1


class Queue:
    """
    Class representing a circular queue with a size limit.

    Attributes:
    -----------
    head : int
        Index of the front element in the queue.
    tail : int
        Index of the last element in the queue.
    """

    def __init__(self, length: int):
        """
        Initializes an empty circular queue with a maximum capacity.

        Parameters:
        -----------
        length : int
            The maximum capacity of the circular queue.
        """
        self.array = [None] * length
        self.head = self.tail = -1
        self.length = length

    def size(self) -> int:
        if self.is_empty():
            return 0
        elif self.tail >= self.head:
            return self.tail - self.head + 1
        else:
            return self.length - (self.head - self.tail - 1)

    def is_full(self) -> bool:
        """
        Checks if the circular queue is full.

        Returns:
        --------
        bool
            True if the circular queue is full, False otherwise.
        """
        if self.is_empty():
            return False
        return (self.tail + 1) % self.length == self.head

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.

        Returns:
        --------
        bool
            True if the queue is empty, False otherwise.
        """
        return self.head == -1 and self.tail == -1

    def enqueue(self, item):
        """
        Adds an element to the circular queue if it is not full.

        Parameters:
        -----------
        item : any type
            The element to add to the circular queue.
        """
        if self.is_full():
            print("Queue is full")
        elif self.head == -1:
            self.head = self.tail = 0
            self.array[self.tail] = item
        else:
            self.tail = (self.tail + 1) % self.length
            self.array[self.tail] = item

    def dequeue(self):
        """
        Removes and returns the front element of the circular queue.

        Returns:
        --------
        any type
            The front element of the circular queue if it is not empty, None otherwise.
        """
        if self.is_empty():
            print("Queue is empty")
            return None
        elif self.head == self.tail:
            temp = self.array[self.head]
            self.array[self.head] = None
            self.head = self.tail = -1
            return temp
        else:
            temp = self.array[self.head]
            self.array[self.head] = None
            self.head = (self.head + 1) % self.length
            return temp

    def show(self):
        """
        Displays the elements of the circular queue in order.
        """
        if self.is_empty():
            print("Queue is empty")
        elif self.tail >= self.head:
            for i in range(self.head, self.tail + 1):
                print(self.array[i], end=" ")
        else:
            for i in range(self.head, self.length):
                print(self.array[i], end=" ")
            for i in range(0, self.tail + 1):
                print(self.array[i], end=" ")
        print()


class RBNode:
    def __init__(self, key, value=None, color=Color.RED):
        self._parent = None
        self._left = None
        self._right = None
        self.key = key
        self.data = value
        self.color = color

    def is_red(self) -> bool:
        return self.color == Color.RED

    def is_black(self) -> bool:
        return self.color == Color.BLACK

    def set_red(self) -> None:
        self.color = Color.RED

    def set_black(self) -> None:
        self.color = Color.BLACK

    def get_left(self) -> "RBNode":
        return self._left

    def set_left(self, node) -> None:
        self._left = node

    def get_right(self) -> "RBNode":
        return self._right

    def set_right(self, node) -> None:
        self._right = node

    def get_parent(self) -> "RBNode":
        return self._parent

    def set_parent(self, node) -> None:
        self._parent = node

    def __str__(self):
        return f"{self.data}"

    def is_nil(self):
        return self.get_left() == self and self.get_right() == self

    def show(self, level=0, prefix="Root: "):
        if self.is_nil():
            return

        indent = " " * (level * 4)
        print(f"{indent}{prefix}{self}")

        if not self.get_left().is_nil():
            self.get_left().show(level + 1, prefix="L--- ")
        if not self.get_right().is_nil():
            self.get_right().show(level + 1, prefix="R--- ")

    def height(self) -> int:
        """
        For each node explored it adds one to the height and follows the path with the higher height between left and right
        """
        if self.is_nil():
            return -1

        left_depth = self.get_left().height()
        right_depth = self.get_right().height()

        return 1 + max(left_depth, right_depth)

    def find_node(self, key) -> "RBNode":
        """
        Uses the structure of the Binary Trees to see in what place should the searched key be and returns the node
        If it doesn't find it it returns None
        """
        if self.is_nil():
            return None

        if self.key == key:
            return self

        if key > self.key:
            return self.get_right().find_node(key)

        if key < self.key:
            return self.get_left().find_node(key)

        return None

    def successor(self) -> "RBNode":
        """
        Finds the node with the following existing key and returns it
        If it doesn't find it it returns None
        """
        right = self.get_right()

        if not right.is_nil():
            return right.min_key()

        current = self
        parent = self.get_parent()

        while not parent.is_nil() and current == parent.get_right():
            current = parent
            parent = parent.get_parent()

        if parent.is_nil():
            return None

        return parent

    def min_key(self) -> "RBNode":
        """
        Goes always left to find the lower key node and returns it
        """
        current = self
        while not current.get_left().is_nil():
            current = current.get_left()
        return current

    def max_key(self) -> "RBNode":
        """
        Goes always right to find the maximum key node and returns it
        """
        current = self
        while not current.get_right().is_nil():
            current = current.get_right()
        return current

    def in_order_show(self) -> None:
        """
        Prints the nodes in order left subtree - right subtree - root
        """   
        if self.is_nil():
            return

        self.get_left().in_order_show()
        print(self)
        self.get_right().in_order_show()

    def pre_order_show(self) -> None:
        """
        Prints the nodes in order root - left subtree - right subtree
        """
        if self.is_nil():
            return

        print(self)
        self.get_left().pre_order_show()
        self.get_right().pre_order_show()

    def post_order_show(self) -> None:
        """
        Prints the nodes in order root - left subtree - right subtree
        """
        if self.is_nil():
            return

        self.get_left().post_order_show()
        self.get_right().post_order_show()
        print(self)

    def level_order_show(self) -> None:
        """
        Prints the nodes in order by levels from left to right using a queue
        We insert the sons of the node that we print and dequeue it until the queue is empty
        """
        if self.is_nil():
            return

        queue = Queue(max(1, 2 ** (self.height() + 2)))
        queue.enqueue(self)

        while not queue.is_empty():
            node = queue.dequeue()
            print(node)

            if not node.get_left().is_nil():
                queue.enqueue(node.get_left())
            if not node.get_right().is_nil():
                queue.enqueue(node.get_right())

    def number_descendants(self) -> int:
        """
        For each son that isn't None it adds one to the number of descentands (counter) and does it for the left and right recursively
        Returns the number of descendants (counter)
        """
        if self.is_nil():
            return 0

        counter = 0

        if not self.get_left().is_nil():
            counter += 1 + self.get_left().number_descendants()

        if not self.get_right().is_nil():
            counter += 1 + self.get_right().number_descendants()

        return counter

    def number_leafs(self) -> int:
        """
        Identifies if the node is a leaf (NIL sons) and it adds one for each of this case
        """
        if self.is_nil():
            return 0

        if self.get_left().is_nil() and self.get_right().is_nil():
            return 1

        counter = 0

        counter += self.get_left().number_leafs()
        counter += self.get_right().number_leafs()

        return counter

    def long_path(self) -> list:
        """
        It  checks if the left subtree has the bigger height or is the right one
        It adds the one that has the bigger high to a list and, recursively it follows that path

        If left is NIL it will always chose right and viceversa

        It ends when it reaches a lead node
        """
        if self.is_nil():
            return []

        if self.get_left().is_nil() and self.get_right().is_nil():
            return []

        if self.get_left().is_nil():
            return [self.get_right().data] + self.get_right().long_path()

        if self.get_right().is_nil():
            return [self.get_left().data] + self.get_left().long_path()

        if self.get_left().height() > self.get_right().height():
            return [self.get_left().data] + self.get_left().long_path()
        else:
            return [self.get_right().data] + self.get_right().long_path()
        
class RedBlackTree:
    def __init__(self, root: RBNode = None):
        self.NIL = RBNode(None, color=Color.BLACK)
        self.NIL.set_left(self.NIL)
        self.NIL.set_right(self.NIL)
        self.NIL.set_parent(self.NIL)

        self.root = self.NIL

        if root is not None:
            self.insert(root)

    def left_rotate(self, x: RBNode):
        """
        Performs a left rotation around node x.
        """
        y = x.get_right()
        x.set_right(y.get_left())

        if y.get_left() != self.NIL:
            y.get_left().set_parent(x)

        y.set_parent(x.get_parent())

        if x.get_parent() == self.NIL:
            self.root = y
        elif x == x.get_parent().get_left():
            x.get_parent().set_left(y)
        else:
            x.get_parent().set_right(y)

        y.set_left(x)
        x.set_parent(y)

    def right_rotate(self, y: RBNode):
        """
        Performs a right rotation around node y.
        """
        x = y.get_left()
        y.set_left(x.get_right())

        if x.get_right() != self.NIL:
            x.get_right().set_parent(y)

        x.set_parent(y.get_parent())

        if y.get_parent() == self.NIL:
            self.root = x
        elif y == y.get_parent().get_right():
            y.get_parent().set_right(x)
        else:
            y.get_parent().set_left(x)

        x.set_right(y)
        y.set_parent(x)

    def insert(self, z: RBNode):
        """
        Inserts a new node into the red-black tree.
        """
        z.set_left(self.NIL)
        z.set_right(self.NIL)

        y = self.NIL
        x = self.root

        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.get_left()
            else:
                x = x.get_right()

        z.set_parent(y)

        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.set_left(z)
        else:
            y.set_right(z)

        z.set_red()
        self.insert_fixup(z)

    def insert_fixup(self, z: RBNode):
        """
        Restores the red-black properties after an insertion.
        """
        while z.get_parent().is_red():
            if z.get_parent() == z.get_parent().get_parent().get_left():
                y = z.get_parent().get_parent().get_right()

                if y.is_red():
                    z.get_parent().set_black()
                    y.set_black()
                    z.get_parent().get_parent().set_red()
                    z = z.get_parent().get_parent()
                else:
                    if z == z.get_parent().get_right():
                        z = z.get_parent()
                        self.left_rotate(z)
                    z.get_parent().set_black()
                    z.get_parent().get_parent().set_red()
                    self.right_rotate(z.get_parent().get_parent())
            else:
                y = z.get_parent().get_parent().get_left()

                if y.is_red():
                    z.get_parent().set_black()
                    y.set_black()
                    z.get_parent().get_parent().set_red()
                    z = z.get_parent().get_parent()
                else:
                    if z == z.get_parent().get_left():
                        z = z.get_parent()
                        self.right_rotate(z)
                    z.get_parent().set_black()
                    z.get_parent().get_parent().set_red()
                    self.left_rotate(z.get_parent().get_parent())

        self.root.set_black()
        self.root.set_parent(self.NIL)

    def transplant(self, u: RBNode, v: RBNode) -> None:
        """
        Replaces the subtree rooted at u with the subtree rooted at v.
        """
        if u.get_parent() == self.NIL:
            self.root = v
        elif u == u.get_parent().get_left():
            u.get_parent().set_left(v)
        else:
            u.get_parent().set_right(v)

        v.set_parent(u.get_parent())

    def minimum(self, node: RBNode) -> RBNode:
        """
        Returns the node with the minimum key in a subtree.
        """
        while node.get_left() != self.NIL:
            node = node.get_left()
        return node

    def delete(self, key) -> None:
        """
        Deletes the node with the given key from the tree.
        """
        z = self.find_node_tree(key)
        if z is None:
            return

        y = z
        y_original_color = y.color

        if z.get_left() == self.NIL:
            x = z.get_right()
            self.transplant(z, z.get_right())

        elif z.get_right() == self.NIL:
            x = z.get_left()
            self.transplant(z, z.get_left())

        else:
            y = self.minimum(z.get_right())
            y_original_color = y.color
            x = y.get_right()

            if y.get_parent() == z:
                x.set_parent(y)
            else:
                self.transplant(y, y.get_right())
                y.set_right(z.get_right())
                y.get_right().set_parent(y)

            self.transplant(z, y)
            y.set_left(z.get_left())
            y.get_left().set_parent(y)
            y.color = z.color

        if y_original_color == Color.BLACK:
            self.delete_fixup(x)

    def delete_fixup(self, x: RBNode) -> None:
        """
        Restores the red-black properties after a deletion.
        """
        while x != self.root and x.is_black():
            if x == x.get_parent().get_left():
                w = x.get_parent().get_right()

                if w.is_red():
                    w.set_black()
                    x.get_parent().set_red()
                    self.left_rotate(x.get_parent())
                    w = x.get_parent().get_right()

                if w.get_left().is_black() and w.get_right().is_black():
                    w.set_red()
                    x = x.get_parent()
                else:
                    if w.get_right().is_black():
                        w.get_left().set_black()
                        w.set_red()
                        self.right_rotate(w)
                        w = x.get_parent().get_right()

                    w.color = x.get_parent().color
                    x.get_parent().set_black()
                    w.get_right().set_black()
                    self.left_rotate(x.get_parent())
                    x = self.root
            else:
                w = x.get_parent().get_left()

                if w.is_red():
                    w.set_black()
                    x.get_parent().set_red()
                    self.right_rotate(x.get_parent())
                    w = x.get_parent().get_left()

                if w.get_right().is_black() and w.get_left().is_black():
                    w.set_red()
                    x = x.get_parent()
                else:
                    if w.get_left().is_black():
                        w.get_right().set_black()
                        w.set_red()
                        self.left_rotate(w)
                        w = x.get_parent().get_left()

                    w.color = x.get_parent().color
                    x.get_parent().set_black()
                    w.get_left().set_black()
                    self.right_rotate(x.get_parent())
                    x = self.root

        x.set_black()

    def find_node_tree(self, key) -> RBNode:
        if self.root == self.NIL:
            return None
        return self.root.find_node(key)

    def in_order(self) -> None:
        if self.root == self.NIL:
            return
        self.root.in_order_show()

    def pre_order(self) -> None:
        if self.root == self.NIL:
            return
        self.root.pre_order_show()

    def post_order(self) -> None:
        if self.root == self.NIL:
            return
        self.root.post_order_show()

    def level_order(self) -> None:
        if self.root == self.NIL:
            return
        self.root.level_order_show()

    def count_nodes_tree(self) -> int:
        if self.root == self.NIL:
            return 0
        return 1 + self.root.number_descendants()

    def count_leafs(self) -> int:
        if self.root == self.NIL:
            return 0
        return self.root.number_leafs()

    def longest_path(self) -> list:
        if self.root == self.NIL:
            return []
        return [self.root.data] + self.root.long_path()

    def is_NIL(self, node: RBNode) -> bool:
        return node is self.NIL

    def paths_to_leaf_with_length(self, node: RBNode, remaining_edges: int, current_path: list[str] = None, results: list[list[str]] = None) -> list[list[str]]:
        """
        Returns all root-to-leaf paths with exact length (in edges) equal
        to remaining_edges at the beginning of the call

        Typical usage:
        paths = paths_to_leaf_with_length(tree.root, 3)

        Parameters:
        - node: current node (starts at the root)
        - remaining_edges: number of edges left to reach the target length
        - current_path: (internal) list storing the current path
        - results: (internal) accumulator of valid paths

        Returns:
        - List of paths; each path is a list of strings (str(node.key))
        """
        if current_path is None:
            current_path = []
        if results is None:
            results = []

        if not self.is_NIL(node) and remaining_edges >= 0:
            if current_path == []:
                current_path.append(node.data)

            if remaining_edges == 0 and self.is_NIL(node.get_left()) and self.is_NIL(node.get_right()):
                add_solution(current_path, results)
            else:
                for next_node in (node.get_left(), node.get_right()):
                    if not self.is_NIL(next_node):
                        remaining_edges = add_to_path(next_node, remaining_edges, current_path)
                        self.paths_to_leaf_with_length(next_node, remaining_edges, current_path, results)
                        remaining_edges = undo_path(remaining_edges, current_path)

        return results
    
def add_solution(current_path: list[str], results: list[list[str]]) -> None:
    results.append(current_path[:])


def add_to_path(node: RBNode, remaining_edges: int, current_path: list[str]) -> int:
    current_path.append(node.data)
    return remaining_edges - 1


def undo_path(remaining_edges: int, current_path: list[str]) -> int:
    current_path.pop()
    return remaining_edges + 1


if __name__ == "__main__":
    tree = RedBlackTree()

    print("INSERTANDO NODOS")
    tree.insert(RBNode(10, "diez"))
    tree.insert(RBNode(5, "cinco"))
    tree.insert(RBNode(15, "quince"))
    tree.insert(RBNode(3, "tres"))
    tree.insert(RBNode(7, "siete"))
    tree.insert(RBNode(12, "doce"))
    tree.insert(RBNode(18, "dieciocho"))
    tree.insert(RBNode(1, "uno"))
    tree.insert(RBNode(4, "cuatro"))
    tree.insert(RBNode(6, "seis"))
    tree.insert(RBNode(8, "ocho"))

    print("\nARBOL")
    tree.root.show()

    print("\nBUSQUEDA")
    print(tree.find_node_tree(7))
    print(tree.find_node_tree(20))

    print("\nRECORRIDOS")
    print("IN ORDER")
    tree.in_order()
    print("PRE ORDER")
    tree.pre_order()
    print("POST ORDER")
    tree.post_order()
    print("LEVEL ORDER")
    tree.level_order()

    print("\nINFORMACION")
    print("Numero de nodos:", tree.count_nodes_tree())
    print("Numero de hojas:", tree.count_leafs())
    print("Camino mas largo:", tree.longest_path())
    print("Caminos de longitud 3:", tree.paths_to_leaf_with_length(tree.root, 3))

    print("\nBORRADO HOJA (1)")
    tree.delete(1)
    tree.root.show()

    print("\nBORRADO NODO CON UN HIJO O REAJUSTE SIMPLE (3)")
    tree.delete(3)
    tree.root.show()

    print("\nBORRADO NODO INTERMEDIO (15)")
    tree.delete(15)
    tree.root.show()

    print("\nBORRADO RAIZ (10)")
    tree.delete(10)
    tree.root.show()

    print("\nRECORRIDOS FINALES")
    print("IN ORDER")
    tree.in_order()
    print("LEVEL ORDER")
    tree.level_order()

    print("\nINFORMACION FINAL")
    print("Numero de nodos:", tree.count_nodes_tree())
    print("Numero de hojas:", tree.count_leafs())
    print("Camino mas largo:", tree.longest_path())