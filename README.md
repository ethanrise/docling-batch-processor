# 📄 docling-batch-processor

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)]()
<!-- [![PyPI](https://img.shields.io/pypi/v/docling-batch-processor)](https://pypi.org/project/docling-batch-processor/) -->
<!-- [![Docker Image](https://img.shields.io/badge/docker-docling--serve-4A90E2)](https://github.com/dlredding/docling-serve) -->

> A powerful batch document conversion tool that transforms PDF, Word, Excel, PPT, and more into clean, structured Markdown — with intelligent image and table handling.

---

## ✨ Features

- ✅ **Batch Processing** – Convert multiple documents in one command  
- 🔄 **Concurrent Execution** – Multi-threaded for faster throughput  
- 🔍 **Auto Discovery** – Recursively scan directories for supported files  
- 🖼️ **Smart Image Handling** – Extract images as files + embed Base64 fallback  
- 📊 **Table Optimization** – Preserve layout with Markdown-compatible formatting  
- 📈 **Conversion Report** – Detailed stats: success/failure, timing, image counts  
- 🛡️ **Robust Error Recovery** – Gracefully handle corrupt or unsupported files  
- ⚙️ **Fully Configurable** – Customize workers, output path, and Docling service URL  

---

## 📁 Supported File Formats

| Format        | Extensions                     |
|---------------|--------------------------------|
| PDF           | `.pdf`                         |
| Microsoft Word| `.docx`, `.doc`                |
| Excel         | `.xlsx`, `.xls`                |
| PowerPoint    | `.pptx`                        |
| Plain Text    | `.txt`                         |
| Web Documents | `.html`, `.xml`                |

---

## ⚙️ System Requirements

- Python 3.9+
- Running [Docling-serve](https://github.com/dlredding/docling-serve) instance (local or remote)

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ethanrise/docling-batch-processor.git
cd docling-batch-processor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Docling-serve Service

#### Using Docker (Recommended)
```bash
docker run -p 9969:5001 quay.io/docling-project/docling-serve:latest
```

#### Using Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  docling-serve:
    image: quay.io/docling-project/docling-serve:latest
    ports:
      - "9969:5001"
    volumes:
      - ./uploads:/app/uploads
```
Then run:
```bash
docker-compose up -d
```

> 💡 Ensure port `9969` is accessible and not blocked by firewall.

---

## ▶️ Usage

### Basic Examples
```bash
# Convert specific files
python main.py file1.pdf file2.docx

# Convert all supported files in a directory
python main.py -d /path/to/documents

# Specify custom output directory
python main.py file1.pdf -o ./results
```

### Advanced Options
```bash
# Increase concurrency & use custom service URL
python main.py -d ./docs --workers 5 --url http://remote-server:9969/v1/convert/file

# Show help
python main.py -h
```

### 📌 Command-Line Arguments

| Argument / Flag       | Description                          | Default                              |
|-----------------------|--------------------------------------|--------------------------------------|
| `input_files`         | List of input file paths             | *(required if `-d` not used)*        |
| `-d`, `--directory`   | Input directory to scan recursively  | —                                    |
| `-o`, `--output`      | Output directory                     | Parent of first input file           |
| `--workers`           | Number of concurrent workers         | `3`                                  |
| `--url`               | Docling service endpoint             | `http://localhost:9969/v1/convert/file` |

---

## 📂 Output Structure

Each converted file generates:

```
output/
├── document.md                 # Clean Markdown output
├── document_images/            # Extracted images (PNG/JPG)
│   ├── image_20260129_001.png
│   └── image_20260129_002.jpg
└── conversion_report.txt       # Summary report
```

---

## 📊 Conversion Report

The `conversion_report.txt` includes:
- Total files processed, success/failure counts
- Per-file processing time
- Number of extracted images
- Error details for failed conversions

Example snippet:
```
✅ Successfully converted: 12 files
❌ Failed: 2 files
⏱️ Total time: 42.3s
📸 Total images extracted: 37
```

---

## 🏗️ Project Structure

```
docling-batch-processor/
├── main.py                     # CLI entry point
├── core/
│   ├── batch_converter.py      # Orchestrates the full pipeline
│   ├── docling_client.py       # HTTP client for Docling API
│   ├── file_validator.py       # Validates input files
│   ├── image_processor.py      # Handles image extraction & saving
│   ├── table_processor.py      # Optimizes table formatting
│   └── output_manager.py       # Manages output files & report
└── requirements.txt
```

### Module Roles
- **`batch_converter`**: Main controller that coordinates all components  
- **`docling_client`**: Wraps API calls to Docling-serve  
- **`image_processor` / `table_processor`**: Post-process conversion results  
- **`output_manager`**: Handles file I/O and report generation  

---

## ❓ Common Issues

### 🔌 Connection Refused
- ✅ Is Docling-serve running? Check with `docker ps`
- ✅ Is the URL correct? Default: `http://localhost:9969/v1/convert/file`
- ✅ Is the port open? Try `curl http://localhost:9969/health`

### 📄 Invalid File Format
- Ensure files aren’t corrupted
- Extension must match actual format (e.g., don’t rename `.zip` to `.docx`)

### 💥 Out of Memory
- Reduce concurrency: `--workers 1`
- Process smaller batches

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Open an issue to discuss feature requests or bugs
2. Fork the repo and submit a PR with clear commit messages
3. Add tests if applicable

See [CONTRIBUTING.md](CONTRIBUTING.md) (optional but recommended).

---

## 📬 Author & Contact

- **Email**: [thanrise.ai@gmail.com](mailto:ethanrise.ai@gmail.com)
- **GitHub**: [@ethanrise](https://github.com/ethanrise)
- **LinkedIn**: [linkedin.com/in/ethanrise](https://www.linkedin.com/in/ethanrise/)

💬 Feel free to reach out for collaboration or feedback!
