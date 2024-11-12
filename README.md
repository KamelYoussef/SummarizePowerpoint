fig <- plot_ly(pca_data, x = ~PC1, y = ~PC2, z = ~PC3, color = ~anomaly_score,
               colors = c("blue", "red"), marker = list(size = 5)) %>%
       layout(scene = list(
           xaxis = list(title = "PCA Component 1"),
           yaxis = list(title = "PCA Component 2"),
           zaxis = list(title = "PCA Component 3")
       ),
       title = "3D PCA Plot with Isolation Forest Anomaly Scores")

fig
