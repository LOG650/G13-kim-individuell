from pathlib import Path
FOLDERS = ["data/raw","data/processed","models","results","plots","reports"]
def setup():
    base = Path(__file__).parent
    for f in FOLDERS:
        (base/f).mkdir(parents=True, exist_ok=True)
        print(f"  OK: {f}/")
    print("Mappestruktur klar!")
if __name__ == "__main__": setup()
