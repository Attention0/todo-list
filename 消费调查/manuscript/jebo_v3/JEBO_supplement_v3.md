# Supplement to Transfer size and form in stated spending responses

## S1 Sample measurement and design details

All new calculations use the adult sample N=5,480; the full delivered sample N=5,497 is retained only when explicitly reusing historical fits. Raw respondent records and identifiers are not included in the replication outputs. The original instrument specifies one random scenario per person; exactly one is observed in each delivered record. No allocation probabilities or formal randomization logs were located.

The main article's declarations identify unresolved collection information. Hosting does not establish recruitment, balanced cells do not prove implementation, and adult-only analysis does not validate collection ethics. The authors must supply recruitment frame/vendor, dates, incentives, response flow, stopping and randomization details, approval/exemption and consent records, funding/conflicts, CRediT and sharing permissions.

The mean recorded age is 33.26 years (SD9.37; 10th–90th percentiles23–46). Category counts and original Chinese labels below preserve the two income schemes. Household size code6 denotes six or more, not exactly six. Food expenditure is monthly household food, while vouchers also permit daily necessities. City tier is an ordinal locality descriptor, not observed provincial coverage.

### Table S1a Adult characteristics and missingness

| variable | category | label | N | missing | mean | sd |
| --- | --- | --- | --- | --- | --- | --- |
| q42_age | summary | Q42 年龄（周岁，平台采集） | 5480 | 0 | 33.255 | 9.3658 |
| q41_gender | summary | Q41 性别（平台采集） | 5480 | 0 | 1.5296 | 0.49917 |
| q41_gender | 1.0 | 男 | 2578 | 0 |  |  |
| q41_gender | 2.0 | 女 | 2902 | 0 |  |  |
| q43_edu | summary | Q43 学历（平台采集） | 5480 | 0 | 3.3396 | 0.94713 |
| q43_edu | 1.0 | 初中及以下 | 218 | 0 |  |  |
| q43_edu | 2.0 | 高中/中专/技校 | 925 | 0 |  |  |
| q43_edu | 3.0 | 大学专科 | 1379 | 0 |  |  |
| q43_edu | 4.0 | 大学本科 | 2694 | 0 |  |  |
| q43_edu | 5.0 | 硕士及以上 | 264 | 0 |  |  |
| q46_income | summary | Q46 个人月收入（平台采集；1-6主档位方案，11-16为混入的旧档位方案） | 5480 | 0 | 4.0469 | 1.3185 |
| q46_income | 1.0 | 500元以下 | 221 | 0 |  |  |
| q46_income | 2.0 | 500-1000元 | 285 | 0 |  |  |
| q46_income | 3.0 | 1001-3000元 | 873 | 0 |  |  |
| q46_income | 4.0 | 3001-8000元 | 2381 | 0 |  |  |
| q46_income | 5.0 | 8001-15000元 | 1296 | 0 |  |  |
| q46_income | 6.0 | 15000元以上 | 394 | 0 |  |  |
| q46_income | 11.0 | 1000元及以下（旧方案） | 4 | 0 |  |  |
| q46_income | 12.0 | 1001-3000元（旧方案） | 5 | 0 |  |  |
| q46_income | 13.0 | 3001-5000元（旧方案） | 9 | 0 |  |  |
| q46_income | 14.0 | 5001-8000元（旧方案） | 6 | 0 |  |  |
| q46_income | 15.0 | 8001-12000元（旧方案） | 2 | 0 |  |  |
| q46_income | 16.0 | 12001-20000元（旧方案） | 4 | 0 |  |  |
| q28_hhsize | summary | Q28 共同生活、共同开支的家庭成员人数（含本人） | 5480 | 0 | 3.1772 | 1.2721 |
| q28_hhsize | 1.0 | 1人 | 550 | 0 |  |  |
| q28_hhsize | 2.0 | 2人 | 964 | 0 |  |  |
| q28_hhsize | 3.0 | 3人 | 2063 | 0 |  |  |
| q28_hhsize | 4.0 | 4人 | 1059 | 0 |  |  |
| q28_hhsize | 5.0 | 5人 | 556 | 0 |  |  |
| q28_hhsize | 6.0 | 6人及以上 | 288 | 0 |  |  |
| q24_workstat | summary | Q24 目前的工作状况 | 5480 | 0 | 1.7755 | 1.2809 |
| q24_workstat | 1.0 | 在职 | 3862 | 0 |  |  |
| q24_workstat | 2.0 | 退休 | 179 | 0 |  |  |
| q24_workstat | 3.0 | 在校学生 | 439 | 0 |  |  |
| q24_workstat | 4.0 | 失业/待业 | 807 | 0 |  |  |
| q24_workstat | 5.0 | 其他 | 193 | 0 |  |  |
| q23_hukou | summary | Q23 户籍类型 | 5480 | 0 | 1.5328 | 0.51799 |
| q23_hukou | 1.0 | 农业户口 | 2613 | 0 |  |  |
| q23_hukou | 2.0 | 非农业户口 | 2814 | 0 |  |  |
| q23_hukou | 3.0 | 其他 | 53 | 0 |  |  |
| q49_citytier | summary | Q49 城市级别（平台采集） | 5480 | 0 | 2.6206 | 1.2714 |
| q49_citytier | 1.0 | 一线城市 | 1013 | 0 |  |  |
| q49_citytier | 2.0 | 二线城市 | 2160 | 0 |  |  |
| q49_citytier | 3.0 | 三线城市 | 863 | 0 |  |  |
| q49_citytier | 4.0 | 四线城市 | 781 | 0 |  |  |
| q49_citytier | 5.0 | 五线城市 | 663 | 0 |  |  |

### Table S1b Baseline randomization diagnostics

| variable | df | p | holm8 | min_expected |
| --- | --- | --- | --- | --- |
| q42_age | 8 | 0.02947 | 0.2063 |  |
| q41_gender | 8 | 0.9067 | 1 | 272.9 |
| q43_edu | 32 | 0.7147 | 1 | 23.07 |
| q46_income | 88 | 0.3119 | 1 | 0.2117 |
| q28_hhsize | 40 | 0.08859 | 0.5315 | 30.48 |
| q24_workstat | 32 | 0.5176 | 1 | 18.95 |
| q23_hukou | 16 | 0.3065 | 1 | 5.609 |
| q49_citytier | 32 | 0.01756 | 0.1405 | 70.17 |

Note: Age uses an HC3 omnibus; categorical variables use chi-square diagnostics across nine cells. Eight tests, Holm8. Income has sparse expected cells (minimum0.212); treat that approximation cautiously. No post hoc merging or additional balance search was performed.

### Table S1c Adult nine cell scale summaries

| Form | RMB | N | Ordinal | Share % | Implied yuan | Above bottom % | Highest % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cash | 200 | 618 | 2.935 | 25.299 | 50.60 | 72.654 | 13.430 |
| Cash | 1000 | 592 | 2.802 | 22.669 | 226.69 | 71.453 | 8.953 |
| Cash | 5000 | 580 | 2.705 | 20.164 | 1008.19 | 72.586 | 5.345 |
| Food | 200 | 613 | 2.780 | 22.700 | 45.40 | 68.842 | 9.788 |
| Food | 1000 | 619 | 2.664 | 19.984 | 199.84 | 69.952 | 6.947 |
| Food | 5000 | 599 | 2.629 | 19.495 | 974.75 | 69.950 | 7.513 |
| Medical | 200 | 614 | 2.464 | 17.728 | 35.46 | 61.401 | 6.026 |
| Medical | 1000 | 611 | 2.529 | 17.827 | 178.27 | 67.103 | 5.237 |
| Medical | 5000 | 634 | 2.517 | 17.843 | 892.15 | 64.511 | 3.943 |

## S2 Yuan increments and affine fits

### Table S2a Incremental implied yuan contrasts

| form | interval | contrast | estimate | bootstrap_lo | bootstrap_hi | p | holm6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash | low | within-form | 0.2201 | 0.1929 | 0.2482 | 9.16e-54 |  |
| cash | high | within-form | 0.1954 | 0.1703 | 0.2202 | 5.435e-53 |  |
| food | low | within-form | 0.193 | 0.1683 | 0.2183 | 6.844e-51 |  |
| food | high | within-form | 0.1937 | 0.1687 | 0.2206 | 1.413e-48 |  |
| medical | low | within-form | 0.1785 | 0.1558 | 0.2024 | 6.58e-49 |  |
| medical | high | within-form | 0.1785 | 0.1567 | 0.201 | 7.181e-53 |  |
|  | low | cash-food | 0.02706 | -0.009463 | 0.06519 | 0.1588 | 0.7938 |
|  | low | cash-medical | 0.04159 | 0.006015 | 0.07847 | 0.02638 | 0.1583 |
|  | low | food-medical | 0.01453 | -0.0191 | 0.04806 | 0.4116 | 1 |
|  | high | cash-food | 0.001647 | -0.03486 | 0.03654 | 0.9286 | 1 |
|  | high | cash-medical | 0.01691 | -0.01756 | 0.05099 | 0.3279 | 1 |
|  | high | food-medical | 0.01526 | -0.01903 | 0.05043 | 0.3869 | 1 |

### Table S2b Endpoint elasticity and pairwise differences

| form | contrast | estimate | bootstrap_lo | bootstrap_hi |
| --- | --- | --- | --- | --- |
| cash | within-form | 0.9295 | 0.8872 | 0.9705 |
| food | within-form | 0.9527 | 0.9081 | 0.9958 |
| medical | within-form | 1.002 | 0.9554 | 1.046 |
|  | cash-food | -0.0232 | -0.0816 | 0.03606 |
|  | cash-medical | -0.0725 | -0.1341 | -0.009214 |
|  | food-medical | -0.04929 | -0.1108 | 0.01381 |

### Table S2c Midpoint affine parameters

| model | parameter | estimate | se | bootstrap_lo | bootstrap_hi |
| --- | --- | --- | --- | --- | --- |
| common | intercept | 8.469 | 4.658 | -0.315 | 17.48 |
| common | slope | 0.1897 | 0.006299 | 0.1772 | 0.202 |
| form_intercepts | cash intercept | 35.51 | 14.44 | 6.957 | 63.97 |
| form_intercepts | food intercept | 14.08 | 14.32 | -13.42 | 43.08 |
| form_intercepts | medical intercept | -24.24 | 14.28 | -53.34 | 3.131 |
| form_intercepts | common slope | 0.1899 | 0.006301 | 0.1774 | 0.2022 |
| form_intercepts_slopes | cash intercept | 18.73 | 8.316 | 2.735 | 35.28 |
| form_intercepts_slopes | food intercept | 6.449 | 8.356 | -10.08 | 22.53 |
| form_intercepts_slopes | medical intercept | -0.2225 | 7.518 | -14.54 | 14.53 |
| form_intercepts_slopes | cash slope | 0.1982 | 0.01105 | 0.1765 | 0.2204 |
| form_intercepts_slopes | food slope | 0.1937 | 0.01155 | 0.1716 | 0.2174 |
| form_intercepts_slopes | medical slope | 0.1785 | 0.01016 | 0.1594 | 0.1978 |
| form_intercepts_slopes | cash-food intercept | 12.28 | 11.79 | -9.658 | 35.4 |
| form_intercepts_slopes | cash-medical intercept | 18.95 | 11.21 | -2.879 | 40.62 |
| form_intercepts_slopes | food-medical intercept | 6.672 | 11.24 | -15.18 | 28.18 |
| form_intercepts_slopes | cash-food slope | 0.004573 | 0.01598 | -0.02733 | 0.0348 |
| form_intercepts_slopes | cash-medical slope | 0.01975 | 0.01501 | -0.009929 | 0.04989 |
| form_intercepts_slopes | food-medical slope | 0.01518 | 0.01539 | -0.0148 | 0.04585 |

