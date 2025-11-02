# backend/models/train_classifier.py
from sentence_transformers import SentenceTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
import json, numpy as np, pickle, os

# List of dataset files
datasets = ["data/opp.json", "data/medical_consents.json"]
records = []

for path in datasets:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")
    with open(path, "r", encoding="utf-8") as f:
        try:
            # Try normal JSON array
            dataset = json.load(f)
        except json.JSONDecodeError:
            # Fallback: JSON Lines format (one object per line)
            f.seek(0)
            dataset = [json.loads(line) for line in f if line.strip()]
    records.extend(dataset)

# Extract text and labels
texts = [r["text"] for r in records]
labels_list = [r.get("label", []) for r in records]

# Create binary label matrix for top-n labels
unique_labels = sorted({lab for labs in labels_list for lab in (labs if isinstance(labs, list) else [labs])})
Y = []
for labs in labels_list:
    if not isinstance(labs, list):
        labs = [labs]
    Y.append([1 if l in labs else 0 for l in unique_labels])

# Load model and train
print(f"Loaded {len(records)} samples from {datasets}")
model = SentenceTransformer("all-mpnet-base-v2")
X = model.encode(texts, convert_to_numpy=True)

clf = OneVsRestClassifier(LogisticRegression(max_iter=1000)).fit(X, Y)

# Save model
os.makedirs("models", exist_ok=True)
pickle.dump(
    {"clf": clf, "label_names": unique_labels, "embed_model": "all-mpnet-base-v2"},
    open("models/label_clf.pkl", "wb")
)

print(f"✅ Model trained and saved successfully! Labels: {unique_labels}")
