import json
import numpy as np

UNKNOWN_PATH = "data/unknown_embeddings.npy"
CLUSTER_PATH = "data/clusters.json"
OUTPUT_PATH = "data/cluster_centroids.json"

# Load data
embeddings = np.load(UNKNOWN_PATH, allow_pickle=True)

with open(CLUSTER_PATH) as f:
    clusters = json.load(f)

centroids = {}

print("Total embeddings:", embeddings.shape)

for cluster_id, indices in clusters.items():
    # Ambil embedding sesuai index
    cluster_vectors = embeddings[indices]

    # Hitung centroid (rata-rata)
    centroid = cluster_vectors.mean(axis=0)

    # (opsional tapi bagus) normalisasi
    centroid = centroid / np.linalg.norm(centroid)

    centroids[cluster_id] = centroid.tolist()

    print(f"Cluster {cluster_id}:")
    print("  jumlah data :", len(indices))
    print("  centroid dim:", len(centroid))

# Simpan centroid
with open(OUTPUT_PATH, "w") as f:
    json.dump(centroids, f, indent=2)

print("\n✅ Centroid berhasil dihitung dan disimpan")