### Table S2d Affine model comparisons

| comparison | wald | df | p | RMSE | type | holm3 |
| --- | --- | --- | --- | --- | --- | --- |
| common vs saturated cells | 40.11 | 7 | 1.2e-06 | 30.76 | diagnostic lack-of-fit |  |
| form_intercepts vs saturated cells | 7.626 | 5 | 0.1781 | 18.28 | diagnostic lack-of-fit |  |
| form_intercepts_slopes vs saturated cells | 1.381 | 3 | 0.7101 | 4.167 | diagnostic lack-of-fit |  |
| common vs form intercepts | 6.979 | 2 | 0.03051 |  | nested robust Wald | 0.06102 |
| common slope vs form slopes | 1.928 | 2 | 0.3813 |  | nested robust Wald | 0.3813 |
| common vs form intercepts and slopes | 22.77 | 4 | 0.0001409 |  | nested robust Wald | 0.0004227 |

### Table S2e Predicted and observed midpoint yuan

| model | form | amount | observed_yuan | predicted_yuan | error |
| --- | --- | --- | --- | --- | --- |
| common | cash | 200 | 50.6 | 46.41 | 4.185 |
| common | cash | 1000 | 226.7 | 198.2 | 28.5 |
| common | cash | 5000 | 1008 | 957.1 | 51.1 |
| common | food | 200 | 45.4 | 46.41 | -1.014 |
| common | food | 1000 | 199.8 | 198.2 | 1.645 |
| common | food | 5000 | 974.7 | 957.1 | 17.66 |
| common | medical | 200 | 35.46 | 46.41 | -10.96 |
| common | medical | 1000 | 178.3 | 198.2 | -19.92 |
| common | medical | 5000 | 892.2 | 957.1 | -64.94 |
| form_intercepts | cash | 200 | 50.6 | 73.49 | -22.9 |
| form_intercepts | cash | 1000 | 226.7 | 225.4 | 1.263 |
| form_intercepts | cash | 5000 | 1008 | 985.1 | 23.11 |
| form_intercepts | food | 200 | 45.4 | 52.06 | -6.659 |
| form_intercepts | food | 1000 | 199.8 | 204 | -4.151 |
| form_intercepts | food | 5000 | 974.7 | 963.6 | 11.1 |
| form_intercepts | medical | 200 | 35.46 | 13.74 | 21.72 |
| form_intercepts | medical | 1000 | 178.3 | 165.7 | 12.6 |
| form_intercepts | medical | 5000 | 892.2 | 925.3 | -33.18 |
| form_intercepts_slopes | cash | 200 | 50.6 | 58.37 | -7.774 |
| form_intercepts_slopes | cash | 1000 | 226.7 | 217 | 9.738 |
| form_intercepts_slopes | cash | 5000 | 1008 | 1010 | -1.657 |
| form_intercepts_slopes | food | 200 | 45.4 | 45.18 | 0.2203 |
| form_intercepts_slopes | food | 1000 | 199.8 | 200.1 | -0.2618 |
| form_intercepts_slopes | food | 5000 | 974.7 | 974.7 | 0.04509 |
| form_intercepts_slopes | medical | 200 | 35.46 | 35.47 | -0.01664 |
| form_intercepts_slopes | medical | 1000 | 178.3 | 178.3 | 0.02006 |
| form_intercepts_slopes | medical | 5000 | 892.2 | 892.2 | -0.003223 |

## S3 Interval affine sensitivity

The bottom category has no numeric separation from the next category. The merged five-category mapping is conditional on essentially no increase lying below10% of the transfer. The interior bounds are approximate; the top wording above75% is right-censored despite a parenthetical example ending at100%. No hard100% cap is imposed. The latent-normal lower tail permits negative values and does not claim that negative or zero actual spending was observed.

The grouped multinomial likelihood uses individual category counts. The primary scale is constant across all cells; the sole sensitivity has one sigma per amount, common across forms. Full form-intercept/form-slope and constrained common-slope models are fitted under each scale. Sandwich covariance uses individual score contributions and the observed Hessian. Both unrestricted models use4,000 independent cell-stratified bootstrap draws. All8,000 converge; the largest normalized observed-fit gradient is6.36×10−7. A fixed neutral-start retry was allowed only for numerical convergence and never changed the model or redrew samples. The per-draw convergence log is retained in aggregate replication files. Calibration is poor enough, and scale sensitivity large enough, to preclude structural interpretation.

### Table S3a Interval parameters and bootstrap precision

| model | parameter | estimate | se | bootstrap_lo | bootstrap_hi | bootstrap_valid | bootstrap_failed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| constant_full | cash intercept | -330.7 | 31.59 | -394.5 | -268.9 | 4000 | 0 |
| constant_full | food intercept | -403.8 | 32.71 | -467.1 | -341.2 | 4000 | 0 |
| constant_full | medical intercept | -530.5 | 35.34 | -600.1 | -462.7 | 4000 | 0 |
| constant_full | cash slope | 0.2271 | 0.01472 | 0.1977 | 0.2567 | 4000 | 0 |
| constant_full | food slope | 0.2311 | 0.01548 | 0.2007 | 0.2623 | 4000 | 0 |
| constant_full | medical slope | 0.241 | 0.01445 | 0.2121 | 0.269 | 4000 | 0 |
| constant_full | sigma | 1001 | 29.22 | 948.2 | 1054 | 4000 | 0 |
| constant_full | cash-food slope | -0.003961 | 0.02132 | -0.04557 | 0.03852 | 4000 | 0 |
| constant_full | cash-medical slope | -0.01394 | 0.02046 | -0.05466 | 0.02695 | 4000 | 0 |
| constant_full | food-medical slope | -0.009983 | 0.02093 | -0.05138 | 0.03182 | 4000 | 0 |
| constant_common_slope | cash intercept | -343.1 | 31.26 |  |  |  |  |
| constant_common_slope | food intercept | -408 | 31.04 |  |  |  |  |
| constant_common_slope | medical intercept | -513 | 34.25 |  |  |  |  |
| constant_common_slope | common slope | 0.2331 | 0.008715 |  |  |  |  |
| constant_common_slope | sigma | 1001 | 29.22 |  |  |  |  |
| amount_full | cash intercept | 8.456 | 5.402 | -2.148 | 19.21 | 4000 | 0 |
| amount_full | food intercept | 3.833 | 5.472 | -6.73 | 15.26 | 4000 | 0 |
| amount_full | medical intercept | -12.26 | 5.683 | -23.35 | -1.467 | 4000 | 0 |
| amount_full | cash slope | 0.09965 | 0.01443 | 0.07082 | 0.1269 | 4000 | 0 |
| amount_full | food slope | 0.07472 | 0.01455 | 0.04606 | 0.1032 | 4000 | 0 |
| amount_full | medical slope | 0.05465 | 0.01441 | 0.02612 | 0.08145 | 4000 | 0 |
| amount_full | sigma 200 | 91.76 | 3.16 | 85.61 | 97.97 | 4000 | 0 |
| amount_full | sigma 1000 | 399.9 | 13.16 | 374.6 | 426.9 | 4000 | 0 |
| amount_full | sigma 5000 | 1856 | 61.68 | 1740 | 1980 | 4000 | 0 |
| amount_full | cash-food slope | 0.02492 | 0.02034 | -0.01544 | 0.06451 | 4000 | 0 |
| amount_full | cash-medical slope | 0.045 | 0.01989 | 0.004992 | 0.08399 | 4000 | 0 |
| amount_full | food-medical slope | 0.02007 | 0.0201 | -0.01977 | 0.0593 | 4000 | 0 |
| amount_common_slope | cash intercept | 14.26 | 4.554 |  |  |  |  |
| amount_common_slope | food intercept | 3.439 | 4.628 |  |  |  |  |
| amount_common_slope | medical intercept | -17.76 | 4.924 |  |  |  |  |
| amount_common_slope | common slope | 0.07607 | 0.008629 |  |  |  |  |
| amount_common_slope | sigma 200 | 91.89 | 3.172 |  |  |  |  |
| amount_common_slope | sigma 1000 | 400.3 | 13.21 |  |  |  |  |
| amount_common_slope | sigma 5000 | 1856 | 61.66 |  |  |  |  |

### Table S3b Fit diagnostics

| model | loglik | slope_equality_p | mean_abs_probability_error | max_probability_error |
| --- | --- | --- | --- | --- |
| constant_full | -9255 | 0.7803 | 0.1015 | 0.2081 |
| constant_common_slope | -9255 |  | 0.1015 | 0.2087 |
| amount_full | -7394 | 0.07687 | 0.03999 | 0.08782 |
| amount_common_slope | -7397 |  | 0.04 | 0.0899 |

### Table S3c Merged category calibration

