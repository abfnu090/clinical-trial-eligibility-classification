"""
consensus.py - Multi-model majority voting for eligibility trait classification

This module implements the consensus logic used across all phases of the pipeline.
"""

import json
import pandas as pd
from collections import Counter
from typing import List, Dict, Tuple

MODELS = ['claude', 'gpt5', 'gemini', 'deepseek', 'grok']

def calculate_consensus(votes: List[str]) -> Tuple[str, str, str]:
    """
    Calculate majority vote consensus from model predictions.
    
    Args:
        votes: List of predictions from each model
        
    Returns:
        Tuple of (consensus_value, agreement_ratio, flag)
        - flag: 🟢 (≥4/5), 🟡 (3/5), 🔴 (<3/5)
    """
    vote_counts = Counter(votes)
    most_common = vote_counts.most_common(1)[0]
    consensus_value = most_common[0]
    agreement_count = most_common[1]
    
    agreement_ratio = f"{agreement_count}/{len(votes)}"
    
    if agreement_count >= 4:
        flag = "🟢"
    elif agreement_count == 3:
        flag = "🟡"
    else:
        flag = "🔴"
    
    return consensus_value, agreement_ratio, flag


def aggregate_phase2_results(model_results: Dict[str, Dict]) -> pd.DataFrame:
    """
    Aggregate trait-to-umbrella mapping results from all models.
    
    Args:
        model_results: Dict mapping model name to their mapping results
        
    Returns:
        DataFrame with consensus mappings
    """
    # Collect all traits
    all_traits = set()
    for model, results in model_results.items():
        all_traits.update(results.keys())
    
    rows = []
    for trait in sorted(all_traits):
        votes = []
        model_votes = {}
        
        for model in MODELS:
            if model in model_results and trait in model_results[model]:
                vote = model_results[model][trait]
                votes.append(vote)
                model_votes[model] = vote
            else:
                model_votes[model] = None
        
        if votes:
            consensus, agreement, flag = calculate_consensus(votes)
            rows.append({
                'trait': trait,
                'umbrella': consensus,
                'agreement': agreement,
                'flag': flag,
                **model_votes
            })
    
    return pd.DataFrame(rows)


def aggregate_phase3_results(model_results: Dict[str, Dict]) -> pd.DataFrame:
    """
    Aggregate umbrella-to-category classification results from all models.
    
    Args:
        model_results: Dict mapping model name to their classification results
        
    Returns:
        DataFrame with consensus classifications
    """
    # Collect all umbrellas
    all_umbrellas = set()
    for model, results in model_results.items():
        all_umbrellas.update(results.keys())
    
    rows = []
    for umbrella in sorted(all_umbrellas):
        votes = []
        model_votes = {}
        
        for model in MODELS:
            if model in model_results and umbrella in model_results[model]:
                vote = model_results[model][umbrella]
                votes.append(vote)
                model_votes[model] = vote
            else:
                model_votes[model] = None
        
        if votes:
            consensus, agreement, flag = calculate_consensus(votes)
            rows.append({
                'umbrella': umbrella,
                'final_category': consensus,
                'agreement': agreement,
                'flag': flag,
                **model_votes
            })
    
    return pd.DataFrame(rows)


def merge_umbrella_proposals(model_proposals: Dict[str, List[str]], 
                             threshold: int = 3) -> List[str]:
    """
    Merge umbrella category proposals using intersection approach.
    
    Args:
        model_proposals: Dict mapping model name to list of proposed umbrellas
        threshold: Minimum number of models that must propose a category
        
    Returns:
        List of unified umbrella categories
    """
    category_counts = Counter()
    
    for model, categories in model_proposals.items():
        for cat in categories:
            # Normalize category name for comparison
            normalized = cat.lower().strip()
            category_counts[normalized] += 1
    
    # Keep categories appearing in >= threshold models
    unified = [cat for cat, count in category_counts.items() 
               if count >= threshold]
    
    return sorted(unified)


def generate_summary_stats(df: pd.DataFrame, flag_column: str = 'flag') -> Dict:
    """
    Generate summary statistics for consensus results.
    
    Args:
        df: DataFrame with consensus results
        flag_column: Name of the flag column
        
    Returns:
        Dict with summary statistics
    """
    total = len(df)
    green = len(df[df[flag_column] == '🟢'])
    yellow = len(df[df[flag_column] == '🟡'])
    red = len(df[df[flag_column] == '🔴'])
    
    return {
        'total': total,
        'green': green,
        'green_pct': round(green / total * 100, 1),
        'yellow': yellow,
        'yellow_pct': round(yellow / total * 100, 1),
        'red': red,
        'red_pct': round(red / total * 100, 1)
    }


if __name__ == "__main__":
    # Example usage
    votes = ['PREDICTABLE_AND_NECESSARY', 'PREDICTABLE_AND_NECESSARY', 
             'PREDICTABLE_BUT_NOT_NECESSARY', 'PREDICTABLE_AND_NECESSARY',
             'PREDICTABLE_AND_NECESSARY']
    
    consensus, agreement, flag = calculate_consensus(votes)
    print(f"Consensus: {consensus}")
    print(f"Agreement: {agreement}")
    print(f"Flag: {flag}")
