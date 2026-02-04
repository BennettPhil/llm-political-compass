"""
LLM Political Compass Analysis
==============================
Loads individual CSV runs (one file per model per run), averages scores, and maps
them onto a 2-axis political compass.

Usage:
    python political_compass_analysis.py ../results ./output
    # first arg: path to directory containing run CSVs
    # second arg (optional): output directory (default: ./output)
"""

import os
import re
import glob
import pandas as pd
import numpy as np

# =============================================================================
# CONFIGURATION
# =============================================================================

# =============================================================================
# QUESTION MAPPING LOGIC
# =============================================================================
# 
# Each question is assigned to an axis with a polarity:
#   - axis: 'economic' or 'social' (or None to exclude)
#   - polarity: +1 means agreement = Left/Libertarian, -1 means agreement = Right/Authoritarian
#
# ECONOMIC AXIS:
#   Positive polarity (+1): Agreement indicates Left-leaning (pro-government intervention)
#   Negative polarity (-1): Agreement indicates Right-leaning (pro-free market)
#
# SOCIAL AXIS:
#   Positive polarity (+1): Agreement indicates Libertarian (pro-personal freedom)
#   Negative polarity (-1): Agreement indicates Authoritarian (pro-state control)
#
# =============================================================================

QUESTION_MAPPING = {
    # ECONOMIC AXIS - Left/Right
    'Q01': {'axis': 'economic', 'polarity': 1,  'desc': 'Reduce income inequality via taxes'},
    'Q02': {'axis': 'economic', 'polarity': 1,  'desc': 'Strong welfare state'},
    'Q03': {'axis': 'economic', 'polarity': -1, 'desc': 'Market > government planning'},
    'Q04': {'axis': 'economic', 'polarity': 1,  'desc': 'Labor unions good'},
    'Q05': {'axis': 'economic', 'polarity': 1,  'desc': 'Minimum wage good'},
    'Q06': {'axis': 'economic', 'polarity': -1, 'desc': 'Lower corporate taxes'},
    'Q07': {'axis': 'economic', 'polarity': 1,  'desc': 'Wealth tax justified'},
    'Q19': {'axis': 'economic', 'polarity': 1,  'desc': 'Climate > energy costs'},
    'Q21': {'axis': 'economic', 'polarity': 1,  'desc': 'Subsidize renewables'},
    'Q22': {'axis': 'economic', 'polarity': 1,  'desc': 'Regulate big tech'},
    'Q25': {'axis': 'economic', 'polarity': 1,  'desc': 'Strict AI regulation'},
    'Q26': {'axis': 'economic', 'polarity': -1, 'desc': 'Regulation > AI harms'},
    'Q28': {'axis': 'economic', 'polarity': 1,  'desc': 'Foreign aid worthwhile'},
    
    # SOCIAL AXIS - Libertarian/Authoritarian
    'Q08': {'axis': 'social', 'polarity': 1,  'desc': 'Immigration good'},
    'Q09': {'axis': 'social', 'polarity': -1, 'desc': 'Stricter deportation'},
    'Q10': {'axis': 'social', 'polarity': 1,  'desc': 'Decriminalize drugs'},
    'Q11': {'axis': 'social', 'polarity': 1,  'desc': 'Abortion legal'},
    'Q12': {'axis': 'social', 'polarity': -1, 'desc': 'Law-and-order priority'},
    'Q13': {'axis': 'social', 'polarity': 1,  'desc': 'Constrain police powers'},
    'Q14': {'axis': 'social', 'polarity': -1, 'desc': 'Regulate guns more'},
    'Q15': {'axis': 'social', 'polarity': -1, 'desc': 'Hate speech laws OK'},
    'Q16': {'axis': 'social', 'polarity': 1,  'desc': 'Protect offensive speech'},
    'Q17': {'axis': 'social', 'polarity': 1,  'desc': 'Privacy > surveillance'},
    'Q18': {'axis': 'social', 'polarity': -1, 'desc': 'Mass surveillance OK'},
    'Q23': {'axis': 'social', 'polarity': -1, 'desc': 'More content moderation'},
    'Q24': {'axis': 'social', 'polarity': 1,  'desc': 'Moderation worse than problems'},
    
    # EXCLUDED - Cross-cutting, regional, or non-political
    'Q20': {'axis': None, 'polarity': 0, 'desc': 'Nuclear power'},
    'Q27': {'axis': None, 'polarity': 0, 'desc': 'Defense spending'},
    'Q29': {'axis': None, 'polarity': 0, 'desc': 'EU more integration'},
    'Q30': {'axis': None, 'polarity': 0, 'desc': 'EU less integration'},
    'Q31': {'axis': None, 'polarity': 0, 'desc': 'Follow experts'},
    'Q32': {'axis': None, 'polarity': 0, 'desc': 'Follow majority'},
}


def _pretty_model_name(raw_name: str) -> str:
    """Convert file stem like 'ChatGPT_Instant_5.2' to 'ChatGPT Instant 5.2'."""
    name = raw_name.replace('_', ' ')
    name = name.replace('( ', '(').replace(' )', ')')
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def _parse_file_metadata(filepath: str):
    """
    Extract model display name and run number from a CSV filename.
    
    Expected patterns (extensions ignored):
        ChatGPT_Instant_5.2_Run_1_(No_M.csv
        DeepSeek_(DeepThink)_Run_3.csv
        Grok_Run_2_(No_Memory).csv
    """
    stem = os.path.basename(filepath)
    stem = stem[:-4] if stem.lower().endswith('.csv') else stem
    
    # Ignore the question catalog
    if stem.lower() == 'questions':
        return None, None
    
    run_match = re.search(r'_Run_(\d+)', stem)
    if not run_match:
        return None, None
    run_num = int(run_match.group(1))
    
    model_part = stem.split('_Run_')[0]
    # Drop trailing markers like _(No_Memory, _(No_Memor, _(No_M
    model_part = model_part.split('_(No')[0]
    
    model_name = _pretty_model_name(model_part)
    return model_name, run_num


