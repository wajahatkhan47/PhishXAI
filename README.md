# PhishXAI — Full FYP Website Demo

A complete React + TypeScript + Vite frontend and FastAPI backend starter for:
Explainable XGBoost-Based Phishing URL Detection with Real-Time Web Platform.

## Run

### Backend
```powershell
cd E:\PhishXAI_Full_Website
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python backend\app.py
```

### Frontend — second PowerShell
```powershell
cd E:\PhishXAI_Full_Website\frontend
npm install
npm run dev
```

Open the Vite URL.

## Model behavior

The UI never invents a prediction. Until a real model file exists, it displays MODEL NOT READY.

Put the real Mendeley CSV into `data\`, inspect it, then train only after confirming the actual columns.
