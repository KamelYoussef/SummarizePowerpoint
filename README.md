algorithms = {
    "Isolation Forest": IsolationForest(contamination=0.05, random_state=42),
    "One-Class SVM": OneClassSVM(nu=0.05, kernel="rbf", gamma=0.1),
    "Local Outlier Factor": LocalOutlierFactor(n_neighbors=20, contamination=0.05),
    "Elliptic Envelope": EllipticEnvelope(contamination=0.05)
}
