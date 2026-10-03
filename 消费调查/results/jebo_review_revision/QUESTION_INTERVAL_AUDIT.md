# Original questionnaire interval audit

Original integrated Chinese DOCX SHA256: 4054f5c4de1f7bdc35ad3507778f03766eb2134b91da939a58b1687dd91d794a.
Read all nine versions, not just the codebook. All54 options and translations are
recorded in questionnaire_options.csv and the appendix.

Category1 is verbal “基本不会额外多消费”, with form-specific saving/debt explanations.
It is not an exact observed zero and has no numeric boundary with category2.
Category2 says “约10%以下” with a0–10% yuan example. The interior percentages and
examples are approximate. Category6 says “约75%以上” but its example ends at100%.
The verbal threshold is open; the example is not an explicit prohibition on spending
more than the transfer. No numerical separation of the bottom two bins or100% cap
will be invented.

Gate: proceed only as a sensitivity mapping. Merging categories1+2 below10% is
compatible with the ordinary meaning of “essentially no additional consumption”
and the second category's example, conditional on a respondent interpreting the
bottom verbal label below the10% threshold. This implication is not an exact
measurement fact. The five merged intervals use left censoring at.10T, then.10–.25T,
.25–.50T,.50–.75T, and right censoring at.75T. The latent normal model may permit
negative spending; its left-censored tail is not an observation of negative or zero
actual expenditure. Approximate wording and implicit horizons remain limitations.
Original six-category counts, ordinal and midpoint results remain primary observed
descriptions. No interval model creates coding-free identification.

The questionnaire describes system random selection of one of nine versions, and
one answered scenario per record. It does not document implementation probabilities,
random-number generator, allocation logs or field dates. Food has six-month expiry;
Medical is described as long-term. There is no common explicit total-spending horizon.
