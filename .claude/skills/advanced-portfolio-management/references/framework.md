# Framework Reference

This reference turns *Advanced Portfolio Management: A Quant's Guide for Fundamental Investors* into a reusable analysis map for active equity portfolios. Use it to choose the right lens for the user's request.

## Book Map

The public table-of-contents metadata and uploaded source point to these major modes:

- Portfolio mission: invest in edge and hedge the rest.
- Simple risk and performance measurement.
- Multi-factor models and risk decomposition.
- Factor understanding: country, industry, beta, volatility, short interest, active-manager holdings or crowdedness, momentum, and valuation.
- Alpha sizing: Sharpe ratio, expected returns, risk-based sizing, and translating ideas into positions.
- Factor-risk management: tactical hedging, strategic limits, market exposure, single-stock limits, single-factor limits, and systematic hedging.
- Performance understanding: factor attribution, idiosyncratic attribution, selection, sizing, timing, diversification, and event trading.
- Alternative data assessment.
- Drawdown and stop-loss policy.
- Sustainable leverage.

## Question Router

For "how big should this position be?"
Use position-sizing mode. Ask for expected return, horizon, volatility or tracking error contribution, liquidity, conviction, correlation with existing book, catalyst timing, and loss tolerance. If forecasts are weak, prefer risk-based sizing and show how much risk the position contributes.

For "why did the portfolio make or lose money?"
Use attribution mode. Separate factor PnL from idiosyncratic PnL first. Then analyze idiosyncratic PnL by stock selection, sizing, timing, event exposure, diversification, and transaction costs.

For "what should I hedge?"
Use separation-of-concerns mode. Identify exposures not central to the alpha thesis. Recommend hedges or constraints only after naming the cost, basis risk, liquidity, and possible impact on upside.

For "is my book too risky?"
Use risk-decomposition mode. Review gross, net, beta-adjusted net, factor concentration, single-name concentration, industry/country concentration, idiosyncratic volatility, expected shortfall or scenario loss, liquidity, borrow, and financing risk.

For "should I optimize?"
Use optimization mode. Prefer transparent heuristics when the book is small or constraints are light. Use optimization when many positions, cross-correlations, factor exposures, and constraints interact. Always state objective function and constraints.

For "what can I learn from history?"
Use learning-loop mode. Compare ex ante expectations with realized returns, risk, drawdowns, hit rate, payoff ratio, holding period, event outcomes, and trading cost. Separate skill from exposure to a favorable or unfavorable environment.

## Position Sizing Heuristics

Use these as decision support, not mechanical rules:

- Higher expected idiosyncratic return supports a larger position only if forecast quality is credible.
- Higher volatility, wider event-gap risk, poorer liquidity, crowdedness, or uncertain borrow supports a smaller position.
- Similar bets should share one risk budget; do not size each clone as if independent.
- A catalyst with binary downside should be sized by scenario loss, not by normal volatility alone.
- A long/short pair should be judged by residual risk after beta, industry, and factor exposures, not only by gross dollars.

## Factor Risk

Distinguish intended and unintended exposures:

- Intended exposure: the PM explicitly wants the factor or theme as part of the thesis.
- Unintended exposure: the portfolio inherited the exposure because multiple names share characteristics.
- Unpriced exposure: the book is paid poorly for bearing the risk, or the exposure swamps stock-selection skill.

For each material factor, report direction, size, likely PnL impact under stress, whether it is intended, hedge options, and reason to keep or reduce it.

## Performance Attribution

A useful review answers:

- Did factor returns or idiosyncratic returns drive the result?
- Were winners sized well before they worked, or only after?
- Were losses from thesis failure, timing, crowding, liquidity, factor drawdown, or event handling?
- Did diversification help, or did many positions express the same bet?
- Did trading costs, borrow, slippage, or turnover absorb the expected edge?

## Drawdown Control

Review drawdowns by cause before prescribing stops:

- Factor drawdown: hedge, resize, or decide the factor exposure is intentional.
- Idiosyncratic thesis break: exit or rewrite the thesis.
- Liquidity or crowdedness drawdown: reduce exposure before the market forces it.
- Volatility shock: lower gross, reduce correlated bets, or shift to higher-conviction names.

Stop-loss policies should define trigger, action, exception process, re-entry rule, and whether the loss reflects price noise or information.

## Leverage

Set leverage from survival constraints:

- expected portfolio volatility
- tail loss and gap risk
- financing and margin terms
- liquidity under stress
- crowding and borrow risk
- investor redemption or capital-withdrawal risk
- operational capacity to resize quickly

Do not recommend more leverage just because recent realized volatility is low.
