algorithms = {
    "K-Means": KMeans(n_clusters=3, random_state=42),
    "Agglomerative": AgglomerativeClustering(n_clusters=3),
    "DBSCAN": DBSCAN(eps=0.5, min_samples=5),
    "Mean-Shift": MeanShift(),
    "Gaussian Mixture": GaussianMixture(n_components=3, random_state=42),
    "Spectral": SpectralClustering(n_clusters=3, affinity='nearest_neighbors', random_state=42),
    "BIRCH": Birch(n_clusters=3)
}
