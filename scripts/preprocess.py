"""
preprocess.py - Preprocessing pipeline for eligibility traits

This module handles:
1. Case normalization
2. Whitespace standardization  
3. Deduplication of exact matches
4. Basic cleaning
"""

import pandas as pd
import re
from typing import List, Set


def normalize_trait(trait: str) -> str:
    """
    Normalize a trait string for comparison.
    
    Args:
        trait: Raw trait string
        
    Returns:
        Normalized trait string
    """
    # Convert to lowercase
    normalized = trait.lower().strip()
    
    # Standardize whitespace
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Remove leading/trailing punctuation
    normalized = normalized.strip('.,;:')
    
    return normalized


def deduplicate_traits(traits: List[str]) -> List[str]:
    """
    Remove exact duplicate traits after normalization.
    
    Args:
        traits: List of raw trait strings
        
    Returns:
        List of unique normalized traits
    """
    seen: Set[str] = set()
    unique_traits = []
    
    for trait in traits:
        normalized = normalize_trait(trait)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_traits.append(normalized)
    
    return sorted(unique_traits)


def preprocess_pipeline(input_file: str, output_file: str) -> dict:
    """
    Run full preprocessing pipeline on raw traits.
    
    Args:
        input_file: Path to CSV with raw traits
        output_file: Path to save preprocessed traits
        
    Returns:
        Dict with preprocessing statistics
    """
    # Load raw traits
    df = pd.read_csv(input_file)
    raw_traits = df.iloc[:, 0].tolist()
    
    initial_count = len(raw_traits)
    
    # Deduplicate
    unique_traits = deduplicate_traits(raw_traits)
    final_count = len(unique_traits)
    
    # Save
    output_df = pd.DataFrame({'trait': unique_traits})
    output_df.to_csv(output_file, index=False)
    
    stats = {
        'initial_count': initial_count,
        'final_count': final_count,
        'removed': initial_count - final_count,
        'reduction_pct': round((initial_count - final_count) / initial_count * 100, 1)
    }
    
    print(f"Preprocessing complete:")
    print(f"  Initial traits: {stats['initial_count']}")
    print(f"  Final traits: {stats['final_count']}")
    print(f"  Removed: {stats['removed']} ({stats['reduction_pct']}%)")
    
    return stats


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = "../data/raw_traits.csv"
        output_file = "../data/preprocessed_traits.csv"
    
    preprocess_pipeline(input_file, output_file)
