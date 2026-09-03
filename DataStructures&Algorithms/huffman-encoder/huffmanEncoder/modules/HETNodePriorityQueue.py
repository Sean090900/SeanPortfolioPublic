# Creator: Sean Dickson

class HETNodePriorityQueue():
    """
    A priority queue for Huffman Tree nodes, implemented using insertion sort.

    This class maintains an ordered list of nodes based on their frequency values
    (i.e., priority). Lower-frequency nodes are prioritized first to align with
    the Huffman encoding algorithm, which repeatedly merges the two least
    frequent nodes into a new combined node.

    Internally, insertion sort is used to insert new nodes into the correct position
    in the queue. This approach, while less efficient for large datasets than a
    binary heap, is simple and effective for Huffman trees where the number of
    nodes is relatively small.

    Attributes
    ----------
    queue : list
        A list of Huffman nodes sorted by ascending frequency.
    """
    
    def __init__(self):
        """
        This class is used to build a Priority Queue.
        """
        self.queue = []

    def length(self):
        """
        Calculates the current length of the Priority Queue
        :return: The length of the Priority Queue as an int
        """
        return len(self.queue)

    def isEmpty(self):
        """
        Determines if the priority queue is currently holding any items.
        :return: True if the priority queue currently has no items, False otherwise
        """
        if self.queue == []:
            return True
        else:
            return False

    def enqueue(self, node):
        """
        Adds a node to the Priority Queue and sorts appropriately
        :param node: The node to add to the Priority Queue
        """
        self.queue.append(node)
        self.insertionSort()
        
    def dequeue(self):
        """
        Removes item from the front of the Priority Queue and returns it
        :return: The current item from front of the Priority Queue
        """
        if not self.isEmpty():
            item = self.queue[0]
            self.queue = self.queue[1:]
            return item
        else:
            raise Exception('Priority Queue is empty! Cannot delete...')
        
    def insertionSort(self):
        """
        Sorts HET nodes in ascending order via the insertion sort algorithm
        """
        for i in range(self.length()):
            j = i
            while j > 0 and self.queue[j].frequency < self.queue[j-1].frequency:
                temp = self.queue[j]
                self.queue[j] = self.queue[j-1]
                self.queue[j-1] = temp
                j -= 1
