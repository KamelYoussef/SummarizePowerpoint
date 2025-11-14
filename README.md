info_lookup = db_cred_info.set_index('sdu') 

result_df = result_df_cible_similaire.join(

    info_lookup, 

    on='cible_similaire', 

    rsuffix='_similar_info'

)


result_df.rename(

    columns={

        'average_tvq_sdu_similar_info': 'average_tvq_cible_similaire',

        'average_tps_sdu_similar_info': 'average_tps_cible_similaire',

        'nombre_declarations_sdu_similar_info': 'nb_decla_cible_similaire',

        'frequence_decla_sdu_similar_info': 'frequence_decla_cible_similaire'

    }, 

    inplace=True

)

result_df = result_df.join(
        info_lookup, 
        on='cible', 
        rsuffix='_cible_info'
    )
    
result_df.rename(
    columns={
        'average_tvq_sdu_cible_info': 'average_tvq_cible',
        'average_tps_sdu_cible_info': 'average_tps_cible',
        'nombre_declarations_sdu_cible_info': 'nb_decla_cible',
        'frequence_decla_sdu_cible_info': 'frequence_decla_cible'
    }, 
    inplace=True
)

del info_lookup

return result_df
