from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import hashlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Risk assessment function to check for potential risks based on filename and size
def check_risks(filename: str, size_bytes: int, file_type: str) -> dict:
    risks = []
    score = 0

    ext = os.path.splitext(filename)[1].lower()

     # dangerous file extensions
    badext = [".exe", ".bat", ".ps1", ".ps2",".vbs",".vb", ".js", ".jse", ".msi"]
    if ext in badext:
        risks.append("Executable file type")
        score += 30

    # No file extension
    if not ext:
        risks.append("No file extension")
        score += 25

    # multiple extensions 
    manyext = os.path.splitext(filename)[0]
    if "." in manyext and any(
        manyext.endswith(e) for e in badext
    ):
        risks.append("Multiple extensions detected")
        score += 20

    # (over 100MB)
    if size_bytes > 100_000_000:
        risks.append("File size exceeds 100MB")
        score += 10

    # starts with dot (hidden file)
    if filename.startswith("."):
        risks.append("Hidden file")
        score += 15

    # risk level based on score
    level = "Low"
    if score >= 40:
        level = "Medium"
    if score >= 70:
        level = "High"

    return {
        "score": score,
        "level": level,
        "indicators": risks
    }


@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):

    # Read the file into memory
    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    # Generates hashes
    md5_hash    = hashlib.md5(contents).hexdigest()
    sha1_hash   = hashlib.sha1(contents).hexdigest()
    sha256_hash = hashlib.sha256(contents).hexdigest()

    # Risk
    risk = check_risks(file.filename, len(contents), os.path.splitext(file.filename)[1].lower())

    # Result
    result = {
        "filename": file.filename,
        "size_kb": round(len(contents) / 1024, 2),
        "file_type": os.path.splitext(file.filename)[1].upper(),
        "hashes": {
            "md5":    md5_hash,
            "sha1":   sha1_hash,
            "sha256": sha256_hash
        },
        "risk": risk
    }

    # Delete the temp file
    os.unlink(tmp_path)

    return result
