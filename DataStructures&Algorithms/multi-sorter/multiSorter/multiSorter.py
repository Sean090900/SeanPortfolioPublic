# multiSorter.py
#
# Contains the main functions used for MultiSorter...
#     quicksort_option1():   Quicksorting algorithm (variant 1)
#     quicksort_option2():   Quicksorting algorithm (variant 2)
#     quicksort_option3():   Quicksorting algorithm (variant 3)
#     quicksort_option4():   Quicksorting algorithm (variant 4)
#     partition():           Partitioning algorithm used by quicksort functions
#     insertionSort():       Insertion sort algorithm used by quicksort functions
#     mergeSort():           Merge Sort algorithm (included as enhancment)
#     naturalMerge():        Natural Merge Sort algorithm
#     merge():               The merging algorithm used by mergeSort() and naturalMerge()
#
# Creator: Sean Dickson

# Imports
from pathlib import Path
import sys

# Set recursion limit to 20000, as necessary for larger files
sys.setrecursionlimit(20000)

def quicksort_option1(integers, lowIndex, highIndex, counters):
    """
    Sorts integers in ascending order via the quicksort sort algorithm.
    Quicksort Option 1: 
        A) Select the first item of the partition as the pivot. 
        B) Treat partitions of size one and two as stopping cases.
    :param integers: The list of integers to be sorted
    :param lowIndex: An index representing the start of the partition
    :param highIndex: An index representing the end of the partition
    :param counters: A dictionary used for counting comparisons and exchanges made
    """
    # Stop Cases: Partition is of size 1 or 2 (ensure sorted if size 2)
    if len(integers[lowIndex:highIndex+1]) == 2:
        counters['comparisons'] += 1
        if integers[lowIndex] > integers[highIndex]:
            integers[lowIndex], integers[highIndex] = integers[highIndex], integers[lowIndex]
            counters['exchanges'] += 1
        return
    elif len(integers[lowIndex:highIndex+1]) <= 1:
        return
    
    # Identify pivot as first element of the list
    pivot = integers[lowIndex]

    # Partition and recurively sort
    lowEndIndex = partition(integers, pivot, lowIndex, highIndex, counters)
    quicksort_option1(integers, lowIndex, lowEndIndex, counters)
    quicksort_option1(integers, lowEndIndex + 1, highIndex, counters)


def quicksort_option2(integers, lowIndex, highIndex, counters):
    """
    Sorts integers in ascending order via the quicksort sort algorithm.
    Quicksort Option 2: 
        A) Select the first item of the partition as the pivot. 
        B) For a partition of size 100 or less, use an insertion sort to finish
    :param integers: The list of integers to be sorted
    :param lowIndex: An index representing the start of the partition
    :param highIndex: An index representing the end of the partition
    :param counters: A dictionary used for counting comparisons and exchanges made
    """
    # Stop Cases: Partition is of size 100 or less (use insertion sort from here)
    if len(integers[lowIndex:highIndex+1]) <= 100:
        insertionSort(integers, lowIndex, highIndex+1, counters)
        return
    
    # Identify pivot as first element of the list
    pivot = integers[lowIndex]

    # Partition and recurively sort
    lowEndIndex = partition(integers, pivot, lowIndex, highIndex, counters)
    quicksort_option2(integers, lowIndex, lowEndIndex, counters)
    quicksort_option2(integers, lowEndIndex + 1, highIndex, counters)


def quicksort_option3(integers, lowIndex, highIndex, counters):
    """
    Sorts integers in ascending order via the quicksort sort algorithm.
    Quicksort Option 3: 
        A) Select the first item of the partition as the pivot. 
        B) For a partition of size 50 or less, use an insertion sort to finish
    :param integers: The list of integers to be sorted
    :param lowIndex: An index representing the start of the partition
    :param highIndex: An index representing the end of the partition
    :param counters: A dictionary used for counting comparisons and exchanges made
    """
    # Stop Cases: Partition is of size 100 or less (use insertion sort from here)
    if len(integers[lowIndex:highIndex+1]) <= 50:
        insertionSort(integers, lowIndex, highIndex+1, counters)
        return
    
    # Identify pivot as first element of the list
    pivot = integers[lowIndex]

    # Partition and recurively sort
    lowEndIndex = partition(integers, pivot, lowIndex, highIndex, counters)
    quicksort_option3(integers, lowIndex, lowEndIndex, counters)
    quicksort_option3(integers, lowEndIndex + 1, highIndex, counters)


