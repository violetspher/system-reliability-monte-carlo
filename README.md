# System Reliability Monte Carlo

Graduate coursework scripts in reliability engineering and systems modeling.

## Overview

`monte_carlo_availability.py` evaluates steady-state operational availability $A_o$ for a multi-stage series-parallel system with independent active-redundant subsystems:

- **Exact analytical model** using component $A_o = \mathrm{MTBF} / (\mathrm{MTBF} + \mathrm{MTTR})$
- **Alternating-renewal Monte Carlo simulation** over exponential up/down cycles with 95% confidence interval reporting

## Run

```bash
python monte_carlo_availability.py
```

Example output:

```text
Analytical series-parallel Ao : 0.995492
Monte Carlo mean Ao (400 runs): 0.995487 (95% CI: [0.995224, 0.995750])
```
