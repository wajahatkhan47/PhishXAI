from pathlib import Path
import pandas as pd
root=Path(__file__).resolve().parents[1]
files=list((root/"data").glob("*.csv"))
if not files:
 print("No CSV found in E:\\PhishXAI_Full_Website\\data"); raise SystemExit
for f in files:
 df=pd.read_csv(f)
 print("\\nFILE:",f)
 print("SHAPE:",df.shape)
 print("COLUMNS:",list(df.columns))
 print("\\nHEAD:\\n",df.head().to_string())
 print("\\nMISSING:\\n",df.isna().sum().to_string())
