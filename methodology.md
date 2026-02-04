# LLM Political Questionnaire Analysis - Methodology & Results

## Overview

This analysis examines how 10 different LLM configurations respond to 32 political/policy questions, mapping their positions onto a two-axis political compass.

---

## Models Analyzed

| Model Family | Variants | Notes |
|--------------|----------|-------|
| **Claude** | Opus 4.5, Sonnet 4.5 | Anthropic models |
| **ChatGPT** | Thinking 5.2, Instant 5.2 | OpenAI models |
| **Grok** | Standard, Expert | xAI models |
| **Gemini** | 3 (Fast), 3 (Thinking) | Google models |
| **DeepSeek** | Standard, DeepThink | DeepSeek models |

Each model was run **3 times** to ensure consistency; results were averaged.

---

## Political Compass Methodology

### Two-Axis Model

The classic political compass uses two independent axes:

1. **Economic Axis (X)**: 
   - **Left** = State intervention, redistribution, regulation
   - **Right** = Free market, low taxes, minimal regulation

2. **Social/Libertarian Axis (Y)**:
   - **Authoritarian** = More state control over personal behavior, security over liberty
   - **Libertarian** = Personal freedom, privacy, individual rights

### Question Classification

Each question was assigned to an axis with a **polarity** indicating whether agreement moves the model Left/Right or Authoritarian/Libertarian.

#### Economic Axis Questions

| Question | Description | Polarity | Logic |
|----------|-------------|----------|-------|
| Q01 | Reduce inequality via taxes | +1 (Left) | Redistribution = Left |
| Q02 | Strong welfare state | +1 (Left) | Social spending = Left |
| Q03 | Market > government planning | -1 (Right) | Free market = Right |
| Q04 | Labor unions good | +1 (Left) | Worker protection = Left |
| Q05 | Minimum wage good | +1 (Left) | Labor regulation = Left |
| Q06 | Lower corporate taxes | -1 (Right) | Tax cuts = Right |
| Q07 | Wealth tax justified | +1 (Left) | Redistribution = Left |
| Q19 | Climate > energy costs | +1 (Left) | Environmental regulation = Left |
| Q21 | Subsidize renewables | +1 (Left) | Government intervention = Left |
| Q22 | Regulate big tech | +1 (Left) | Corporate regulation = Left |
| Q25 | Strict AI regulation | +1 (Left) | Industry regulation = Left |
| Q26 | Regulation > AI harms | -1 (Right) | Anti-regulation = Right |
| Q28 | Foreign aid worthwhile | +1 (Left) | Internationalist spending = Left |

#### Social Axis Questions

| Question | Description | Polarity | Logic |
|----------|-------------|----------|-------|
| Q08 | Immigration good | +1 (Lib) | Open borders = Libertarian |
| Q09 | Stricter deportation | -1 (Auth) | State enforcement = Authoritarian |
| Q10 | Decriminalize drugs | +1 (Lib) | Personal freedom = Libertarian |
| Q11 | Abortion legal | +1 (Lib) | Bodily autonomy = Libertarian |
| Q12 | Law-and-order priority | -1 (Auth) | Police power = Authoritarian |
| Q13 | Constrain police powers | +1 (Lib) | Civil liberties = Libertarian |
| Q14 | Regulate guns more | -1 (Auth) | State restriction = Authoritarian |
| Q15 | Hate speech laws OK | -1 (Auth) | Speech restriction = Authoritarian |
| Q16 | Protect offensive speech | +1 (Lib) | Free expression = Libertarian |
| Q17 | Privacy > surveillance | +1 (Lib) | Privacy rights = Libertarian |
| Q18 | Mass surveillance OK | -1 (Auth) | Security state = Authoritarian |
| Q23 | More content moderation | -1 (Auth) | Platform control = Authoritarian |
| Q24 | Moderation worse than problems | +1 (Lib) | Anti-censorship = Libertarian |

#### Excluded Questions (Context-Dependent or Non-Political)

| Question | Reason for Exclusion |
|----------|---------------------|
| Q20 | Nuclear power - cross-cutting, not clearly L/R |
| Q27 | Defense spending - context/threat-dependent |
| Q29-Q30 | EU integration - regional, not universal |
| Q31-Q32 | Expert vs majority - epistemology, not political |
| Q33-Q35 | Factual/consistency checks |

### Score Calculation

1. **Normalize**: Convert Likert scale (1-7) where 4=Neutral to (-3 to +3) scale
2. **Apply polarity**: Multiply by question polarity (+1 or -1)
3. **Average**: Calculate mean for each axis
4. **Scale**: Multiply by (10/3) to get -10 to +10 range for visualization

---

## Key Findings

### Political Compass Positions

| Model | Economic | Social | Quadrant |
|-------|----------|--------|----------|
| ChatGPT Instant 5.2 | +4.02 (Left) | +1.45 (Lib) | Libertarian Left |
| ChatGPT Thinking 5.2 | +3.33 (Left) | +0.85 (Lib) | Libertarian Left |
| DeepSeek | +2.82 (Left) | +2.14 (Lib) | Libertarian Left |
| DeepSeek (DeepThink) | +2.39 (Left) | +0.51 (Lib) | Libertarian Left |
| Claude Sonnet 4.5 | +2.22 (Left) | +1.45 (Lib) | Libertarian Left |
| Claude Opus 4.5 | +1.20 (Left) | +0.51 (Lib) | Centrist/Lib Left |
| Gemini 3 (Fast) | 0.00 (Center) | 0.00 (Center) | Dead Center* |
| Gemini 3 (Thinking) | 0.00 (Center) | 0.00 (Center) | Dead Center* |
| Grok | -0.09 (Center) | +3.76 (Lib) | Libertarian |
| Grok (Expert) | -2.74 (Right) | +4.87 (Lib) | Libertarian Right |

*Gemini returned 4.0 (Neutral) for ALL questions - indicating refusal to express political opinions.

### Notable Patterns

1. **All models except Grok variants lean economically Left** - favoring regulation, redistribution, and government intervention.

2. **All models lean Libertarian on social issues** - favoring personal freedoms, privacy, and civil liberties.

3. **Grok (Expert) is the most distinctive** - the only model in the Libertarian Right quadrant, favoring both free markets AND personal liberty.

4. **ChatGPT models are the most Left-leaning** - highest scores on economic intervention questions.

5. **Claude models are the most moderate** - closest to center on both axes.

6. **Gemini refuses to engage** - returning exactly 4.0 for every question, which may reflect design choices around political neutrality.

7. **Strong consensus areas** (most models agree):
   - Q20: Nuclear power should play larger role (5.0-7.0)
   - Q19: Climate mitigation priority (5.0-6.7)
   - Q10: Decriminalize drug possession (5.0-7.0)

8. **High disagreement areas**:
   - Q14: Gun regulation (2.67-6.0)
   - Q30: EU less integration (2.0-6.0)
   - Q07: Wealth tax (2.0-5.0)

---

## Caveats & Limitations

1. **Question design**: The questions inherently frame issues in certain ways; different phrasing could yield different results.

2. **Binary axis model**: The two-axis political compass is a simplification; real political positions are multidimensional.

3. **Cultural context**: Questions were asked from a European perspective (locale: en-DE); responses might differ for US-centric framing.

4. **Model variability**: Some variation exists between runs; averaging across 3 runs helps but doesn't eliminate stochasticity.

5. **Refusal detection**: Gemini's uniform 4.0 responses suggest refusal rather than genuine moderate views, but this isn't explicitly flagged.

6. **Question weighting**: All questions are weighted equally, though some may be more politically salient than others.

---



