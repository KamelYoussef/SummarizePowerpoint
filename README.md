"""
    Retourne un dataframe augmenté d'une colonne dans laquelle on a extrait les 
    « i » premiers chiffres d'un nombre.

    Cette fonction extrait les « i » premiers chiffres significatifs d'un champ numérique donné 
    dans un DataFrame et les ajoute comme une nouvelle colonne.

    Parameters
    ----------
    data : pandas.DataFrame
        Jeu de données contenant les valeurs numériques à traiter.
    
    nombre : str
        Le nom de la colonne contenant les nombres dont on souhaite extraire les premiers chiffres.
    
    position : int
        Nombre de positions du nombre à extraire (c'est-à-dire combien de chiffres significatifs).

    Returns
    -------
    pandas.DataFrame
        Le DataFrame original avec une colonne supplémentaire contenant les « i » premiers chiffres du champ donné.
