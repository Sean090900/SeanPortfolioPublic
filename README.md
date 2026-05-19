# Sean Dickson — Software Development Portfolio

> Building practical, well-engineered solutions at the intersection of software and science.

---

## About

I'm a software engineer with a focus on AI/ML, data pipelines, and scientific tooling. This repository showcases a selection of personal and professional projects that demonstrate how I approach real-world problems — from bioinformatics workflows to classical algorithms.

---

## Projects

### [Assay Data Uploader](./assay-data-uploader) `Nov 2025 – Feb 2026`

**Automating analytical data registration for laboratory workflows**

A Python automation tool that ingests raw instrument output, validates experimental metadata, and registers results into internal data infrastructure (Benchling) via authenticated REST APIs. Designed to reduce manual data entry and improve traceability across analytical experiments.

| Area | Details |
|---|---|
| Input | Raw instrument output files |
| Validation | Experiment structure, sample IDs, required metadata fields |
| Output | Standardized payloads registered through REST API endpoints |
| Observability | Per-upload logging with structured error reporting |

**Skills:** Python · ETL Pipelines · REST APIs · Data Validation · Scientific Data Pipelines · Error Handling

---

### [CRISPR Guide Designer](./crispr-guide-designer) `Oct 2025 – Nov 2025`

**Computational tool for CRISPR guide RNA design and plasmid assembly**

A Python-based system that automates the design of CRISPR guide RNA constructs. Given a target gene or genomic region, the tool identifies candidate guide sequences, scores them against design criteria, assembles plasmid construct designs, and registers results in the lab database (Benchling).

| Stage | Description |
|---|---|
| Input | Gene name or genomic region |
| Guide Selection | PAM compatibility, sequence quality, cloning compatibility scoring |
| Construct Assembly | Automated plasmid map generation using standardized vector architectures |
| Registration | REST API calls to register guides and plasmids in the lab database |

**Skills:** Python · Bioinformatics · CRISPR Guide Optimization · Automation

---

### [SecureBank](./securebank) `Nov 2025`

**ML-driven fraud detection system with class imbalance handling**

An end-to-end fraud detection pipeline built and deployed as a REST API. Applied SMOTE for synthetic minority oversampling and hard-negative mining to improve model recall on highly imbalanced transaction data. Deployed with health checks and structured logging.

**Skills:** Python · Machine Learning · SMOTE · Hard-Negative Mining · REST APIs · Model Deployment

---

### [Huffman Encoder](./huffman-encoder) `Mar 2025`

**Lossless data compression via Huffman coding**

A modular Python implementation of the Huffman coding algorithm. Encodes and decodes arbitrary text or files into compact binary representations using frequency-based variable-length codes. Built around clean OOP design with clear separation between tree construction, encoding, and decoding.

- Builds a min-heap priority queue from character frequency analysis
- Recursively constructs a Huffman tree and derives prefix-free binary codes
- Encodes input to binary and decodes back to the original string without loss

**Skills:** Python · Algorithm Design · OOP · Recursion · Data Structures · Bitwise Manipulation

---

### [Multi-Sorter](./multi-sorter) `Apr 2025`

**CLI playground for comparing sorting algorithm performance**

A command-line utility for running and benchmarking multiple sorting algorithms side-by-side on the same dataset. Built as a learning and analysis tool for understanding algorithmic complexity trade-offs in practice.

- Supports insertion sort, merge sort, and additional configurable methods
- Outputs per-algorithm runtime and comparison metrics
- Designed to be extensible for adding new sorting strategies

**Skills:** Python · CLI Applications · Complexity Analysis · Algorithm Optimization

---

## Skills at a Glance

| Domain | Technologies |
|---|---|
| Languages | Python |
| Automation & Pipelines | REST APIs, Data Parsing, Scientific Data Pipelines |
| Machine Learning | SMOTE, Hard-Negative Mining, Fraud Detection |
| Bioinformatics | CRISPR Design, Sequence Analysis, Plasmid Assembly |
| Algorithms & DS | Sorting, Huffman Coding, Trees, Priority Queues |
| Engineering Practices | OOP, Error Handling, Logging, Modular Design |

---

*Last updated: May 2026*
