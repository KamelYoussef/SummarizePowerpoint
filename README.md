def benford_fid(data, nombre, position):
    # Crée le nom de la nouvelle colonne en fonction de la position et du champ nombre
    fid = f"F{position}D_{nombre}"
    
    # Calcul des premiers "i" chiffres significatifs (FiD)
    data[fid] = np.sign(data[nombre]) * np.floor(np.abs(data[nombre]) / 10**(np.floor(np.log10(np.abs(data[nombre]))) - position + 1))
    
    # Convertit la colonne en chaîne de caractères avec des zéros initiaux si nécessaire et une largeur fixe
    data[fid] = data[fid].apply(lambda x: f'{int(x):0{position}d}' if not pd.isna(x) else np.nan)
    
    # Définit la colonne FiD à NaN lorsque la valeur absolue du champ 'nombre' est inférieure ou égale à 10
    data.loc[np.abs(data[nombre]) <= 10, fid] = np.nan
    
    # Retourne le DataFrame avec la nouvelle colonne ajoutée
    return data
