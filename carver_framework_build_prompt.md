# Build Prompt — Systematic Trading Framework (Carver, *Systematic Trading*, Part Three)

> **You are a coding agent.** This document is your complete specification. Build a modular,
> back-testable, production-grade implementation of the position-sizing framework described in
> Part Three (Chapters 5–12) and Appendices B–D of Rob Carver's *Systematic Trading*.
> Follow the interface contracts exactly. Every formula below is the source of truth; do not
> "improve" the maths. When a value in the book is stated, your code must reproduce it to the
> tolerances in the golden tests (§9). If you find an ambiguity, resolve it in favour of the
> book's worked examples and leave a `# SPEC-NOTE:` comment.

---

## 0. Mission & mental model

The framework is a **pipeline of independent modules** wrapped around a set of trading rules. It
converts market data into correctly-risk-sized trades. The engine (trading rules) is swappable;
the risk plumbing around it is fixed and must be *boringly correct*.

```
prices/data ─▶ [Rule forecasts] ─▶ [Combine forecasts] ─▶ [Volatility target]
                                                                │
              [Trades] ◀─ [Portfolio positions] ◀─ [Subsystem position sizing] ◀─┘
```

Three supported "trader personas" flow through the **same** pipeline, differing only in the
forecast stage:

| Persona | Forecast source | Notes |
|---|---|---|
| **Staunch systems trader** | Systematic rules (EWMAC, Carry, …), combined | Full pipeline |
| **Asset-allocating investor** | Constant `+10` "no-rule" rule for every instrument | No combining; instrument correlations used *unadjusted* |
| **Semi-automatic trader** | Discretionary forecast in `[-20, +20]` + systematic stop-loss exit | Equal instrument weights; special IDM |

**Design invariant (the "interface contract"):** a forecast of `+10` always means "average-strength
long," a forecast of `+20` the strongest allowed, regardless of instrument, rule, or persona. Every
module downstream relies on this. Preserve it everywhere.

---

## 1. Scope

**In scope (build this):** the full Part Three calculation chain — instruments → forecasts →
combined forecast → volatility target → subsystem position → portfolio position → trades — plus the
cost/turnover ("Speed and Size") tooling, the EWMAC and Carry rules, the volatility estimators, the
diversification multipliers, and handcrafted weighting.

**Out of scope (do NOT build unless asked):** live broker order routing, an execution/HFT algo,
tax accounting, options/non-linear derivatives, a data-vendor integration beyond a thin adapter,
and any auto-trading loop that places real orders without a human gate. Build the *decision engine*;
stop at "here are the trades to do."

**Not financial advice.** This is research/decision-support software. Ship it defaulting to
`--dry-run` and paper trading. See §10.

---

## 2. Architecture & engineering principles

1. **Modular with well-defined interfaces.** Each stage is a pure function / small class with typed
   inputs and outputs. A new trading rule must plug in without touching any other module.
2. **Everything is volatility-standardised.** Positions, forecasts, and costs are all expressed in
   risk-adjusted terms. This is what lets one rule work across all instruments.
3. **No look-ahead.** Every estimate at time *t* uses data available at *t* only. Volatility, EWMAs,
   and (if you back-test weights) correlations must be causal. Unit-test for leakage.
4. **Deterministic & reproducible.** Same inputs + config ⇒ identical outputs. Seed any randomness
   (bootstrap). Pin dependencies.
5. **No premature rounding.** Carry full float precision through the whole chain. Round **once**, at
   the `rounded_target_position` step (§5.6), and nowhere else. This is explicit in the book.
6. **Config over code.** Look-back windows, forecast scalars, caps, targets, weights, and costs live
   in config, not literals. Ship the book's defaults as the shipped config.
7. **Observability.** Every stage emits its intermediate values (forecast, vol scalar, subsystem
   position, etc.) to a structured diagnostics record so a human can audit any single instrument on
   any day, matching the book's worked-example tables.

### Suggested stack & layout
- **Python 3.11+**, `pandas`/`numpy` for series maths, `pydantic` for config/DTO validation,
  `pytest` for tests, `typer` or `argparse` for CLI. (If the team standard differs, adapt — but keep
  the module boundaries.)
