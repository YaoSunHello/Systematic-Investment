# Audit Prompt — Verify the Systematic Trading Framework Implementation

> **You are a verification engineer.** A previous developer built a systematic-trading
> position-sizing framework (Carver, *Systematic Trading*, Part Three) from a build spec. Your job
> is **not** to build or refactor it — it is to **prove whether it is correct and complete**, then
> deliver a pass/fail verdict backed by evidence. Treat the implementation as untrusted: assume
> nothing works until a test demonstrates it. Every numeric expectation below is independently
> computable from the inputs given (you do not need the book). Reproduce each check, record
> PASS/FAIL with the actual value observed, and grade against the rubric in §3.

---

## 1. Audit mission & rules of engagement

- **Do not fix code.** If you find a defect, log it — do not silently patch it and re-run green.
  (You may write throwaway test harnesses and adapters; you may not edit the system under test.)
- **Black-box first, white-box second.** Prefer driving the system through its public API. Where a
  behaviour cannot be observed from outputs (look-ahead, single-rounding discipline, EWMA seeding),
  read the source and cite file+line as evidence.
- **Independent arithmetic.** Compute every expected value yourself from the inputs; never accept the
  system's own output as its own oracle.
- **Every FAIL needs a repro.** Record the exact input, the expected value, the observed value, and
  the file/function exercised.
- **Tolerance:** unless stated otherwise, a numeric check PASSES if
  `abs(observed − expected) ≤ max(1e-6, 5e-4 × abs(expected))` (≈0.05% relative or 1e-6 absolute).
  Integer outputs (rounded positions, trades) must match **exactly**.

### 1.1 Discovery step (do this first)
1. Locate the modules for: volatility estimation, forecasts (EWMAC / Carry / no-rule / discretionary),
   forecast combining + FDM, volatility target, subsystem position sizing, instrument weights +
   handcrafting, IDM + portfolio position + trades, costs/turnover/feasibility, orchestration.
2. Build a thin adapter per module so you can feed the §4 inputs and read outputs, regardless of the
   exact function signatures the developer chose.
3. If a module is **absent or not reachable**, mark its tests **FAIL (missing)** — do not skip.

---

## 2. What "complete" means — required inventory (P0 presence check)

Each item must exist and be exercised by at least one passing test. A missing item is a P0 failure.

| # | Capability | Must exist |
|---|---|---|
| C1 | Price-volatility estimator, SMA (25d default) | ✔ |
| C2 | Price-volatility estimator, EWMA (36d default, λ=0.054, **recursive/adjust=False**) | ✔ |
| C3 | EWMAC rule: recursive EWMAs, vol-adjusted crossover, per-pair forecast scalar, ±20 cap | ✔ |
| C4 | Carry rule: per-asset net-return-in-price-units, ÷ annualised σ points, ×30 scalar, ±20 cap | ✔ |
| C5 | No-rule rule: constant +10 | ✔ |
| C6 | Discretionary input: validates `[-20,+20]`; rejects out-of-range | ✔ |
| C7 | Forecast combining: weighted average → × FDM → ±20 cap | ✔ |
| C8 | FDM = `1/√(w·H·wᵀ)`, correlations floored ≥0, capped ≤2.5 | ✔ |
| C9 | Volatility target: capital × %target = annual cash; ÷16 = daily cash; capital updatable | ✔ |
| C10 | `recommend_vol_target` (Half-Kelly table, negative-skew halving, persona caps) | ✔ |
| C11 | Subsystem position: block value → ICV → IVV (FX) → vol scalar → subsystem position (all unrounded) | ✔ |
| C12 | Handcrafting weights (Table-8 patterns) + optional SR adjustment | ✔ |
| C13 | Instrument weights: 0.70 subsystem-corr scaling (dynamic) vs 1.0 (static); semi-auto equal weights | ✔ |
| C14 | IDM = `1/√(w·H·wᵀ)` (asset alloc/staunch) or `max_bets/avg_bets` (semi-auto), capped ≤2.5 | ✔ |
| C15 | Portfolio position = subsystem × weight × IDM; **single** rounding; position inertia; trade calc | ✔ |
| C16 | Standardised cost = `2·C/(16·ICV)`; turnover; cost-in-SR; speed limits by persona | ✔ |
| C17 | Min-position feasibility: `k·volscalar·weight·IDM` (k=2 staunch/semi, k=1 asset alloc); warn <4 | ✔ |
| C18 | Config-driven scalars/look-backs/caps/targets (no magic numbers in logic paths) | ✔ |
| C19 | Per-instrument diagnostics record exposing every intermediate value | ✔ |
| C20 | Dry-run default / no live-order path enabled by default | ✔ |

