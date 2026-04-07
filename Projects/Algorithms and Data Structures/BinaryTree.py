import sys
from enum import Enum

sys.setrecursionlimit(15000)

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


class Node:
    def __init__(self, key, value=None):
        """
        Initializes a new Node with a key and an optional value.

        Parameters:
        ----------
        key : any
            Unique identifier for the node.
        value : any, optional
            Additional data associated with the node.
        """
        self._parent = None
        self._left = None
        self._right = None
        self.key = key
        self.data = value

    def get_left(self) -> 'Node':
        """
        Retrieves the left child of the node.

        Returns:
        -------
        Node or None
        """
        return self._left

    def set_left(self, node) -> None:
        """
        Sets the left child of the node and updates the parent reference.

        Parameters:
        ----------
        node : Node
        """
        self._left = node
        if node is not None:
            node.set_parent(self)

    def get_right(self) -> 'Node':
        """
        Retrieves the right child of the node.

        Returns:
        -------
        Node or None
        """
        return self._right

    def set_right(self, node) -> None:
        """
        Sets the right child of the node and updates the parent reference.

        Parameters:
        ----------
        node : Node
        """
        self._right = node
        if node is not None:
            node.set_parent(self)

    def get_parent(self) -> 'Node':
        """
        Retrieves the parent of the node.

        Returns:
        -------
        Node or None
        """
        return self._parent

    def set_parent(self, node) -> None:
        """
        Sets the parent of the node.

        Parameters:
        ----------
        node : Node
        """
        self._parent = node

    def __str__(self):
        """
        Returns a string representation of the node (its key).
        """
        return f"Word: {self.data} Lenght: {self.key}"

    def show(self, level=0, prefix="Root: ") -> None:
        indent = " " * (level * 4)
        print(f"{indent}{prefix}{self}")

        if self.get_left() is not None:
            self.get_left().show(level + 1, prefix="L--- ")
        if self.get_right() is not None:
            self.get_right().show(level + 1, prefix="R--- ")

    def height(self) -> int:
        if self.get_left() is None:
            left_depth = -1
        else:
            left_depth = self.get_left().height()

        if self.get_right() is None:
            right_depth = -1
        else:
            right_depth = self.get_right().height()
        
        return 1 + max(left_depth, right_depth)
    
    def find_node(self, key) -> "Node":
        if self.key == key:
            return self
        if key > self.key and self.get_right() is not None:
            return self.get_right().find_node(key)
        if key < self.key and self.get_left() is not None:
            return self.get_left().find_node(key)
        return None
    
    def successor(self) -> "Node":
        right = self.get_right()
        if right is not None:
            return right.min_key()
        
        current = self
        parent = self.get_parent()

        while parent is not None and current == parent.get_right():
            current = parent
            parent = parent.get_parent()
        
        return parent

    def min_key(self) -> "Node":
        current = self
        while current.get_left() is not None:
            current = current.get_left()
        return current
    
    def max_key(self) -> "Node":
        current = self
        while current.get_right() is not None:
            current = current.get_right()
        return current
        
    def in_order_show(self) -> None:
        if self.get_left() is not None:
            self.get_left().in_order_show()
        print(self)
        if self.get_right() is not None:
            self.get_right().in_order_show()

    def pre_order_show(self) -> None:
        print(self)
        if self.get_left() is not None:
            self.get_left().pre_order_show()
        if self.get_right() is not None:
            self.get_right().pre_order_show()

    def post_order_show(self) -> None:
        if self.get_left() is not None:
            self.get_left().post_order_show()
        if self.get_right() is not None:
            self.get_right().post_order_show()
        print(self)

    def level_order_show(self) -> None:
        queue = Queue(max(1, 2 ** (self.height() + 1)))
        queue.enqueue(self)
        while not queue.is_empty():
            node = queue.dequeue()
            print(node)
            if node.get_left() is not None:
                queue.enqueue(node.get_left())
            if node.get_right() is not None:
                queue.enqueue(node.get_right())

    def number_descendants(self) -> int:
        counter = 0

        if self.get_left() is not None:
            counter += 1 + self.get_left().number_descendants()

        if self.get_right() is not None:
            counter += 1 + self.get_right().number_descendants()

        return counter
        
    def number_leafs(self) -> int:
        counter = 0

        if self.get_left() is None and self.get_right() is None:
            return 1
        
        if self.get_left() is not None:
            counter += self.get_left().number_leafs()
        
        if self.get_right() is not None:
            counter += self.get_right().number_leafs()
    
        return counter
    
    def long_path(self) -> list:
        if self.get_left() is None and self.get_right() is None:
            return []

        if self.get_left() is None:
            return [self.get_right().data] + self.get_right().long_path()

        if self.get_right() is None:
            return [self.get_left().data] + self.get_left().long_path()

        if self.get_left().height() > self.get_right().height():
            return [self.get_left().data] + self.get_left().long_path()
        else:
            return [self.get_right().data] + self.get_right().long_path()