def quicksort_option4(integers, lowIndex, highIndex, counters):
    """
    Sorts integers in ascending order via the quicksort sort algorithm.
    Quicksort Option 4: 
        A) Select the median-of-three as the pivot. 
        B) Treat partitions of size one and two as stopping cases.
    :param integers: The list of integers to be sorted
    :param lowIndex: An index representing the start of the partition
    :param highIndex: An index representing the end of the partition
    :param counters: A dictionary used for counting comparisons and exchanges made
    """
    # Stop Cases: Partition is of size 1 or 2 (ensure sorted if size 2)
    if len(integers[lowIndex:highIndex+1]) == 2:
        counters['comparisons'] += 1
        if integers[lowIndex] > integers[highIndex]:
            integers[lowIndex], integers[highIndex] = integers[highIndex], integers[lowIndex]
            counters['exchanges'] += 1
        return
    elif len(integers[lowIndex:highIndex+1]) <= 1:
        return
    
    # Identify pivot as 'median-of-three'
    median_of_three_list = [integers[lowIndex], integers[int(lowIndex + (highIndex - lowIndex) / 2)], integers[highIndex]]
    insertionSort(median_of_three_list, 0, len(median_of_three_list), counters)
    pivot = median_of_three_list[1]

    # Partition and recurively sort
    lowEndIndex = partition(integers, pivot, lowIndex, highIndex, counters)
    quicksort_option4(integers, lowIndex, lowEndIndex, counters)
    quicksort_option4(integers, lowEndIndex + 1, highIndex, counters)


def partition(integers, pivot, lowIndex, highIndex, counters):
    """
    Partitioning algorithm used for Quicksort functions
    :param integers: The list of integers to be sorted
    :param pivot: The integer in the list used to split into 2 partitions
    :param lowIndex: An index representing the start of the partition
    :param highIndex: An index representing the end of the partition
    :param counters: A dictionary used for counting comparisons and exchanges made
    """
    # Loop until the low index is higher than the high index
    done = False
    while not done:
        
        # Raise lowIndex until its greater than or equal to pivot
        while integers[lowIndex] < pivot:
            counters['comparisons'] += 1
            lowIndex += 1

        # Lower lowIndex until its less than or equal to pivot
        while pivot < integers[highIndex]:
            counters['comparisons'] += 1
            highIndex -= 1

        counters['comparisons'] += 2

        # If zero or one elements remain, then all numbers are partitioned
        if lowIndex >= highIndex:
            done = True

        else:
            
            # Swap integers[lowIndex] and integers[highIndex]
            temp = integers[lowIndex]
            integers[lowIndex] = integers[highIndex]
            integers[highIndex] = temp
            counters['exchanges'] += 1

            # Update lowIndex and highIndex
            lowIndex += 1
            highIndex -= 1

    # Return the value of highIndex
    return highIndex


def insertionSort(integers, lowEndIndex, highIndex, counters):
    """
    Sorts integers in ascending order via the insertion sort algorithm.
    :param integers: The list of integers to be sorted
    :param lowIndex: An index representing the start of the partition
    :param highIndex: An index representing the end of the partition
    :param counters: A dictionary used for counting comparisons and exchanges made
    """
    for i in range(lowEndIndex, highIndex):
        j = i
        while j > 0 and integers[j] < integers[j-1]:
            counters['comparisons'] += 1
            temp = integers[j]
            integers[j] = integers[j-1]
            integers[j-1] = temp
            counters['exchanges'] += 1
            j -= 1
        counters['comparisons'] += 1


def mergeSort(integers, i, k, counters):
    """
    Sorts integers in ascending order via the merge sort algorithm.
    :param integers: The list of integers to be sorted.
    :param i: An index representing the start of the partition.
    :param k: An index representing the end of the partition.
    :param counter: A dictionary used for counting comparisons and exchanges made.
    """
    j = 0

    if i < k:

        # Find the midpoint in the partition
        j = int((i + k) / 2)  
        
        # Recursively sort left and right partitions
        mergeSort(integers, i, j, counters)
        mergeSort(integers, j + 1, k, counters)
        
        # Merge left and right partition in sorted order
        merge(integers, i, j, k, counters)