- Repo layout:
  ```
  systrading/
    core/
      instruments.py        # Instrument metadata, block value, FX
      volatility.py         # price volatility estimators (SMA / EWMA)
      forecasts/
        base.py             # TradingRule ABC + forecast scaling/capping
        ewmac.py
        carry.py
        norule.py           # constant +10
        discretionary.py    # semi-auto input adapter
      combine.py            # forecast weights + forecast diversification multiplier
      voltarget.py          # capital, % vol target, cash vol targets
      position.py           # volatility scalar, subsystem position
      portfolio.py          # instrument weights + IDM + portfolio position + trades
      costs.py              # standardised cost, turnover, speed limits, min-size checks
      diversification.py    # shared 1/sqrt(w H w^T) multiplier + table-18 approximation
      handcraft.py          # handcrafting weights (Table 8) + SR adjustment (Table 12)
    config/
      defaults.yaml         # book defaults (scalars, look-backs, caps, correlations)
    pipeline.py             # orchestrates one dated run for a portfolio
    backtest.py             # optional: run pipeline over history, compute turnover/costs
    cli.py
  tests/
    golden/                 # the §9 worked-example fixtures
    unit/
    property/
  ```

---

## 3. Data model (interface contracts)

Define typed DTOs. Currencies matter: track the **instrument currency** and the **account/base
currency** separately and convert explicitly — never implicitly.

```python
class Instrument(BaseModel):
    symbol: str
    asset_class: str                 # e.g. "bond", "equity", "fx", "commodity", "vol"
    currency: str                    # instrument currency, e.g. "USD"
    block_multiplier: float          # units per block: 1 share, 1000 bbl, £ per point, etc.
    # block_value at time t is DERIVED, not stored (see §5.4)
    min_block: float = 1.0           # minimum tradeable size
    tradeable_long_only: bool = False

class MarketSnapshot(BaseModel):     # per instrument, per date
    date: date
    price: float                     # quoted price of the block instrument
    price_history: pd.Series         # causal daily price series up to `date`
    fx_rate_instr_per_base: float    # instrument-ccy / base-ccy  (see §5.4 — direction is critical)
    extra: dict                      # carry inputs: dividend_yield, funding_cost, nearer_price, etc.

class Forecast(BaseModel):
    rule_id: str
    value: float                     # scaled to E|f|≈10, capped to [-20, 20] (or [0,20] long-only)

class SubsystemResult(BaseModel):
    symbol: str
    combined_forecast: float
    price_volatility: float          # daily %, as a *number of percent* (e.g. 1.33 means 1.33%)
    block_value: float               # instrument ccy, cash per +1% move of one block
    instrument_ccy_vol: float        # ICV, instrument ccy
    instrument_value_vol: float      # IVV, base ccy
    volatility_scalar: float
    subsystem_position: float        # blocks, fractional, UNROUNDED

class PortfolioResult(BaseModel):
    date: date
    per_instrument: dict[str, dict]  # subsystem_position, weight, idm, portfolio_position,
                                     # rounded_target, current_position, trade
```

> **Percent convention (read carefully).** The book expresses `price_volatility` as a *number of
> percent* (crude oil = `1.33`, not `0.0133`) and defines `block_value` as "cash per **+1%** move."
> Consequently `ICV = block_value × price_volatility` multiplies by `1.33`, **not** `0.0133`
> (`$750 × 1.33 = $997.50`). Pick this convention, encode it once in `volatility.py`, and assert it
> in tests. If you prefer decimals internally, then `block_value` must be "cash per +1.00 (=100%)
> move" — but do not mix conventions.

---

## 4. Configuration (ship the book's defaults)

`config/defaults.yaml`:

```yaml
forecast:
  target_abs_value: 10          # E|forecast|
  cap: 20                       # hard cap, symmetric
  ewmac:
    pairs: [[2,8],[4,16],[8,32],[16,64],[32,128],[64,256]]   # slow = 4 × fast
    forecast_scalars: {"2,8": 10.6, "4,16": 7.5, "8,32": 5.3,
                       "16,64": 3.75, "32,128": 2.65, "64,256": 1.87}
  carry:
    forecast_scalar: 30
    update_frequency: weekly
    turnover_rule_of_thumb: 10

volatility:
  method: ewma                  # "sma" or "ewma"
  sma_lookback_days: 25
  ewma_lookback_days: 36        # λ = 2/(1+36) = 0.054  (same half-life as 25-day SMA)
  business_days_per_year: 256
  annualisation_factor: 16      # sqrt(256)

diversification:
  max_multiplier: 2.5           # cap for BOTH FDM and IDM
  floor_correlations_at_zero: true
  subsystem_corr_scale_dynamic: 0.70   # applied to instrument-return correlations for dynamic traders
  subsystem_corr_scale_static: 1.00    # asset-allocating investor uses correlations unadjusted

voltarget:
  # percentage vol target is chosen by the human per §5.3 tables; this is a placeholder default.
  percentage_vol_target: 0.25

portfolio:
  position_inertia_pct: 0.10    # skip trade if |current-target| < 10% of rounded target

costs:
  speed_limit_sr:
    staunch: 0.13               # = (1/3) × 0.40 max pre-cost SR
    asset_allocator: 0.08       # = (1/3) × 0.25
    semi_auto: 0.08
  min_max_position_blocks: 4    # warn if max feasible position < this
```

Include the rule-of-thumb correlation tables (Appendix C, Tables 50–57) and the handcrafting/SR
tables (Ch.4, Tables 8 & 12) as data files under `config/` — see §5.2, §5.5, §7.

---

## 5. Module specifications

Each subsection = one module. Build in this order; each has its own golden test in §9.

### 5.1 Trading rules → forecasts (Ch.7, Appendix B)

`TradingRule` ABC exposes `forecast(snapshot, instrument) -> Forecast`. Contract: return a value
scaled to `E|f| ≈ 10` and **capped** to `[-cap, +cap]` (or `[0, +cap]` when
`tradeable_long_only`). Capping is the rule's responsibility so downstream never sees > 20.

Shared helper `apply_scalar_and_cap(raw, scalar, cap, long_only)`:
`f = clip(raw * scalar, -cap, +cap)`; if `long_only`, lower-clip at 0.

**EWMAC** (`ewmac.py`) — trend following. For a `(L_fast, L_slow)` pair (slow = 4×fast):
1. Decay `λ = 2 / (L + 1)` for each window.
2. EWMA recursively: `E_t = λ·P_t + (1-λ)·E_{t-1}` (seed `E_0 = P_0`). Use `pandas.ewm(span=L)` —
   its `span` = the look-back window, matching the book.
3. `raw_crossover = EWMA_fast − EWMA_slow` (in price points).
4. `price_vol_points = price_volatility_pct × current_price` (daily σ of returns, in price points).
5. `vol_adjusted = raw_crossover / price_vol_points`.
6. `forecast = clip(vol_adjusted × forecast_scalar[pair], ±20)`, using Table 49 scalars.

Default variation set = the six pairs above. Prune any two variations with correlation > 0.95
(adjacent pairs sit at ~0.90, which is fine); reject variations that trade too fast/slow for the
instrument's cost (see §5.7). Slowest sensible pair is 64:256.

**Carry** (`carry.py`) — earns when prices are stable. Two steps:

*(a) Net annualised expected return in price units* (asset-class specific):
| Asset | Net expected return in **price units** |
|---|---|
| Futures, not nearest contract *(preferred)* | `(current_price − nearer_price) / years_between_contracts` |
| Futures, nearest contract *(approx)* | `(next_price − current_price) / years_between_contracts` |
| Equity (cash/margin) | `(dividend_yield − funding_cost) × price` |
| Equity CFD | `(dividend_yield − avg_funding_cost) × price` |
| FX cash | `(foreign_interest − domestic_funding) × price` |
| Spread bet | `(spot_level − bet_level) / time_to_maturity_years` |

