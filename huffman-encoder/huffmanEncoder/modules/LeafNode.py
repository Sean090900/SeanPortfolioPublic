# Creator: Sean Dickson

class LeafNode():
    """
    Represents a leaf node in a Huffman Encoding Tree.

    Leaf nodes correspond to the actual characters (or symbols) being encoded.
    Each leaf stores a single character and its associated frequency, which
    determines its priority during Huffman tree construction.

    Unlike internal nodes, leaf nodes have no children — both `left` and `right`
    attributes are set to `None`. During encoding, the path from the tree root
    to a leaf defines the binary code assigned to that character.

    Attributes
    ----------
    character : str
        The character or symbol represented by this node.
    frequency : int or float
        The frequency (or weight) of this character in the input data.
    left : None
        Always None for leaf nodes (present for structural consistency).
    right : None
        Always None for leaf nodes (present for structural consistency).
    """

    def __init__(self, character, frequency):
        """
        This class is used to build leaf nodes for a Huffman Encoding Tree
        """
        self.character = character
        self.frequency = frequency
        self.right = None 
        self.left = None