# Natural Merge
def naturalMerge(integers, counters, start=0):
    """
    Sorts integers in ascending order via the natural merge sort algorithm.
    :param integers: The list of integers to be sorted.
    :param counter: A dictionary used for counting comparisons and exchanges made.
    :param start: An integer representing the start of the list (0 by default)
    """
    # Base case: no more runs to process
    n = len(integers)
    if start >= n:
        return  

    # Find the end of the current sorted run
    end = start
    while end + 1 < n and integers[end] <= integers[end + 1]:
        counters['comparisons'] += 1
        end += 1
    counters['comparisons'] += 1
    
    # Recursively find and merge the remaining runs
    if end < n - 1:
        naturalMerge(integers, counters, end + 1)
    
    # Merge the current run with the next run (if there is a next one)
    if end + 1 < n:
        merge(integers, start, end, n - 1, counters)
    
    # Return the sorted list after all merges
    return integers


def merge(integers, i, j, k, counters):
    """
    The merging algorithm for merge sort and natural merge sort functions.
    :param integers: The list of integers to be sorted.
    :param i: An index representing the start of the partition.
    :param j: An index representing the midpoint of the partition.
    :param k: An index representing the end of the partition.
    :param counter: A dictionary used for counting comparisons and exchanges made.
    """
    mergedSize = k - i + 1
    mergePos = 0
    leftPos = i
    rightPos = j + 1
    mergedNumbers = [None for _ in range(mergedSize)]
    
    # Add smallest element from left or right partition to merged numbers
    while leftPos <= j and rightPos <= k:
        counters['comparisons'] += 1
        if integers[leftPos] <= integers[rightPos]:
            mergedNumbers[mergePos] = integers[leftPos]
            leftPos += 1
        else:
            counters['exchanges'] += 1
            mergedNumbers[mergePos] = integers[rightPos]
            rightPos += 1
        mergePos += 1
    
    # If left partition is not empty, add remaining elements to merged numbers
    while leftPos <= j:
        counters['comparisons'] += 1
        mergedNumbers[mergePos] = integers[leftPos]
        leftPos += 1
        mergePos += 1
    
    # If right partition is not empty, add remaining elements to merged numbers
    while rightPos <= k:
        counters['comparisons'] += 1
        mergedNumbers[mergePos] = integers[rightPos]
        rightPos += 1
        mergePos += 1
    
    # Copy merged numbers back to the integers
    for mergePos in range(mergedSize):
        integers[i + mergePos] = mergedNumbers[mergePos]