---

## 3. Grading rubric & pass/fail rule

Classify every check into a severity, then apply the decision rule.

- **P0 — Critical (correctness or safety).** Core formula correctness, the four "silent-corruption
  traps" (§5), look-ahead, cap/floor enforcement, single-rounding, dry-run default.
  → **Any P0 FAIL ⇒ overall verdict = FAIL.**
- **P1 — Major (completeness/behaviour).** A required module missing, a persona path broken, wrong
  handcraft pattern, wrong turnover/cost, diagnostics absent.
  → **≥1 P1 FAIL ⇒ at best CONDITIONAL PASS; ≥3 P1 FAILs ⇒ FAIL.**
- **P2 — Minor (quality).** Weak validation, no property tests, unclear errors, style.
  → Logged; does not block, but must appear in the report.

**Verdict definitions**
- **PASS:** all P0 pass, zero P1 fail, P2 issues logged.
- **CONDITIONAL PASS:** all P0 pass, 1–2 P1 fail, each with a documented remediation.
- **FAIL:** any P0 fail, or ≥3 P1 fail.

A "% complete" score = `(passed weighted checks) / (total weighted checks)`, weights P0=5, P1=3,
P2=1. Report it, but the **verdict is governed by the P0/P1 rules above, not the percentage.**

---

## 4. Numeric conformance tests (self-contained; compute expectations yourself)

Each test lists inputs and the expected result you must independently reproduce. Severity in brackets.

### T1 — EWMA decay parameter [P1]
`λ = 2/(L+1)`. For `L=36 ⇒ λ = 0.0540541`. For `L=25 ⇒ λ = 0.0769231`.
**PASS** if the estimator's decay matches to 1e-6.

### T2 — EWMA recursion & seeding (adjust=False) [P0 — trap, see §5.3]
Prices `[100, 102, 101, 105]`, EWMA span `L=2` ⇒ `λ = 2/3`. Recursive with seed `E₀ = P₀`:
| t | Pₜ | Expected EWMAₜ (adjust=False) |
|---|---|---|
| 0 | 100 | 100.00000 |
| 1 | 102 | 101.33333 |
| 2 | 101 | 101.11111 |
| 3 | 105 | 103.70370 |
**PASS** only if these match. If instead `E₁ ≈ 101.5`, the implementation used pandas' default
`adjust=True` (normalised finite-sample weights) — that is a **P0 FAIL** (§5.3).

### T3 — SMA price volatility [P1]
Daily returns `r_t = (P_t−P_{t−1})/P_{t−1}`. For a flat-then-step series where the last 25 returns
are all `0.01` (1%), the 25-day SMA std dev = `0.0` (no dispersion). For 25 returns alternating
`+0.01, −0.01`, the sample std dev ≈ `0.01` (i.e. 1%). Feed a controlled series and verify the
estimator returns the daily σ of *returns*, not of prices, in the documented convention.

### T4 — Percent convention & ICV two-way check [P0 — trap, see §5.1]
Instrument: price `75`, contract multiplier `1000`, daily return σ `v = 0.0133` (=1.33%).
- `block_value` (cash per **+1%** move) `= 0.01 × 75 × 1000 = 750`.
- Path A: `ICV = block_value × (100·v) = 750 × 1.33 = 997.50`.
- Path B: `ICV = (v × price) × multiplier = (0.0133×75) × 1000 = 997.50`.
**PASS** if the system's ICV = `997.50` (±0.05%) **and** both derivations agree. A result near
`9.975` or `13.3` means the percent convention is mixed up ⇒ **P0 FAIL**.