class BinaryTree:
    def __init__(self):
        """
        Initializes the binary tree with no root node.

        Parameters:
        ----------
        root : Node
            The root node of the binary tree.
        """
        self.root = None

    def show(self) -> None:
        """Displays the entire binary tree."""
        if self.root is not None:
            self.root.show()
    
    def height(self) -> int:
        if self.root is None:
            return -1
        return self.root.height()
    
    def find_node(self, key) -> Node | None:
        if self.root is None:
            return None
        return self.root.find_node(key)
    
    def insert_node(self, node: Node) -> None:
        if self.root is None:
            self.root = node
            node.set_parent(None)
            return

        current = self.root

        while current is not None:
            if node.key > current.key:
                if current.get_right() is None:
                    current.set_right(node)
                    return
                current = current.get_right()
            else:
                if current.get_left() is None:
                    current.set_left(node)
                    return
                current = current.get_left()

    def delete_node(self, key) -> bool:
        node = self.find_node(key)
        if node is None:
            return False

        left = node.get_left()
        right = node.get_right()
        parent = node.get_parent()

        if left is None and right is None:
            if parent is None:
                self.root = None
            elif parent.get_left() == node:
                parent.set_left(None)
            else:
                parent.set_right(None)

        elif left is None:
            if parent is None:
                self.root = right
                right.set_parent(None)
            elif parent.get_left() == node:
                parent.set_left(right)
            else:
                parent.set_right(right)

        elif right is None:
            if parent is None:
                self.root = left
                left.set_parent(None)
            elif parent.get_left() == node:
                parent.set_left(left)
            else:
                parent.set_right(left)

        else:
            successor = node.successor()
            node.key = successor.key
            node.data = successor.data

            succ_parent = successor.get_parent()
            succ_right = successor.get_right()

            if succ_parent.get_left() == successor:
                succ_parent.set_left(succ_right)
            else:
                succ_parent.set_right(succ_right)

            if succ_right is not None:
                succ_right.set_parent(succ_parent)

        return True
    
    def skew(self) -> bool:
        node = self.root
        if self.root is None:
            print("Empty tree")
            return False

        if node.get_left() is not None:
            height_left = node.get_left().height()
        else:
            height_left = -1

        if node.get_right() is not None:
            height_right = node.get_right().height()
        else:
            height_right = -1

        return abs(height_right - height_left) <= 1
        
    def in_order(self) -> None:
        if self.root is None:
            return
        self.root.in_order_show()

    def pre_order(self) -> None:
        if self.root is None:
            return
        self.root.pre_order_show()

    def post_order(self) -> None:
        if self.root is None:
            return
        self.root.post_order_show()

    def level_order(self) -> None:
        if self.root is None:
            return
        self.root.level_order_show()

    def count_nodes_tree(self) -> int:
        if self.root is None:
            return 0
        return 1 + self.root.number_descendants()

    def count_leafs(self) -> int:
        if self.root is None:
            return 0
        return self.root.number_leafs()
    
    def longest_path(self) -> list:
        if self.root is None:
            return []
        return [self.root.data] + self.root.long_path()
    

class Color(Enum):
    RED = 0
    BLACK = 1

class RBNode:
    def __init__(self, key, value=None, color=Color.RED):
        # Pointer to parent, left, and right children
        self._parent = None
        self._left = None
        self._right = None
        # Key that identifies the node
        self.key = key
        # Additional data
        self.data = value
        # Color of the node
        self.color = color

    def is_red(self) -> bool:
        """
        Checks if the node is red.
        """
        return self.color == Color.RED

    def is_black(self) -> bool:
        """
        Checks if the node is black.
        """
        return self.color == Color.BLACK

    def set_red(self) -> None:
        """
        Sets the node color to red.
        """
        self.color = Color.RED

    def set_black(self) -> None:
        """
        Sets the node color to black.
        """
        self.color = Color.BLACK

    def get_left(self) -> 'RBNode':
        """
        Gets the left child node.
        """
        return self._left

    def set_left(self, node) -> None:
        """
        Sets the left child node.
        """
        self._left = node

    def get_right(self) -> 'RBNode':
        """
        Gets the right child node.
        """
        return self._right

    def set_right(self, node) -> None:
        """
        Sets the right child node.
        """
        self._right = node

    def get_parent(self) -> 'RBNode':
        """
        Gets the parent node.
        """
        return self._parent

    def set_parent(self, node) -> None:
        """
        Sets the parent node.
        """
        self._parent = node

    def __str__(self):
        """
        Returns a string representation of the node, showing the key and color.
        """
        color_str = "R" if self.is_red() else "B"
        return f"{self.key} ({color_str})"

    def show(self, level=0, prefix="Root: "):
        """
        Displays the node and its descendants hierarchically, including color information.
        """
        indent = " " * (level * 4)
        print(f"{indent}{prefix}{self}")

        if self.get_left() is not None and self.get_left().get_left() is not None:
            self.get_left().show(level + 1, prefix="L--- ")
        if self.get_right() is not None and self.get_right().get_right() is not None:
            self.get_right().show(level + 1, prefix="R--- ")


class RedBlackTree:
    def __init__(self, root: RBNode = None):
        self.NIL = RBNode(None)
        self.NIL.set_black()
        self.NIL.set_left(None)
        self.NIL.set_right(None)

        self.root = self.NIL
        if root is not None:
            self.insert(root.key, root.data)
        

    def left_rotate(self, x: RBNode):
        """
        Performs a left rotation on the node x.
        """
        y = x.get_right()  # Set y
        x.set_right(y.get_left())  # Turn y's left subtree into x's right subtree
        if y.get_left() != self.NIL:
            y.get_left().set_parent(x)  # Update parent of y's left subtree

        y.set_parent(x.get_parent())  # Link y's parent to x's parent
        if x.get_parent() is self.NIL:  # x was the root
            self.root = y
        elif x == x.get_parent().get_left():  # x was a left child
            x.get_parent().set_left(y)
        else:  # x was a right child
            x.get_parent().set_right(y)

        y.set_left(x)  # Put x on y's left
        x.set_parent(y)

    def right_rotate(self, y: RBNode):
        """
        Performs a right rotation on the node y.
        """
        pass

    def insert(self, key, value):
        """
        Inserts a node z into the Red-Black Tree.
        """
        pass

    def insert_fixup(self, z: RBNode):
        """
        Fixes the Red-Black Tree properties after insertion.
        """
        pass