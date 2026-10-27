
import pandas as pd
from backend.app import features

df = pd.read_csv("data/url_features_extracted1.csv")
df = df.dropna(subset=["URL", "ClassLabel"]).head(1000)

cols = [
    "url_length",
    "has_ip_address",
    "dot_count",
    "https_flag",
    "url_entropy",
    "token_count",
    "subdomain_count",
    "query_param_count",
    "tld_length",
    "path_length",
    "has_hyphen_in_domain",
    "number_of_digits",
    "tld_popularity",
    "suspicious_file_extension",
    "domain_name_length",
    "percentage_numeric_chars",
]

mismatches = {col: 0 for col in cols}
errors = 0

for _, row in df.iterrows():
    try:
        website_features = features(str(row["URL"]))

        for col in cols:
            if abs(float(row[col]) - float(website_features[col])) > 1e-8:
                mismatches[col] += 1

    except Exception as exc:
        errors += 1

print("Rows checked:", len(df))
print("\nFeature mismatches:")
for col, count in mismatches.items():
    print(f"{col}: {count}")

print("\nErrors:", errors)