### T5 — FX direction (IVV) [P0 — trap, see §5.2]
`ICV = 997.50` (USD), FX `USD/GBP = 0.67` (base value of 1 USD). Expected
`IVV = 997.50 × 0.67 = 668.325` GBP. **PASS** if `≈668.33`. A result near `1488.8` (divided instead
of multiplied, or inverted rate) ⇒ **P0 FAIL**.

### T6 — Volatility scalar & subsystem position [P0]
`daily_cash_vol_target = 10000`, `IVV = 500` ⇒ `volatility_scalar = 20.0`.
| forecast | expected subsystem position `= forecast × scalar / 10` |
|---|---|
| +10 | 20.0 |
| −6 | −12.0 |
| +20 | 40.0 |
| 0 | 0.0 |
All **unrounded**. **PASS** on exact linear scaling and the +20 ⇒ 2× property.

### T7 — Subsystem position, book integration case [P0]
Crude future, forecast `−6`, annualised cash vol target `£1,000,000`, price `$75`, multiplier
`1000`, `v=0.0133`, FX `USD/GBP=0.67`. Expected chain: daily target `£62,500`; block value `$750`;
`ICV=$997.50`; `IVV=£668.325`; `vol_scalar=93.52`; `subsystem_position=−56.11` (unrounded).

### T8 — EWMAC forecast scaling & cap [P0]
Isolate the scaling: `raw_crossover = 3.0` price points, `v=0.02`, `price=100` ⇒
`price_vol_points = 0.02×100 = 2.0` ⇒ `vol_adjusted = 3.0/2.0 = 1.5`. With EWMAC(8,32) scalar `5.3`:
`forecast = 1.5 × 5.3 = 7.95`. Cap test: `raw_crossover = 12` ⇒ `vol_adjusted = 6` ⇒ `6×5.3 = 31.8`
⇒ **capped to 20.0**. Verify the six scalars load exactly: 2,8→10.6; 4,16→7.5; 8,32→5.3;
16,64→3.75; 32,128→2.65; 64,256→1.87.

### T9 — Carry forecast [P0]
Futures, not-nearest: `current=100.0`, `nearer=99.0`, `distance=0.25y`.
`net_return_price_units = (100−99)/0.25 = 4.0`. With `v=0.01`, `price=100`:
`σ_points_daily = 1.0`, `σ_points_annual = 1.0×16 = 16.0`, `raw_carry = 4.0/16.0 = 0.25`,
`forecast = 30 × 0.25 = 7.5`. **PASS** at `7.5`. Also verify the per-asset net-return formulas
select correctly by asset class (equity uses `(div−funding)×price`, spread bet uses
`(spot−bet)/T`, etc.).

### T10 — Combine forecasts + FDM cap [P0]
Forecasts `EWMAC=+15`, `Carry=−10`, weights `[0.5, 0.5]` ⇒ `raw_combined = 2.5`.
Cap case: both `+16`, weights `[0.5,0.5]`, `FDM=1.5` ⇒ `16 × 1.5 = 24` ⇒ **capped to 20.0**.

### T11 — Diversification multiplier (shared FDM/IDM) [P0]
`div_multiplier(weights, corr)` with equal weights `[0.5,0.5]`:
| correlation | `w·H·wᵀ` | expected DM = `1/√(·)` |
|---|---|---|
| 1.0 | 1.000 | 1.0000 |
| 0.5 | 0.750 | 1.1547 |
| 0.0 | 0.500 | 1.4142 |
| −0.5 (floored to 0) | 0.500 | 1.4142 |
Cap: 10 uncorrelated assets, equal weight 0.1, `H=I` ⇒ `w·H·wᵀ = 0.1` ⇒ raw `3.1623` ⇒
**capped to 2.5**. **PASS** requires the floor **and** the cap both applied.

### T12 — Standardised cost [P1]
`ICV = 500`, `cost_per_block = 10` ⇒ `standardised_cost = (2×10)/(16×500) = 0.0025 SR`.
Speed-limit gate: persona `staunch` limit `0.13`; with this cost, `max_turnover = 0.13/0.0025 = 52`.
Reject any rule whose turnover exceeds that.

