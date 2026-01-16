import json
import numpy as np

UNKNOWN_PATH = "data/unknown_embeddings.npy"
CLUSTER_PATH = "data/clusters.json"

with open(CLUSTER_PATH) as f:
    clusters = json.load(f)

data = np.load(UNKNOWN_PATH, allow_pickle=True)

print("Total embeddings:", data.shape)

for cluster_id, indices in clusters.items():
    print(f"\nCluster {cluster_id}")
    print("Jumlah data:", len(indices))
    print("Index sample:", indices[:5])
    