import pandas as pd
from rapidfuzz import fuzz
from typing import List, Tuple

def find_closest_matches_rapidfuzz(
    potential_name: str,
    company_data: pd.Series,
    num_matches: int
) -> List[Tuple[str, float]]:
    """
    Finds the 'num_matches' closest company names in the data using rapidfuzz.

    Args:
        potential_name: The name to match against the dataset.
        company_data: A pandas Series containing the company names (3M rows).
        num_matches: The number of closest matches to return.

    Returns:
        A list of tuples (company_name, similarity_score), sorted by score.
    """
    print(f"Searching for closest matches to '{potential_name}'...")
    
    # 1. Calculate similarity for all names
    # fuzz.ratio is a robust, symmetric measure (like Levenshtein distance)
    scores = company_data.apply(lambda name: fuzz.ratio(potential_name.lower(), name.lower()))
    
    # 2. Combine names and scores into a DataFrame
    results_df = pd.DataFrame({
        'name': company_data,
        'score': scores
    })
    
    # 3. Sort by score (descending) and get the top N
    # We use nlargest for efficiency on large datasets
    top_matches = results_df.nlargest(num_matches, 'score')
    
    # 4. Format the output
    return list(zip(top_matches['name'], top_matches['score']))

# --- Example Usage ---

# 1. Prepare your (simulated) 3 million row data
# In a real scenario, 'company_names_series' would be loaded from your file (e.g., CSV).
data = [
    "Google Inc.", "Gogle Inc.", "Alphabet Co.", 
    "Amazon Web Services", "Microsoft Corp.", 
    "Googlle", "Apple", "Tesla Motors"
] * 375000  # Simulating 3 million rows (8 * 375000 = 3,000,000)
company_names_series = pd.Series(data)

# 2. Define the search parameters
search_name = "Googl"
k_matches = 3

# 3. Run the search
closest_companies = find_closest_matches_rapidfuzz(search_name, company_names_series, k_matches)

# 4. Print the results
print("\nTop Matches (Name, Score):")
for name, score in closest_companies:
    print(f"- {name}: {score:.2f}")