| model | form | amount | merged_category | observed_probability | predicted_probability | error |
| --- | --- | --- | --- | --- | --- | --- |
| constant_full | cash | 200 | 1 | 0.4531 | 0.6199 | 0.1668 |
| constant_full | cash | 200 | 2 | 0.2039 | 0.01136 | -0.1925 |
| constant_full | cash | 200 | 3 | 0.1586 | 0.01868 | -0.1399 |
| constant_full | cash | 200 | 4 | 0.05016 | 0.01832 | -0.03184 |
| constant_full | cash | 200 | 5 | 0.1343 | 0.3318 | 0.1975 |
| constant_full | cash | 1000 | 1 | 0.4797 | 0.5806 | 0.1009 |
| constant_full | cash | 1000 | 2 | 0.201 | 0.05748 | -0.1435 |
| constant_full | cash | 1000 | 3 | 0.1605 | 0.08872 | -0.07176 |
| constant_full | cash | 1000 | 4 | 0.06926 | 0.07637 | 0.007108 |
| constant_full | cash | 1000 | 5 | 0.08953 | 0.1968 | 0.1073 |
| constant_full | cash | 5000 | 1 | 0.4759 | 0.3803 | -0.09552 |
| constant_full | cash | 5000 | 2 | 0.2448 | 0.2915 | 0.04663 |
| constant_full | cash | 5000 | 3 | 0.1569 | 0.2831 | 0.1262 |
| constant_full | cash | 5000 | 4 | 0.06897 | 0.04351 | -0.02546 |
| constant_full | cash | 5000 | 5 | 0.05345 | 0.001625 | -0.05182 |
| constant_full | food | 200 | 1 | 0.4845 | 0.647 | 0.1625 |
| constant_full | food | 200 | 2 | 0.199 | 0.01107 | -0.1879 |
| constant_full | food | 200 | 3 | 0.155 | 0.01815 | -0.1368 |
| constant_full | food | 200 | 4 | 0.06362 | 0.01774 | -0.04588 |
| constant_full | food | 200 | 5 | 0.09788 | 0.306 | 0.2081 |
| constant_full | food | 1000 | 1 | 0.4992 | 0.6074 | 0.1082 |
| constant_full | food | 1000 | 2 | 0.2278 | 0.05625 | -0.1715 |
| constant_full | food | 1000 | 3 | 0.1519 | 0.08564 | -0.06621 |
| constant_full | food | 1000 | 4 | 0.0517 | 0.07247 | 0.02077 |
| constant_full | food | 1000 | 5 | 0.06947 | 0.1782 | 0.1088 |
| constant_full | food | 5000 | 1 | 0.5175 | 0.4008 | -0.1168 |
| constant_full | food | 5000 | 2 | 0.2387 | 0.29 | 0.0513 |
| constant_full | food | 5000 | 3 | 0.1152 | 0.2689 | 0.1537 |
| constant_full | food | 5000 | 4 | 0.05342 | 0.03893 | -0.01449 |
| constant_full | food | 5000 | 5 | 0.07513 | 0.001366 | -0.07376 |
| constant_full | medical | 200 | 1 | 0.57 | 0.6922 | 0.1221 |
| constant_full | medical | 200 | 2 | 0.1857 | 0.01046 | -0.1752 |
| constant_full | medical | 200 | 3 | 0.1287 | 0.01707 | -0.1116 |
| constant_full | medical | 200 | 4 | 0.05537 | 0.01658 | -0.0388 |
| constant_full | medical | 200 | 5 | 0.06026 | 0.2637 | 0.2035 |
| constant_full | medical | 1000 | 1 | 0.5368 | 0.6514 | 0.1146 |
| constant_full | medical | 1000 | 2 | 0.2275 | 0.05365 | -0.1738 |
| constant_full | medical | 1000 | 3 | 0.1293 | 0.07983 | -0.04946 |
| constant_full | medical | 1000 | 4 | 0.05401 | 0.06562 | 0.01161 |
| constant_full | medical | 1000 | 5 | 0.05237 | 0.1495 | 0.09709 |
| constant_full | medical | 5000 | 1 | 0.5221 | 0.4307 | -0.09139 |
| constant_full | medical | 5000 | 2 | 0.235 | 0.2866 | 0.0516 |
| constant_full | medical | 5000 | 3 | 0.1309 | 0.2486 | 0.1177 |
| constant_full | medical | 5000 | 4 | 0.07256 | 0.03302 | -0.03954 |
| constant_full | medical | 5000 | 5 | 0.03943 | 0.001059 | -0.03837 |
| constant_common_slope | cash | 200 | 1 | 0.4531 | 0.6241 | 0.1711 |
| constant_common_slope | cash | 200 | 2 | 0.2039 | 0.01132 | -0.1926 |
| constant_common_slope | cash | 200 | 3 | 0.1586 | 0.01861 | -0.14 |
| constant_common_slope | cash | 200 | 4 | 0.05016 | 0.01824 | -0.03192 |
| constant_common_slope | cash | 200 | 5 | 0.1343 | 0.3277 | 0.1934 |
| constant_common_slope | cash | 1000 | 1 | 0.4797 | 0.5831 | 0.1034 |
| constant_common_slope | cash | 1000 | 2 | 0.201 | 0.05738 | -0.1436 |
| constant_common_slope | cash | 1000 | 3 | 0.1605 | 0.08846 | -0.07202 |
| constant_common_slope | cash | 1000 | 4 | 0.06926 | 0.07602 | 0.00676 |
| constant_common_slope | cash | 1000 | 5 | 0.08953 | 0.195 | 0.1055 |
| constant_common_slope | cash | 5000 | 1 | 0.4759 | 0.3736 | -0.1022 |
| constant_common_slope | cash | 5000 | 2 | 0.2448 | 0.2918 | 0.04698 |
| constant_common_slope | cash | 5000 | 3 | 0.1569 | 0.2878 | 0.1309 |
| constant_common_slope | cash | 5000 | 4 | 0.06897 | 0.04508 | -0.02388 |
| constant_common_slope | cash | 5000 | 5 | 0.05345 | 0.001716 | -0.05173 |
| constant_common_slope | food | 200 | 1 | 0.4845 | 0.6485 | 0.164 |
| constant_common_slope | food | 200 | 2 | 0.199 | 0.01106 | -0.188 |
| constant_common_slope | food | 200 | 3 | 0.155 | 0.01813 | -0.1368 |
| constant_common_slope | food | 200 | 4 | 0.06362 | 0.01771 | -0.04591 |
| constant_common_slope | food | 200 | 5 | 0.09788 | 0.3046 | 0.2068 |
| constant_common_slope | food | 1000 | 1 | 0.4992 | 0.6083 | 0.1091 |
| constant_common_slope | food | 1000 | 2 | 0.2278 | 0.05622 | -0.1716 |
| constant_common_slope | food | 1000 | 3 | 0.1519 | 0.08555 | -0.0663 |
| constant_common_slope | food | 1000 | 4 | 0.0517 | 0.07235 | 0.02065 |
| constant_common_slope | food | 1000 | 5 | 0.06947 | 0.1776 | 0.1082 |
| constant_common_slope | food | 5000 | 1 | 0.5175 | 0.3985 | -0.1191 |
| constant_common_slope | food | 5000 | 2 | 0.2387 | 0.2903 | 0.05154 |
| constant_common_slope | food | 5000 | 3 | 0.1152 | 0.2705 | 0.1553 |
| constant_common_slope | food | 5000 | 4 | 0.05342 | 0.0394 | -0.01402 |
| constant_common_slope | food | 5000 | 5 | 0.07513 | 0.001391 | -0.07373 |
| constant_common_slope | medical | 200 | 1 | 0.57 | 0.6866 | 0.1165 |
| constant_common_slope | medical | 200 | 2 | 0.1857 | 0.01055 | -0.1751 |
| constant_common_slope | medical | 200 | 3 | 0.1287 | 0.01722 | -0.1114 |
| constant_common_slope | medical | 200 | 4 | 0.05537 | 0.01674 | -0.03863 |
| constant_common_slope | medical | 200 | 5 | 0.06026 | 0.2689 | 0.2087 |
| constant_common_slope | medical | 1000 | 1 | 0.5368 | 0.6479 | 0.1111 |
| constant_common_slope | medical | 1000 | 2 | 0.2275 | 0.0539 | -0.1736 |
| constant_common_slope | medical | 1000 | 3 | 0.1293 | 0.08034 | -0.04895 |
| constant_common_slope | medical | 1000 | 4 | 0.05401 | 0.06619 | 0.01218 |
| constant_common_slope | medical | 1000 | 5 | 0.05237 | 0.1517 | 0.09929 |
| constant_common_slope | medical | 5000 | 1 | 0.5221 | 0.4394 | -0.08266 |
| constant_common_slope | medical | 5000 | 2 | 0.235 | 0.2854 | 0.05036 |
| constant_common_slope | medical | 5000 | 3 | 0.1309 | 0.2428 | 0.1119 |
| constant_common_slope | medical | 5000 | 4 | 0.07256 | 0.03143 | -0.04113 |
| constant_common_slope | medical | 5000 | 5 | 0.03943 | 0.0009813 | -0.03845 |
| amount_full | cash | 200 | 1 | 0.4531 | 0.4636 | 0.01052 |
| amount_full | cash | 200 | 2 | 0.2039 | 0.1295 | -0.07436 |
| amount_full | cash | 200 | 3 | 0.1586 | 0.1893 | 0.03075 |
| amount_full | cash | 200 | 4 | 0.05016 | 0.125 | 0.07487 |
| amount_full | cash | 200 | 5 | 0.1343 | 0.09252 | -0.04178 |
| amount_full | cash | 1000 | 1 | 0.4797 | 0.4919 | 0.01219 |
| amount_full | cash | 1000 | 2 | 0.201 | 0.1467 | -0.05428 |
| amount_full | cash | 1000 | 3 | 0.1605 | 0.1978 | 0.03735 |
| amount_full | cash | 1000 | 4 | 0.06926 | 0.1093 | 0.04005 |
| amount_full | cash | 1000 | 5 | 0.08953 | 0.05422 | -0.03531 |
| amount_full | cash | 5000 | 1 | 0.4759 | 0.4986 | 0.0227 |
| amount_full | cash | 5000 | 2 | 0.2448 | 0.157 | -0.08782 |
| amount_full | cash | 5000 | 3 | 0.1569 | 0.203 | 0.04606 |
| amount_full | cash | 5000 | 4 | 0.06897 | 0.1012 | 0.03219 |
| amount_full | cash | 5000 | 5 | 0.05345 | 0.04031 | -0.01313 |
| amount_full | food | 200 | 1 | 0.4845 | 0.5053 | 0.02081 |
| amount_full | food | 200 | 2 | 0.199 | 0.1279 | -0.07116 |
| amount_full | food | 200 | 3 | 0.155 | 0.1788 | 0.02382 |
| amount_full | food | 200 | 4 | 0.06362 | 0.1117 | 0.04806 |
| amount_full | food | 200 | 5 | 0.09788 | 0.07635 | -0.02153 |
| amount_full | food | 1000 | 1 | 0.4992 | 0.5214 | 0.02219 |
| amount_full | food | 1000 | 2 | 0.2278 | 0.1446 | -0.08322 |
| amount_full | food | 1000 | 3 | 0.1519 | 0.1881 | 0.03624 |
| amount_full | food | 1000 | 4 | 0.0517 | 0.09939 | 0.04769 |
| amount_full | food | 1000 | 5 | 0.06947 | 0.04656 | -0.02291 |
| amount_full | food | 5000 | 1 | 0.5175 | 0.5263 | 0.008788 |
| amount_full | food | 5000 | 2 | 0.2387 | 0.1545 | -0.08422 |
| amount_full | food | 5000 | 3 | 0.1152 | 0.1927 | 0.07753 |
| amount_full | food | 5000 | 4 | 0.05342 | 0.09181 | 0.03839 |
| amount_full | food | 5000 | 5 | 0.07513 | 0.03463 | -0.04049 |
| amount_full | medical | 200 | 1 | 0.57 | 0.5919 | 0.02188 |
| amount_full | medical | 200 | 2 | 0.1857 | 0.1201 | -0.06552 |
| amount_full | medical | 200 | 3 | 0.1287 | 0.1532 | 0.02455 |
| amount_full | medical | 200 | 4 | 0.05537 | 0.08518 | 0.0298 |
| amount_full | medical | 200 | 5 | 0.06026 | 0.04955 | -0.01071 |
| amount_full | medical | 1000 | 1 | 0.5368 | 0.5573 | 0.02045 |
| amount_full | medical | 1000 | 2 | 0.2275 | 0.1409 | -0.08659 |
| amount_full | medical | 1000 | 3 | 0.1293 | 0.1756 | 0.04629 |
| amount_full | medical | 1000 | 4 | 0.05401 | 0.08783 | 0.03382 |
| amount_full | medical | 1000 | 5 | 0.05237 | 0.0384 | -0.01398 |
| amount_full | medical | 5000 | 1 | 0.5221 | 0.5512 | 0.02914 |
| amount_full | medical | 5000 | 2 | 0.235 | 0.1517 | -0.08334 |
| amount_full | medical | 5000 | 3 | 0.1309 | 0.1832 | 0.0523 |
| amount_full | medical | 5000 | 4 | 0.07256 | 0.0838 | 0.01124 |
| amount_full | medical | 5000 | 5 | 0.03943 | 0.03009 | -0.009338 |
| amount_common_slope | cash | 200 | 1 | 0.4531 | 0.4589 | 0.005862 |
| amount_common_slope | cash | 200 | 2 | 0.2039 | 0.1294 | -0.07444 |
| amount_common_slope | cash | 200 | 3 | 0.1586 | 0.1902 | 0.03166 |
| amount_common_slope | cash | 200 | 4 | 0.05016 | 0.1266 | 0.07641 |
| amount_common_slope | cash | 200 | 5 | 0.1343 | 0.09481 | -0.03949 |
| amount_common_slope | cash | 1000 | 1 | 0.4797 | 0.5096 | 0.02991 |
| amount_common_slope | cash | 1000 | 2 | 0.201 | 0.1454 | -0.05564 |
| amount_common_slope | cash | 1000 | 3 | 0.1605 | 0.1919 | 0.03146 |
| amount_common_slope | cash | 1000 | 4 | 0.06926 | 0.1034 | 0.03412 |
| amount_common_slope | cash | 1000 | 5 | 0.08953 | 0.04968 | -0.03984 |
| amount_common_slope | cash | 5000 | 1 | 0.4759 | 0.5226 | 0.04678 |
| amount_common_slope | cash | 5000 | 2 | 0.2448 | 0.1549 | -0.0899 |
| amount_common_slope | cash | 5000 | 3 | 0.1569 | 0.1941 | 0.03723 |
| amount_common_slope | cash | 5000 | 4 | 0.06897 | 0.09299 | 0.02403 |
| amount_common_slope | cash | 5000 | 5 | 0.05345 | 0.0353 | -0.01815 |
| amount_common_slope | food | 200 | 1 | 0.4845 | 0.5058 | 0.02134 |
| amount_common_slope | food | 200 | 2 | 0.199 | 0.1277 | -0.07136 |
| amount_common_slope | food | 200 | 3 | 0.155 | 0.1785 | 0.02352 |
| amount_common_slope | food | 200 | 4 | 0.06362 | 0.1116 | 0.04794 |
| amount_common_slope | food | 200 | 5 | 0.09788 | 0.07644 | -0.02144 |
| amount_common_slope | food | 1000 | 1 | 0.4992 | 0.5204 | 0.02122 |
| amount_common_slope | food | 1000 | 2 | 0.2278 | 0.1445 | -0.08329 |
| amount_common_slope | food | 1000 | 3 | 0.1519 | 0.1883 | 0.03647 |
| amount_common_slope | food | 1000 | 4 | 0.0517 | 0.09979 | 0.04809 |
| amount_common_slope | food | 1000 | 5 | 0.06947 | 0.04697 | -0.0225 |
| amount_common_slope | food | 5000 | 1 | 0.5175 | 0.525 | 0.007438 |
| amount_common_slope | food | 5000 | 2 | 0.2387 | 0.1547 | -0.08403 |
| amount_common_slope | food | 5000 | 3 | 0.1152 | 0.1933 | 0.07807 |
| amount_common_slope | food | 5000 | 4 | 0.05342 | 0.09223 | 0.03881 |
| amount_common_slope | food | 5000 | 5 | 0.07513 | 0.03485 | -0.04028 |
| amount_common_slope | medical | 200 | 1 | 0.57 | 0.5969 | 0.02688 |
| amount_common_slope | medical | 200 | 2 | 0.1857 | 0.1194 | -0.06629 |
| amount_common_slope | medical | 200 | 3 | 0.1287 | 0.1515 | 0.02284 |
| amount_common_slope | medical | 200 | 4 | 0.05537 | 0.08377 | 0.02839 |
| amount_common_slope | medical | 200 | 5 | 0.06026 | 0.04844 | -0.01182 |
| amount_common_slope | medical | 1000 | 1 | 0.5368 | 0.5415 | 0.004649 |
| amount_common_slope | medical | 1000 | 2 | 0.2275 | 0.1425 | -0.08499 |
| amount_common_slope | medical | 1000 | 3 | 0.1293 | 0.1811 | 0.05179 |
| amount_common_slope | medical | 1000 | 4 | 0.05401 | 0.09293 | 0.03892 |
| amount_common_slope | medical | 1000 | 5 | 0.05237 | 0.042 | -0.01037 |
| amount_common_slope | medical | 5000 | 1 | 0.5221 | 0.5295 | 0.007431 |
| amount_common_slope | medical | 5000 | 2 | 0.235 | 0.1542 | -0.08079 |
| amount_common_slope | medical | 5000 | 3 | 0.1309 | 0.1915 | 0.06063 |
| amount_common_slope | medical | 5000 | 4 | 0.07256 | 0.09074 | 0.01818 |
| amount_common_slope | medical | 5000 | 5 | 0.03943 | 0.03398 | -0.005455 |

