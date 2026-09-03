## Case Study Analysis | Ironclad - Visual Search

Sean Dickson

*Date: 10/25/25*

### 1. Model Performance Comparison (Model Selection):

**Objective:** Compare the overall performance of casia-webface and vggface on the full IronClad dataset. For this selection process, include the impact of environmental noise (e.g., Gaussian blur, resizing, and brightness adjustments) on the casia-webface and vggface performance. Argue for which model should be selected.

|Model         |Mean AVG Precision @ k  |
|--------------|------------------------|
|vggface2      |0.99765                 |
|casia-webface |0.11483                 |

*Table 1: Mean AVG Precision @ K for vggface vs casia-webface models (no augmentations besides resizing to 160x160)*

Here, I calculated the mean average precision @ K across the top 5 nearest neighbors identified by both models, for the full ironclad dataset. All images were preprocessed to size 160x160, and no augmentations were applied here.

By far, the better model for visual search, given these image settings, was the vggface2 model.

By adding augmentations to the images as they were preprocessed, the following results were observed:

|Model         |Augmentation      |Mean AVG Precision @ k  |
|--------------|------------------|------------------------|
|vggface2      |Guassian Blur     |0.50179                 |
|vggface2      |Resizing: 224     |0.50019                 |
|casia-webface |Guassian Blur     |0.08580                 |
|casia-webface |Resizing: 224     |0.04480                 |

*Table 2: Mean AVG Precision @ K for vggface vs casia-webface models (augementations applied...)*

Applying the augmenations (both increasing image size and adding blur) seriously deteriorated the mean average precision @ K values for each model. That said, vggface2 still performed better in both cases compared to the casia-webface model.

Because vggface2 performs better with both the normal and augmented images, I will select this model to use for the remainder of this analysis, when only 1 model is required.

### 2. Threshold Design (Indexing Selection):

**Objective:** Measure the impact of selecting Brute Force, HNSW, LSH indexing strategy on the systems' retrieval performance. Compare their performance on a billion images (as per the requirements).

|Indexing Strategy    |Mean AVG Precision @ k    |
|---------------------|--------------------------|
|Bruteforce           |0.99765                   |
|HNSW                 |0.55219                   |
|LSH                  |0.54678                   |

*Table 3: Mean AVG Precision @ K for differing indexing strategies (all vggface2 model)*

Above, the mean AVG Precision @ K for each indexing strategy was recorded, using the vggface2 model and eucludian calculations.

By far, the best performing indexing strategy was **bruteforce**.

### 3. Number of Identies Returned (Parameter Configuration): 

**Objective:** Define N as the final number of candidate identities the system returns to the user (i.e., Top-N nearest neighbors). Argue and justify for the best N for casia-webface and vggface given the provided dataset (probe and gallery). Finally, show how N will change between Brute Force vs HNSW vs LSH.

|Model          |N-Nearest Neighbors  |Mean AVG Precision @ k   |
|---------------|---------------------|-------------------------|
|vggface2       |**1**                |**1.00000**              |
|vggface2       |3                    |1.00000                  |
|vggface2       |5                    |0.99765                  |
|vggface2       |7                    |0.99135                  |

*Table 3: Varying n-nearest neighbors and affect on mean average precision @ K for vggface model*

|Model          |N-Nearest Neighbors  |Mean AVG Precision @ k   |
|---------------|---------------------|-------------------------|
|casia-webface  |1                    |0.09209                  |
|casia-webface  |3                    |0.10978                  |
|casia-webface  |5                    |0.11483                  |
|casia-webface  |7                    |0.11710                  |
|casia-webface  |9                    |0.11809                  |
|casia-webface  |11                   |0.12004                  |
|casia-webface  |**13**               |**0.12011**              |
|casia-webface  |15                   |0.11949                  |

*Table 4: Varying n-nearest neighbors and affect on mean average precision @ K for casia-webface model*

For all tests in the above tables, FAISS bruteforce method was used for indexing and eucludian scoring was used as the distance calculation. 

The vggface2 method turned out to make perfect predictions for each probe image in the dataset. Thus, specifying a k-nearest neighbors value of N=1 led to a perfect mean average precision at K score of 1.0.

The casia-webface model was less optimal at predictions, are required finding an optimum k-nearest neighbors value. Based on the above table, that optimum seems to be near a value of N=13.

Below, we test our vggface2 model using our best N-nearest neighbor value, comparing results for each indexing strategy...

|Indexing Strategy   |Model         |N-Nearest Neighbors  |Mean AVG Precision @ k   |
|--------------------|--------------|---------------------|-------------------------|
|Bruteforce          |vggface2      |1                    |1.00000                  |
|HNSW                |vggface2      |1                    |0.50450                  |
|LSH                 |vggface2      |1                    |0.49226                  |

*Table 5: Comparing best N-nn value against other indexing strategies.*

It seems that what works as the best N-nearest neighbors value for one indexing strategy, does not transfer over wll to other indexing strategies. When N=1 was applyed to each other indexing strategy, both took significant hits to their mAP@K values, compared to baseline.

### 4. Optimize the Number of Images in Gallery (Dataset Design):

