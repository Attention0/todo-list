import argparse
from common import *
p=argparse.ArgumentParser();p.add_argument('--data',required=True);a=p.parse_args();d=load(a.data)
rows=[];q80=stats.norm.ppf(.8)
def add(label,pred,status,r=None,K=1,span=None,benchmark=None,source='',unit='',N=5480):
    row=dict(account=label,prediction=pred,evidence_status=status,source=source,N=N,unit=unit,family_K=K)
    if r is not None and np.isfinite(r.get('se',np.nan)):
        row.update({k:r[k] for k in ['estimate','se','lo','hi','p'] if k in r});row['MDE80_nominal']=(stats.norm.ppf(.975)+q80)*r['se'];row['MDE80_family']=(stats.norm.ppf(1-.05/(2*K))+q80)*r['se']
        if span is not None and benchmark is not None:
            row.update(moderator_p10_p90_span=span,compatible_change_lo=span*r['lo'],compatible_change_hi=span*r['hi'],headline_slope=benchmark,change_lo_over_absolute_headline=span*r['lo']/abs(benchmark),change_hi_over_absolute_headline=span*r['hi']/abs(benchmark))
    else:row['precision_limit']='Joint test has no unique scalar MDE, or estimands are not commensurate; not an exclusion/equivalence test.'
    rows.append(row)
fam=pd.read_csv(O/'scientific_family42.csv');bm=fam.query("outcome=='midpoint' and test=='cash'").estimate.iloc[0];bt=fam.query("outcome=='top75' and test=='cash'").estimate.iloc[0]
add('Fixed-yuan arithmetic','Constant midpoint-implied yuan across amounts','Midpoint-coded cell means do not fit constant yuan; weak benchmark withdrawn',source='adult_share_yuan_table.csv',unit='Not a mechanism or local MPC')
ap=pd.read_csv(O/'affine_midpoint_parameters.csv')
for _,r in ap.query("model=='form_intercepts_slopes'").iterrows():
    if '-' in r.parameter and 'slope' in r.parameter:add('Affine '+r.parameter,'Common slopes: difference=0','No affirmative slope difference; equivalence not established',r.to_dict(),3,source='affine_midpoint_parameters.csv',unit='Midpoint-implied yuan per transfer yuan')
mt=pd.read_csv(PRIOR/'mechanism_tests.csv')
for _,r in mt.iterrows():
    status='Sharp proxy sign contradicted; mechanism not excluded' if r.test=='inframarginal_triple1df' else 'No affirmative moderated interaction; precision limited'
    if r.test=='income_ABS3df':status='Pure nominal-only logit restriction rejected in historical seven-test family'
    if r.test=='income_REL3df':status='Pure ratio restriction not rejected after Holm7; not supported by equivalence'
    add(r.test,'Historical frozen restriction; see supplement for exact coefficients',status,r.to_dict(),7,source='nc_evidence_revision/mechanism_tests.csv',unit=str(r.scale),N=int(r.N))
foodspan=pd.read_csv(O/'food_bindingness_moderator_coding.csv').query("variable=='food_band_z'").iloc[0];span=foodspan.p90-foodspan.p10
for file in ['food_bindingness_continuous.csv','food_bindingness_adjusted.csv']:
    for _,r in pd.read_csv(O/file).iterrows():
        bench=fam.query("outcome==@r.outcome and test=='cash'").estimate.iloc[0]
        add('Food band '+r.outcome+(' adjusted' if r.adjusted else ''),'Higher food expenditure weakens a negative Food−Cash gradient','No affirmative continuous moderation; meaningful changes remain compatible',r.to_dict(),6,span,bench,file,'Outcome units per fivefold amount step per1SD ordered Food band',int(r.N))
# Reuse historical full-delivery baseline moderator fits; do not refit/search.
sys.path.insert(0,str(O.parent/'mpc_size_curve'));from size_curve import prepare
sys.path.insert(0,str(O.parent/'nc_revision_audit'));from secondary import covariates
full=covariates(prepare(a.data));h=pd.read_csv(O.parent/'nc_revision_audit'/'theory_moderators.csv')
for _,r in h.query("outcome=='top75' and target=='cash'").iterrows():
    s=full[r.variable].quantile(.9)-full[r.variable].quantile(.1)
    bench=pd.read_csv(PRIOR/'within_form_slopes.csv').query("sample=='R' and outcome=='top75' and test=='cash'").estimate.iloc[0]
    add('Historical '+r.variable,'Specified baseline association moderates Cash amount slope','No affirmative moderator evidence; broad compatible range',r.to_dict(),len(h),s,bench,'nc_revision_audit/theory_moderators.csv','Probability per fivefold step per1SD baseline variable; historical full delivery N5497',int(r.N))
md=pd.read_csv(PRIOR/'mechanism_details.csv')
for _,r in md[md.test.str.startswith(('Q1 ','Q2 '))].iterrows():add(r.test,'Screen-conditioned form gradient; not passage effect','Subgroup gradient imprecise; joint pass/fail difference not detected',r.to_dict(),1,source='nc_evidence_revision/mechanism_details.csv',unit='Food/Medical−Cash probability per fivefold step',N=int(r.subgroup_N))
add('Observable composition','Stable demographic moderator/predictive structure','Historical broad screen found no robust moderator; not homogeneity',source='mpc_who_drives/prediction_summary.csv; nc_revision_audit/allx_supplemental_reuse.md',unit='Different predictive estimands; no commensurate percent explained')
save(rows,'MECHANISM_PREDICTION_PRECISION_LEDGER.csv')
note('MECHANISM_PREDICTION_PRECISION_NOTE.md','# Prediction and precision\n\nScalar 80% normal-design MDE is (z0.975+z0.8)×HC3 SE; family MDE uses Bonferroni critical value with recorded K, not an achieved power claim. These are plug-in detectable effect sizes, not equivalence margins. Joint restrictions have no unique scalar MDE; historical test definitions and p values are retained without refitting. Historical baseline-moderator estimates use the original full delivery N5,497, their original full-sample standardization and matching full-sample Cash benchmark; they are explicitly separate from adult new analyses. Adult new Food estimates use within-adult Cash/Food standardization and matching adult outcome benchmarks. P10–P90 spans multiply coefficient confidence bounds where units match. These are compatible observational moderation ranges, NOT causal proportions explained. Q1/Q2 subgroup gradients cannot replace pass/fail interaction CIs; their joint nonrejections remain precision-limited. No broad screening was rerun.\n\n'+mdtable(pd.DataFrame(rows)[['account','evidence_status','MDE80_nominal','MDE80_family','compatible_change_lo','compatible_change_hi']]))
print(pd.DataFrame(rows).query("account.str.startswith('Food band')",engine='python')[['account','MDE80_nominal','compatible_change_lo','compatible_change_hi']].to_string(index=False))
