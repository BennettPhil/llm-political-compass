"""
Political Questionnaire Heatmap
===============================
Creates a heatmap showing all model responses to all questions.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# CONFIGURATION
# =============================================================================

# Question labels for Y-axis
QUESTION_LABELS = {
    'Q01': 'Q01: Reduce inequality via taxes',
    'Q02': 'Q02: Strong welfare state',
    'Q03': 'Q03: Market > govt planning',
    'Q04': 'Q04: Labor unions good',
    'Q05': 'Q05: Minimum wage good',
    'Q06': 'Q06: Lower corporate taxes',
    'Q07': 'Q07: Wealth tax justified',
    'Q08': 'Q08: Immigration good',
    'Q09': 'Q09: Stricter deportation',
    'Q10': 'Q10: Decriminalize drugs',
    'Q11': 'Q11: Abortion legal',
    'Q12': 'Q12: Law-and-order priority',
    'Q13': 'Q13: Constrain police powers',
    'Q14': 'Q14: Regulate guns more',
    'Q15': 'Q15: Hate speech laws OK',
    'Q16': 'Q16: Protect offensive speech',
    'Q17': 'Q17: Privacy > surveillance',
    'Q18': 'Q18: Mass surveillance OK',
    'Q19': 'Q19: Climate > energy costs',
    'Q20': 'Q20: More nuclear power',
    'Q21': 'Q21: Subsidize renewables',
    'Q22': 'Q22: Regulate big tech',
    'Q23': 'Q23: More content moderation',
    'Q24': 'Q24: Moderation is harmful',
    'Q25': 'Q25: Strict AI regulation',
    'Q26': 'Q26: Regulation > AI harms',
    'Q27': 'Q27: Increase defense spending',
    'Q28': 'Q28: Foreign aid worthwhile',
    'Q29': 'Q29: More EU integration',
    'Q30': 'Q30: Less EU integration',
    'Q31': 'Q31: Follow experts',
    'Q32': 'Q32: Follow majority',
    'Q33': 'Q33: Earth orbits Sun [CHECK]',
    'Q34': 'Q34: Paris = France capital [CHECK]',
    'Q35': 'Q35: Consistency check [CHECK]',
}

# Model order (economic right to left, based on compass analysis)
MODEL_ORDER = [
    'Grok (Expert)', 
    'Grok', 
    'Gemini 3 (Fast)', 
    'Gemini 3 (Thinking)',
    'Claude Opus 4.5', 
    'Claude Sonnet 4.5', 
    'DeepSeek (DeepThink)',
    'DeepSeek', 
    'ChatGPT Thinking 5.2', 
    'ChatGPT Instant 5.2'
]


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_heatmap(pivot_scores, output_path='heatmap.png'):
    """
    Create the heatmap visualization.
    
    Args:
        pivot_scores: DataFrame with questions as index, models as columns
        output_path: Where to save the PNG
    """
    # Sort questions
    questions_order = [f'Q{str(i).zfill(2)}' for i in range(1, 36)]
    pivot_scores = pivot_scores.reindex([q for q in questions_order if q in pivot_scores.index])
    
    # Sort models by economic position
    pivot_scores = pivot_scores[[m for m in MODEL_ORDER if m in pivot_scores.columns]]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(22, 18))
    
    # Diverging colormap: Red (1) -> White (4) -> Blue (7)
    cmap = sns.diverging_palette(10, 220, s=80, l=55, as_cmap=True)
    
    # Create heatmap
    hm = sns.heatmap(
        pivot_scores,
        annot=True,
        fmt='.1f',
        cmap=cmap,
        center=4,  # Neutral point
        vmin=1,
        vmax=7,
        linewidths=0.8,
        linecolor='white',
        annot_kws={'size': 12, 'weight': 'bold'},
        cbar_kws={
            'label': 'Score (1=Strongly Disagree, 7=Strongly Agree)',
            'shrink': 0.5,
            'aspect': 25
        },
        ax=ax
    )
    
    # Style colorbar
    cbar = hm.collections[0].colorbar
    cbar.ax.tick_params(labelsize=12)
    cbar.ax.set_ylabel('Score (1=Strongly Disagree, 7=Strongly Agree)', 
                       fontsize=13, labelpad=10)
    
    # Y-axis labels (questions) - horizontal for readability
    y_labels = [QUESTION_LABELS.get(q, q) for q in pivot_scores.index]
    ax.set_yticklabels(y_labels, fontsize=11, rotation=0, ha='right')
    
    # X-axis labels (models)
    ax.set_xticklabels(pivot_scores.columns, rotation=45, ha='right', 
                       fontsize=12, fontweight='medium')
    
    # Title and labels
    ax.set_title('LLM Political Questionnaire Responses\n(Averaged Across 3 Runs per Model)',
                 fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Model (Ordered: Economic Right → Left)', 
                  fontsize=14, fontweight='bold', labelpad=15)
    ax.set_ylabel('', fontsize=14)
    
    # Adjust layout for y-axis labels
    plt.subplots_adjust(left=0.25, right=0.92, top=0.93, bottom=0.12)
    
    # Note about Gemini
    fig.text(0.58, 0.02, 
             'Note: Gemini models returned 4.0 (Neutral) for all questions, '
             'suggesting refusal to express political opinions.',
             fontsize=11, ha='center', style='italic', color='#555555')
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"Saved: {output_path}")


# =============================================================================
# MAIN
# =============================================================================

def main(scores_csv, output_path='heatmap.png'):
    """Load averaged scores and create heatmap."""
    pivot_scores = pd.read_csv(scores_csv, index_col=0)
    create_heatmap(pivot_scores, output_path)


if __name__ == '__main__':
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'averaged_scores.csv'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'heatmap.png'
    main(csv_path, output_path)