Note: The complete table reports45 probabilities per model, including both constrained fits. Category labels are below10%,10–25%,25–50%,50–75%,above75%. Errors are predicted minus observed. No numerically successful fit is silently substituted for the primary model.

## S4 Multiplicity timing and historical inference

This study was not preregistered. Earlier analyses and reviewer revisions used the same dataset. The present bounded plan was fixed after those results were observed, before the new calculations. Freezing limits further analytic flexibility but does not retroactively preregister outcomes. The expanded family is a reviewer sensitivity, not a claim that the original findings were confirmed prospectively.

The family has42 tests, exactly seven codings by six tests. All within-form trends and pairwise contrasts use HC3 normal inference; the interaction omnibus uses chi-square2. Joint min-P retains the covariance of all21 within-form slopes across outcomes. Ten thousand centered unrestricted Gaussian-error draws generate a p-value minimum; adjusted probabilities use the plus-one correction. This calibrates degrees of freedom before combining tests and is not sharp-null randomization inference. Bonferroni42 scalar intervals provide conservative95% simultaneous coverage under the normal approximation. Holm and min-P answer family-selection questions; robustness samples and model alternatives are not added into this scientific family.

### Table S4a Complete 42 test family

| outcome | test | estimate | p | holm42 | minP42 |
| --- | --- | --- | --- | --- | --- |
| ordinal | cash | -0.1152 | 0.01141 | 0.3995 | 0.1818 |
| ordinal | food | -0.07535 | 0.09578 | 1 | 0.7362 |
| ordinal | medical | 0.02639 | 0.5332 | 1 | 0.9999 |
| ordinal | omnibus |  | 0.06029 | 1 | 0.5731 |
| ordinal | cash-food | -0.03989 | 0.5344 | 1 | 0.9999 |
| ordinal | cash-medical | -0.1416 | 0.02279 | 0.7292 | 0.3035 |
| midpoint | cash | -0.02568 | 0.0009555 | 0.03918 | 0.0199 |
| midpoint | food | -0.01607 | 0.0354 | 1 | 0.4168 |
| midpoint | medical | 0.000573 | 0.9323 | 1 | 1 |
| midpoint | omnibus |  | 0.03263 | 1 | 0.3946 |
| midpoint | cash-food | -0.009617 | 0.3776 | 1 | 0.9975 |
| midpoint | cash-medical | -0.02626 | 0.01076 | 0.3874 | 0.173 |
| any_spending | cash | -0.0004601 | 0.9716 | 1 | 1 |
| any_spending | food | 0.005562 | 0.6747 | 1 | 1 |
| any_spending | medical | 0.01533 | 0.2626 | 1 | 0.9756 |
| any_spending | omnibus |  | 0.7004 | 1 | 1 |
| any_spending | cash-food | -0.006023 | 0.7448 | 1 | 1 |
| any_spending | cash-medical | -0.01579 | 0.4012 | 1 | 0.9984 |
| ge10 | cash | -0.01155 | 0.4234 | 1 | 0.9993 |
| ge10 | food | -0.01651 | 0.2508 | 1 | 0.9709 |
| ge10 | medical | 0.02393 | 0.08964 | 1 | 0.7136 |
| ge10 | omnibus |  | 0.08959 | 1 | 0.7134 |
| ge10 | cash-food | 0.004952 | 0.8079 | 1 | 1 |
| ge10 | cash-medical | -0.03548 | 0.07862 | 1 | 0.6677 |
| ge25 | cash | -0.03178 | 0.0174 | 0.5742 | 0.2488 |
| ge25 | food | -0.0364 | 0.004693 | 0.1783 | 0.08399 |
| ge25 | medical | -0.000657 | 0.9569 | 1 | 1 |
| ge25 | omnibus |  | 0.08793 | 1 | 0.7065 |
| ge25 | cash-food | 0.004615 | 0.8036 | 1 | 1 |
| ge25 | cash-medical | -0.03112 | 0.08506 | 1 | 0.6961 |
| ge50 | cash | -0.03097 | 0.002857 | 0.1143 | 0.05349 |
| ge50 | food | -0.01657 | 0.1015 | 1 | 0.7552 |
| ge50 | medical | -0.001785 | 0.8429 | 1 | 1 |
| ge50 | omnibus |  | 0.1031 | 1 | 0.76 |
| ge50 | cash-food | -0.0144 | 0.3206 | 1 | 0.9906 |
| ge50 | cash-medical | -0.02919 | 0.0337 | 1 | 0.4031 |
| top75 | cash | -0.04047 | 1.223e-06 | 5.136e-05 | 9.999e-05 |
| top75 | food | -0.01144 | 0.1567 | 1 | 0.8821 |
| top75 | medical | -0.01043 | 0.09079 | 1 | 0.7188 |
| top75 | omnibus |  | 0.009025 | 0.3339 | 0.1486 |
| top75 | cash-food | -0.02903 | 0.01243 | 0.4225 | 0.1923 |
| top75 | cash-medical | -0.03005 | 0.003773 | 0.1471 | 0.06859 |

### Table S4b Simultaneous scalar intervals

| outcome | test | estimate | sim_lo | sim_hi |
| --- | --- | --- | --- | --- |
| ordinal | cash | -0.1152 | -0.2629 | 0.03241 |
| ordinal | food | -0.07535 | -0.222 | 0.07127 |
| ordinal | medical | 0.02639 | -0.1109 | 0.1637 |
| ordinal | cash-food | -0.03989 | -0.248 | 0.1682 |
| ordinal | cash-medical | -0.1416 | -0.3432 | 0.05997 |
| midpoint | cash | -0.02568 | -0.05089 | -0.0004833 |
| midpoint | food | -0.01607 | -0.04082 | 0.008687 |
| midpoint | medical | 0.000573 | -0.0213 | 0.02245 |
| midpoint | cash-food | -0.009617 | -0.04494 | 0.02571 |
| midpoint | cash-medical | -0.02626 | -0.05963 | 0.007112 |
| any_spending | cash | -0.0004601 | -0.04229 | 0.04137 |
| any_spending | food | 0.005562 | -0.0374 | 0.04852 |
| any_spending | medical | 0.01533 | -0.02903 | 0.0597 |
| any_spending | cash-food | -0.006023 | -0.06598 | 0.05394 |
| any_spending | cash-medical | -0.01579 | -0.07677 | 0.04518 |
| ge10 | cash | -0.01155 | -0.05833 | 0.03522 |
| ge10 | food | -0.01651 | -0.0631 | 0.03008 |
| ge10 | medical | 0.02393 | -0.02176 | 0.06962 |
| ge10 | cash-food | 0.004952 | -0.06107 | 0.07097 |
| ge10 | cash-medical | -0.03548 | -0.1009 | 0.02991 |
| ge25 | cash | -0.03178 | -0.07509 | 0.01153 |
| ge25 | food | -0.0364 | -0.07812 | 0.005327 |
| ge25 | medical | -0.000657 | -0.0401 | 0.03878 |
| ge25 | cash-food | 0.004615 | -0.05553 | 0.06476 |
| ge25 | cash-medical | -0.03112 | -0.0897 | 0.02746 |
| ge50 | cash | -0.03097 | -0.06462 | 0.002683 |
| ge50 | food | -0.01657 | -0.04937 | 0.01623 |
| ge50 | medical | -0.001785 | -0.03097 | 0.0274 |
| ge50 | cash-food | -0.0144 | -0.06139 | 0.03259 |
| ge50 | cash-medical | -0.02919 | -0.07373 | 0.01536 |
| top75 | cash | -0.04047 | -0.06751 | -0.01344 |
| top75 | food | -0.01144 | -0.03763 | 0.01474 |
| top75 | medical | -0.01043 | -0.03041 | 0.009556 |
| top75 | cash-food | -0.02903 | -0.06667 | 0.008609 |
| top75 | cash-medical | -0.03005 | -0.06367 | 0.003574 |

### Table S4c Earlier 21 interaction tests

