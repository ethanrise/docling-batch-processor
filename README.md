# docling-batch-processor
A powerful document conversion tool that can batch convert various document formats (PDF, Word, Excel, PPT, etc.) to Markdown format, with intelligent processing of images and tables.

## Features

- ✅ **Batch Processing** - Support for converting multiple document files simultaneously
- 🔄 **Concurrent Processing** - Multi-threaded concurrent conversion for improved efficiency
- 📁 **Auto Discovery** - Automatically scan all supported files in a directory
- 🖼️ **Image Processing** - Automatically extract Base64 images and save as separate files
- 📊 **Table Optimization** - Optimize table formatting for proper display
- 📊 **Conversion Report** - Generate detailed conversion statistics report
- 🛡️ **Error Handling** - Comprehensive error handling and exception recovery
- ⚙️ **Flexible Configuration** - Support custom concurrency, output directory, and service address

## Supported File Formats

| Format | Extensions |
|--------|------------|
| PDF | `.pdf` |
| Word | `.docx`, `.doc` |
| Excel | `.xlsx`, `.xls` |
| PowerPoint | `.pptx` |
| Text | `.txt` |
| Web | `.html`, `.xml` |

## System Requirements

- Python 3.9+
- Docling-serve service (running locally or on remote server)

## Installation

### 1. Clone the Project

```bash
git clone https://github.com/ethanrise/docling-batch-processor.git
cd docling-batch-converter
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Docling-serve Service

Make sure the Docling-serve service is running (default port 9969):

```bash
# Start Docling-serve service (command depends on your deployment method)
docker run -p 9969:9969 ghcr.io/dlredding/docling-serve:latest
```

Or using Docker Compose:

```yaml
version: '3.8'
services:
  docling-serve:
    image: ghcr.io/dlredding/docling-serve:latest
    ports:
      - "9969:9969"
    volumes:
      - ./uploads:/app/uploads
```

## Usage

### Basic Usage

```bash
# Convert multiple files
python main.py file1.pdf file2.docx file3.txt

# Convert all supported files in a directory
python main.py -d /path/to/documents

# Convert files to specified directory
python main.py file1.pdf file2.docx -o ./output
```

### Advanced Options

```bash
# Specify concurrency and Docling service address
python main.py -d ./docs --workers 5 --url http://localhost:9969/v1/convert/file

# View help information
python main.py -h
```

### Parameter Description

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `input_files` | List of input file paths | - |
| `-d, --directory` | Directory path to convert | - |
| `-o, --output` | Output directory | First input file's directory |
| `--workers` | Concurrency count | 3 |
| `--url` | Docling service URL | http://localhost:9969/v1/convert/file |

## Output Structure

After conversion, the following content will be generated in the output directory:

```
output/
├── file1.md           # Converted Markdown file
├── file1_images/      # Extracted image files
│   ├── image_20240101_001.png
│   └── image_20240101_002.jpg
├── file2.md
├── file2_images/
└── conversion_report.txt  # Conversion report
```

## Conversion Report

The generated `conversion_report.txt` includes:

- Total file count, success/failure statistics
- Processing time for each file
- Image count statistics
- Failure reason analysis

## Project Structure

```
docling_batch_converter/
├── main.py                 # Main program entry point
├── core/
│   ├── file_validator.py   # File validator
│   ├── docling_client.py   # Docling client
│   ├── image_processor.py  # Image processor
│   ├── table_processor.py  # Table processor
│   ├── output_manager.py   # Output manager
│   └── batch_converter.py  # Batch converter
└──  main class
```

## Module Description

- **validators**: Responsible for validating input file validity
- **clients**: HTTP communication with Docling service
- **processors**: Process document content (images, tables, etc.)
- **managers**: Manage file output and report generation
- **core**: Core controller that coordinates components

## Common Issues

### 1. Connection Error
If prompted that connection to Docling service fails, please check:
- Whether the service is running
- If the URL address is correct
- If the port is occupied

### 2. File Format Error
Ensure input files are not corrupted documents and that extensions match actual content.

### 3. Memory Insufficient
For large numbers of files or large files, reduce concurrency:
```bash
python main.py -d ./docs --workers 1
```


## Contributing

Welcome to submit Issues and Pull Requests to improve this tool.

---

**Note**: This tool depends on the Docling-serve service. Please ensure the service is running before executing conversion operations.
