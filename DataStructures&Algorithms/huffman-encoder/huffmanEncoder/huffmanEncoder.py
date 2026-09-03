# huffmanEncoder.py
#
# Contains the main functions used for huffmanEncoder...
#   huffmanBuildTree() builds the Huffman Encoding Tree (HET)
#   buildCharacterFrequencyTable() models the frequency table used to build the HET
#   huffmanGetCodes() obtains codes for each character in the HET
#   preorderTraverse() prints the HET by traversing in preorder
#   process_files() reads input and writes output
#
# Creator: Sean Dickson

from huffmanEncoder.modules.HETNodePriorityQueue import HETNodePriorityQueue
from huffmanEncoder.modules.LeafNode import LeafNode
from huffmanEncoder.modules.InternalNode import InternalNode

def huffmanBuildTree(inputFile):
    """
    Builds a Huffman Encoding Tree via a Frequency Table provides by user and returns its root
    :param inputFile: Frequency table file provided by the user
    :return: Root node of the tree
    """
    # First build the frequency table
    table = buildCharacterFrequencyTable(inputFile)

    # Make a priority queue of nodes
    nodes = HETNodePriorityQueue()
    for character, frequency in table.items():
        newLeaf = LeafNode(character, frequency)
        nodes.enqueue(newLeaf)

    # Make parent nodes up to the root
    while nodes.length() > 1:

        # Dequeue 2 lowest-priority nodes
        left = nodes.dequeue()
        right = nodes.dequeue()

        # Resolve tie if necessary
        if left.frequency == right.frequency and len(left.character) > len(right.character):
            left, right = right, left

        # Make a parent for the two nodes
        charSum = left.character + right.character
        freqSum = left.frequency + right.frequency
        parent = InternalNode(charSum, freqSum, left, right)

        # Enqueue parent back into priority queue
        nodes.enqueue(parent)

    # Return the root node
    return nodes.dequeue()


def buildCharacterFrequencyTable(file):
    """
    Builds a dictionary representing a frequency table provided by the user
    :param file: Frequency table file provided by the user
    :return: A dictionary representing the frequency table 
    """
    try:
        # Initialize dictionary
        table = dict()

        # Open input file
        for line in file.readlines():

            # Trim line and obtain character and frequency
            line = line.strip('\n').strip(' ')
            char = line.split(' - ')[0]
            freq = int(line.split(' - ')[1])

            # Raise error id more than one of the same character is found, otherise add char:freq to dictionary
            if char in table:
                raise Exception(f'Error: Character "{char}" found more than once in file...')
            else:
                table[char] = freq

        # Return dictionary
        return table
    
    except:
        raise Exception('Invalid FreqTable! Each line must be in format: "letter - frequency"')


def huffmanGetCodes(node, prefix, output):
    """
    Obtains Huffman codes for each chacter (leaf node) in a given tree
    :param node: The root of the Huffman Encoding Tree
    :param prefix: The string used to recursively build each Huffman code
    :param output: The dictionary used to store all Character:Code pairs
    :return: Returns the output dictionary
    """
    # Base Case: Check if node is a LeafNode
    if type(node) == LeafNode:
        output[node.character] = prefix
    
    # Otherwise, recursively build codes
    else:
        huffmanGetCodes(node.left, prefix + "0", output)
        huffmanGetCodes(node.right, prefix + "1", output)

    # Return codes dictionary
    return output


def preorderTraverse(node, output_file):
    """
    Prints out a Huffman Encoding Tree by traversing in Preorder
    :param node: The root of the tree
    :param output_file: The open output file as a TextIO object
    """
    if node != None: 
        output_file.write(node.character + ': ' + str(node.frequency) + '\n')
        preorderTraverse(node.left, output_file)
        preorderTraverse(node.right, output_file)


def process_files(encode, input_file, output_file, table_file):
    """
    Reads input file data, and writes output data to appropriate files.
    :param encode: A boolean describing if the task is encoding or decoding the input file
    :param input_file: The open input file as a TextIO object
    :param output_file: The open output file as a TextIO object
    :param table_file: The frequency table file as a TextIO object
    """
    # Build Huffman Encoding Tree
    treeRoot = huffmanBuildTree(table_file)

    # Obtain Huffman codes for each charcter, create inverse dict too
    codes = huffmanGetCodes(treeRoot, "", dict())
    inverse_codes = {v:k for k, v in codes.items()}

    # If the task is encoding...
    if encode:

        # Write header to output file
        output_file.write('--> ENCODED MESSAGES:\n\n')

        # Clean lines from file
        lines = [line.strip('\n').strip(' ').strip('.') for line in input_file.readlines()]

        for line in lines:

            # Skip line if empty
            if line == '':
                continue

            # Encode each line
            cipher = ''
            for char in line:
                if char.upper() in codes:
                    cipher += codes[char.upper()]

            # Write encoded lines to output
            if cipher:
                output_file.write(line + ' --> ')
                output_file.write(cipher + '\n')

    # Otherwise, the task is decoding...
    else:

        # Write header to output file
        output_file.write('--> DECODED MESSAGES:\n\n')

        # Clean lines from file
        lines = [line.strip('\n').strip(' ').strip('.') for line in input_file.readlines()]

        for line in lines:

            # Skip line if empty
            if line == '':
                continue

            # Decode each line
            message = ''
            chunk = ''
            for char in line:

                # Check for invalid characters
                if char not in ['0', '1']: 
                    output_file.write(f"Invalid Huffman code: Character '{char}' not allowed...\n")
                    break

                # Identify characters represented by code
                chunk += char
                if chunk in inverse_codes:
                    message += inverse_codes[chunk]
                    chunk = ''

            # Write decoded lines to output
            if message:
                output_file.write(line + ' --> ')
                output_file.write(message + '\n')

    # Print tree in preorder to terminal
    output_file.write('\n--> HUFFMAN TREE IN PREORDER:\n\n')
    preorderTraverse(treeRoot, output_file)
    