## Case Study Analysis | Textwave - Retrieval Augmented Generation Systems

Sean Dickson

*Date: 11/08/25*

### Important Notes:

1. Due to limitations on my machine, I was experincing multiple kernel crashes in my Jupyter notebooks. Becuase of this, I switched to using the smallest cross-encoding model I could find: `cross-encoder/nli-distilroberta-base`
2. Due to long runtimes, I decided to filter down the number of questions I sent through Mistral API. When filtering the list of questions in `questions.tsv`, I made sure to keep an easy number of easy, medium, and hard questions, so as not to bias the data in a particular dircetion.

### 1. Chunking Strategy Performance (Text Preprocessing and Index Selection)

**Objective: Determine the optimal chunking and indexing strategy for efficient searching.**

For this task, I test various different text chunking strategies to see which one offers the best search results. For all below methods, a given result was "positive" if the search result was found in the coresponding "ArticleFile" for the provided question, otherwise it was negative.

For each provided question, I searched for 3 nearest neighbor search results, designating each as "positive" or "negative".

|Chunking Strategy  |Sentences per Chunk    |Positives     |Negatives    |% Positive   |
|-------------------|-----------------------|--------------|-------------|-------------|
|Sentence           |3                      |556           |2540         |0.1796       |
|Sentence           |5                      |119           |2977         |0.0384       |
|Sentence           |10                     |13            |3083         |0.0042       |

*Table 1: Quality of search results using sentence chunking methods*

|Chunking Strategy  |Chunk Size   |Positives     |Negatives    |% Positive   |
|-------------------|-------------|--------------|-------------|-------------|
|Fixed-Length       |150          |842           |2254         |0.2720       |
|Fixed-Length       |200          |667           |2429         |0.2154       |
|Fixed-Length       |500          |167           |2929         |0.0539       |

*Table 2: Quality of search results using fixed-length chunking methods*

|Chunking Strategy       |Chunk Overlap     |Positives     |Negatives    |% Positive   |
|------------------------|------------------|--------------|-------------|-------------|
|Fixed-Length (size=150) |100 characters    |802           |2294         |0.259        |

*Table 3: Quality of search results using fixed-length chunking (size=150) with 100 char overlap*

**BEST PERFORMING CHUNKING STRATEGY: Fixed-Length chunking, chunk_size=150**

The above, best performing chunking strategy was used in the following table, where we test search results over our 3 different indexing strategies.

|Indexing Strategy      |Positives     |Negatives    |% Positive   |
|-----------------------|--------------|-------------|-------------|
|Bruteforce             |842           |2254         |0.2720       |
|HNSW                   |802           |2294         |0.2590       |
|LSH                    |664           |2432         |0.2145       |

*Table 4: Quality of search results between indexing strategies*

**BEST PERFORMING INDEXING STRATEGY: Bruteforce indexing**

Together, the best method for chunking/indexing method for efficient search results appears to be fixed-length chunking (of size 150 characters), combined with bruteforce indexing.



### 2. Generative Model Performance Comparison (Baseline Selection)

**Objective: Determine the best Mistral Model for QA.**

For this task, we test 3 distinct mistral models against several provided questions without using RAG. By testing the quality of these repsonses using Exact Match and Transformer Match, we can determine which mistral model performs best under baseline conditions.

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Small              |Easy                  |0.8125            |0.8125                |
|Small              |Medium                |0.5               |0.625                 |
|Small              |Hard                  |0.55              |0.6                   |

*Table 5: Testing baseline "mistral-small-latest" model performance, stratified by question difficulty*

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Medium             |Easy                  |1.0               |1.0                   |
|Medium             |Medium                |0.625             |0.6875                |
|Medium             |Hard                  |0.55              |0.55                  |

*Table 6: Testing baseline "mistral-medium-latest" model performance, stratified by question difficulty*

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Large              |Easy                  |1.0               |1.0                   |
|Large              |Medium                |0.625             |0.6875                |
|Large              |Hard                  |0.55              |0.55                  |

*Table 7: Testing baseline "mistral-large-latest" model performance, stratified by question difficulty*

