# Sean Dickson's Software Development Portfolio

Welcome! 👋

Thanks for visiting my portfolio repository!

Here you’ll find a collection of personal projects that highlight my approach to problem-solving, software design, and technical creativity. Each project reflects how I build real-world, practical solutions.

## 1. HPLC Uploader Tool | Nov 2025 - Feb 2026

A Python-based automation tool for uploading and validating HPLC experimental data into internal data infrastructure. The tool parses instrument output files, performs validation and metadata checks, and programmatically registers experimental results through secure APIs, reducing manual data entry and improving traceability of analytical experiments.

**How It Works:**
  - Parses raw HPLC output files and extracts relevant data.
  - Validates experiment structure, sample identifiers, and required metadata fields.
  - Formats processed data into standardized payloads.
  - Uploads experiment records and results through authenticated REST API endpoints.
  - Logs upload status and validation errors to ensure reproducibility.

**Core Skills:** 

Python, Data Parsing, REST APIs, Data Validation, Automation, Scientific Data Pipelines, Error Handling

## 2. CRISPR Guide Designer | Oct 2025 - Nov 2025

A Python-based automation tool for designing CRISPR guide RNA constructs and corresponding plasmids for genomic engineering workflows. The system identifies optimal guide sequences for a target gene, assembles plasmid designs based on standardized cloning architectures, and programmatically registers the resulting constructs through APIs.

**How It Works:**
  - Accepts gene or genomic region input and scans for candidate CRISPR guide RNA sequences.
  - Scores guides based on design constraints (e.g., PAM compatibility, sequence quality, and cloning requirements).
  - Selects optimal guides and generates corresponding plasmid construct designs.
  - Automatically assembles plasmid maps using standardized vector architectures.
  - Registers designed guides and plasmids in the lab database through REST API calls.

**Core Skills:** 

Python, Bioinformatics, Algorithmic Sequence Design, CRISPR Guide Optimization, REST APIs, Automation, Laboratory Data Systems, Scientific Software Development

## 3. Huffman Encoder | Mar 2025

**Project Description:**

HuffmanEncoder is a Python-based implementation of the classic Huffman coding algorithm, used in data compression. It efficiently converts text or files into compact binary representations by assigning shorter codes to more frequent characters.

**How It Works:**
  - Encodes and decodes arbitrary strings or files into binary form.
  - Demonstrates tree-based data structures, priority queues, and bitwise manipulation.
  - Designed with modular Python classes for reusability and clarity.

**Core Skills:** 

Python, Algorithm Design, OOP, Recursion, Data Structures

## 4. Multi-Sorter | Apr 2025

**Project Description:**

Multi-Sorter is a command-line utility that allows users to experiment with multiple sorting algorithms side-by-side. It was designed as a playground for understanding algorithmic complexity and runtime trade-offs in real-world data handling.

**How It Works:**
  - Supports both built-in and custom sorting methods (e.g., insertion sort, merge sort).
  - Outputs detailed runtime analysis for comparison between algorithms.

**Core Skills:** 

Python, CLI Applications, Complexity Analysis, Algorithm Optimization

## 5. Beer Die Stat Recorder | Aug 2020

>“Because friendly competition deserves better than a whiteboard.”

**Project Description:**

Beer Die is a competitive game my friends and I used to play often. Tracking our wins, losses, and stats on a whiteboard just wasn’t cutting it — so I built a cloud-powered stats app that automates everything.

**How It Works:**

Uses Twilio SMS webhooks to trigger game data uploads from text messages.
  - AWS Lambda functions handle message parsing and data processing.
  - AWS DynamoDB provides persistent, cloud-hosted storage for user stats.
  - Players can view, edit, and compare their records through text commands.

**Note:**

This is an earlier project, included here to illustrate the progression of my software development skills over time. The system has been archived due to AWS/Twilio costs, but the full source code and workflow are preserved here for demonstration.

**Core Skills:**
  - Python, AWS Lambda, DynamoDB, Twilio API
  - Webhooks & Cloud Functions
  - API Design, Data Persistence, Error Handling
  - Deployment Automation
  - Virtual Environments (environment.yml)