| outcome | test | p | holm21 | minP21 | estimate |
| --- | --- | --- | --- | --- | --- |
| ordinal | omnibus | 0.06029 | 0.844 | 0.3727 |  |
| ordinal | cash-food | 0.5344 | 1 | 0.996 | -0.03989 |
| ordinal | cash-medical | 0.02279 | 0.3874 | 0.1752 | -0.1416 |
| midpoint | omnibus | 0.03263 | 0.522 | 0.2316 |  |
| midpoint | cash-food | 0.3776 | 1 | 0.9634 | -0.009617 |
| midpoint | cash-medical | 0.01076 | 0.2044 | 0.09299 | -0.02626 |
| any_spending | omnibus | 0.7004 | 1 | 1 |  |
| any_spending | cash-food | 0.7448 | 1 | 1 | -0.006023 |
| any_spending | cash-medical | 0.4012 | 1 | 0.9733 | -0.01579 |
| ge10 | omnibus | 0.08959 | 1 | 0.4932 |  |
| ge10 | cash-food | 0.8079 | 1 | 1 | 0.004952 |
| ge10 | cash-medical | 0.07862 | 1 | 0.4495 | -0.03548 |
| ge25 | omnibus | 0.08793 | 1 | 0.4868 |  |
| ge25 | cash-food | 0.8036 | 1 | 1 | 0.004615 |
| ge25 | cash-medical | 0.08506 | 1 | 0.4756 | -0.03112 |
| ge50 | omnibus | 0.1031 | 1 | 0.543 |  |
| ge50 | cash-food | 0.3206 | 1 | 0.9333 | -0.0144 |
| ge50 | cash-medical | 0.0337 | 0.522 | 0.2365 | -0.02919 |
| top75 | omnibus | 0.009025 | 0.1805 | 0.08209 |  |
| top75 | cash-food | 0.01243 | 0.2237 | 0.1055 | -0.02903 |
| top75 | cash-medical | 0.003773 | 0.07923 | 0.0391 | -0.03005 |

### Table S4d Earlier adult factorial main effects

| outcome | test | estimate | lo | hi | p | holm6 |
| --- | --- | --- | --- | --- | --- | --- |
| ordinal | food-cash | -0.1232 | -0.2254 | -0.02106 | 0.01808 |  |
| ordinal | medical-cash | -0.3109 | -0.4105 | -0.2113 | 9.555e-10 |  |
| ordinal | 1000-200 | -0.06141 | -0.1631 | 0.04031 | 0.2367 |  |
| ordinal | 5000-200 | -0.1091 | -0.2096 | -0.008629 | 0.03331 |  |
| ordinal | form_omnibus |  |  |  | 4.471e-09 |  |
| ordinal | amount_omnibus |  |  |  | 0.1037 |  |
| midpoint | food-cash | -0.01984 | -0.03713 | -0.002564 | 0.0244 |  |
| midpoint | medical-cash | -0.04911 | -0.06562 | -0.03261 | 5.48e-09 |  |
| midpoint | 1000-200 | -0.01749 | -0.03455 | -0.0004281 | 0.04452 |  |
| midpoint | 5000-200 | -0.02742 | -0.04416 | -0.01068 | 0.001328 |  |
| midpoint | form_omnibus |  |  |  | 2.197e-08 |  |
| midpoint | amount_omnibus |  |  |  | 0.005532 |  |
| any_spending | food-cash | -0.0265 | -0.05612 | 0.003129 | 0.0796 |  |
| any_spending | medical-cash | -0.07893 | -0.109 | -0.04881 | 2.791e-07 |  |
| any_spending | 1000-200 | 0.0187 | -0.0113 | 0.04871 | 0.2218 |  |
| any_spending | 5000-200 | 0.01384 | -0.01624 | 0.04391 | 0.3672 |  |
| any_spending | form_omnibus |  |  |  | 1.307e-06 |  |
| any_spending | amount_omnibus |  |  |  | 0.4485 |  |
| ge10 | food-cash | -0.03085 | -0.06345 | 0.001742 | 0.06356 |  |
| ge10 | medical-cash | -0.07342 | -0.1058 | -0.04102 | 8.963e-06 |  |
| ge10 | 1000-200 | -0.002712 | -0.03504 | 0.02961 | 0.8694 |  |
| ge10 | 5000-200 | -0.002621 | -0.035 | 0.02976 | 0.8739 |  |
| ge10 | form_omnibus |  |  |  | 4.687e-05 |  |
| ge10 | amount_omnibus |  |  |  | 0.9827 |  |
| ge25 | food-cash | -0.03612 | -0.06583 | -0.006421 | 0.01714 |  |
| ge25 | medical-cash | -0.07291 | -0.1019 | -0.0439 | 8.355e-07 |  |
| ge25 | 1000-200 | -0.02529 | -0.05456 | 0.003985 | 0.09042 |  |
| ge25 | 5000-200 | -0.04596 | -0.07495 | -0.01696 | 0.001893 |  |
| ge25 | form_omnibus |  |  |  | 5.111e-06 |  |
| ge25 | amount_omnibus |  |  |  | 0.007974 |  |
| ge50 | food-cash | -0.01815 | -0.04114 | 0.00484 | 0.1218 |  |
| ge50 | medical-cash | -0.04389 | -0.06592 | -0.02186 | 9.443e-05 |  |
| ge50 | 1000-200 | -0.02509 | -0.04761 | -0.002572 | 0.02897 |  |
| ge50 | 5000-200 | -0.03288 | -0.05517 | -0.0106 | 0.00383 |  |
| ge50 | form_omnibus |  |  |  | 0.0003733 |  |
| ge50 | amount_omnibus |  |  |  | 0.01158 |  |
| top75 | food-cash | -0.0116 | -0.02985 | 0.006645 | 0.2127 | 0.2127 |
| top75 | medical-cash | -0.04174 | -0.05837 | -0.0251 | 8.771e-07 | 4.627e-06 |
| top75 | 1000-200 | -0.02703 | -0.04492 | -0.009131 | 0.003075 | 0.006151 |
| top75 | 5000-200 | -0.04148 | -0.05864 | -0.02432 | 2.153e-06 | 8.61e-06 |
| top75 | form_omnibus |  |  |  | 7.712e-07 | 4.627e-06 |
| top75 | amount_omnibus |  |  |  | 1.307e-05 | 3.92e-05 |

### Table S4e Earlier amount specific highest category contrasts

| amount | test | estimate | lo | hi | holm6 |
| --- | --- | --- | --- | --- | --- |
| 200 | food-cash | -0.03642 | -0.07221 | -0.0006444 | 0.184 |
| 200 | medical-cash | -0.07404 | -0.1069 | -0.04117 | 6.063e-05 |
| 1000 | food-cash | -0.02006 | -0.05061 | 0.01049 | 0.3961 |
| 1000 | medical-cash | -0.03715 | -0.0662 | -0.008106 | 0.0609 |
| 5000 | food-cash | 0.02168 | -0.006311 | 0.04967 | 0.387 |
| 5000 | medical-cash | -0.01402 | -0.03782 | 0.009785 | 0.3961 |

## S5 Bottom category arithmetic

For the midpoint code, E[S]=p×m where p is above-bottom-category probability and m is the conditional-above-bottom mean. Between endpoints0 and1, the symmetric decomposition is ΔE[S]=Δp×(m1+m0)/2+Δm×(p1+p0)/2. We call the terms bottom-category and conditional-above-bottom components. The bottom code is a convention and the underlying verbal response is not an exact zero. Conditioning on a response affected by assignment does not identify a causal effect among a fixed set of respondents. The labels and neighboring percentage thresholds do not impose a common yuan cutoff across amounts. The old decomposition is reproduced arithmetically without repeating the spending-participation interpretation.

### Table S5 Bottom category decomposition

| form | above_bottom_change | conditional_above_bottom_change | bottom_category_component | conditional_above_bottom_component | total | bottom_lo | bottom_hi | conditional_lo | conditional_hi |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | -0.0006751 | -0.07043 | -0.0002113 | -0.05114 | -0.05136 | -0.01662 | 0.01598 | -0.0759 | -0.02565 |
| food | 0.01108 | -0.05104 | 0.003371 | -0.03542 | -0.03205 | -0.01152 | 0.01933 | -0.06161 | -0.009036 |
| medical | 0.0311 | -0.01214 | 0.008792 | -0.007641 | 0.00115 | -0.006381 | 0.02364 | -0.02921 | 0.01362 |

## S6 Food expenditure prediction and precision

Food−Cash is the sign convention throughout. The sharp prediction was negative in the subgroup more likely to face increasing bindingness. Historical G=0 and G=1 estimates are independently reproduced as positive8.00 and1.33pp, respectively. G=0 is failure of a conservative lower-bound proxy, not observed bindingness. The sharp prediction is contradicted conditional on the proxy, rather than confirmed. No more general bindingness model is thereby excluded.

Continuous models use all lower-order terms in form×amount-step×ordered-food-band. Adjusted models add log mapped income and ordered household size, with their full form and size interactions. Income uses the inherited M1 mapping, while household-size code6 is six or more. Standardization is within adult Cash/Food (N3,621); moderator units and10th/90th percentiles are retained below. Six focal food coefficients use Holm6. Ratio sensitivities use two frozen monthly-food proxy mappings, multiplied by six and logged. These proxy values are not observed exact expenditure. The ratio-only model requires both common and form-dependent coefficient sums to equal zero; the interaction-only restriction is not a complete model test. The one-degree-of-freedom columns apply that historical type of restriction to the new mapped-expenditure sample; the actual earlier lower-bound fit excluded the lowest food band and used N=3,476, with nominal p=0.415 (Holm7=1). These are not identical fits.

### Table S6a Food subgroup raw cells

| G | form | amount | N | ordinal | midpoint | top75 | above_bottom |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | cash | 200 | 133 | 2.714 | 0.2258 | 0.1353 | 0.6541 |
| 0 | cash | 1000 | 126 | 2.468 | 0.1782 | 0.07143 | 0.6349 |
| 0 | cash | 5000 | 135 | 2.274 | 0.1344 | 0.02222 | 0.637 |
| 0 | food | 200 | 143 | 2.217 | 0.1376 | 0.03497 | 0.5594 |
| 0 | food | 1000 | 132 | 2.462 | 0.1809 | 0.09091 | 0.6288 |
| 0 | food | 5000 | 146 | 2.37 | 0.1652 | 0.08219 | 0.5822 |
| 1 | cash | 200 | 485 | 2.996 | 0.2605 | 0.134 | 0.7464 |
| 1 | cash | 1000 | 466 | 2.893 | 0.2398 | 0.09442 | 0.7361 |
| 1 | cash | 5000 | 445 | 2.836 | 0.222 | 0.06292 | 0.7528 |
| 1 | food | 200 | 470 | 2.951 | 0.2542 | 0.117 | 0.7277 |
| 1 | food | 1000 | 487 | 2.719 | 0.205 | 0.06366 | 0.7187 |
| 1 | food | 5000 | 453 | 2.713 | 0.2045 | 0.07285 | 0.7373 |

### Table S6a continued Original six category frequencies