*(b) Forecast* (same for all assets):
1. `sigma_points_daily = price_volatility_pct × current_price`.
2. `sigma_points_annual = sigma_points_daily × 16`.
3. `raw_carry = net_expected_return_price_units / sigma_points_annual`  (an annualised Sharpe-like #).
4. `forecast = clip(raw_carry × 30, ±20)`  (forecast scalar = 30).
Update weekly to avoid noise; turnover rule-of-thumb = 10.

**No-rule rule** (`norule.py`): constant `Forecast(value=+10)` for every instrument (asset allocator).

**Discretionary** (`discretionary.py`): validate a human forecast is in `[-20, +20]`; map the verbal
scale if provided — very-strong-sell −20, strong-sell −15, sell −10, weak-sell −5, neutral 0, and
mirror for buys. Reject out-of-range. Forecast must **not** change once a bet is open (exit is via
stop-loss, not by editing the forecast).

**Creating/adapting a rule (Appendix D "Rescaling"):** a new rule's `forecast_scalar = 10 / mean(|raw
forecast|)`, where the mean is measured across many instruments and long history *without looking at
performance*. Provide a `calibrate_forecast_scalar(raw_forecasts) -> float` utility.

### 5.2 Combine forecasts (Ch.8, Appendix D)

Only for staunch traders with >1 rule variation. Skip entirely for no-rule/discretionary.

1. **Forecast weights** `w_r`: positive, sum to 1. Obtain via handcrafting (§5.5) or bootstrapping.
   May differ per instrument or be shared.
2. **Raw combined** `= Σ_r w_r · f_r`.
3. **Forecast diversification multiplier (FDM)** `= 1 / sqrt(w · H · wᵀ)` where `H` is the forecast
   correlation matrix (§5.8), correlations **floored at 0**, FDM **capped at 2.5**.
4. **Rescaled** `= raw_combined × FDM` (restores `E|f| ≈ 10`).
5. **Final** `= clip(rescaled, ±20)`.

Correlation inputs (Appendix C): from back-tested forecasts, or rules of thumb — variations of one
rule ≈ 0.7 (adjacent EWMAC ~0.9, see Table 57); different rules same style ≈ 0.5; different styles
≈ 0.25 (Table 56). Prefer pooling forecasts across instruments before computing `H`.

### 5.3 Volatility target (Ch.9)

Human-set risk parameters; the module computes the cash targets and enforces sanity.

- `annualised_cash_vol_target = trading_capital × percentage_vol_target`
- `daily_cash_vol_target = annualised_cash_vol_target / 16`
- **Capital updates:** `trading_capital` tracks P&L, injections, withdrawals daily. `percentage_vol_
  target` is **fixed** (only ever adjusted **down**, once, if the human grossly misjudged risk).
- **Choosing `percentage_vol_target` (Half-Kelly).** Optimal ≈ realistic Sharpe ratio; the book uses
  **Half-Kelly** (target ≈ 0.5 × realistic SR), halved **again** for negative skew. Ship these as
  lookup tables and a helper `recommend_vol_target(realistic_sr, skew_sign, persona)`:

  | Realistic SR | Skew ≥ 0 | Negative skew |
  |---|---|---|
  | 0.25 | 12% | 6% |
  | 0.40 | 20% | 10% |
  | 0.50 | 25% | 12% |
  | 0.75 | 37% | 19% |
  | ≥1.00 | 50% | 25% |

  Caps by persona: asset allocator SR ≤ 0.40 (target ≤ 20%); semi-auto SR ≤ 0.50 (target ≤ 25%,
  halved for negative skew). Nobody exceeds 50%. Discount back-tested SR to "realistic" (e.g. ×0.75
  for out-of-sample bootstrap) **before** using the table.
- **Leverage guard:** emit a warning if hitting the target would require leverage such that the
  single largest plausible market move wipes out the account; exclude ultra-low-vol instruments
  (pegged FX, front Eurodollar, etc.).

### 5.4 Subsystem position sizing (Ch.10)

Per instrument, assuming (for now) the whole account trades this one instrument.
1. `price_volatility` — daily σ of % returns, from §5.9. (number-of-percent convention).
2. `block_value` — cash gain in **instrument ccy** for a **+1%** price move of one block. Derive per
   instrument type: equity block of N shares → `N × price × 0.01`; future →
   `contract_multiplier × price × 0.01`; spread bet → `stake_per_point × price × 0.01`. (For a
   Eurodollar-style rate future, block value follows the notional×tenor rule — implement per the
   book's example, `$1m × Δrate × 0.25`.)
3. `instrument_ccy_vol (ICV) = block_value × price_volatility`.
4. `instrument_value_vol (IVV) = ICV × fx_rate`, where **fx_rate has instrument currency as
   numerator and base currency as denominator** (book uses `USD/GBP = 0.67`, i.e. base value of one
   unit of instrument ccy). Double-check the direction against the golden test — getting it inverted
   silently corrupts everything.
5. `volatility_scalar = daily_cash_vol_target / IVV`. (Both in base ccy.) **Do not round.**
6. `subsystem_position = (combined_forecast × volatility_scalar) / 10`. **Do not round.**

Interpretation: the vol scalar is the position for a constant `+10` forecast; the subsystem position
scales linearly with the forecast (so `+20` ⇒ 2× the scalar; `−6` ⇒ `−0.6×`).

### 5.5 Instrument weights (Ch.11)

Allocate capital **across trading subsystems** (one per instrument), positive, summing to 1.

- **Asset allocators & staunch traders:** handcraft (§5.6) or bootstrap. Correlations needed are
  between **subsystem returns**: take instrument-return correlations (Tables 50–55) and multiply by
  **0.70** for dynamic strategies, or **1.00** for the static asset allocator. Do **not** adjust
  weights for Sharpe differences between instruments (rarely enough evidence — see §5.7).
- **Semi-automatic:** equal weights = `1 / max_concurrent_bets`. Constrain
  `max_bets ≤ 2.5 × avg_bets` (see IDM below).

### 5.6 Handcrafting weights (Ch.4)

Implement `handcraft(groups, correlations) -> weights`:
- Build the portfolio bottom-up: form groups of highly-correlated assets (1–3 members ideal),
  allocate **within** each group using the Table-8 patterns, then allocate **across** groups
  (recursively, any number of levels). Final asset weight = product of its weights at every level.
- **Table 8 patterns** (encode as a lookup; round correlations to the nearest listed pattern; floor
  negatives at 0). Three-asset rows are keyed by correlations (AB, AC, BC) → weights (A, B, C):
  | Pattern | Weights |
  |---|---|
  | 1 asset | 100% |
  | 2 assets | 50% / 50% |
  | Any group, identical correlations | equal weights |
  | 3 assets (0.0, 0.5, 0.0) | 30 / 40 / 30 |
  | 3 assets (0.0, 0.9, 0.0) | 27 / 46 / 27 |
  | 3 assets (0.5, 0.0, 0.5) | 37 / 26 / 37 |
  | 3 assets (0.0, 0.5, 0.9) | 45 / 45 / 10 |
  | 3 assets (0.9, 0.0, 0.9) | 39 / 22 / 39 |
  | 3 assets (0.5, 0.9, 0.5) | 29 / 42 / 29 |
  | 3 assets (0.9, 0.5, 0.9) | 42 / 16 / 42 |
  | 4+ assets, non-identical corr | split into sub-groups until each matches a row above |
  Reorder any 3-asset correlation triple to match a listed row, then map weights back.
- **Optional SR adjustment (Table 12):** multiply a group member's handcrafted weight by an
  adjustment factor keyed on `(SR − group_average_SR)` and confidence. Use **column A ("with
  certainty")** for cost-driven differences. Renormalise the group to sum to 1 afterwards. Book's
  guidance: with the recommended speed limit, cost adjustments never exceed ×0.95–×1.05, so this is
  usually negligible — but implement it for completeness.

### 5.7 Instrument diversification multiplier & portfolio position (Ch.11)

- **IDM (asset allocator / staunch):** `= 1 / sqrt(w · H · wᵀ)`, `H` = subsystem-return correlations
  (Tables 50–55 × 0.70 dynamic, or ×1.0 static; **floor negatives at 0**), capped at **2.5**. May
  use the Table-18 approximation (by #assets and average correlation) as a cross-check.
- **IDM (semi-auto):** `= max_bets / avg_bets`, capped at 2.5.
- `portfolio_position = subsystem_position × instrument_weight × IDM`. **Unrounded.**
- `rounded_target_position = round(portfolio_position)`  ← **the one and only rounding step.**
- **Trade generation with position inertia:** compare to `current_position`. If
  `|current − rounded_target| < inertia_pct × |rounded_target|` (default 10%) ⇒ **no trade**.
  Otherwise `trade = rounded_target − current`. (For very fast rules the book suggests a smaller
  inertia or none — expose as config.)

### 5.8 Diversification multiplier helper (Appendix D)

One shared function used by both FDM and IDM:
```python
def div_multiplier(weights, corr, cap=2.5, floor_zero=True):
    H = np.where(corr < 0, 0.0, corr) if floor_zero else corr
    w = np.asarray(weights, float)
    dm = 1.0 / np.sqrt(w @ H @ w.T)
    return min(dm, cap)
