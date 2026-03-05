# Creator: Sean Dickson

class InternalNode():
    """
    Represents an internal (non-leaf) node in a Huffman Encoding Tree.

    In a Huffman tree, internal nodes are created by merging two child nodes—
    typically the two nodes with the lowest frequencies in the priority queue.
    The resulting node's frequency is the sum of its children's frequencies,
    and it stores references to the left and right child nodes.

    These nodes do not directly represent characters but instead act as
    intermediate connectors that help define the binary encoding structure
    of the final Huffman codes.

    Attributes
    ----------
    character : str or None
        The combined character(s) represented by this node (usually None or
        a concatenation of child symbols, used mainly for debugging).
    frequency : int or float
        The total frequency (or weight) of this node, equal to the sum of the
        frequencies of its left and right children.
    left : InternalNode or LeafNode
        The left child node in the Huffman tree.
    right : InternalNode or LeafNode
        The right child node in the Huffman tree.
    """

    def __init__(self, charSum, freqSum, left, right):
        """
        This class is used to build leaf nodes for a Huffman Encoding Tree
        """
        self.character = charSum
        self.frequency = freqSum
        self.left = left
        self.right = right 