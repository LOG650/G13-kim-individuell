import subprocess, sys
from pathlib import Path

SCRIPTS = ["00_setup_project.py","01_generate_data.py","02_preprocess_data.py","03_baseline_model.py","04_ml_model.py","05_visualize_results.py"]
BASE = Path(__file__).parent

for script in SCRIPTS:
    print(f"\n▶ {script}")
    r = subprocess.run([sys.executable, str(BASE/script)])
    if r.returncode != 0:
        print(f"❌ Feil i {script}")
        sys.exit(1)
print("\n✅ Pipeline fullført!")
