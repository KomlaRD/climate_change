from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "https://docs.google.com/spreadsheets/d/e/2PACX-1vR02rJg_sHzdSP3DSoWGZFfau7wvlVaEq5JTbQMVCjjQTeSIvoSe5ELPw8ntijsn4xZgutN2QW9kE6y/pub?output=csv")
