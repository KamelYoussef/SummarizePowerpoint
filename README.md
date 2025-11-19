chunk_size = 10000
pairs_to_delete = set()

for chunk in usag_meme_admin.DataFrame().iter_chunks(chunk_size):
    chunk_pairs = set(zip(
        chunk['no usag'], 
        chunk['no usag cible']
    ))
    pairs_to_delete.update(chunk_pairs)