### T13 — Portfolio position, single rounding, inertia, trades [P0]
`subsystem=20.0`, `instrument_weight=0.5`, `IDM=1.4` ⇒ `portfolio_position = 14.0` ⇒ rounded `14`.
Inertia band = `10% × 14 = 1.4`.
| current | |target−current| | expected trade |
|---|---|---|
| 13 | 1.0 (<1.4) | **None** (inertia) |
| 12 | 2.0 | **Buy 2** |
| 16 | 2.0 | **Sell 2** |
Also confirm **no rounding happens before** `rounded_target_position` (inspect the chain).

### T14 — Volatility target & Half-Kelly recommendation [P1]
`capital=500000`, `%target=0.25` ⇒ annual cash `125000`, daily cash `7812.5`.
`recommend_vol_target(realistic_sr=0.75, skew≥0) ⇒ 37%`; `(0.75, negative skew) ⇒ 19%`;
`(0.40, skew≥0) ⇒ 20%`. Persona caps: asset allocator ≤20%, semi-auto ≤25%, global ≤50%.

### T15 — Min-position feasibility [P1]
`vol_scalar=1.49`, `weight=0.25`, `IDM=1.41`, `k=2` (staunch) ⇒
`max_position = 2×1.49×0.25×1.41 = 1.05` ⇒ **warn (<4)**. Asset-allocator variant uses `k=1`.

### T16 — Handcrafting patterns [P1]
Three-asset pattern with correlations `(AB,AC,BC) = (0.0, 0.9, 0.0)` ⇒ weights `27% / 46% / 27%`.
Grouped bond + two 0.9-correlated equities ⇒ `{bond 50%, equity 25%, equity 25%}`. Weights within
any group sum to 100%; final weights across the portfolio sum to 100%.

### T17 — Full three-instrument integration (end-to-end) [P0]
Euro investor, annual cash vol target `€100,000` (daily `€6,250`), FX `USD/EUR=0.88`, instrument
weights `{bond 0.50, S&P 0.25, NASDAQ 0.25}`, `IDM=1.41`. Drive the whole pipeline and reconcile
against this table (integers exact; floats ±0.5%):

| Instrument | price vol% | block value | ICV | IVV | vol scalar | forecast | subsys | port pos | rounded | current | trade |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US 20y bond | 0.52 | 1500 | 780 | 686 | 9.11 | +10 | 9.11 | 6.42 | 6 | 4 | Buy 2 |
| S&P 500 | 0.84 | 1145 | 956 | 841 | 7.43 | −10 | −7.43 | −2.62 | −3 | −2 | Sell 1 |
| NASDAQ | 0.87 | 880 | 766 | 674 | 9.28 | −15 | −13.9 | −4.91 | −5 | −5 | None |

This single test exercises ICV, FX, vol scalar, subsystem sizing, IDM, single-rounding, and trade
generation together. If it reconciles, the happy path is sound.

---

## 5. Trap tests — the silent-corruption bugs (all P0)

These pass superficial smoke tests but are wrong. Explicitly probe each.

### 5.1 Percent-convention mismatch
The system must apply **one** convention consistently. Re-run **T4** and additionally check that
`price_vol_points` used inside EWMAC/Carry equals `v_decimal × price` (T8/T9). A system that gets
ICV right but divides by `100·v` inside EWMAC (or vice-versa) will pass position sizing yet produce
forecasts off by 100×. Verify both call sites, not just one.

### 5.2 FX inversion
Re-run **T5**, then feed a second instrument whose currency **equals** the base currency (FX rate
`1.0`) and one whose rate is `> 1` and `< 1`. Confirm IVV scales the right direction. An inverted
rate is invisible when the rate happens to be near 1.0 — that's why you test 0.67 and 1.5.

### 5.3 EWMA `adjust=True` leakage
Re-run **T2**. If the code calls `series.ewm(span=L).mean()` **without** `adjust=False`, the early
values are normalised differently from the book's recursion and the seed differs. Cite the exact
call. Expected early value `E₁ = 101.3333`, not `101.5`.

### 5.4 Multiple / premature rounding
Grep the pipeline for rounding/`int()`/`round()` between `subsystem_position` and
`rounded_target_position`. There must be **exactly one** rounding, at the portfolio-target step.
Construct a case (e.g. subsystem `9.49`, weight `1.0`, IDM `1.0`) where premature rounding to `9`
then reapplying weight would differ from rounding once. Expected: round happens only at the end.

