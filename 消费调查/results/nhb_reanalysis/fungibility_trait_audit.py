"""Identification audit; aggregate outputs only, no fitted individual trait."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCEN=['q32_cash200','q33_cash1k','q34_cash5k','q35_vouch200','q36_vouch1k','q37_vouch5k','q38_med200','q39_med1k','q40_med5k']
FORMS=['cash','food','medical']; MID={1:0,2:.05,3:.175,4:.375,5:.625,6:.875}

def main(data,out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    d=pd.read_stata(data,convert_categoricals=False); hit=d[SCEN].notna()
    assert hit.sum(axis=1).eq(1).all()
    cell=hit.to_numpy().argmax(axis=1); d['form']=np.array(FORMS)[cell//3]; d['amount']=np.array([200,1000,5000])[cell%3]
    d['ordinal']=d[SCEN].bfill(axis=1).iloc[:,0]; d['midpoint']=d.ordinal.map(MID)
    assert np.array_equal(d.scen_mpc,d.ordinal) and np.array_equal(d.scen_amount,d.amount)
    counts=hit.astype(int); counts['id']=d.id
    perid=counts.groupby('id',dropna=False)[SCEN].sum()
    perid.sum(axis=1).value_counts().sort_index().rename_axis('observed_MPC_count_per_ID').rename('N_ID').to_csv(out/'trait_measurement_count_distribution.csv')
    pd.DataFrame([(s,FORMS[i//3],[200,1000,5000][i%3],int(hit[s].sum())) for i,s in enumerate(SCEN)],columns=['item','form','amount','N_observed']).to_csv(out/'trait_measurement_cells.csv',index=False)
    byform=pd.DataFrame({f:perid[SCEN[j*3:j*3+3]].sum(axis=1) for j,f in enumerate(FORMS)})
    pairs=[(a,b,int((byform[a].gt(0)&byform[b].gt(0)).sum())) for a in FORMS for b in FORMS]
    pd.DataFrame(pairs,columns=['form_1','form_2','N_ID_with_both']).to_csv(out/'trait_form_overlap.csv',index=False)
    pd.DataFrame([(s,int(perid[s].ge(2).sum())) for s in SCEN],columns=['item','N_ID_with_repeated_same_item']).to_csv(out/'trait_repeat_counts.csv',index=False)
    rows=[]
    for y in ['ordinal','midpoint']:
        for spec,formula in [('form',f'{y}~C(form)'),('amount',f'{y}~C(amount)'),('form_amount',f'{y}~C(form)*C(amount)')]:
            fit=smf.ols(formula,d).fit(); total=np.var(d[y],ddof=0); residual=np.mean(fit.resid**2)
            rows.append([y,spec,len(d),total,total-residual,residual,fit.rsquared,'Residual includes unmeasured person heterogeneity, measurement error and other variation; not identified noise'])
    pd.DataFrame(rows,columns=['outcome','specification','N','total_variance','between_fitted_cell_variance','unresolved_residual_variance','r2','interpretation']).to_csv(out/'trait_identified_variance_decomposition.csv',index=False)
    # Construct observationally equivalent covariance structures with identical marginals.
    # These are algebraic sensitivity examples, not estimated factor models.
    variances=d.groupby('form').midpoint.var(ddof=0).reindex(FORMS)
    sens=[]
    for share in [0,.25,.5,.75,1]:
        for f,v in variances.items(): sens.append([share,f,float(v),float(share*v),float((1-share)*v),'assumed_only_not_estimated'])
    pd.DataFrame(sens,columns=['assumed_common_factor_share','form','observed_marginal_variance','assumed_factor_variance','assumed_residual_variance','status']).to_csv(out/'trait_nonidentification_witness.csv',index=False)
    fig,ax=plt.subplots(figsize=(6,4)); mat=pd.DataFrame(pairs,columns=['a','b','N']).pivot(index='a',columns='b',values='N').reindex(index=FORMS,columns=FORMS)
    im=ax.imshow(mat,cmap='Blues'); ax.set_xticks(range(3),FORMS); ax.set_yticks(range(3),FORMS)
    for i in range(3):
        for j in range(3): ax.text(j,i,str(mat.iloc[i,j]),ha='center',va='center',color='white' if i==j else 'black')
    ax.set_title('Respondent overlap across MPC forms'); fig.colorbar(im,ax=ax,label='IDs with both forms'); fig.tight_layout(); fig.savefig(out/'trait_measurement_overlap.png',dpi=200); plt.close(fig)
    summary={'N_rows':len(d),'N_unique_ID':int(d.id.nunique(dropna=False)),'N_missing_ID':int(d.id.isna().sum()),'N_duplicate_ID_rows':int(d.id.duplicated(False).sum()),'N_rows_one_MPC':int(hit.sum(axis=1).eq(1).sum()),'N_ID_multiple_forms':int(byform.gt(0).sum(axis=1).gt(1).sum()),'N_ID_repeated_same_item':int(perid.ge(2).any(axis=1).sum()),'data_sha256':hashlib.sha256(Path(data).read_bytes()).hexdigest(),'pandas':pd.__version__,'numpy':np.__version__}
    (out/'trait_audit_manifest.json').write_text(json.dumps(summary,indent=2),encoding='utf-8'); print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('data'); p.add_argument('--out',required=True); a=p.parse_args(); main(a.data,a.out)
