"""Presentation only: two frozen aggregate inputs; no raw data or estimators.

Run from any directory. Dependencies: numpy, pandas, matplotlib, Pillow.
Data-row references are one-based, excluding the CSV header.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.ticker import PercentFormatter
from PIL import Image, ImageOps

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
PRIOR = OUT.parent / 'nature_main_figures'
FILES = ['figureS_distribution_source.csv', 'figure1_main_source.csv']
FORMS = ['cash', 'food', 'medical']
AMOUNTS = [200, 1000, 5000]
NAMES = ['Cash', 'Food', 'Medical']
# Six discrete flat swatches; no continuous gradient or treatment hue in atlas.
INTENSITY = ['#F0F1F2', '#D9E1E7', '#B4C6D4', '#849FB5', '#527997', '#1F4E79']
TREATMENT = ['#1F4E79', '#2A9D8F', '#D97757']
MARKERS = ['o', 's', '^']
BIN_LABELS = ['No extra\nspending', '<10%', '10–25%', '25–50%', '50–75%', '>75%']
FULL_BINS = ['basically no additional spending', '<10%', '10–25%', '25–50%', '50–75%', '>75%']
plt.rcParams.update({'font.family': 'Arial', 'font.size': 8,
    'axes.labelsize': 8, 'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5,
    'axes.linewidth': .6, 'pdf.fonttype': 42, 'svg.fonttype': 'none',
    'savefig.facecolor': 'white', 'figure.facecolor': 'white'})

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def provenance(row, filename, data_row):
    return dict(source_file=str((PRIOR / filename).relative_to(ROOT)).replace('\\', '/'),
                source_row=int(data_row), source_commit='167ccbd993826991d43ae3d27880913a8cfe674b',
                upstream_source_file=row.source_file, upstream_source_row=int(row.source_row),
                upstream_source_commit=row.source_commit)

def load_sources():
    dist = pd.read_csv(PRIOR / FILES[0], float_precision='round_trip')
    means = pd.read_csv(PRIOR / FILES[1], float_precision='round_trip')
    hero, fingerprint = [], []
    for fi, form in enumerate(FORMS):
        for amount in AMOUNTS:
            idx = dist.index[(dist.form == form) & (dist.amount == amount)][0]
            r = dist.loc[idx]
            for b in range(1, 7):
                hero.append(dict(panel='A', statistic='category_share', form=form,
                    amount=amount, category=b, category_label=FULL_BINS[b-1],
                    estimate=r[f'p{b}'], lower_ci=np.nan, upper_ci=np.nan, N=int(r.N),
                    ci_definition='not shown; descriptive composition',
                    **provenance(r, FILES[0], idx+1)))
            ix = means.index[(means.form == form) & (means.amount == amount) & (means.outcome == 'midpoint')][0]
            m = means.loc[ix]
            hero.append(dict(panel='B', statistic='midpoint_mean', form=form, amount=amount,
                category=np.nan, category_label='', estimate=m.estimate,
                lower_ci=m.lower_ci, upper_ci=m.upper_ci, N=int(m.N),
                ci_definition=m.ci_definition, **provenance(m, FILES[1], ix+1)))
        ilo = dist.index[(dist.form == form) & (dist.amount == 200)][0]
        ihi = dist.index[(dist.form == form) & (dist.amount == 5000)][0]
        lo, hi = dist.loc[ilo], dist.loc[ihi]
        for b in range(1, 7):
            fingerprint.append(dict(panel=chr(65+fi), form=form, category=b,
                category_label=FULL_BINS[b-1], amount_low=200, amount_high=5000,
                probability_200=lo[f'p{b}'], probability_5000=hi[f'p{b}'],
                difference=hi[f'p{b}']-lo[f'p{b}'],
                difference_pp=100*(hi[f'p{b}']-lo[f'p{b}']),
                N_200=int(lo.N), N_5000=int(hi.N),
                lower_ci=np.nan, upper_ci=np.nan,
                ci_definition='none available in frozen sources; descriptive subtraction only',
                source_file=str((PRIOR/FILES[0]).relative_to(ROOT)).replace('\\', '/'),
                source_row_200=int(ilo+1), source_row_5000=int(ihi+1),
                source_commit='167ccbd993826991d43ae3d27880913a8cfe674b',
                upstream_source_file=lo.source_file, upstream_source_row_200=int(lo.source_row),
                upstream_source_row_5000=int(hi.source_row), upstream_source_commit=lo.source_commit))
    return pd.DataFrame(hero), pd.DataFrame(fingerprint)

def save(fig, name):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    box = fig.get_tightbbox(renderer)
    w, h = fig.get_size_inches()
    assert box.x0 >= 0 and box.y0 >= 0 and box.x1 <= w and box.y1 <= h, (name, box, w, h)
    for ext in ['pdf', 'svg', 'png']:
        path = OUT / f'{name}.{ext}'
        fig.savefig(path, dpi=600)
        if ext == 'svg':
            path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
    qa = OUT / 'qa'
    qa.mkdir(exist_ok=True)
    with Image.open(OUT/f'{name}.png') as im:
        ImageOps.grayscale(im).save(qa/f'{name}_grayscale.png')
        im.resize((1063, round(im.height*1063/im.width)), Image.Resampling.LANCZOS).save(qa/f'{name}_89mm_preview.png')
    plt.close(fig)

def hero_figure(src):
    fig = plt.figure(figsize=(180/25.4, 138/25.4))
    # Amount centers exactly align between atlas and summary.
    atlas = fig.add_axes([.175, .515, .775, .385])
    atlas.set_xlim(-.5, 2.5)
    atlas.set_ylim(-.38, 2.82)
    atlas.axis('off')
    fig.text(.035, .955, 'A', weight='bold', fontsize=10)
    fig.text(.095, .955, 'Stated MPC distribution', fontsize=8.5)
    for j, amount in enumerate(AMOUNTS):
        atlas.text(j, 2.7, f'¥{amount:,}', ha='center', va='center', fontsize=8)
    width, height = .80, .34
    for i, (form, name) in enumerate(zip(FORMS, NAMES)):
        y = 2-i
        atlas.text(-.61, y, name, ha='right', va='center', fontsize=8,
                   weight='bold' if form == 'cash' else 'normal')
        for j, amount in enumerate(AMOUNTS):
            shares = src[(src.panel == 'A') & (src.form == form) & (src.amount == amount)].sort_values('category').estimate
            left = j-width/2
            for b, share in enumerate(shares):
                atlas.add_patch(Rectangle((left, y-height/2), width*share, height,
                    facecolor=INTENSITY[b], edgecolor='white', linewidth=.45))
                left += width*share
            # Boundary makes the very light no-spending segment visible on white.
            atlas.add_patch(Rectangle((j-width/2, y-height/2), width, height,
                facecolor='none', edgecolor='#CBD1D6', linewidth=.35))
    endpoints = src[(src.panel == 'A') & (src.form == 'cash') & (src.category == 6)].set_index('amount').estimate
    atlas.text(0, 1.63, f'>75%: {100*endpoints[200]:.1f}%', color=INTENSITY[-1], ha='center', fontsize=7)
    atlas.text(2, 1.63, f'>75%: {100*endpoints[5000]:.1f}%', color=INTENSITY[-1], ha='center', fontsize=7)
    # All six bins retain order; single row of compact swatch labels.
    legend = fig.add_axes([.10, .446, .86, .058])
    legend.axis('off')
    for b, label in enumerate(BIN_LABELS):
        x = b/6
        legend.add_patch(Rectangle((x, .47), .018, .32, facecolor=INTENSITY[b], edgecolor='#CBD1D6', linewidth=.35))
        legend.text(x+.026, .63, label, va='center', fontsize=7,
                    weight='bold' if b == 5 else 'normal')
    fig.text(.035, .385, 'B', weight='bold', fontsize=10)
    fig.text(.095, .385, 'Midpoint-coded stated MPC', fontsize=8.5)
    ax = fig.add_axes([.175, .105, .775, .245])
    ax.set_xlim(-.5, 2.5)
    ax.set_ylim(0, .35)
    ax.set_xticks(range(3), [f'¥{a:,}' for a in AMOUNTS])
    ax.set_yticks([0, .1, .2, .3])
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.set_ylabel('Share spent', labelpad=8)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', color='#E9ECEF', linewidth=.45)
    ax.set_axisbelow(True)
    for i, form in enumerate(FORMS):
        d = src[(src.panel == 'B') & (src.form == form)].sort_values('amount')
        ax.errorbar(range(3), d.estimate, yerr=[d.estimate-d.lower_ci, d.upper_ci-d.estimate],
            color=TREATMENT[i], marker=MARKERS[i], markersize=3.6,
            linewidth=1.6 if i == 0 else 1.15, elinewidth=.65, capsize=1.7,
            label=NAMES[i])
    ax.legend(loc='upper center', bbox_to_anchor=(.5, -.22), ncol=3, frameon=False,
              fontsize=7, handlelength=2, columnspacing=2)
    save(fig, 'hero_figure')

def fingerprint_figure(src):
    fig, axes = plt.subplots(1, 3, figsize=(180/25.4, 79/25.4), sharey=True)
    fig.subplots_adjust(left=.105, right=.97, bottom=.25, top=.83, wspace=.17)
    for i, (form, ax) in enumerate(zip(FORMS, axes)):
        d = src[src.form == form].sort_values('category')
        ax.axhline(0, color='#777777', lw=.7, zorder=0)
        for b, val in enumerate(d.difference_pp):
            # Lollipops encode signed endpoint difference, NOT a transition flow.
            ax.plot([b, b], [0, val], color=INTENSITY[b], lw=1.5)
            ax.plot(b, val, 'o', color=INTENSITY[b], markersize=4.2,
                    markeredgecolor='#8996A1' if b == 0 else INTENSITY[b], markeredgewidth=.5)
        ax.set_ylim(-10, 6)
        ax.set_xlim(-.55, 5.55)
        ax.set_yticks([-10, -5, 0, 5])
        ax.set_xticks(range(6), ['None', '<10%', '10–\n25%', '25–\n50%', '50–\n75%', '>75%'], fontsize=6.8)
        ax.spines[['top', 'right', 'bottom']].set_visible(False)
        ax.tick_params(axis='x', length=0, pad=7)
        ax.grid(axis='y', color='#EDF0F2', lw=.45)
        ax.set_axisbelow(True)
        ax.text(-.045/ax.get_position().width, 1.10, chr(65+i), transform=ax.transAxes, weight='bold', fontsize=10)
        ax.text(.5, 1.10, NAMES[i], transform=ax.transAxes, ha='center', fontsize=8.5)
        tail = d.iloc[-1].difference_pp
        ax.annotate(f'{tail:.1f} pp', (5, tail), xytext=(-2, -13), textcoords='offset points', ha='center', color=INTENSITY[-1], fontsize=7)
    axes[0].set_ylabel('Change in bin share (percentage points)', fontsize=8)
    fig.text(.54, .07, '¥5,000 minus ¥200 · independent randomized cells', ha='center', fontsize=7, color='#555555')
    save(fig, 'distribution_shift_fingerprint')

def main():
    before = {f: sha(PRIOR/f) for f in FILES}
    hero, fingerprint = load_sources()
    hero.to_csv(OUT/'hero_figure_source.csv', index=False)
    fingerprint.to_csv(OUT/'distribution_shift_fingerprint_source.csv', index=False)
    hero_figure(hero)
    fingerprint_figure(fingerprint)
    after = {f: sha(PRIOR/f) for f in FILES}
    assert before == after, 'Frozen inputs changed during rendering'
    (OUT/'source_manifest.json').write_text(json.dumps(dict(
        base_commit='167ccbd993826991d43ae3d27880913a8cfe674b',
        inputs=[dict(path=str((PRIOR/f).relative_to(ROOT)).replace('\\', '/'), sha256=before[f]) for f in FILES],
        operation='reshape approved summaries and subtract approved endpoint bin probabilities only',
        empirical_estimation=False, respondent_data_read=False,
        sizes_mm={'hero_figure':[180,138], 'distribution_shift_fingerprint':[180,79]},
        dpi=600, font='Arial', intensity_palette=INTENSITY,
        means_CI='copied pointwise 95% bootstrap percentile intervals; see source ci_definition',
        fingerprint_CI='none; no new inferential procedure'), indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print('Rendered two frozen-source figures; input hashes unchanged.')

if __name__ == '__main__':
    main()