**Objective:** Define m_i as the number of images the gallery contains for individual i. Investigate how retrieval performance on casia-webface and vggface as m_i vary (i.e., m = 1, 2, 3, ...). Suggest the optimal m, supported by your findings, and discuss dataset-specific factors that may influence your conclusion.

**Proposal:** We can start by sorting each individual in the gallery into buckets based on the number of images (i_m) present in their respective directories. From there, we can calculate the mean average precision @ K values for each "bucket" of images, and compare. 

NOTE: There is significant class imbalance between buckets (see belwo chart). (e.g. there are far more individuals with only 1 image present in tha gallery that those with 5, etc.). This may cause an issue -- the more images present to search through, the more difficult it will be to identify correct neighbors. We are not interested in testing the accuracy of each model against TOTAL number of images. We are interested in testing accuracy against the number of images PER individual.

[Gallery Class Imbalance](ironclad/storage/charts/gallery_class_imbalance.png)

*Chart 1: Class imbalances between individuals with different numbers of associated images in the original dataset.*

To resolve this issue, the dataset will be sampled such that each "bucket" of individuals will contain almost exactly the same number of images (between 36-40 each). This will normalize the cost of search across all buckets, and allow us to zero-in on differences between the numbers of images PER individual.

The results of this sampling can be found here: 

[Sampled Gallery Class Balance](ironclad/storage/charts/sampled_gallery_balance.png)

*Chart 2: Resolution of imbalances between buckets in original dataset.*

Further, each bucket will only be probed with images from the individuals that reside within that bucket. Otherwise, scores will be artificially low due to an absorbanant number of 0.0-scores from probes not present in the index.

Below are the results of testing each model, using bruteforce indexing with N=1 nearest neighbors search...

**Vggface2:**

[Vggface2 mAP@K Per Bucket](ironclad/storage/charts/vggface2_mAP@K_per_bucket.png)

*Chart 3: Comparing mAP@k values for each image-number "bucket" for vggface2 model.*

Given the plot, it looks like the optimum number of images tends towards 8-9. That said, the data here is so sporadic that I am not convinced that this is a true optimum. THe model vggface2 seems to perform rather well regardless of the number of images tested here.

**Casia-webface:**

[Casia-Webface mAP@K Per Bucket](ironclad/storage/charts/casia-webface_mAP@K_per_bucket.png)

*Chart 3: Comparing mAP@k values for each image-number "bucket" for casia-webface model.*

Given this data, the casia-webface model seems to perform better and better the more images you provide it.

### 5. Uncertainty Estimation (Robustness Design):

**Objective:** Identify those individuals in the dataset on which the system performs poorly and those who perform well. Characterize their behavior in the image space and the embedding space. Without manipulating the images in the gallery (i.e., do not use Task 4), propose, implement, and evaluate a strategy to improve the performance of your best model in Task 1.

**Proposal:** Our best performing model/indexing strategy pairing historically has been vggface2, with bruteforce indexing and N=1 nearest neighbor search -- yeilding a mAP@K value of 1.000 across the entire dataset (perfect score). Thus, for this analysis section, we will attempt to improve the score of a lesser performing model: casia-webface, with bruteforce indexing and N=16 nearest neighbor search.

First, I needed to perform the visual search, and find which specific images perofrmed worst during search. After doing this, I investigated each images, and determined various attributes including but not limited to "distance fron first nearest neighbor", "average distance", "contrast", "brightness", and "probe mode", in order to get a broad-scope view of each image.

I then developed a linear regression model (via sklearn's RidgeCV), and identified which image attributes were most highly coorilated with a low mean average precision at K score. The top feature that came up was: "distance fron first nearest neighbor", which was highly negatively coorilated with mAP@K score.

So, this became a question of reducing the distances between probe and its nearest neighbors. On doing some research into the subject, I found that averaging out multiple, slightly-augmented versions of the same probe image into a query vector can help to "normalize" the embeddings in such a way that reduced distance to its neighbors, making the search process slight more effective. 

So, I proposed that by normalizing the probes in this way, we might be able to slightly increase the performance of the search.

**Implementation:** 

I developed a function to alter the query vectors in this way, and processed the resulting augmented query like normal...

```python
def tta_embedding(model, preprocessor, img):
    aug_imgs_tensors = [preprocessor.process(img), preprocessor.process(img.transpose(Image.FLIP_LEFT_RIGHT))]
    embs = [model.encode(aug) for aug in aug_imgs_tensors]
    emb = np.mean(embs, axis=0)
    return emb / np.linalg.norm(emb)
```

See task5.ipynb for remaining code:

[Implementation for Task 5](ironclad/analysis/task5.ipynb)

**Evaluation:** 

The results are summarized below...

|Model          |Query Vector Type               |mAP@K Score    |
|---------------|---------------------------------|---------------|
|casia-webface  |Normal                           |0.12011        |
|casia-webface  |Average of Augmented versions    |**0.12074**    |

*Table 6: Comparing distance metrics and mAP@K scores for casia-webhook model.*

Through this augemntation. of query vectors, I was able to improve the average performance of the visual search model by 0.006 points!