| G | form | amount | share1 | share2 | share3 | share4 | share5 | share6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | cash | 200 | 0.3459 | 0.1955 | 0.1654 | 0.1203 | 0.03759 | 0.1353 |
| 0 | cash | 1000 | 0.3651 | 0.2381 | 0.1508 | 0.127 | 0.04762 | 0.07143 |
| 0 | cash | 5000 | 0.363 | 0.2519 | 0.2148 | 0.1111 | 0.03704 | 0.02222 |
| 0 | food | 200 | 0.4406 | 0.2028 | 0.1538 | 0.1399 | 0.02797 | 0.03497 |
| 0 | food | 1000 | 0.3712 | 0.2424 | 0.1742 | 0.06818 | 0.05303 | 0.09091 |
| 0 | food | 5000 | 0.4178 | 0.1644 | 0.2466 | 0.05479 | 0.03425 | 0.08219 |
| 1 | cash | 200 | 0.2536 | 0.1753 | 0.2144 | 0.1691 | 0.05361 | 0.134 |
| 1 | cash | 1000 | 0.2639 | 0.1824 | 0.2146 | 0.1695 | 0.07511 | 0.09442 |
| 1 | cash | 5000 | 0.2472 | 0.1865 | 0.2539 | 0.1708 | 0.07865 | 0.06292 |
| 1 | food | 200 | 0.2723 | 0.1638 | 0.2128 | 0.1596 | 0.07447 | 0.117 |
| 1 | food | 1000 | 0.2813 | 0.1869 | 0.2423 | 0.1745 | 0.05133 | 0.06366 |
| 1 | food | 5000 | 0.2627 | 0.234 | 0.2362 | 0.1347 | 0.0596 | 0.07285 |

### Table S6b Sign reproduction

| test | N | estimate | lo | hi | p |
| --- | --- | --- | --- | --- | --- |
| Food-Cash slope G=0 | 815 | 0.08005 | 0.03829 | 0.1218 | 0.0001717 |
| Food-Cash slope G=1 | 2806 | 0.01332 | -0.01348 | 0.04013 | 0.33 |
| G1-G0 Food-Cash slope | 3621 | -0.06673 | -0.1163 | -0.01711 | 0.008396 |

### Table S6c Continuous unadjusted moderation

| outcome | estimate | se | lo | hi | sim_lo | sim_hi | p | holm6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top75 | 0.002893 | 0.01337 | -0.02331 | 0.02909 | -0.03238 | 0.03816 | 0.8287 | 1 |
| midpoint | -0.009896 | 0.01158 | -0.03259 | 0.0128 | -0.04044 | 0.02065 | 0.3927 | 1 |
| ordinal | -0.06066 | 0.06641 | -0.1908 | 0.0695 | -0.2359 | 0.1145 | 0.361 | 1 |

### Table S6d Continuous adjusted moderation

| outcome | estimate | se | lo | hi | sim_lo | sim_hi | p | holm6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top75 | 0.004387 | 0.01392 | -0.0229 | 0.03167 | -0.03234 | 0.04111 | 0.7526 | 1 |
| midpoint | -0.009036 | 0.01216 | -0.03287 | 0.01479 | -0.04111 | 0.02304 | 0.4573 | 1 |
| ordinal | -0.05374 | 0.07011 | -0.1912 | 0.08369 | -0.2387 | 0.1312 | 0.4434 | 1 |

### Table S6e Moderator scaling

| variable | source | transform | mean | sd | p10 | p90 | N |
| --- | --- | --- | --- | --- | --- | --- | --- |
| food_band_z | q29_foodexp | ordered response code | 3.398 | 1.165 | -1.2 | 1.376 | 3621 |
| income_z | income_M1 | log | 8.487 | 1.006 | -0.881 | 0.8578 | 3621 |
| household_band_z | q28_hhsize | ordered response code | 3.161 | 1.256 | -1.721 | 1.464 | 3621 |

### Table S6f Complete ratio restriction tests

| mapping | outcome | N | df | p | holm6 | R2_loss | interaction_only1df_p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | top75 | 3621 | 2 | 0.0213 | 0.0426 | 0.002327 | 0.8177 |
| M1 | midpoint | 3621 | 2 | 2.074e-11 | 8.295e-11 | 0.0139 | 0.8928 |
| M1 | ordinal | 3621 | 2 | 5.694e-15 | 3.417e-14 | 0.01814 | 0.8546 |
| M2 | top75 | 3621 | 2 | 0.04372 | 0.04372 | 0.001765 | 0.5154 |
| M2 | midpoint | 3621 | 2 | 5.896e-10 | 1.769e-09 | 0.01166 | 0.6847 |
| M2 | ordinal | 3621 | 2 | 2.421e-13 | 1.211e-12 | 0.01578 | 0.7159 |

### Table S6g Ratio coefficient pairs

| mapping | outcome | term | estimate | lo | hi |
| --- | --- | --- | --- | --- | --- |
| M1 | top75 | la | -0.02485 | -0.03496 | -0.01474 |
| M1 | top75 | lf | 0.0447 | 0.02318 | 0.06622 |
| M1 | top75 | C(form)[T.food]:la | 0.01763 | 0.003556 | 0.03171 |
| M1 | top75 | C(form)[T.food]:lf | -0.01392 | -0.04237 | 0.01453 |
| M1 | midpoint | la | -0.01553 | -0.02487 | -0.006188 |
| M1 | midpoint | lf | 0.06487 | 0.04618 | 0.08357 |
| M1 | midpoint | C(form)[T.food]:la | 0.005327 | -0.00774 | 0.01839 |
| M1 | midpoint | C(form)[T.food]:lf | -0.003372 | -0.0285 | 0.02176 |
| M1 | ordinal | la | -0.06893 | -0.1236 | -0.0143 |
| M1 | ordinal | lf | 0.4006 | 0.2932 | 0.5081 |
| M1 | ordinal | C(form)[T.food]:la | 0.02072 | -0.05613 | 0.09758 |
| M1 | ordinal | C(form)[T.food]:lf | -0.00523 | -0.1511 | 0.1406 |
| M2 | top75 | la | -0.02474 | -0.03485 | -0.01462 |
| M2 | top75 | lf | 0.03644 | 0.01764 | 0.05524 |
| M2 | top75 | C(form)[T.food]:la | 0.01757 | 0.003498 | 0.03165 |
| M2 | top75 | C(form)[T.food]:lf | -0.00818 | -0.03275 | 0.01639 |
| M2 | midpoint | la | -0.01535 | -0.02469 | -0.005997 |
| M2 | midpoint | lf | 0.05419 | 0.03792 | 0.07046 |
| M2 | midpoint | C(form)[T.food]:la | 0.005262 | -0.007812 | 0.01834 |
| M2 | midpoint | C(form)[T.food]:lf | 2.333e-05 | -0.02159 | 0.02164 |
| M2 | ordinal | la | -0.06777 | -0.1224 | -0.01308 |
| M2 | ordinal | lf | 0.3391 | 0.2457 | 0.4326 |
| M2 | ordinal | C(form)[T.food]:la | 0.0203 | -0.05659 | 0.0972 |
| M2 | ordinal | C(form)[T.food]:lf | 0.007335 | -0.1184 | 0.1331 |

## S7 Prediction and precision ledger

For scalar estimates the nominal80% normal-design minimum detectable effect is (z0.975+z0.8)×SE; the family-adjusted value uses z at1−0.05/(2K). These plug-in quantities do not constitute realized power or justify equivalence. Joint restrictions have no unique scalar MDE. Where moderator and outcome units match, the observed10th–90th span multiplies the coefficient interval and is compared with the matching Cash trend. It is a compatible observational range, not a causal proportion explained.

Historical baseline-moderator fits retain the original full delivered sample N5,497 and full-sample standardization, with a matching full-sample headline slope. They were not rerun or searched. New Food results use adult Cash/Food standardization and the adult benchmark. Joint income and screen nonrejections are retained as restrictions with no manufactured scalar precision. All-X and prediction summaries have different estimands and cannot be converted into percent explained. The ledger separates contradiction, affirmative restriction evidence, lack of affirmative moderation and inadequate precision.

### Table S7a Scalar precision

| account | N | estimate | lo | hi | family_K | MDE80_nominal | MDE80_family |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fixed-yuan arithmetic | 5480 |  |  |  | 1 |  |  |
| Affine cash-food slope | 5480 | 0.004573 | -0.02676 | 0.0359 | 3 | 0.04478 | 0.05172 |
| Affine cash-medical slope | 5480 | 0.01975 | -0.009676 | 0.04917 | 3 | 0.04206 | 0.04857 |
| Affine food-medical slope | 5480 | 0.01518 | -0.01498 | 0.04533 | 3 | 0.04311 | 0.04979 |
| income_ABS3df | 5480 |  |  |  | 7 |  |  |
| income_REL3df | 5480 |  |  |  | 7 |  |  |
| income_triple2df | 5480 |  |  |  | 7 |  |  |
| inframarginal_triple1df | 3621 | -0.06673 | -0.1163 | -0.01711 | 7 | 0.07093 | 0.08941 |
| ratio_restriction1df | 3476 | -0.01443 | -0.04911 | 0.02025 | 7 | 0.04958 | 0.0625 |
| Q1_triple2df | 5480 |  |  |  | 7 |  |  |
| Q2_triple2df | 5480 |  |  |  | 7 |  |  |
| Food band top75 | 3621 | 0.002893 | -0.02331 | 0.02909 | 6 | 0.03745 | 0.04652 |
| Food band midpoint | 3621 | -0.009896 | -0.03259 | 0.0128 | 6 | 0.03244 | 0.04029 |
| Food band ordinal | 3621 | -0.06066 | -0.1908 | 0.0695 | 6 | 0.186 | 0.2311 |
| Food band top75 adjusted | 3621 | 0.004387 | -0.0229 | 0.03167 | 6 | 0.039 | 0.04844 |
| Food band midpoint adjusted | 3621 | -0.009036 | -0.03287 | 0.01479 | 6 | 0.03406 | 0.04231 |
| Food band ordinal adjusted | 3621 | -0.05374 | -0.1912 | 0.08369 | 6 | 0.1964 | 0.244 |
| Historical income_rank_z | 5497 | 0.008321 | -0.009053 | 0.0257 | 36 | 0.02483 | 0.0358 |
| Historical fundraising | 5497 | -0.0001561 | -0.02063 | 0.02031 | 36 | 0.02926 | 0.04218 |
| Historical food_need | 5497 | -0.009032 | -0.02795 | 0.009883 | 36 | 0.02704 | 0.03897 |
| Historical medical_need | 5497 | -0.003688 | -0.02201 | 0.01463 | 36 | 0.02618 | 0.03774 |
| Q1 0 food-cash | 2765 | 0.03417 | 0.005582 | 0.06277 | 1 | 0.04087 | 0.04087 |
| Q1 0 medical-cash | 2765 | 0.03011 | 0.004076 | 0.05615 | 1 | 0.03721 | 0.03721 |
| Q1 1 food-cash | 2715 | 0.02685 | -0.008579 | 0.06228 | 1 | 0.05064 | 0.05064 |
| Q1 1 medical-cash | 2715 | 0.03022 | -0.001126 | 0.06157 | 1 | 0.04481 | 0.04481 |
| Q2 0 food-cash | 4272 | 0.03203 | 0.007554 | 0.05652 | 1 | 0.03499 | 0.03499 |
| Q2 0 medical-cash | 4272 | 0.03128 | 0.009424 | 0.05313 | 1 | 0.03124 | 0.03124 |
| Q2 1 food-cash | 1208 | 0.0308 | -0.02447 | 0.08606 | 1 | 0.07899 | 0.07899 |
| Q2 1 medical-cash | 1208 | 0.03278 | -0.01742 | 0.08298 | 1 | 0.07175 | 0.07175 |
| Observable composition | 5480 |  |  |  | 1 |  |  |

### Table S7b Compatible moderator ranges

