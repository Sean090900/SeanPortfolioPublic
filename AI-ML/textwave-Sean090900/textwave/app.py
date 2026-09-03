from flask import Flask, request, jsonify
import os

from .modules.extraction.preprocessing import DocumentProcessing
from .modules.extraction.embedding import Embedding
from .modules.retrieval.reranker import Reranker
from .modules.generator.question_answering import QAGeneratorMistral

from .modules.retrieval.index.bruteforce import FaissBruteForce
from .modules.retrieval.index.hnsw import FaissHNSW
from .modules.retrieval.index.lsh import FaissLSH
from .modules.retrieval.search import FaissSearch

app = Flask(__name__)

STORAGE_DIRECTORY = "textwave/storage/"
CHUNKING_STRATEGY = 'fixed-length' # or 'sentence'
CHUNKING_PARAMETERS = {
    "chunk_size": 100, 
    "overlap_size": 0
}
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
INDEX_STRATEGY = "bruteforce"
INDEX_PARAMETERS = {
    'metric': 'cosine',
}
RERANKING_STRATEGY = 'tfidf' 
RERANKING_PARAMETERS = {}
API_KEY = os.environ["MISTRAL_API_KEY"]

def initialize_index():
    """
    1. Parse through all the documents contained in storage/corpus directory
    2. Chunk the documents using either a'sentence' and 'fixed-length' chunking strategies (indicated by the CHUNKING_STRATEGY value):
        NOTE: The CHUNKING_STRATEGY will configure either fixed chunk or sentence chunking
    3. Embed each chunk using Embedding class, using 'all-MiniLM-L6-v2' text embedding model as default.
    4. Store vector embeddings of these chunks in a FAISS index, along with the chunks as metadata. 
        NOTE: You will decide the best strategy. Use `bruteforce` as default.
    5. This function should return the FAISS index
    """
    # Initialize objects
    processing = DocumentProcessing()
    embedding_model = Embedding()

    # Preprocess and gather embeddings for corpus docs
    metadata = []
    embeddings = []
    doc_count = 0
    for doc in os.listdir(STORAGE_DIRECTORY):
        print(doc)

        # Process document into chunks
        chunk_size, overlap = CHUNKING_PARAMETERS['chunk_size'], CHUNKING_PARAMETERS['overlap_size']
        if CHUNKING_STRATEGY == 'fixed-length':
            chunks = processing.fixed_length_chunking(f"{STORAGE_DIRECTORY}/{doc}", chunk_size=chunk_size, overlap_size=overlap)
        elif CHUNKING_STRATEGY == 'sentence':
            chunks = processing.fixed_length_chunking(f"{STORAGE_DIRECTORY}/{doc}", chunk_size=chunk_size, overlap_size=overlap)
        else:
            raise ValueError('CHUNKING_STRATEGY must be one of: "fixed-length" or "sentence"')
        
        # Collect embeddings for each chunk
        for chunk in chunks:
            metadata.append(chunk)
            embeddings.append(embedding_model.encode(chunk))

        # Increment doc count, break loop after 3 docs
        doc_count += 1
        if doc_count == 3:
            break

    # Store embeddings in a FAISS index
    if INDEX_STRATEGY == 'bruteforce':
        index = FaissBruteForce(len(embeddings[0]), INDEX_PARAMETERS['metric'])
    elif INDEX_STRATEGY == 'hnsw':
        index = FaissHNSW(len(embeddings[0]), INDEX_PARAMETERS['metric'])
    elif INDEX_STRATEGY == 'lsh':
        index = FaissLSH(len(embeddings[0]))
    else:
        ValueError('INDEX_STRATEGY must be one of: "bruteforce", "hnsw", or "lsh"')

    # Add embeddings and metadata to index, return 
    index.add_embeddings(embeddings, metadata)
    return index
    

@app.route("/generate", methods=["POST"])
def generate_answer():
    """
    Generate an answer to a given query by running the retrieval and reranking pipeline.

    This endpoint accepts a POST request with a JSON body containing the "query" field.
    It preprocesses and indexes the corpus if necessary, retrieves top-k relevant documents,
    and uses a language model to generate a final answer.

    Example curl command:
    curl -X POST http://localhost:5000/generate \
         -H "Content-Type: application/json" \
         -d '{"query": "What is the role of antioxidants in green tea?"}'

    :return: JSON response containing the generated answer.
    """
    try:
        # Attempt to get json from request
        query = request.get_json()['query']
    except Exception as e:
        return jsonify({
            "error": "No payload in request.",
            "details": str(e)
        }), 400
    
    if str(query).strip() == '':
        return jsonify({
            "error": "Query is empty.",
        }), 400

    # Embed query vector
    query_vector = Embedding().encode(query)

    # Generate index
    index = initialize_index()

    # Via search(), get list of nearby chunks/sentences -- convert back to text to provide to re-ranker?
    search_euclidean = FaissSearch(index, metric=INDEX_PARAMETERS['metric'])
    _, _, meta_results = search_euclidean.search(query_vector, k=5)

    # Re-rank the context chunks/sentences by providing query, and corpus of docs (text)
    reranker = Reranker(type=RERANKING_STRATEGY)
    docs, indices, scores = reranker.rerank(query, meta_results)

    print(f'Query: {query}')
    print(f'Context: {docs}')

    # Trigger QA object to ping MISTRAL, get reponse, return
    answer = QAGeneratorMistral(API_KEY).generate_answer(query=query, context=docs)
    return jsonify({"query": query, "answer": answer})


if __name__ == "__main__":
    app.run(debug=True)