**BEST PERFORMING BASELINE MODEL: "mistral-medium-latest" / "mistral-large-latest"**

Both the "medium" and "large" mistral models performed similarly, and both performed better than the "small" model. Therefore, I will choose to move forward with the "mistral-medium-latest" model through ther remaining tasks.



### 3. Retrieval-Augmented Generative Model Performance Comparison (Architecture Selection)

**Objective: Determine how the mistral models perform using RAG, without re-ranking.**

For this task, I introduce RAG into the pipeline - providing mistral API with my own context to produce its answers. Here, we will not use re-ranking strategies. 

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Small              |Easy                  |0.75              |0.75                  |
|Small              |Medium                |0.625             |0.75                  |
|Small              |Hard                  |0.2               |0.25                  |

*Table 8: Testing RAG "mistral-small-latest" model performance, stratified by question difficulty*

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Medium             |Easy                  |0.75              |0.75                  |
|Medium             |Medium                |0.625             |0.75                  |
|Medium             |Hard                  |0.35              |0.4                   |

*Table 9: Testing RAG "mistral-medium-latest" model performance, stratified by question difficulty*

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Large              |Easy                  |0.75              |0.75                  |
|Large              |Medium                |0.625             |0.75                  |
|Large              |Hard                  |0.35              |0.4                   |

*Table 10: Testing RAG "mistral-large-latest" model performance, stratified by question difficulty*

**BEST PERFORMING RAG MODEL: "mistral-medium-latest" / "mistral-large-latest"**

While introducing RAG (with 3 context chunks) seemed to lower perfomance, both the "medium" and "large" mistral models still performed similarly, and both performed better than the "small" model. 



### 4. Reranker Performance Comparison (Architecture Selection)

**Objective: Identify how RAG performs when paired with re-ranking.**

For this task, I introduce RAG + a reranking strategy into the pipeline. Here, I choose to re-rank using the **"TF-IDF"** strategy.

**NOTE: Here, I ran into significant crashing issues when using Transformer Matching - even with the smallest cross-encoding model. This is likely due to machine limitations -- specifically my 8GB memory capacity. So, after 2 hours of troubleshooting, I decided to only consider exact matching going forward.**

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Small              |Easy                  |0.75              |N/a                   |
|Small              |Medium                |0.625             |N/a                   |
|Small              |Hard                  |0.1               |N/a                    |

*Table 11: Testing RAG "mistral-small-latest" + re-ranking model performance, stratified by question difficulty*

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Medium             |Easy                  |0.75              |N/a                   |
|Medium             |Medium                |0.625             |N/a                   |
|Medium             |Hard                  |0.3               |N/a                   |

*Table 12: Testing RAG "mistral-medium-latest" + re-ranking model performance, stratified by question difficulty*

|Mistral Model      |Difficulty Rating     |% Exact Matches   |% Transformer Matches |
|-------------------|----------------------|------------------|----------------------|
|Large              |Easy                  |0.75              |N/a                   |
|Large              |Medium                |0.625             |N/a                   |
|Large              |Hard                  |0.25              |N/a                   |

*Table 13: Testing RAG "mistral-large-latest" + re-ranking model performance, stratified by question difficulty*

Re-ranking via "TF-IDF" did not seem to have a significant effect on the performance of the model -- if anything, reducing its accuracy. That said, the best performing model of the bunch was still the "medium" mistral model.



### 5. Optimize the Number of Retrieved Chunks (Parameter Configuration)

**Objective: Identify the optimal number of context chunks to inlcude in the RAG pipeline.**

Here, we will attempt to measure the performance of the RAG model using different numbers of provided context chunks (M-values). For each tested M-value, the performance metrics are summarized below:

|M        |Mistral Model      |% Exact Matches   |% Transformer Matches |
|---------|-------------------|------------------|----------------------|
|1        |Medium             |0.4915            |N/a                   |
|3        |Medium             |0.4915            |N/a                   |
|5        |Medium             |0.4915            |N/a                   |
|10       |Medium             |0.4915            |N/a                   |
|100      |Medium             |0.4915            |N/a                   |

Increasing the M-value did not effect the performance of the model in any way.
