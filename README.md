def benford_calcul_cote_z(benf_percent, mt):
    # Extracting the relevant columns using mt
    percent_col = f'PERCENT_{mt}'
    tot_col = f'TOT_{mt}'
    
    # Calculating the numerator
    numerateur = (abs(benf_percent[percent_col] / 100 - benf_percent['EXPECTED'] / 100) - (1 / (2 * benf_percent[tot_col])))
    
    # Calculating the denominator
    denominateur = np.sqrt(benf_percent['EXPECTED'] / 100 * (1 - benf_percent['EXPECTED'] / 100) / benf_percent[tot_col])
    
    # Z-score calculation
    out = numerateur / denominateur
    
    return out