| account | moderator_p10_p90_span | compatible_change_lo | compatible_change_hi | headline_slope |
| --- | --- | --- | --- | --- |
| Food band top75 | 2.576 | -0.06004 | 0.07495 | -0.04047 |
| Food band midpoint | 2.576 | -0.08395 | 0.03296 | -0.02568 |
| Food band ordinal | 2.576 | -0.4916 | 0.179 | -0.1152 |
| Food band top75 adjusted | 2.576 | -0.05898 | 0.08159 | -0.04047 |
| Food band midpoint adjusted | 2.576 | -0.08466 | 0.03811 | -0.02568 |
| Food band ordinal adjusted | 2.576 | -0.4924 | 0.2156 | -0.1152 |
| Historical income_rank_z | 2.318 | -0.02098 | 0.05956 | -0.04055 |
| Historical fundraising | 2.797 | -0.05769 | 0.05682 | -0.04055 |
| Historical food_need | 2.567 | -0.07174 | 0.02537 | -0.04055 |
| Historical medical_need | 2.892 | -0.06365 | 0.04231 | -0.04055 |

### Table S7c Historical adult mechanism restrictions

| test | N | df | p | holm7 | estimate | lo | hi |
| --- | --- | --- | --- | --- | --- | --- | --- |
| income_ABS3df | 5480 | 3 | 0.004244 | 0.02971 |  |  |  |
| income_REL3df | 5480 | 3 | 0.03515 | 0.1758 |  |  |  |
| income_triple2df | 5480 | 2 | 0.4708 | 1 |  |  |  |
| inframarginal_triple1df | 3621 | 1 | 0.008396 | 0.05037 | -0.06673 | -0.1163 | -0.01711 |
| ratio_restriction1df | 3476 | 1 | 0.4148 | 1 | -0.01443 | -0.04911 | 0.02025 |
| Q1_triple2df | 5480 | 2 | 0.9265 | 1 |  |  |  |
| Q2_triple2df | 5480 | 2 | 0.9943 | 1 |  |  |  |

### Table S7d Historical relative income prediction

| mapping | model | N | logloss | absolute_gain_vs_additive | relative_gain_vs_additive | absolute_gain_vs_ABS | relative_gain_vs_ABS |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | additive | 5480 | 0.2615 | 0 | 0 | -0.0001889 | -0.0007229 |
| M1 | ABS | 5480 | 0.2613 | 0.0001889 | 0.0007224 | 0 | 0 |
| M1 | REL | 5480 | 0.2609 | 0.0006373 | 0.002437 | 0.0004483 | 0.001716 |
| M1 | unrestricted | 5480 | 0.2606 | 0.0009602 | 0.003671 | 0.0007712 | 0.002951 |
| M1 | triple | 5480 | 0.2609 | 0.0006101 | 0.002333 | 0.0004212 | 0.001612 |
| M2 | additive | 5480 | 0.2615 | 0 | 0 | -0.0001889 | -0.0007229 |
| M2 | ABS | 5480 | 0.2613 | 0.0001889 | 0.0007224 | 0 | 0 |
| M2 | REL | 5480 | 0.261 | 0.0005144 | 0.001967 | 0.0003254 | 0.001245 |
| M2 | unrestricted | 5480 | 0.2607 | 0.000853 | 0.003262 | 0.0006641 | 0.002541 |
| M2 | triple | 5480 | 0.261 | 0.0005344 | 0.002043 | 0.0003454 | 0.001322 |

## S8 Response style and calibration sensitivity

Q1 requires the within-person SD across15 pre-scenario attitude responses to be at least1 and at least four distinct values. Q2 requires SD at least1.5, at least five distinct values, and no more than80% endpoints (0 or10). Components are life satisfaction, safety, three fairness items, government and social trust, social security, emergency fundraising, support, gain, effort, mobility, voice and pressure. The integrated questionnaire numbers these items before scenario32; confirmation of fielded sequence remains an author item. These are response-style screens, not comprehension or attention tests. Passing can relate to respondent type, and exclusion need not improve validity.

Adult Q1 pass/fail Ns are2,715/2,765; Q2 Ns1,208/4,272. Historical highest-category joint pass/fail interaction p values are0.927 and0.994 (Holm7=1). Subgroup gradients and their intervals below prevent interpreting this as equivalence; the strict screen is especially imprecise. Ordinal results attenuate under the strict screen. The original full grid of sample and outcome robustness remains in the aggregate replication archive without adding it to the scientific42 family.

Age×education post-stratification targets the historical census transcription and does not repair the recruitment frame or selection on unobservables. Uncapped weights have ESS314.84 and maximum51.16; cap10 gives ESS1,190.95 with maximum absolute target discrepancy0.1653. These are historical sensitivity results, not a national estimate.

### Table S8a Passed and failed screen gradients

| test | subgroup_N | estimate | lo | hi | p |
| --- | --- | --- | --- | --- | --- |
| Q1 0 food-cash | 2765 | 0.03417 | 0.005582 | 0.06277 | 0.01915 |
| Q1 0 medical-cash | 2765 | 0.03011 | 0.004076 | 0.05615 | 0.0234 |
| Q1 1 food-cash | 2715 | 0.02685 | -0.008579 | 0.06228 | 0.1374 |
| Q1 1 medical-cash | 2715 | 0.03022 | -0.001126 | 0.06157 | 0.05881 |
| Q2 0 food-cash | 4272 | 0.03203 | 0.007554 | 0.05652 | 0.01032 |
| Q2 0 medical-cash | 4272 | 0.03128 | 0.009424 | 0.05313 | 0.005029 |
| Q2 1 food-cash | 1208 | 0.0308 | -0.02447 | 0.08606 | 0.2747 |
| Q2 1 medical-cash | 1208 | 0.03278 | -0.01742 | 0.08298 | 0.2006 |

### Table S8b Screen cell counts

| screen | passed | form | amount | N | events |
| --- | --- | --- | --- | --- | --- |
| Q1 | 0 | cash | 200 | 316 | 34 |
| Q1 | 0 | cash | 1000 | 299 | 24 |
| Q1 | 0 | cash | 5000 | 295 | 9 |
| Q1 | 0 | food | 200 | 280 | 21 |
| Q1 | 0 | food | 1000 | 330 | 17 |
| Q1 | 0 | food | 5000 | 320 | 21 |
| Q1 | 0 | medical | 200 | 306 | 17 |
| Q1 | 0 | medical | 1000 | 311 | 17 |
| Q1 | 0 | medical | 5000 | 308 | 12 |
| Q1 | 1 | cash | 200 | 302 | 49 |
| Q1 | 1 | cash | 1000 | 293 | 29 |
| Q1 | 1 | cash | 5000 | 285 | 22 |
| Q1 | 1 | food | 200 | 333 | 39 |
| Q1 | 1 | food | 1000 | 289 | 26 |
| Q1 | 1 | food | 5000 | 279 | 24 |
| Q1 | 1 | medical | 200 | 308 | 20 |
| Q1 | 1 | medical | 1000 | 300 | 15 |
| Q1 | 1 | medical | 5000 | 326 | 13 |
| Q2 | 0 | cash | 200 | 498 | 60 |
| Q2 | 0 | cash | 1000 | 464 | 39 |
| Q2 | 0 | cash | 5000 | 426 | 17 |
| Q2 | 0 | food | 200 | 455 | 39 |
| Q2 | 0 | food | 1000 | 497 | 25 |
| Q2 | 0 | food | 5000 | 462 | 32 |
| Q2 | 0 | medical | 200 | 488 | 28 |
| Q2 | 0 | medical | 1000 | 477 | 25 |
| Q2 | 0 | medical | 5000 | 505 | 20 |
| Q2 | 1 | cash | 200 | 120 | 23 |
| Q2 | 1 | cash | 1000 | 128 | 14 |
| Q2 | 1 | cash | 5000 | 154 | 14 |
| Q2 | 1 | food | 200 | 158 | 21 |
| Q2 | 1 | food | 1000 | 122 | 18 |
| Q2 | 1 | food | 5000 | 137 | 13 |
| Q2 | 1 | medical | 200 | 126 | 9 |
| Q2 | 1 | medical | 1000 | 134 | 7 |
| Q2 | 1 | medical | 5000 | 129 | 5 |

### Table S8c Historical calibration diagnostics

| scheme | N | ESS | min_weight | max_weight | normalized_cap | max_abs_target_discrepancy | cap_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| unweighted | 5480 | 5480 | 1 | 1 |  | 0.3324 | 0 |
| uncapped | 5480 | 314.8 | 0.186 | 51.16 |  | 2.776e-17 | 0 |
| cap10 | 5480 | 1191 | 0.32 | 10 | 10 | 0.1653 | 0.0292 |

## S9 Original questionnaire and English translation


Chinese text is transcribed verbatim from the original integrated questionnaire. English is a translation, not a separately administered instrument. Wording and approximate numeric examples are retained.

### Randomization and common instruction

随机情景题（第 32 题，单选）
【填答说明】下面请您阅读一个简短的假设情境，并根据自己的真实想法作答。该情境仅用于学术研究中，问题没有对错之分，请根据您在类似情况下最可能的选择作答，感谢您的耐心填答。
【随机化说明】本题采用情景随机设计：系统从下列 9 个版本（3 种补贴形式 × 3 档金额：现金补贴、食品/日用消费券、医保个人账户注入，各含 200 元、1000 元、5000 元）中随机抽取一个版本呈现给每位受访者，每位受访者仅作答其中一题。在交付数据中，9 个版本分别对应第 32–40 列（题号 32–40），未被抽中的版本在该受访者的记录中为空值。

English common instruction: Read a short hypothetical scenario and answer according to your true thoughts. The scenario is used only for academic research; there are no correct or incorrect answers. Select what you would most likely do in a similar situation. System randomization selects one of nine versions (three forms by three amounts), and each respondent answers only that version; the other eight data columns are empty.

### 版本 1（数据题号 32）：现金补贴 × 200 元

【情境说明】假设政府一次性向您发放了一笔现金补贴 200 元，直接打入您的银行账户或微信/支付宝。这笔钱使用不受任何限制，可以花掉、存起来或用于还债。

S1．收到这笔 200 元现金补贴后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（因现金补贴节省的钱几乎全部存起来或用于还债）

② 补贴的小部分，约 10% 以下（约 0–20 元）

③ 补贴的一部分，约 10–25%（约 20–50 元）

④ 补贴的大约一半，约 25–50%（约 50–100 元）

⑤ 补贴的大部分，约 50–75%（约 100–150 元）

⑥ 补贴的几乎全部，约 75% 以上（约 150–200 元）

English scenario: Suppose the government gives you a one-time cash subsidy of RMB 200, paid directly into your bank account or WeChat/Alipay. Its use is unrestricted; you can spend it, save it, or repay debt.

English question: After receiving this cash subsidy of RMB 200, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (almost all the money saved because of the cash transfer is put into savings or used to repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–20)

3. A part of the subsidy, approximately 10–25% (approximately RMB 20–50)

4. About half of the subsidy, approximately 25–50% (approximately RMB 50–100)

5. Most of the subsidy, approximately 50–75% (approximately RMB 100–150)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 150–200)

### 版本 2（数据题号 33）：现金补贴 × 1000 元

【情境说明】假设政府一次性向您发放了一笔现金补贴 1000 元，直接打入您的银行账户或微信/支付宝。这笔钱使用不受任何限制，可以花掉、存起来或用于还债。

S1．收到这笔 1000 元现金补贴后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（因现金补贴节省的钱几乎全部存起来或用于还债）

② 补贴的小部分，约 10% 以下（约 0–100 元）

③ 补贴的一部分，约 10–25%（约 100–250 元）

④ 补贴的大约一半，约 25–50%（约 250–500 元）

⑤ 补贴的大部分，约 50–75%（约 500–750 元）

