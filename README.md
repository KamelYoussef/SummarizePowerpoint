Voici une présentation des **obstacles courants en apprentissage automatique (ML)** en français, basée sur les résultats de recherche :

---

### 1. **Jeu de données déséquilibré (Imbalanced Dataset)**  
Un jeu de données déséquilibré se produit lorsque les classes dans les données ne sont pas représentées de manière égale. Par exemple, dans un problème de classification binaire, une classe peut être beaucoup plus fréquente que l'autre. Cela entraîne des modèles biaisés qui privilégient la classe majoritaire, ce qui réduit la précision pour la classe minoritaire.  
**Exemple** : Dans un modèle de classification de difficulté de phrases en français, la classe A2 avait une précision inférieure à 36 % en raison de la similarité avec les niveaux A1 et B1 .  

---

### 2. **Fuites de données (Data Leakage)**  
La fuite de données se produit lorsque des informations du jeu de test ou de validation sont involontairement utilisées pendant l'entraînement du modèle. Cela peut entraîner des performances artificiellement élevées mais non généralisables.  
**Exemple** : Dans un projet de traduction automatique, une mauvaise séparation des données d'entraînement et de test pourrait fausser les résultats, rendant le modèle inefficace en production .  

---

### 3. **Changement de distribution (Distribution Shift)**  
Le changement de distribution se produit lorsque les données utilisées pour entraîner le modèle diffèrent significativement des données réelles rencontrées en production. Cela peut être dû à des changements dans les conditions environnementales ou à des évolutions dans les données.  
**Exemple** : Un modèle entraîné sur des textes littéraires français pourrait mal performer sur des textes techniques ou des conversations informelles .  

---

### 4. **Manque de données de qualité**  
La qualité des données est cruciale pour entraîner des modèles performants. Des données bruyantes, incomplètes ou mal annotées peuvent entraîner des erreurs de prédiction.  
**Exemple** : Dans un projet de classification de sentiments en français, l'utilisation de données mal annotées a nécessité un nettoyage manuel pour améliorer la précision du modèle .  

---

### 5. **Complexité des modèles et sur-ajustement (Overfitting)**  
Les modèles complexes peuvent s'adapter trop bien aux données d'entraînement, ce qui réduit leur capacité à généraliser à de nouvelles données.  
**Exemple** : Un modèle de génération de texte en français basé sur une architecture LSTM a montré des signes de sur-ajustement, nécessitant des techniques de régularisation pour améliorer ses performances .  

---

### 6. **Coûts de calcul élevés**  
L'entraînement de modèles de grande envergure, comme les modèles de langage, peut nécessiter des ressources matérielles importantes, ce qui peut être un obstacle pour les petites équipes ou les projets à budget limité.  
**Exemple** : L'entraînement d'un modèle de langage français sur des TPUs a coûté environ 621,20 $ par mois, ce qui peut être prohibitif pour certains projets .  

---

### 7. **Interprétabilité des modèles**  
Les modèles complexes, comme les réseaux de neurones profonds, sont souvent considérés comme des "boîtes noires", ce qui rend difficile l'interprétation de leurs décisions.  
**Exemple** : Dans un projet de classification de textes en français, l'utilisation de modèles basés sur BERT a nécessité des techniques supplémentaires pour expliquer les prédictions .  

---

### 8. **Problèmes de tokenisation et de prétraitement**  
La tokenisation et le prétraitement des textes en français peuvent poser des défis spécifiques, comme la gestion des accents, des contractions et des variations régionales.  
**Exemple** : L'utilisation de tokenizers comme SentencePiece a permis d'améliorer les performances des modèles de langage en français en gérant mieux les spécificités linguistiques .  

---

### 9. **Biais dans les données**  
Les modèles peuvent hériter des biais présents dans les données d'entraînement, ce qui peut entraîner des prédictions discriminatoires ou injustes.  
**Exemple** : Un modèle de génération de texte en français a dû être nettoyé de contenus toxiques pour réduire les biais de 14,7 % par rapport aux modèles existants .  

---

### 10. **Manque de ressources pour les langues non anglaises**  
Les modèles de langage et les jeux de données sont souvent plus développés pour l'anglais, ce qui peut limiter les performances pour d'autres langues comme le français.  
**Exemple** : Le modèle Cedille a été développé spécifiquement pour combler ce manque en offrant un modèle de langage français de haute qualité .  

---

Ces obstacles sont courants dans les projets ML, mais des solutions existent pour les surmonter, comme l'augmentation des données, la régularisation, et l'utilisation de techniques de validation rigoureuses. Pour plus de détails, vous pouvez consulter les sources citées.