```
Also provide the **Table-18 approximation** (interpolate by #assets and average off-diagonal
correlation) for validation and for the no-back-test path.

### 5.9 Volatility estimators (Ch.10, Appendix D)

`price_volatility(price_history, method, lookback)` → daily σ of **percentage returns**, returned in
the number-of-percent convention (multiply the decimal σ by 100 if you compute returns as decimals —
just be consistent with §3).
- **Returns:** `r_t = (P_t − P_{t−1}) / P_{t−1}`.
- **SMA:** rolling std dev of `r` over `sma_lookback_days` (default 25).
- **EWMA:** `λ = 2 / (1 + ewma_lookback_days)` (default 36 ⇒ λ = 0.054). Recurse on **squared
  returns**: `Var_t = λ·r_t² + (1−λ)·Var_{t−1}` (seed `Var_0 = r_0²`); `σ_t = sqrt(Var_t)`.
- **Slow-down for expensive instruments:** allow longer look-backs (SMA 25/50/100 ≙ EWMA 36/72/144)
  to cut turnover; never exceed ~20 weeks (performance degrades). Selection driven by §5.10 costs.
- **Guard:** flag suspiciously low σ (pegged/zero-rate regimes) — these blow up position sizes.

### 5.10 Speed & size — costs, turnover, feasibility (Ch.12)

Cost tooling that gates instrument/rule selection.
- **Standardised cost per round trip (SR units):** `= (2 × cost_per_block) / (16 × ICV)`
  where `cost_per_block` = execution cost (≈ half the bid-offer spread for small size) + per-ticket
  fee + per-unit fee + %-value fees/taxes, in instrument ccy. Lower price-vol ⇒ higher standardised
  cost (another reason to avoid low-vol instruments).
- **Turnover (round trips/yr):** from back-test `= blocks_traded_per_year / (2 × avg_abs_blocks_
  held)`, or rules of thumb (Carry ≈ 10; EWMAC per variation; semi-auto from stop-loss holding
  period). Combined-forecast turnover ≈ forecast-weighted avg of rule turnovers × FDM, then adjusted
  for the vol look-back and position inertia (Table 36).
- **Cost in SR/yr** `= standardised_cost × turnover`.
- **Speed limit:** reject instrument/rule combos whose cost exceeds `speed_limit_sr[persona]`
  (staunch 0.13; asset allocator & semi-auto 0.08). Provide `max_turnover = speed_limit / standardised_cost`.
- **Minimum-capital / max-position check:**
  `max_feasible_position = k × volatility_scalar × instrument_weight × IDM`, with `k = 2`
  (staunch/semi, uses `forecast = +20`) or `k = 1` (asset allocator, `forecast = +10`).
  **Warn if `< 4` blocks**; error if `< 1`. Suggest remedies: raise the instrument's weight (in
  moderation), shrink the portfolio, or drop the instrument.
- **Portfolio construction rule:** hold the most diversified portfolio possible (≥1 instrument per
  major asset class) subject to every instrument clearing the ≥4-block max-position bar.

---

## 6. Orchestration

`pipeline.run(portfolio, config, date, current_positions) -> PortfolioResult`:
1. For each instrument: compute forecasts → combine (FDM) → price vol / block value → ICV → IVV →
   volatility scalar → subsystem position.
2. Compute cash vol targets (§5.3).
3. Apply instrument weights + IDM → portfolio positions.
4. Round once → apply position inertia vs `current_positions` → emit trades.
5. Emit full per-instrument diagnostics (every intermediate) so a human can reconcile against the
   book's tables.

`backtest.run(...)` (optional but recommended): replay the pipeline over history to measure realised
turnover and after-cost performance; use those to set weights (bootstrap) and the vol target.

---

## 7. Reference data to embed (from Appendix C)

Ship as `config/correlations.yaml`. Key rule-of-thumb instrument-return correlations:
cross-super-class ≈ 0.1 (equity↔vol 0.6); within-region same-class equities/bonds/FX ≈ 0.75;
same-industry different firm ≈ 0.80; commodities same sub-class ≈ 0.70; bond-duration matrix
(2/5/10/20/30y: 0.80 adjacent down to 0.50 far). Forecast correlations: EWMAC adjacent-pair 0.90
(Table 57 full matrix), cross-style 0.25, same-style 0.5. Handcraft/SR tables per §5.6.

---

## 8. Testing strategy

- **Golden tests (§9):** reproduce the book's worked examples exactly (within tolerance). These are
  the acceptance gate — do not mark a module done until its golden test passes.
- **Property tests:** (a) forecast always in `[-cap, cap]`; (b) doubling the forecast doubles the
  unrounded subsystem position; (c) doubling price volatility halves it; (d) FDM/IDM ∈ `[1.0, 2.5]`;
  (e) weights sum to 1; (f) no-look-ahead: truncating history at `t` doesn't change the value at `t`.
- **Convention tests:** assert the percent convention (§3) and the FX direction (§5.4).
- **Regression tests:** freeze pipeline output for a fixed fixture portfolio.

---

## 9. Golden acceptance tests (verbatim from the book)

Encode these as fixtures. Tolerance: ±0.5% relative (the book rounds intermediates in display; your
engine keeps full precision, so match its *stated* results within rounding).

**GT-1 — Subsystem position sizing (Ch.10 worked example).** WTI crude future, forecast **−6**,
annualised cash vol target **£1,000,000**, FX `USD/GBP = 0.67`, price `$75`, contract = 1000 bbl.
Expected chain: daily cash vol target `£62,500`; price volatility `1.33%`; block value `$750`;
`ICV = 750 × 1.33 = $997.50`; `IVV = 997.50 × 0.67 = £668.325`;
`volatility_scalar = 62,500 / 668.325 = 93.52`; `subsystem_position = (−6 × 93.52)/10 = −56.11`
(short 56.11 contracts, unrounded).

**GT-2 — Full three-asset portfolio (Ch.11, Tables 30–33).** Euro investor, cash vol target
**€100,000** (daily €6,250), `USD/EUR = 0.88`, weights {bond 50%, S&P 25%, NASDAQ 25%}, **IDM 1.41**.

| Instrument | price vol % | block value | ICV | IVV | vol scalar | forecast | subsys pos | port pos | rounded | current | trade |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US 20y bond | 0.52 | $1500 | $780 | €686 | 9.11 | +10 | 9.11 | 6.42 | 6 | 4 | **Buy 2** |
| S&P 500 | 0.84 | $1145 | $956 | €841 | 7.43 | −10 | −7.43 | −2.62 | −3 | −2 | **Sell 1** |
| NASDAQ | 0.87 | $880 | $766 | €674 | 9.28 | −15 | −13.9 | −4.91 | −5 | −5 | **None** |

(Verifies ICV, FX conversion, vol scalar, subsystem position, IDM application, single rounding,
and position-inertia/trade logic simultaneously.)

**GT-3 — Combine forecasts (Ch.8).** EWMAC `+15`, Carry `−10`, forecast weights 50/50 ⇒
`raw_combined = 2.5`. Capping case: two rules both `+16`, weights 50/50, FDM `1.5` ⇒
`16 × 1.5 = 24` ⇒ **capped to 20**. FDM sanity: 4 EWMAC/Carry variations, avg corr ≈ 0.5 ⇒
Table-18 approx `1.27`, precise formula `1.31` (both ≤ 2.5).

**GT-4 — Diversification multiplier (Ch.8 concept box).** Two equal-weighted assets: corr 1.0 ⇒
`1.00`; corr 0.5 ⇒ `10/8.66 = 1.15`; corr 0.0 ⇒ `10/7.07 = 1.41` (Table-18 value; precise 1.44).

**GT-5 — Standardised costs (Ch.12).** Euro Stoxx future: `ICV €506`, cost `€8` ⇒
`2×8/(16×506) = 0.002 SR`. FTSE £1 spread bet: `ICV £49.50`, cost `£4` ⇒
`2×4/(16×49.50) = 0.01 SR`. IGIL ETF: `ICV $62`, cost `$40` ⇒ `2×40/(16×62) = 0.08 SR`.

**GT-6 — Min-position feasibility (Ch.12).** S&P subsystem vol scalar `1.49` (at a €20k target),
weight 25%, IDM 1.41 ⇒ `max_position = 2 × 1.49 × 0.25 × 1.41 = 1.05` ⇒ **warn (<4)**. After
concentrating to 100% weight, IDM→1.0 ⇒ `2 × 1.49 × 1.0 = 2.98`.

**GT-7 — Handcrafting (Ch.4).** {US 20y bond, S&P, NASDAQ}, corr(bond,equities)≈0, corr(S&P,NASDAQ)
≈0.9 ⇒ grouped handcraft weights {bond 50%, S&P 25%, NASDAQ 25%}. Also the 3-asset pattern
`(0.0, 0.9, 0.0)` ⇒ `{27%, 46%, 27%}`.

**GT-8 — EWMAC scalars & volatility.** `λ(span=36) = 2/37 = 0.054`. Forecast scalars load exactly:
2,8→10.6; 4,16→7.5; 8,32→5.3; 16,64→3.75; 32,128→2.65; 64,256→1.87. Carry scalar = 30.

---

## 10. Guardrails, risk notes, and definition of done

**Guardrails (non-negotiable):**
- Default to `--dry-run`; a real-order path (if ever added) must require an explicit human
  confirmation gate and a hard kill-switch. This tool outputs *recommended trades*, not orders.
- Never silently swap the FX direction, the percent convention, or the rounding point — assert them.
- Cap FDM and IDM at 2.5 and floor correlations at 0 **always** (crisis correlations spike; the cap
  is a safety feature, not a nuisance).
- Refuse to size positions on instruments flagged ultra-low-vol / excessive-leverage; surface the
  reason.
- This is decision-support software, not financial advice, and back-tested numbers overstate future
  performance — keep the vol-target discounting (§5.3) prominent in any report output.

**Definition of done:**
1. All eight golden tests (§9) pass within tolerance.
2. Property and convention tests pass; no-look-ahead proven by test.
3. `pipeline.run` produces a full auditable diagnostics record per instrument that a human can
   reconcile line-by-line against GT-2's table.
4. Config-driven: changing look-backs / scalars / caps / weights requires no code change.
5. A new trading rule can be added by subclassing `TradingRule` alone, with its own golden test,
   touching no other module.
6. CLI: `systrading run --portfolio p.yaml --date 2015-01-23 --positions pos.csv` prints the trade
   list + diagnostics; `systrading costs --portfolio p.yaml` prints standardised costs, turnover
   headroom, and min-position warnings.

**Suggested build order:** volatility (§5.9) → EWMAC & Carry & no-rule (§5.1) → div-multiplier
helper (§5.8) → combine (§5.2) → vol target (§5.3) → subsystem position (§5.4) → handcraft (§5.6) →
instrument weights + IDM + portfolio/trades (§5.5, §5.7) → costs/feasibility (§5.10) →
orchestration (§6) → optional back-test. Land each module with its golden test before moving on.

---

*Source of truth: Rob Carver, "Systematic Trading," Part Three (Ch. 5–12) and Appendices B–D.
Reproduce the maths; don't reinvent it.*
