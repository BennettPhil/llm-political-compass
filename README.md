# LLM Political Questionnaire Benchmark
Compare how modern LLMs answer a 35-question political Likert survey and where they land on a two-axis (Economic ↔ Social) political compass. This repo includes raw responses, scoring logic, and plotting scripts you can reuse for your own write-up or replication.

## What’s Inside
- `results/*.csv` – raw model outputs (3 runs each) plus `Questions.csv` with the exact prompts. Columns follow `model, run_id, locale, question_id, score, confidence_0_1, justification_25w, steelman_opposite_25w, refusal, notes`.
- `prompt.md` – the instruction prompt shown to every model.
- `methodology.md` – scoring rules, axis mapping, exclusions, and headline findings.
- `visualisation/` – Python scripts to aggregate results, compute compass coordinates, and draw charts (compass plot + heatmap). See `visualisation/README.md` for details.

## Quickstart (reproduce the charts)
1) Install deps: `pip install pandas numpy matplotlib seaborn openpyxl`
2) Run analysis directly on the CSVs (no Excel step needed):
```bash
cd visualisation
python political_compass_analysis.py ../results ./output
python create_compass_chart.py output/compass_coordinates.csv output/political_compass.png
python create_heatmap.py output/averaged_scores.csv output/heatmap.png
```
Outputs land in `visualisation/output/` by default (folder is created if missing).

## Methodology at a Glance
- 10 model configs, 3 runs each; scores averaged before plotting.
- Economic axis: agreement with regulation/redistribution → Left; free-market items → Right.
- Social axis: agreement with individual-freedom items → Libertarian; state-control items → Authoritarian.
- Questions without a clean axis fit (e.g., nuclear power, EU integration, factual checks) are excluded from scoring. Full mapping lives in `methodology.md` and `visualisation/political_compass_analysis.py`.

## Headline Findings (from the included analysis)
- Most models lean economically Left and socially Libertarian; Grok (Expert) is the main Libertarian-Right outlier.
- Gemini 3 (Fast/Thinking) returned neutral 4.0 on every item, effectively refusing to take positions.
- Strong agreement across models: climate mitigation priority, larger role for nuclear, and decriminalizing personal-use drugs.
- High disagreement: gun regulation, wealth tax size, and EU integration.

## How to Use in a Blog Post
- Embed `political_compass.png` and `heatmap.png` as visuals; cite `methodology.md` for scoring logic.
- Link to `prompt.md` so readers can inspect the exact wording and output constraints.
- If you rerun with new models, drop new CSVs into `results/`, regenerate the Excel workbook, and rerun the analysis pipeline.
