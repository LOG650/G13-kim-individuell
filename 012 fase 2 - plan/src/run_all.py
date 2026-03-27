import subprocess, sys
from pathlib import Path
SCRIPTS = ["00_setup_project.py","01_generate_data.py","02_preprocess_data.py",
           "03_baseline_model.py","04_ml_model.py","05_visualize_results.py"]
BASE = Path(__file__).parent
print("LOG650 Pipeline starter...")
for s in SCRIPTS:
    print(f"\n--- {s} ---")
    r = subprocess.run([sys.executable, str(BASE/s)])
    if r.returncode != 0:
        print(f"FEIL i {s}")
        sys.exit(1)
print("\nPipeline fullfort! Sjekk results/ og plots/")