⑥ 补贴的几乎全部，约 75% 以上（约 750–1000 元）

English scenario: Suppose the government gives you a one-time cash subsidy of RMB 1,000, paid directly into your bank account or WeChat/Alipay. Its use is unrestricted; you can spend it, save it, or repay debt.

English question: After receiving this cash subsidy of RMB 1,000, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (almost all the money saved because of the cash transfer is put into savings or used to repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–100)

3. A part of the subsidy, approximately 10–25% (approximately RMB 100–250)

4. About half of the subsidy, approximately 25–50% (approximately RMB 250–500)

5. Most of the subsidy, approximately 50–75% (approximately RMB 500–750)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 750–1000)

### 版本 3（数据题号 34）：现金补贴 × 5000 元

【情境说明】假设政府一次性向您发放了一笔现金补贴 5000 元，直接打入您的银行账户或微信/支付宝。这笔钱使用不受任何限制，可以花掉、存起来或用于还债。

S1．收到这笔 5000 元现金补贴后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（因现金补贴节省的钱几乎全部存起来或用于还债）

② 补贴的小部分，约 10% 以下（约 0–500 元）

③ 补贴的一部分，约 10–25%（约 500–1250 元）

④ 补贴的大约一半，约 25–50%（约 1250–2500 元）

⑤ 补贴的大部分，约 50–75%（约 2500–3750 元）

⑥ 补贴的几乎全部，约 75% 以上（约 3750–5000 元）

English scenario: Suppose the government gives you a one-time cash subsidy of RMB 5,000, paid directly into your bank account or WeChat/Alipay. Its use is unrestricted; you can spend it, save it, or repay debt.

English question: After receiving this cash subsidy of RMB 5,000, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (almost all the money saved because of the cash transfer is put into savings or used to repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–500)

3. A part of the subsidy, approximately 10–25% (approximately RMB 500–1250)

4. About half of the subsidy, approximately 25–50% (approximately RMB 1250–2500)

5. Most of the subsidy, approximately 50–75% (approximately RMB 2500–3750)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 3750–5000)

### 版本 4（数据题号 35）：食品/日用消费券 × 200 元

【情境说明】假设政府一次性向您发放了一笔电子消费券，面额 200 元，仅限用于超市、菜市场、便利店等购买食品和日用品，有效期 6 个月，不能提现、不能用于其他用途。

S1．收到这笔 200 元消费券后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（用券购买原来计划要买的东西，省下的现金存起来或还债）

② 补贴的小部分，约 10% 以下（约 0–20 元）

③ 补贴的一部分，约 10–25%（约 20–50 元）

④ 补贴的大约一半，约 25–50%（约 50–100 元）

⑤ 补贴的大部分，约 50–75%（约 100–150 元）

⑥ 补贴的几乎全部，约 75% 以上（约 150–200 元）

English scenario: Suppose the government gives you a one-time electronic consumption voucher worth RMB 200, usable only for food and daily necessities at supermarkets, food markets, convenience stores and similar outlets. It is valid for six months, cannot be cashed out, and cannot be used for other purposes.

English question: After receiving this voucher of RMB 200, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (use the voucher to buy items originally planned, and save the freed cash or repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–20)

3. A part of the subsidy, approximately 10–25% (approximately RMB 20–50)

4. About half of the subsidy, approximately 25–50% (approximately RMB 50–100)

5. Most of the subsidy, approximately 50–75% (approximately RMB 100–150)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 150–200)

### 版本 5（数据题号 36）：食品/日用消费券 × 1000 元

【情境说明】假设政府一次性向您发放了一笔电子消费券，面额 1000 元，仅限用于超市、菜市场、便利店等购买食品和日用品，有效期 6 个月，不能提现、不能用于其他用途。

S1．收到这笔 1000 元消费券后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（用券购买原来计划要买的东西，省下的现金存起来或还债）

② 补贴的小部分，约 10% 以下（约 0–100 元）

③ 补贴的一部分，约 10–25%（约 100–250 元）

④ 补贴的大约一半，约 25–50%（约 250–500 元）

⑤ 补贴的大部分，约 50–75%（约 500–750 元）

⑥ 补贴的几乎全部，约 75% 以上（约 750–1000 元）

English scenario: Suppose the government gives you a one-time electronic consumption voucher worth RMB 1,000, usable only for food and daily necessities at supermarkets, food markets, convenience stores and similar outlets. It is valid for six months, cannot be cashed out, and cannot be used for other purposes.

English question: After receiving this voucher of RMB 1,000, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (use the voucher to buy items originally planned, and save the freed cash or repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–100)

3. A part of the subsidy, approximately 10–25% (approximately RMB 100–250)

4. About half of the subsidy, approximately 25–50% (approximately RMB 250–500)

5. Most of the subsidy, approximately 50–75% (approximately RMB 500–750)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 750–1000)

### 版本 6（数据题号 37）：食品/日用消费券 × 5000 元

【情境说明】假设政府一次性向您发放了一笔电子消费券，面额 5000 元，仅限用于超市、菜市场、便利店等购买食品和日用品，有效期 6 个月，不能提现、不能用于其他用途。

S1．收到这笔 5000 元消费券后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（用券购买原来计划要买的东西，省下的现金存起来或还债）

② 补贴的小部分，约 10% 以下（约 0–500 元）

③ 补贴的一部分，约 10–25%（约 500–1250 元）

④ 补贴的大约一半，约 25–50%（约 1250–2500 元）

⑤ 补贴的大部分，约 50–75%（约 2500–3750 元）

⑥ 补贴的几乎全部，约 75% 以上（约 3750–5000 元）

English scenario: Suppose the government gives you a one-time electronic consumption voucher worth RMB 5,000, usable only for food and daily necessities at supermarkets, food markets, convenience stores and similar outlets. It is valid for six months, cannot be cashed out, and cannot be used for other purposes.

English question: After receiving this voucher of RMB 5,000, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (use the voucher to buy items originally planned, and save the freed cash or repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–500)

3. A part of the subsidy, approximately 10–25% (approximately RMB 500–1250)

4. About half of the subsidy, approximately 25–50% (approximately RMB 1250–2500)

5. Most of the subsidy, approximately 50–75% (approximately RMB 2500–3750)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 3750–5000)

### 版本 7（数据题号 38）：医保个人账户注入 × 200 元

【情境说明】假设医保部门向您的医保个人账户注入 200 元。这笔钱长期有效、可以累积结余，可用于您本人及家人的医疗相关支出（看病、买药、体检、康复护理等），不能提现，不能用于医疗以外的消费。

S1．收到这笔 200 元医疗补贴后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（用补贴支付原来计划的医疗支出，省下的现金存起来或还债）

② 补贴的小部分，约 10% 以下（约 0–20 元）

③ 补贴的一部分，约 10–25%（约 20–50 元）

④ 补贴的大约一半，约 25–50%（约 50–100 元）

⑤ 补贴的大部分，约 50–75%（约 100–150 元）

⑥ 补贴的几乎全部，约 75% 以上（约 150–200 元）

English scenario: Suppose the medical-insurance authority credits RMB 200 to your medical-insurance personal account. The funds remain valid over the long term and can accumulate as a balance. They can be used for medical-related expenses for you and your family, including consultations, medicines, health checks, rehabilitation and nursing care. They cannot be cashed out or used for nonmedical consumption.

English question: After receiving this medical subsidy of RMB 200, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (use the subsidy to pay originally planned medical expenses, and save the freed cash or repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–20)

3. A part of the subsidy, approximately 10–25% (approximately RMB 20–50)

4. About half of the subsidy, approximately 25–50% (approximately RMB 50–100)

5. Most of the subsidy, approximately 50–75% (approximately RMB 100–150)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 150–200)

### 版本 8（数据题号 39）：医保个人账户注入 × 1000 元

【情境说明】假设医保部门向您的医保个人账户注入 1000 元。这笔钱长期有效、可以累积结余，可用于您本人及家人的医疗相关支出（看病、买药、体检、康复护理等），不能提现，不能用于医疗以外的消费。

S1．收到这笔 1000 元医疗补贴后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（用补贴支付原来计划的医疗支出，省下的现金存起来或还债）

② 补贴的小部分，约 10% 以下（约 0–100 元）

③ 补贴的一部分，约 10–25%（约 100–250 元）

④ 补贴的大约一半，约 25–50%（约 250–500 元）

⑤ 补贴的大部分，约 50–75%（约 500–750 元）

⑥ 补贴的几乎全部，约 75% 以上（约 750–1000 元）

English scenario: Suppose the medical-insurance authority credits RMB 1,000 to your medical-insurance personal account. The funds remain valid over the long term and can accumulate as a balance. They can be used for medical-related expenses for you and your family, including consultations, medicines, health checks, rehabilitation and nursing care. They cannot be cashed out or used for nonmedical consumption.

English question: After receiving this medical subsidy of RMB 1,000, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (use the subsidy to pay originally planned medical expenses, and save the freed cash or repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–100)

3. A part of the subsidy, approximately 10–25% (approximately RMB 100–250)

4. About half of the subsidy, approximately 25–50% (approximately RMB 250–500)

5. Most of the subsidy, approximately 50–75% (approximately RMB 500–750)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 750–1000)

### 版本 9（数据题号 40）：医保个人账户注入 × 5000 元

【情境说明】假设医保部门向您的医保个人账户注入 5000 元。这笔钱长期有效、可以累积结余，可用于您本人及家人的医疗相关支出（看病、买药、体检、康复护理等），不能提现，不能用于医疗以外的消费。

S1．收到这笔 5000 元医疗补贴后，您的【总消费】预计会比原计划多花多少钱？

① 基本不会额外多消费（用补贴支付原来计划的医疗支出，省下的现金存起来或还债）

② 补贴的小部分，约 10% 以下（约 0–500 元）

③ 补贴的一部分，约 10–25%（约 500–1250 元）

④ 补贴的大约一半，约 25–50%（约 1250–2500 元）

⑤ 补贴的大部分，约 50–75%（约 2500–3750 元）

⑥ 补贴的几乎全部，约 75% 以上（约 3750–5000 元）

English scenario: Suppose the medical-insurance authority credits RMB 5,000 to your medical-insurance personal account. The funds remain valid over the long term and can accumulate as a balance. They can be used for medical-related expenses for you and your family, including consultations, medicines, health checks, rehabilitation and nursing care. They cannot be cashed out or used for nonmedical consumption.

English question: After receiving this medical subsidy of RMB 5,000, by how many yuan do you expect your TOTAL consumption to exceed your original plan?

1. Essentially no additional consumption (use the subsidy to pay originally planned medical expenses, and save the freed cash or repay debt)

2. A small part of the subsidy, approximately below 10% (approximately RMB 0–500)

3. A part of the subsidy, approximately 10–25% (approximately RMB 500–1250)

4. About half of the subsidy, approximately 25–50% (approximately RMB 1250–2500)

5. Most of the subsidy, approximately 50–75% (approximately RMB 2500–3750)

6. Almost all of the subsidy, approximately above 75% (approximately RMB 3750–5000)


## S10 Replication definitions and declarations

Fixed seeds are2026100417 for cell/midpoint bootstrap,2026100418 for interval bootstrap, and2026100419 for the10,000 joint min-P draws. All new bootstrap cells retain their observed sizes. Original data are hash-verified against the earlier freeze; no individual records are exported. The aggregate numerical package contains exact estimates, covariance, calibration and draw-level convergence summaries, together with analysis scripts. Outcome identifiers in machine-readable tables may retain legacy names for continuity; the displayed interpretation is always above-bottom-category rather than observed participation. Author metadata and human review of the AI-assisted preparation remain pending as stated in the main draft.
