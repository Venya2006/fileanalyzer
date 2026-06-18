# Forensic File Analyzer

Developed a Python-based digital forensics tool using FastAPI to analyze uploaded files, generate cryptographic hashes, and automatically detect suspicious file indicators including executable types, hidden files, and disguised extensions. Built a dark-themed frontend with CSV export functionality.


---

## Features

- File Metadata
- MD5, SHA1, and SHA256 hash generation
- Risk scoring with indicator breakdown
- Executable and hidden file detection
- Multiple extension and missing extension detection
- CSV export of the full analysis report

---

## Tech stack

- Python
- FastAPI
- Uvicorn
- HTML
- CSS
- JavaScript

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/fileanalyzer.git
cd fileanalyzer
```
**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

**5. Open the tool**

Open `index.html` directly in your browser. Make sure the server is running first.

---

## Usage

1. Open `index.html` in your browser
2. Click **Choose file** and select any file
3. Click **Analyze**
4. You're taken to a results page showing file info, hashes, and risk assessment
5. Click **Export as CSV** to download a forensic report
6. Click **Back** to analyze another file

---
## Risk scoring

| Indicator                    | Score |
| ---                          |  ---  |
| Executable file type         |  +30  |
| No file extension            |  +25  |
| Multiple extensions detected |  +20  |
| Hidden file                  |  +15  |
| File size exceeds 100MB      |  +10  |

| Score |Risk level |
|---|---|
|Below 40 |Low |
|40–70 |Medium |
|Above 70 |High |

---
