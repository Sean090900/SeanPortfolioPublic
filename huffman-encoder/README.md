# Huffman Encoder
**Created By:** Sean Dickson

**IDE Used:** Visual Studio Code

**Python Version:** 3.13.0

## Running
Steps for running this package:
1. Download and install Python on your computer
2. Navigate to [this](.) directory (containing the README.md)
4. Run the program as a module: `python -m huffmanEncoder <encode/decode> <input_path> <output_path> <frequency_table_path>`

### Usage:
For encoding clear text...
```bash
python -m huffmanEncoder encode resources/ClearText.txt resources/ClearText-OUT.txt resources/FreqTable.txt
```

For decoding encoded text...
```bash
python -m huffmanEncoder decode resources/Encoded.txt resources/Encoded-OUT.txt resources/FreqTable.txt
```

**Positional arguments:**
|Argument         |Description              |
|-----------------|-------------------------|
|input_path       |Input File Pathname      |
|output_path      |Output File Pathname     |
|frequency_table  |Frequency Table Pathname |