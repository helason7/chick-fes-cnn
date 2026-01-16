import numpy as np
import hdbscan
import json
import os

UNKNOWN_PATH = "data/unknown_embeddings.npy"
OUTPUT_PATH = "data/clusters.json"

# Load embeddings
X = np.load(UNKNOWN_PATH, allow_pickle=True)

print("Total unknown embeddings:", X.shape)

# Jangan cluster kalau masih sedikit
if X.shape[0] < 10:
    print("❌ Belum cukup data untuk clustering")
    exit()

# Clustering
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=3,
    min_samples=2,
    metric="euclidean"
)


labels = clusterer.fit_predict(X)

clusters = {}

for idx, label in enumerate(labels):
    if label == -1:
        continue
    clusters.setdefault(str(label), []).append(idx)

# Simpan hasil
with open(OUTPUT_PATH, "w") as f:
    json.dump(clusters, f, indent=2)

print("✅ Clustering selesai")
print("Clusters:", clusters.keys())
