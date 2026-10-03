# Food expenditure, prediction and precision

| outcome | adjusted | estimate | lo | hi | p | holm6 |
| --- | --- | --- | --- | --- | --- | --- |
| top75 | False | 0.0028927938670750674 | -0.023308769164646637 | 0.029094356898796768 | 0.828680198106082 | 1.0 |
| top75 | True | 0.004387177366177041 | -0.02289659920048156 | 0.03167095393283564 | 0.7526370407175017 | 1.0 |
| midpoint | False | -0.009895676769286637 | -0.03258778428211425 | 0.012796430743540976 | 0.39270304406561907 | 1.0 |
| midpoint | True | -0.009036404637709449 | -0.032865099571101494 | 0.014792290295682593 | 0.45731317539354965 | 1.0 |
| ordinal | False | -0.060656632203239275 | -0.19081703505998923 | 0.06950377065351068 | 0.3610383163178338 | 1.0 |
| ordinal | True | -0.05373790114038856 | -0.19116112463932447 | 0.08368532235854734 | 0.443416137840175 | 1.0 |

Ratio restrictions, now correctly testing BOTH common and form-dependent coefficients (2df):

| mapping | outcome | p | holm6 | R2_loss | interaction_only1df_p |
| --- | --- | --- | --- | --- | --- |
| M1 | top75 | 0.02130063453401566 | 0.04260126906803132 | 0.002326849913578233 | 0.8176597826836893 |
| M1 | midpoint | 2.073676598992125e-11 | 8.2947063959685e-11 | 0.013896153328137983 | 0.8928465392735073 |
| M1 | ordinal | 5.694269945817528e-15 | 3.416561967490517e-14 | 0.01814416991859924 | 0.8545857490566886 |
| M2 | top75 | 0.04372049737649675 | 0.04372049737649675 | 0.0017653716569475675 | 0.5154172945387421 |
| M2 | midpoint | 5.895665096735667e-10 | 1.7686995290207001e-09 | 0.01166214531476939 | 0.684653945520556 |
| M2 | ordinal | 2.4211638431774063e-13 | 1.210581921588703e-12 | 0.015775470443687434 | 0.715876557449361 |

The sharp simple increasing-bindingness sign is contradicted in the historical G=0 proxy subgroup. Positive descriptive Food−Cash gradients cannot be relabelled as predicted. Continuous and adjusted tests describe observational moderation, not randomized expenditure or a mediated causal effect. Failure to reject a ratio restriction is not evidence that a ratio governs responses; all confidence intervals and model fit losses are retained. Food-band proxies are not exact expenditure and open-ended mappings are sensitivity assumptions. No additional moderators or outcomes were searched.
