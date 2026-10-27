
from pathlib import Path
from urllib.parse import urlparse
import re
import math

import joblib
import numpy as np

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Project paths
ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "phishxai_model.joblib"
FEATURES_FILE = ROOT / "feature_columns.joblib"

# FastAPI application
app = FastAPI(title="PhishXAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Req(BaseModel):
    url: str


def entropy(s):
    if not s:
        return 0.0

    n = len(s)
    counts = {c: s.count(c) for c in set(s)}

    return -sum(
        (v / n) * math.log2(v / n)
        for v in counts.values()
    )


def features(raw):
    raw = raw.strip()

    u = (
        raw
        if re.match(r"^[a-zA-Z][\w+.-]*://", raw)
        else "http://" + raw
    )

    p = urlparse(u)
    host = p.hostname or ""
    path = p.path or ""
    query = p.query or ""

    digits = sum(c.isdigit() for c in raw)
    parts = [x for x in host.split(".") if x]
    tld = parts[-1] if len(parts) > 1 else ""

    tokens = [
        x for x in re.split(r"[^A-Za-z0-9]+", raw) if x
    ]

    return {
        "url_length": len(raw),

        "has_ip_address": int(
            bool(
                re.fullmatch(
                    r"\d{1,3}(?:\.\d{1,3}){3}",
                    host
                )
            )
        ),

        "dot_count": raw.count("."),
        "https_flag": int(u.lower().startswith("https://")),
        "url_entropy": entropy(raw),
        "token_count": len(tokens),
        "subdomain_count": max(0, len(parts) - 2),

        "query_param_count": (
            0 if not query
            else len([x for x in query.split("&") if x])
        ),

        "tld_length": len(tld),
        "path_length": len(path),
        "has_hyphen_in_domain": int("-" in host),
        "number_of_digits": digits,

        "tld_popularity": int(
            tld.lower() in {
                "com", "org", "net", "edu", "gov",
                "io", "co", "uk", "de", "in", "pk"
            }
        ),

        "suspicious_file_extension": int(
            bool(
                re.search(
                    r"\.(exe|zip|scr|bat|cmd|msi)(?:$|\?)",
                    raw.lower()
                )
            )
        ),

        "domain_name_length": len(host),

        "percentage_numeric_chars": (
            digits / len(raw) * 100 if raw else 0
        ),
    }


@app.get("/api/health")
def health():
    return {
        "api": "online",
        "model_loaded": MODEL.exists() and FEATURES_FILE.exists(),
        "model": "Random Forest",
        "explainability": "SHAP",
    }


@app.post("/api/analyze")
def analyze(req: Req):
    fx = features(req.url)

    if not MODEL.exists() or not FEATURES_FILE.exists():
        return {
            "status": "model_not_ready",
            "message": "The trained model or feature file is missing.",
            "features": fx,
        }

    try:
        model = joblib.load(MODEL)
        names = joblib.load(FEATURES_FILE)

        x = np.array(
            [[fx[name] for name in names]],
            dtype=float
        )

        pred = int(model.predict(x)[0])
        probs = model.predict_proba(x)[0]

        # Dataset labels: 0 = Phishing, 1 = Legitimate
        label = "Legitimate" if pred == 1 else "Phishing"

        # Confidence for the predicted class
        class_index = list(model.classes_).index(pred)
        confidence = float(probs[class_index])

        shap_rows = []

        try:
            import shap

            explainer = shap.TreeExplainer(model)
            sv = explainer.shap_values(x)

            # Select SHAP values for the predicted class
            if isinstance(sv, list):
                # Older SHAP versions: list of class arrays
                class_sv = np.asarray(sv[class_index])
                vals = (
                    class_sv[0]
                    if class_sv.ndim == 2
                    else class_sv.reshape(-1)
                )
            else:
                vals = np.asarray(sv)

                if vals.ndim == 3:
                    # Newer SHAP format:
                    # (samples, features, classes)
                    vals = vals[0, :, class_index]
                elif vals.ndim == 2:
                    # (samples, features)
                    vals = vals[0]
                else:
                    vals = vals.reshape(-1)

            shap_rows = [
                {
                    "feature": name,
                    "value": float(fx[name]),
                    "impact": float(vals[i]),
                }
                for i, name in enumerate(names)
                if i < len(vals)
            ]

            shap_rows.sort(
                key=lambda item: abs(item["impact"]),
                reverse=True
            )

        except Exception as shap_error:
            # Keep prediction available if SHAP fails
            print("SHAP explanation error:", shap_error)
            shap_rows = []

        return {
            "status": "ok",
            "prediction": label,
            "confidence": confidence,
            "features": fx,
            "shap": shap_rows[:10],
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
