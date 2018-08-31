
"""
written by Sophia Hyun
"""
from typing import Any, List


class Tree:
    """
    A class representing a Tree.

    value - The value of the Tree's root
    children - The root nodes of the children of this Tree.
    """
    value: Any
    children: List['Tree']

    def __init__(self, value: Any, children: List['Tree'] = None) -> None:
        """
        Initialize this Tree with the root value value and children children.
        """
        self.value = value

        # We make this a copy of the list children, in case it gets modified
        # at some point elsewhere.
        self.children = children[:] if children else []

    def sum_values(self) -> int:
        """
        Return the sum of all of the values in this Tree.

        >>> t = Tree(5, [Tree(3, [Tree(2)]), Tree(1)])
        >>> t.sum_values()
        11
        """
        if not self.children:
            return self.value

        return self.value + sum([child.sum_values() for child in self.children])

    def get_values(self) -> List:
        """
        Return a list of all values in this Tree.
        >>> t1 = Tree(1, [Tree(3, [Tree(4)])])
        >>> t2 = Tree(2, [Tree(8)])
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> t.get_values()
        [0, 1, 3, 4, 2, 8, 9, 7, 5]
        """
        return [self.value] + \
               sum([child.get_values() for child in self.children], [])

    def get_leaves(self) -> List:
        """
        Return a list of all of the leaves in this Tree.

        >>> t1 = Tree(1, [Tree(3, [Tree(4)])])
        >>> t2 = Tree(2, [Tree(8)])
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> t.get_leaves()
        [4, 8, 7, 5]
        """
        if self.children == []:
            return [self.value]

        return sum([child.get_leaves() for child in self.children], [])

    def get_height(self) -> int:
        """
        Return the height of this Tree.

        >>> t1 = Tree(1, [Tree(3, [Tree(4)])])
        >>> t2 = Tree(2, [Tree(8)])
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> t.get_height()
        4
        """
        if self.children == []:
            return 1

        return 1 + max([child.get_height() for child in self.children])

    def contains(self, value: Any) -> bool:
        """
        Return whether value appears anywhere in this Tree.

        >>> t1 = Tree(1, [Tree(3, [Tree(4)])])
        >>> t2 = Tree(2, [Tree(8)])
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> t.contains(5)
        True
        >>> t.contains(20)
        False
        """
        if self.value == value:
            return True

        return any([child.contains(value) for child in self.children])

    def get_closest_common_ancestor(self, value1: Any, value2: Any) -> Any:
        """
        Return the value of the closest common ancestor of the node with
        value value1 and the node with value value2, None if no such nodes
        exist.

        >>> t1 = Tree(1, [Tree(3, [Tree(4)])])
        >>> t2 = Tree(2, [Tree(8)])
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> t.get_closest_common_ancestor(5, 7)
        9
        >>> t.get_closest_common_ancestor(5, 9)
        0
        >>> t.get_closest_common_ancestor(0, 5) == None
        True
        >>> t.get_closest_common_ancestor(10, 3) == None
        True
        """
        recursive_calls = [child.get_closest_common_ancestor(value1, value2)
                           for child in self.children]

        for result in recursive_calls:
            if result is not None:
                return result

        # We check the child instead of self, otherwise we could count as
        # an ancestor.
        found_value1 = any([child.contains(value1) for child in self.children])
        found_value2 = any([child.contains(value2) for child in self.children])

        return self.value if (found_value1 and found_value2) else None

    def print_preorder(self) -> None:
        """
        Print the nodes in this Tree in pre-order.

        >>> t1 = Tree(1, [Tree(3, [Tree(4)])])
        >>> t2 = Tree(2, [Tree(8)])
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> t.print_preorder()
        0
        1
        3
        4
        2
        8
        9
        7
        5
        """
        print(self.value)
        for child in self.children:
            child.print_preorder()

    def print_postorder(self) -> None:
        """
        Print the nodes in this Tree in post-order.

        >>> t1 = Tree(1, [Tree(3, [Tree(4)])])
        >>> t2 = Tree(2, [Tree(8)])
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> t.print_postorder()
        4
        3
        1
        8
        2
        7
        5
        9
        0
        """
        for child in self.children:
            child.print_postorder()
        print(self.value)

    # __str__ wasn't covered in class, but feel free to look it over.
    # This is just for convenience when printing a Tree.
    def __str__(self) -> str:
        """
        Return the string representation of this Tree, such that the root
        node is at the top, and all subtrees are below it. Every line of
        the string has the same length (being padded with spaces if needed).

        >>> t1 = Tree(1, [Tree(3, [Tree(4), Tree(6)])])
        >>> print(t1)
          1
          3
        4   6
        >>> t2 = Tree(2, [Tree(8)])
        >>> print(t2)
        2
        8
        >>> t3 = Tree(9, [Tree(7), Tree(5)])
        >>> print(t3)
          9
        7   5
        >>> children = [t1, t2, t3]
        >>> t = Tree(0, children)
        >>> print(t)
                0
          1     2     9
          3     8   7   5
        4   6
        """
        child_strings = [str(child).split('\n') for child in self.children]

        # Get the maximum number of lines from a child's string
        max_lines = 0
        if child_strings:
            max_lines = max([len(child) for child in child_strings])

        # Create a list with max_lines empty lists in it
        new_string = [[] for _ in range(max_lines)]

        # Join each line of each child's string
        for i in range(max_lines):
            for child in child_strings:
                if i < len(child):
                    new_string[i].append(child[i])
                else:
                    # If there is no such line, just pad it with spaces
                    new_string[i].append(" " * len(child[0]))

        # Put 3 spaces between each subtree
        new_string_joined = [(' ' * 3).join(child) for child in new_string]

        # Add in the value of the current Tree
        str_width = 0
        if new_string_joined:
            str_width = len(new_string_joined[0])

        left_padding = str_width // 2
        right_padding = (str_width - str_width // 2) - 1

        new_string_joined.insert(0, "{}{}{}".format(" " * left_padding,
                                                    self.value,
                                                    " " * right_padding))

        # Return the new string
        return "\n".join(new_string_joined)