def process_files(input_file, output_file):
    """
    Reads input file data, and writes output data to appropriate files.
    :param input_file: The open input file as a TextIO object
    :param output_file: The open output file as a TextIO object
    """
    # Attmept to convert file to array of ints
    try:
        integers = [int(integer.strip()) for integer in input_file.readlines()]
    except:
        raise Exception(f'Invalid input in file: {input_file}. Ensure only integers are present!')

    # Write head for output file
    output_file.write('1. Quicksort (Variation 1): Pivot = 1st Item, Stopping Cases = Partions of size 1 and 2\n\n')

    # Run Quicksort (option 1) on input file, write output
    try:
        # Attempt to make list of integers
        integers_copy = list(integers)

        # Setup counters for comparisons and exchanges
        counters = {
            'comparisons': 0,
            'exchanges': 0
        }

        # Run sorting algorithm
        quicksort_option1(integers_copy, 0, len(integers_copy)-1, counters)

        # Write out comparisons and exchanges made
        output_file.write(f'Comparisons: {counters["comparisons"]}\n')
        output_file.write(f'Exchanges: {counters["exchanges"]}\n\n')

        # If size is <= 50, print the sorted results
        if len(integers_copy) <= 50:
            output_file.write('--> Sorted Integers:\n')
            for item in integers_copy:
                output_file.write('    ' + str(item) + '\n')

    except RecursionError as e:
        output_file.write(f'Hit max recursion limit! {e}\n\n')

    # Write head for output file
    output_file.write('\n2. Quicksort (Variation 2): Pivot = 1st Item, Insertion Sort used for partitions <= 100\n\n')

    # Run Quicksort (option 2) on input file, write output
    try:
        # Attempt to make list of integers
        integers_copy = list(integers)

        # Setup counters for comparisons and exchanges
        counters = {
            'comparisons': 0,
            'exchanges': 0
        }

        # Run sorting algorithm
        quicksort_option2(integers_copy, 0, len(integers_copy)-1, counters)

        # Write out comparisons and exchanges made
        output_file.write(f'Comparisons: {counters["comparisons"]}\n')
        output_file.write(f'Exchanges: {counters["exchanges"]}\n\n')

        # If size is <= 50, print the sorted results
        if len(integers_copy) <= 50:
            output_file.write('--> Sorted Integers:\n')
            for item in integers_copy:
                output_file.write('    ' + str(item) + '\n')

    except RecursionError:
        output_file.write('Hit max recursion limit of 1000!\n\n')

    # Write head for output file
    output_file.write('\n3. Quicksort (Variation 3): Pivot = 1st Item, Insertion Sort used for partitions <= 50\n\n')

    # Run Quicksort (option 3) on input file, write output
    try:
        # Attempt to make list of integers
        integers_copy = list(integers)

        # Setup counters for comparisons and exchanges
        counters = {
            'comparisons': 0,
            'exchanges': 0
        }

        # Run sorting algorithm
        quicksort_option3(integers_copy, 0, len(integers_copy)-1, counters)

        # Write out comparisons and exchanges made
        output_file.write(f'Comparisons: {counters["comparisons"]}\n')
        output_file.write(f'Exchanges: {counters["exchanges"]}\n\n')

        # If size is <= 50, print the sorted results
        if len(integers_copy) <= 50:
            output_file.write('--> Sorted Integers:\n')
            for item in integers_copy:
                output_file.write('    ' + str(item) + '\n')

    except RecursionError:
        output_file.write('Hit max recursion limit of 1000!\n\n')

    # Write head for output file
    output_file.write('\n4. Quicksort (Variation 4): Pivot = Median-of-Three, Stopping Cases = Partions of size 1 and 2\n\n')

    # Run Quicksort (option 4) on input file, write output
    try:
        # Attempt to make list of integers
        integers_copy = list(integers)

        # Setup counters for comparisons and exchanges
        counters = {
            'comparisons': 0,
            'exchanges': 0
        }

        # Run sorting algorithm
        quicksort_option4(integers_copy, 0, len(integers_copy)-1, counters)

        # Write out comparisons and exchanges made
        output_file.write(f'Comparisons: {counters["comparisons"]}\n')
        output_file.write(f'Exchanges: {counters["exchanges"]}\n\n')

        # If size is <= 50, print the sorted results
        if len(integers_copy) <= 50:
            output_file.write('--> Sorted Integers:\n')
            for item in integers_copy:
                output_file.write('    ' + str(item) + '\n')

    except RecursionError:
        output_file.write('Hit max recursion limit of 1000!\n\n')

    # Write head for output file
    output_file.write('\n5. Natural Merge Sort:\n\n')

    # Run Natural Merge Sort on input file, write output
    try:
        # Attempt to make list of integers
        integers_copy = list(integers)

        # Setup counters for comparisons and exchanges
        counters = {
            'comparisons': 0,
            'exchanges': 0
        }

        # Run sorting algorithm
        naturalMerge(integers_copy, counters)

        # Write out comparisons and exchanges made
        output_file.write(f'Comparisons: {counters["comparisons"]}\n')
        output_file.write(f'Exchanges: {counters["exchanges"]}\n\n')

        # If size is <= 50, print the sorted results
        if len(integers_copy) <= 50:
            output_file.write('--> Sorted Integers:\n')
            for item in integers_copy:
                output_file.write('    ' + str(item) + '\n')
    
    except RecursionError:
        output_file.write('Hit max recursion limit of 1000!\n\n')


    # Write head for output file
    output_file.write('\n6. Merge Sort (Normal):\n\n')

    # Run Merge Sort on input file, write output (enhancment)
    try:
        # Attempt to make list of integers
        integers_copy = list(integers)

        # Setup counters for comparisons and exchanges
        counters = {
            'comparisons': 0,
            'exchanges': 0
        }

        # Run sorting algorithm
        mergeSort(integers_copy, 0, len(integers_copy)-1, counters)

        # Write out comparisons and exchanges made
        output_file.write(f'Comparisons: {counters["comparisons"]}\n')
        output_file.write(f'Exchanges: {counters["exchanges"]}\n\n')

        # If size is <= 50, print the sorted results
        if len(integers_copy) <= 50:
            output_file.write('--> Sorted Integers:\n')
            for item in integers_copy:
                output_file.write('    ' + str(item) + '\n')
    
    except RecursionError:
        output_file.write('Hit max recursion limit of 1000!\n\n')
    