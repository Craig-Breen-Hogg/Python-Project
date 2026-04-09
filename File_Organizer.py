from pathlib import Path

FOLDERS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".txt", ".docx", ".xlsx"],
    "Code": [".py", ".cs", ".js"],
    "Archives": [".zip", ".rar"]
}

def organise(directory="."):
    base = Path(directory)

    for file in base.iterdir():
        if file.is_file():
            for folder, extensions in FOLDERS.items():
                if file.suffix.lower() in extensions:
                    target = base / folder
                    target.mkdir(exist_ok=True)
                    file.rename(target / file.name)
                    break

if __name__ == "__main__":
    organise()
    print("✅ Files organised successfully")