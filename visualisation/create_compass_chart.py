"""
Political Compass Visualization
===============================
Creates a 2-axis political compass plot from LLM survey results.
"""

import pandas as pd
import matplotlib.pyplot as plt


# =============================================================================
# CONFIGURATION
# =============================================================================

MODEL_COLORS = {
    'Claude Opus 4.5': '#8B4513',
    'Claude Sonnet 4.5': '#D2691E',
    'ChatGPT Thinking 5.2': '#228B22',
    'ChatGPT Instant 5.2': '#32CD32',
    'Grok': '#4169E1',
    'Grok (Expert)': '#1E90FF',
    'Gemini 3 (Fast)': '#FF6347',
    'Gemini 3 (Thinking)': '#FF4500',
    'DeepSeek': '#9932CC',
    'DeepSeek (DeepThink)': '#BA55D3',
}


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_political_compass(compass_df, output_path='political_compass.png'):
    """
    Create the political compass visualization.
    
    Args:
        compass_df: DataFrame with columns ['model', 'economic', 'social']
        output_path: Where to save the PNG
    """
    fig, ax = plt.subplots(figsize=(16, 14))
    
    # Draw axes
    ax.axhline(y=0, color='black', linewidth=2, zorder=1)
    ax.axvline(x=0, color='black', linewidth=2, zorder=1)
    
    # Shade quadrants
    ax.fill_between([-10, 0], [0, 0], [10, 10], alpha=0.15, color='red')    # Auth Left
    ax.fill_between([0, 10], [0, 0], [10, 10], alpha=0.15, color='blue')   # Auth Right
    ax.fill_between([-10, 0], [-10, -10], [0, 0], alpha=0.15, color='green')  # Lib Left
    ax.fill_between([0, 10], [-10, -10], [0, 0], alpha=0.15, color='purple')  # Lib Right
    
    # Quadrant labels
    ax.text(-7, 8, 'Authoritarian\nLeft', fontsize=16, ha='center', va='center', 
            alpha=0.4, fontweight='bold')
    ax.text(7, 8, 'Authoritarian\nRight', fontsize=16, ha='center', va='center', 
            alpha=0.4, fontweight='bold')
    ax.text(-7, -8, 'Libertarian\nLeft', fontsize=16, ha='center', va='center', 
            alpha=0.4, fontweight='bold')
    ax.text(7, -8, 'Libertarian\nRight', fontsize=16, ha='center', va='center', 
            alpha=0.4, fontweight='bold')
    
    # Plot each model
    for _, row in compass_df.iterrows():
        model = row['model']
        # Flip signs for traditional compass orientation:
        # - Left on left side (negative x)
        # - Authoritarian on top (positive y)
        x = -row['economic']
        y = -row['social']
        
        color = MODEL_COLORS.get(model, 'gray')
        ax.scatter(x, y, s=400, c=color, edgecolors='black', linewidth=2, 
                   zorder=5, label=model)
    
    # Legend
    ax.legend(loc='upper left', fontsize=12, framealpha=0.95,
              title='Models', title_fontsize=14, bbox_to_anchor=(0.02, 0.98))
    
    # Labels
    ax.set_xlabel('← Economic Left                    Economic Right →', 
                  fontsize=16, fontweight='bold', labelpad=15)
    ax.set_ylabel('← Libertarian                    Authoritarian →', 
                  fontsize=16, fontweight='bold', labelpad=15)
    ax.set_title('LLM Political Compass\nBased on Policy Question Responses (Averaged Across 3 Runs)',
                 fontsize=20, fontweight='bold', pad=20)
    
    # Axis setup
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xticks(range(-10, 11, 2))
    ax.set_yticks(range(-10, 11, 2))
    ax.tick_params(axis='both', labelsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"Saved: {output_path}")


# =============================================================================
# MAIN
# =============================================================================

def main(coordinates_csv, output_path='political_compass.png'):
    """Load coordinates and create visualization."""
    compass_df = pd.read_csv(coordinates_csv)
    create_political_compass(compass_df, output_path)


if __name__ == '__main__':
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'compass_coordinates.csv'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'political_compass.png'
    main(csv_path, output_path)
