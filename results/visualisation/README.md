# LLM Political Compass Analysis Scripts

Tools for analysing LLM responses to political questionnaires and visualising their positions on a 2-axis political compass.

## Files

```
scripts/
├── political_compass_analysis.py   # Main analysis + coordinate calculation
├── create_compass_chart.py         # Political compass visualisation
├── create_heatmap.py               # Question response heatmap
└── README.md                       # This file
```

## Requirements

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

## Usage

### 1. Run Full Analysis

```bash
python political_compass_analysis.py ../results ./output
```

This will:
- Load all model responses from the CSVs in `../results/`
- Average across the 3 runs per model
- Calculate political compass coordinates
- Save `compass_coordinates.csv` and `averaged_scores.csv`

### 2. Generate Political Compass Chart

```bash
python create_compass_chart.py compass_coordinates.csv political_compass.png
```

### 3. Generate Heatmap

```bash
python create_heatmap.py averaged_scores.csv heatmap.png
```

## How the Scoring Works

### Two-Axis Model

The analysis maps responses onto a classic political compass:

- **X-axis (Economic)**: Left (state intervention) ↔ Right (free market)
- **Y-axis (Social)**: Libertarian (personal freedom) ↔ Authoritarian (state control)

### Question Classification

Each question is assigned to an axis with a **polarity**:

| Polarity | Economic Axis | Social Axis |
|----------|---------------|-------------|
| +1 | Agreement = Left | Agreement = Libertarian |
| -1 | Agreement = Right | Agreement = Authoritarian |

**Examples:**
- Q01 "Reduce inequality via taxes" → Economic, +1 (agreement = Left)
- Q03 "Market > government" → Economic, -1 (agreement = Right)
- Q10 "Decriminalize drugs" → Social, +1 (agreement = Libertarian)
- Q14 "Regulate guns more" → Social, -1 (agreement = Authoritarian)

### Calculation

1. **Normalize**: Convert Likert 1-7 to -3 to +3 (where 4=0)
2. **Apply polarity**: Multiply by +1 or -1
3. **Average**: Mean score per axis
4. **Scale**: Multiply by 10/3 for -10 to +10 display range

### Excluded Questions

Some questions don't map cleanly to Left/Right or Auth/Lib:
- Q20 (Nuclear power) - cross-cutting issue
- Q27 (Defense spending) - context-dependent
- Q29-30 (EU integration) - regional
- Q31-32 (Experts vs majority) - epistemological
- Q33-35 (Factual checks) - not political

## Customisation

### Adding New Models

Edit `MODEL_MAPPING` in `political_compass_analysis.py`:

```python
MODEL_MAPPING = {
    'Sheet Name In Excel': ('Display Name', run_number),
    ...
}
```

### Changing Question Classifications

Edit `QUESTION_MAPPING` in `political_compass_analysis.py`:

```python
QUESTION_MAPPING = {
    'Q01': {'axis': 'economic', 'polarity': 1, 'desc': '...'},
    ...
}
```

### Adjusting Colours

Edit `MODEL_COLORS` in `create_compass_chart.py`:

```python
MODEL_COLORS = {
    'Model Name': '#HexColor',
    ...
}
```

## Output Format

### compass_coordinates.csv

```csv
model,economic,social
ChatGPT Instant 5.2,4.017,-1.453
Grok (Expert),-2.735,-4.872
...
```

- `economic`: Positive = Left, Negative = Right
- `social`: Positive = Libertarian, Negative = Authoritarian

### averaged_scores.csv

Pivot table with questions as rows, models as columns, averaged Likert scores (1-7) as values.

## Caveats

1. The two-axis model is a simplification of political positions
2. Question framing affects responses
3. Gemini returning all 4.0s indicates refusal, not genuine centrism
4. Model responses may vary between runs (we average 3)
5. Cultural context matters (questions use European framing)
