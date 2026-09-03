import re
import numpy as np
from collections import Counter
from typing import List
from .text_processing import process_text
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords", quiet=True)

# TODO: You will need to implement: 
#  - BagOfWords._tokenize()
#  - BagOfWords.fit()
#  - BagOfWords.transform()

# NOTE: Efficiency is not the primary goal here; nevertheless, 
#       using :class:`collections.Counter` is recommended. See 
#       the following resources for more information: 
#       - https://docs.python.org/3/library/collections.html
#       - https://www.geeksforgeeks.org/python/counters-in-python-set-1/

class BagOfWords:
    """
    A Bag-of-Words represnation transformer that learns a vocabulary from a corpus and transforms
    documents into their Bag-of-Words (BoW) representation.

    The BoW model represents text data as a collection of word counts, ignoring the
    order and structure of words. This transformer builds a vocabulary from the provided
    training corpus and then counts occurrences of these vocabulary words in new documents.
    """

    def __init__(self):
        """
        Initializes the Bag_of_Words transformer with an empty vocabulary.

        Attributes:
            vocabulary_ (dict): A dictionary mapping each unique word found in the corpus
                                to a unique index. This is constructed during the fit process.
        """
        self.vocabulary_ = {}

    def _tokenize(self, text: str):
        """
        Tokenizes the input text by converting it to lowercase and extracting words using a regular expression.

        This basic tokenization approach splits the text on word boundaries, capturing only alphanumeric
        sequences. Adjust the regular expression if you require a different tokenization strategy.

        Parameters:
            text (str): The input text to be tokenized.

        Returns:
            list: A list of word tokens extracted from the text.
        """
        # Return list of processed tokens
        preocessed_tokens = [token for token in process_text(text, use_lemmatization=True).split(' ') if token != 's']

        # Remove stop words
        stop_words = set(stopwords.words("english"))
        tokens = []
        for token in preocessed_tokens:
            if token not in stop_words:
                tokens.append(token)
        
        # Return tokenized text
        return tokens

    def fit(self, documents: List[str]):
        """
        Learns the vocabulary from the corpus by processing each document and extracting unique tokens.

        During this process, each document in the training corpus is tokenized, and the set of unique
        words is aggregated across all documents. The vocabulary is then created by sorting these unique words
        and assigning each a unique index.

        Parameters:
            documents (list of str): The training corpus where each document is a string.

        Returns:
            Bag_of_Words: The fitted transformer instance with an updated vocabulary_ attribute.
        """
        # Find all unique tokens from within corpus
        unique_tokens = set()
        for text in documents:
            # Tokenize
            tokens = self._tokenize(text)
            for token in tokens:
                unique_tokens.add(token)

        # Sort unique tokens
        unique_tokens = sorted(unique_tokens)

        # Assign each token a unique index starting at 0
        vocabulary = {}
        index = 0
        for token in unique_tokens:
            vocabulary[token] = index
            index += 1

        # Save fitted vocab, return self
        self.vocabulary_ = vocabulary
        return self 

    def transform(self, document: str):
        """
        Transforms a single document into its Bag-of-Words representation.

        This method tokenizes the input document and counts the occurrences of each token that exists
        in the learned vocabulary. The output is a numpy array indexed by ordered tokens (words) and values
        are their corresponding counts in the document.

        Parameters:
            document (str): A single document to be transformed into a BoW vector.

        Returns:
            numpy: A numpy array indexing each term (from the learned vocabulary) with its count in the document.
                  Only tokens present in the vocabulary are included.
        """
        # If fitting has not occured yet, throw AttributeError
        if not self.vocabulary_:
            raise AttributeError('You must fit the BoW object before transforming.')

        # If text is empty, return empty vector
        if not document:
            return np.array([0.])

        # Tokenize the document
        tokens = self._tokenize(document)

        # If no known tokens exist in the document, return empty vector
        if not [token for token in tokens if token in self.vocabulary_]:
            return np.array([0., 0.])

        # Index each term with its count
        transformed_document = np.array([0. for _ in range(len(self.vocabulary_))])
        for token in set(tokens):
            if token in self.vocabulary_:
                occurrences = Counter(tokens)[token]
                index = self.vocabulary_[token]
                transformed_document[index] = occurrences

        # Normailize vector between 0 and 1
        norm = np.linalg.norm(transformed_document)
        if norm > 0:
            transformed_document = transformed_document / norm

        # Return transformed document
        return transformed_document


if __name__ == "__main__":
    # Example corpus of 9 documents to train the Bag-of-Words representation.
    corpus = [
        "The quick brown fox jumps over the lazy dog.",
        "Never jump over the lazy dog quickly.",
        "A quick movement of the enemy will jeopardize six gunboats.",
        "All that glitters is not gold.",
        "To be or not to be, that is the question.",
        "I think, therefore I am.",
        "The only thing we have to fear is fear itself.",
        "Ask not what your country can do for you; ask what you can do for your country.",
        "That's one small step for man, one giant leap for mankind.",
    ]

    # Fit the transform on the corpus.
    transform = BagOfWords()
    transform.fit(corpus)

    print(transform.vocabulary_)
    
    # Test document to transform after fitting the corpus.
    test_document = "The quick dog jumps high over the lazy fox."
    bow_test = transform.transform(test_document)
    
    print(bow_test)
