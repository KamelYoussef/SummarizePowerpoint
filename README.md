"""
    Calcul de la cote Z attribuée au test.

    Cette fonction calcule la cote Z à partir des pourcentages observés et attendus, pour un champ numérique donné.

    Parameters
    ----------
    benf_percent : pandas.DataFrame
        Jeu de données qui contient les pourcentages attendus et observés, ainsi que les totaux pour chaque catégorie.
    
    mt : str
        Le nom du champ qui contient la valeur numérique à tester (par exemple : 'RTI', 'TVQ', 'TPS', 'CTI', 'NET', etc.).

    Returns
    -------
    pandas.Series
        Une série contenant la cote Z calculée pour chaque ligne du DataFrame.