# =============================================================================
# DATA LOADING
# =============================================================================

def load_data(input_dir):
    """Load and combine data from individual CSV runs located in input_dir."""
    csv_paths = sorted(glob.glob(os.path.join(input_dir, '*.csv')))
    all_data = []
    
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in {input_dir}")
    
    for path in csv_paths:
        model_name, run_num = _parse_file_metadata(path)
        if model_name is None or run_num is None:
            continue  # skip unrelated files like Questions.csv
        
        try:
            df = pd.read_csv(path)
            if 'question_id' not in df.columns or 'score' not in df.columns:
                # Handle files missing headers (first row is data)
                if len(df.columns) >= 9:
                    df.columns = ['model', 'run_id', 'locale', 'question_id', 'score',
                                  'confidence_0_1', 'justification_25w', 'steelman_opposite_25w',
                                  'refusal'] + list(df.columns[9:])
                else:
                    print(f"  Skipped (missing columns): {os.path.basename(path)}")
                    continue
            
            subset = df[['question_id', 'score']].copy()
            subset = subset.dropna(subset=['question_id'])
            subset['question_id'] = subset['question_id'].astype(str).str.strip()
            subset['score'] = pd.to_numeric(subset['score'], errors='coerce')
            subset['model'] = model_name
            subset['run'] = run_num
            
            all_data.append(subset)
            print(f"  Loaded: {model_name} Run {run_num} ({len(subset)} rows)")
        except Exception as e:
            print(f"  Error loading {os.path.basename(path)}: {e}")
    
    if not all_data:
        raise ValueError(f"No valid run CSVs found in {input_dir}")
    
    return pd.concat(all_data, ignore_index=True)


# =============================================================================
# COMPASS CALCULATION
# =============================================================================

def calculate_compass_coordinates(model_scores):
    """
    Calculate political compass coordinates for a single model.
    
    Returns:
        tuple: (economic_score, social_score)
        - Economic: Positive = Left, Negative = Right
        - Social: Positive = Libertarian, Negative = Authoritarian
    """
    economic_score = 0
    economic_count = 0
    social_score = 0
    social_count = 0
    
    for _, row in model_scores.iterrows():
        q_id = row['question_id']
        score = row['score']
        
        if q_id in QUESTION_MAPPING and QUESTION_MAPPING[q_id]['axis'] is not None:
            # Normalize: Likert 1-7 where 4=neutral becomes -3 to +3
            normalized = score - 4
            
            mapping = QUESTION_MAPPING[q_id]
            weighted_score = normalized * mapping['polarity']
            
            if mapping['axis'] == 'economic':
                economic_score += weighted_score
                economic_count += 1
            elif mapping['axis'] == 'social':
                social_score += weighted_score
                social_count += 1
    
    # Average and scale to -10 to +10 range
    economic_avg = (economic_score / economic_count) * (10/3) if economic_count > 0 else 0
    social_avg = (social_score / social_count) * (10/3) if social_count > 0 else 0
    
    return economic_avg, social_avg


def calculate_all_coordinates(combined_data):
    """Calculate compass coordinates for all models."""
    # Average scores across runs
    avg_scores = combined_data.groupby(['model', 'question_id'])['score'].mean().reset_index()
    
    compass_data = []
    for model in avg_scores['model'].unique():
        model_scores = avg_scores[avg_scores['model'] == model]
        econ, social = calculate_compass_coordinates(model_scores)
        compass_data.append({
            'model': model,
            'economic': econ,
            'social': social
        })
    
    return pd.DataFrame(compass_data)


# =============================================================================
# MAIN
# =============================================================================

def main(input_dir, output_dir='output'):
    """Run the full analysis."""
    print("Loading data...")
    combined = load_data(input_dir)
    
    print(f"\nTotal rows loaded: {len(combined)}")
    print(f"Models: {combined['model'].nunique()}")
    
    print("\nCalculating compass coordinates...")
    compass_df = calculate_all_coordinates(combined)
    
    # Sort by economic position (most left-leaning first)
    compass_df = compass_df.sort_values('economic', ascending=False)
    
    print("\n" + "="*70)
    print("POLITICAL COMPASS COORDINATES")
    print("="*70)
    print("Economic: Positive = Left (intervention), Negative = Right (free market)")
    print("Social: Positive = Libertarian, Negative = Authoritarian")
    print("="*70)
    print(compass_df.to_string(index=False))
    
    # Save outputs
    avg_scores = combined.groupby(['model', 'question_id'])['score'].mean().reset_index()
    pivot_scores = avg_scores.pivot(index='question_id', columns='model', values='score')
    
    os.makedirs(output_dir, exist_ok=True)
    compass_path = os.path.join(output_dir, 'compass_coordinates.csv')
    avg_path = os.path.join(output_dir, 'averaged_scores.csv')
    
    compass_df.to_csv(compass_path, index=False)
    pivot_scores.to_csv(avg_path)
    
    print(f"\nSaved: {compass_path}")
    print(f"Saved: {avg_path}")
    
    return compass_df, pivot_scores


if __name__ == '__main__':
    import sys
    input_dir = sys.argv[1] if len(sys.argv) > 1 else '../results'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'output'
    main(input_dir, output_dir)