### 5.5 Cap / floor not enforced under composition
Feed a combined forecast that would exceed 20 after FDM (T10 cap case) **and** an individual rule
that raw-produces `+35` (must clamp to `+20`). Then feed a negative correlation into both FDM and
IDM (T11 floor case). A system that caps the individual forecast but forgets to cap the *combined*
one, or floors correlations for IDM but not FDM, fails here.

### 5.6 Look-ahead / non-causality
Take any instrument series of length N. Compute volatility/forecast/subsystem-position at date
`t = N−10` using (a) the full series and (b) the series truncated at `t`. Results at `t` **must be
identical**. Any dependence on future rows ⇒ **P0 FAIL**. If the API can't truncate, read the code
and confirm every rolling/EWMA/correlation window is backward-looking only.

### 5.7 Discretionary forecast mutated while position open
Simulate: open a bet at forecast `+12`; on a later bar, attempt to change the live forecast. The
system must **not** resize from a changed discretionary forecast mid-trade (exit is via stop-loss,
not forecast edits). Verify the semi-auto path enforces this or at least does not silently resize.

### 5.8 Diversification multiplier unbounded
Construct 50 near-uncorrelated subsystems. IDM must clamp to `2.5`, never blow up. Confirm the cap
is a hard `min(dm, 2.5)`, not advisory.

---

## 6. Guardrail & robustness checks

| Check | Expectation | Severity |
|---|---|---|
| G1 | Default run is dry-run; no path places live orders without explicit human gate | P0 |
| G2 | Ultra-low-volatility instrument (σ≈0) is flagged/excluded, not sized into a huge position | P0 |
| G3 | Long-only instrument: negative forecasts clamped to 0 (no shorts generated) | P1 |
| G4 | Missing/NaN price, zero price, single-row history → explicit error, not silent 0 or crash | P1 |
| G5 | Weights that don't sum to 1 → rejected or renormalised with a warning | P1 |
| G6 | Back-tested SR is discounted to "realistic" before feeding the vol-target table | P1 |
| G7 | Determinism: same inputs+config+seed ⇒ byte-identical outputs across two runs | P1 |
| G8 | Config change (e.g. swap EWMA→SMA, change a scalar) alters output with no code edit | P1 |

---

## 7. Failure taxonomy (use these labels in the report)

`WRONG_FORMULA`, `CONVENTION_MISMATCH` (percent/FX), `EWMA_ADJUST`, `ROUNDING_DISCIPLINE`,
`CAP_NOT_ENFORCED`, `FLOOR_NOT_ENFORCED`, `LOOK_AHEAD`, `MISSING_MODULE`, `PERSONA_PATH_BROKEN`,
`GUARDRAIL_MISSING`, `NONDETERMINISM`, `HARDCODED_CONFIG`, `WEAK_VALIDATION`, `NO_DIAGNOSTICS`.

---

## 8. Required audit report (deliverable)

Produce `AUDIT_REPORT.md` with exactly these sections:

1. **Verdict** — `PASS` / `CONDITIONAL PASS` / `FAIL`, plus the `% complete` score and the one-line
   justification tied to the §3 rule.
2. **Scorecard** — a table of every check (C1–C20, T1–T17, §5, §6) with: severity, PASS/FAIL,
   expected value, observed value, and evidence (file:line or repro command).
3. **P0 failures** — each with taxonomy label, minimal repro, and the exact discrepancy.
4. **P1 failures** — same detail, plus suggested remediation (description only; do not implement).
5. **P2 notes** — quality issues.
6. **Coverage gaps** — anything you could not test and why (e.g. module not reachable).
7. **Reproduction appendix** — the harness/adapters you wrote and how to re-run the whole audit.

**Do not declare PASS unless:** every P0 check passes, T17 reconciles end-to-end, and each of the
eight §5 traps has been explicitly probed (not assumed). A green happy path with untested traps is
reported as **CONDITIONAL PASS at best**, with the untested traps listed as coverage gaps.

---

*Reference framework: Carver, "Systematic Trading," Part Three (Ch. 5–12) + Appendices B–D. All
expected values in §4 are derivable from the stated inputs; verify by computation, not by trust.*
