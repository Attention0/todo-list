# Fertility Geography Project — Identification Feasibility

## Design-feasibility matrix

| Component | Fully feasible | With assumptions | Not feasible | Explanation |
|---|:---:|:---:|:---:|---|
| Births before arrival | X |  |  | Dated child histories support -5…-1; 2017 needs sensitivity |
| Births after arrival | X |  |  | Supports +1…+5; exclude move year for ordering |
| Event time | X |  |  | Relative to current-destination arrival |
| Birth pre-trend diagnostic |  | X |  | Prior location is assumed; selection/anticipation remain |
| Marriage relative to arrival |  | X |  | 2013–2016 only; unavailable 2017 |
| Marriage vs conditional fertility |  | X |  | Requires dated-marriage subset/risk sets |
| Actual prior city |  |  | X | Hukou is not last residence |
| Current-destination arrival year | X |  |  | Complete in main sample |
| Province fertility gap | X |  |  | External CBR matched for all final women |
| Prefecture mover design |  | X |  | 4,819 women from 2017; harmonization unfinished |
| Full multiple-move correction |  |  | X | Partial counts, no spell locations |
| Province external merges | X |  |  | Stable province keys |
| City external merges |  | X |  | Limited 2017 origin precision and crosswalk needed |
| Destination assimilation |  | X |  | Dynamics observed; continuous exposure assumed |
| Immediate vs gradual response |  | X |  | Estimable dynamics do not uniquely identify mechanisms |

## Identified object

The cleanest estimand is how retrospective annual birth probability changes around reported current-destination arrival among selected work migrants, differentially by an external destination-minus-hukou-origin province CBR gap. It is not a randomized place effect: there are no stayers, destinations are chosen, and repeat movers' origin exposure is mismeasured.

## Three largest threats

### Endogenous migration and anticipation

Destination and move timing can respond to marriage, pregnancy, and fertility plans. This affects every causal interpretation; the sign is unknown. Leads, marriage-linked exclusions, conception-timing checks, and reason heterogeneity are diagnostics, not solutions. Without external variation, present results as conditional mover evidence.

### Origin/exposure misclassification

Hukou province replaces residence immediately before arrival, and intermediate moves are unobserved. This contaminates the gap and the pre/post location path. Use first-leave/current-arrival comparisons, 2016 move counts, 2017 city counts, and strict-direct-move sensitivity; label the treatment destination-minus-hukou-origin.

### Retrospective and wave-specific fertility measurement

Births are retrospective; 2017 zeros come from no roster child; marriage dates are absent in 2017. Roster omission would undercount births. Preserve provenance, report exclusion of 2017, and do not use 2017 in marriage hazards.

## Required synthesis

1. **Migration event:** current-destination arrival year/month.
2. **Origin:** hukou province, not prior residence.
3. **Destination:** current destination/survey province; city name after harmonization.
4. **Marriage events:** first marriage/cohabitation year/month for 2013–2016; current status otherwise.
5. **Birth events:** child-specific year/month through parity five; roster-derived in 2017.
6. **Person-year data:** yes, already exported; annual location is assumption-dependent.
7. **Credible window:** births -5…-1 and +1…+5; move year is ambiguous; pre-location weaker for repeat movers.
8. **Pre-trend:** a lead diagnostic, not a true untreated counterfactual test.
9. **Prefecture analysis:** exploratory 2017 subset only after harmonization.
10. **Place measure:** destination minus origin province three-year pre-arrival mean CBR.
11. **Measure problems:** CBR composition, province aggregation, hukou-origin error, selected migration; no own-outcome mechanical correlation.
12. **Credible benchmark pieces:** province-gap dynamics, short-run averages, parity outcomes, strict-move robustness.
13. **Not credible:** full residence histories, complete multiple-move correction, stayers, common-wave marriage hazards, common-wave city design.
14. **Supported China mechanisms:** hukou nature, spouse education/hukou, migration reason, family stage, limited city geography.
15. **Highest-value additions:** residence spells; comparable marriage histories; city-year ASFR/TFR; access, housing, labor, childcare, and family-network data.

## Recommended boundary

Proceed with a transparent province-level study framed around arrival and hukou-origin contrast, with 2017 and strict-move sensitivities. Do not call the reconstruction a true panel, treat CBR gaps as pure norms, or infer mechanisms from event-time shape alone.
