"""
experiments.py — Expériences & visualisations stylisées
Mini-projet : Planification Robuste A* + Chaînes de Markov
Étudiant : Farahi Abderahim | SDIA
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec
import warnings; warnings.filterwarnings('ignore')

from astar import make_grid, astar, ucs, greedy, weighted_astar, search
from astar import h_zero, h_manhattan, h_euclidean
from markov import (build_policy, build_transition_matrix,
                    initial_distribution, markov_distribution,
                    absorption_analysis, monte_carlo, _perpendicular)

C = {'bg':'#0F1117','panel':'#1A1D2E','a1':'#4F8EF7','a2':'#F7874F','a3':'#4FF7A0',
     'a4':'#F74F8E','obs':'#2C2F45','free':'#1E2236','start':'#4FF7A0','goal':'#F74F8E',
     'text':'#E8EAF0','sub':'#8B90A0','grid':'#2A2D3E'}

plt.rcParams.update({'figure.facecolor':C['bg'],'axes.facecolor':C['panel'],
    'axes.edgecolor':C['grid'],'axes.labelcolor':C['text'],'xtick.color':C['sub'],
    'ytick.color':C['sub'],'text.color':C['text'],'grid.color':C['grid'],'grid.alpha':.5,
    'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})

# ── GRILLES FINALES ──
def _grids():
    obs_e = [(2,c) for c in range(0,6)]+[(4,c) for c in range(2,8)]+[(6,c) for c in range(0,6)]
    obs_m = [(3,c) for c in range(0,7)]+[(7,c) for c in range(5,12)]+\
            [(1,8),(2,9),(5,2),(5,3),(9,2),(9,3),(10,9),(10,10)]
    obs_h = ([(2,c) for c in range(0,9)]+[(4,c) for c in range(3,14)]+
             [(6,c) for c in range(0,11)]+[(8,c) for c in range(2,14)]+
             [(10,c) for c in range(0,12)]+[(12,c) for c in range(3,14)]+
             [(r,5) for r in range(3,6)]+[(r,9) for r in range(7,10)]+[(r,12) for r in range(11,13)])
    return {
        'easy':  {'size':(8,8),'obs':obs_e,'start':(0,0),'goal':(7,7),
                  'label':'Facile — Zigzag (8×8)','obstacles':[o for o in obs_e if o not in [(0,0),(7,7)]]},
        'medium':{'size':(12,12),'obs':obs_m,'start':(0,0),'goal':(11,11),
                  'label':'Moyen — Labyrinthe (12×12)','obstacles':[o for o in obs_m if o not in [(0,0),(11,11)]]},
        'hard':  {'size':(15,15),'obs':obs_h,'start':(0,0),'goal':(14,14),
                  'label':'Difficile — Serpentin (15×15)','obstacles':[o for o in obs_h if o not in [(0,0),(14,14)]]},
    }

GRIDS = _grids()

def viz(ax, grid, path, start, goal, title='', show_path=True):
    rows,cols=len(grid),len(grid[0]); ax.set_facecolor(C['panel'])
    for r in range(rows):
        for c in range(cols):
            col=C['obs'] if grid[r][c]==1 else C['free']
            ec='#3A3D52' if grid[r][c]==1 else C['grid']
            ax.add_patch(plt.Rectangle((c-.5,r-.5),1,1,facecolor=col,edgecolor=ec,lw=.5,zorder=1+(grid[r][c]==1)))
    if show_path and path:
        cm=mcolors.LinearSegmentedColormap.from_list('p',['#4F8EF7','#A44FF7','#F74F8E']); n=len(path)
        for i,pos in enumerate(path):
            if pos==start or pos==goal: continue
            ax.add_patch(plt.Rectangle((pos[1]-.5,pos[0]-.5),1,1,facecolor=cm(i/max(1,n-1)),alpha=.88,edgecolor='none',zorder=3))
        step=max(1,n//7)
        for i in range(0,n-1,step):
            r0,c0=path[i]; r1,c1=path[i+1]
            ax.annotate('',xy=(c1,r1),xytext=(c0,r0),arrowprops=dict(arrowstyle='->',color='white',lw=1.2,alpha=.5),zorder=5)
    ax.plot(start[1],start[0],'o',color=C['start'],ms=14,zorder=10,markeredgecolor='white',markeredgewidth=1.5)
    ax.text(start[1],start[0],'S',ha='center',va='center',fontsize=8,fontweight='bold',color='#0F1117',zorder=11)
    ax.plot(goal[1],goal[0],'*',color=C['goal'],ms=18,zorder=10,markeredgecolor='white',markeredgewidth=1.5)
    ax.text(goal[1],goal[0],'G',ha='center',va='center',fontsize=7,fontweight='bold',color='white',zorder=11)
    ax.set_xlim(-.5,cols-.5); ax.set_ylim(rows-.5,-.5); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title,color=C['text'],fontsize=10,fontweight='bold',pad=6)
    if show_path and path:
        ax.text(.02,.02,f'Coût: {len(path)-1}',transform=ax.transAxes,fontsize=9,color=C['a3'],
                bbox=dict(boxstyle='round,pad=0.3',facecolor='#0F1117',alpha=.8),va='bottom')

def exp1_comparison():
    print('\n'+'═'*65+'\n  EXP 1 — Comparaison UCS / Greedy / A*\n'+'═'*65)
    results={}
    for gname,cfg in GRIDS.items():
        grid=make_grid(*cfg['size'],cfg['obstacles']); s,g=cfg['start'],cfg['goal']
        for aname,afn in [('UCS',ucs),('Greedy',greedy),('A*',astar)]:
            res=afn(grid,s,g); results[(gname,aname)]=res; st='✓' if res['found'] else '✗'
            print(f"  {st} {cfg['label']:<30} {aname:<8} coût={res['cost']:>4.0f}  nœuds={res['nodes_expanded']:>4}  {res['time_ms']:.3f}ms")
    fig=plt.figure(figsize=(21,16),facecolor=C['bg'])
    fig.suptitle('Expérience 1 — Comparaison des Algorithmes de Planification\nUCS vs Greedy vs A* sur 3 labyrinthes',
                 fontsize=16,fontweight='bold',color=C['text'],y=.99)
    gs=GridSpec(3,3,figure=fig,hspace=.3,wspace=.1,top=.93,bottom=.03,left=.02,right=.98)
    algo_list=['UCS','Greedy','A*']; acols={'UCS':C['a2'],'Greedy':C['a4'],'A*':C['a1']}
    for ri,(gname,cfg) in enumerate(GRIDS.items()):
        grid=make_grid(*cfg['size'],cfg['obstacles']); s,g=cfg['start'],cfg['goal']
        for ci,aname in enumerate(algo_list):
            ax=fig.add_subplot(gs[ri,ci]); res=results[(gname,aname)]
            t=f"{aname} — {cfg['label']}\n"
            t+=(f"Coût={res['cost']:.0f} | Nœuds={res['nodes_expanded']} | {res['time_ms']:.2f}ms" if res['found'] else "Non résolu ✗")
            viz(ax,grid,res['path'],s,g,t)
            for sp in ax.spines.values(): sp.set_edgecolor(acols[aname]); sp.set_linewidth(2.5); sp.set_visible(True)
    plt.savefig('exp1_grilles.png',dpi=150,bbox_inches='tight',facecolor=C['bg']); plt.close()
    fig2,axes2=plt.subplots(1,3,figsize=(18,6),facecolor=C['bg'])
    fig2.suptitle('Expérience 1 — Métriques de Performance',fontsize=15,fontweight='bold',color=C['text'])
    gnames=list(GRIDS.keys()); glabels=[GRIDS[g]['label'].split('—')[0].strip() for g in gnames]
    x=np.arange(len(gnames)); width=.25
    for ax,(metric,ylabel) in zip(axes2,[('nodes_expanded','Nœuds développés'),('cost','Coût du chemin'),('time_ms','Temps (ms)')]):
        for j,aname in enumerate(algo_list):
            vals=[results.get((gn,aname),{}).get(metric,0) for gn in gnames]
            vals=[v if v!=float('inf') else 0 for v in vals]
            bars=ax.bar(x+j*width,vals,width,label=aname,color=list(acols.values())[j],alpha=.85,edgecolor='white',lw=.5)
            for bar,v in zip(bars,vals):
                if v>0: ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+max(vals)*.01,
                    f'{v:.0f}' if metric!='time_ms' else f'{v:.3f}',ha='center',va='bottom',fontsize=8,color=C['text'])
        ax.set_xticks(x+width); ax.set_xticklabels(glabels,fontsize=10); ax.set_ylabel(ylabel)
        ax.set_title(ylabel,fontweight='bold'); ax.legend(fontsize=10); ax.grid(axis='y',alpha=.3); ax.set_facecolor(C['panel'])
    plt.tight_layout(); plt.savefig('exp1_metriques.png',dpi=150,bbox_inches='tight',facecolor=C['bg']); plt.close()
    print('  → exp1_grilles.png, exp1_metriques.png'); return results

def exp2_epsilon(cfg_name='medium',epsilons=[0.0,.1,.2,.3],n_sim=3000):
    print(f'\n'+'═'*65+f'\n  EXP 2 — Impact de ε ({cfg_name})\n'+'═'*65)
    cfg=GRIDS[cfg_name]; grid=make_grid(*cfg['size'],cfg['obstacles']); s,g=cfg['start'],cfg['goal']; rows,cols=cfg['size']
    res_a=astar(grid,s,g)
    if not res_a['found']: print('  ERREUR'); return None
    policy=build_policy(res_a['path'])
    free=[(r,c) for r in range(rows) for c in range(cols) if grid[r][c]==0 and (r,c)!=g]; N=len(free)
    print(f'  A* : coût={res_a["cost"]}, nœuds={res_a["nodes_expanded"]}')
    print(f'\n  {"ε":>5} | {"P_GOAL mat":>12} | {"P_GOAL MC":>10} | {"Tps moy":>10} | {"P_FAIL":>8}')
    print('  '+'-'*55)
    results=[]
    for eps in epsilons:
        Pm,si,GI,FI=build_transition_matrix(grid,free,g,policy,eps)
        pi0=initial_distribution(si,s,N+2); pin=markov_distribution(Pm,pi0,60)
        mc=monte_carlo(grid,free,si,policy,g,eps,n_sim=n_sim,start=s)
        print(f'  {eps:>5.2f} | {pin[GI]:>12.4f} | {mc["p_goal"]:>10.4f} | {(mc["mean_time"] or 0):>10.2f} | {mc["p_fail"]:>8.4f}')
        results.append({'eps':eps,'p_mat':pin[GI],'mc':mc,'si':si,'GI':GI,'FI':FI})
    ep_v=[r['eps'] for r in results]; pg_mat=[r['p_mat'] for r in results]
    pg_mc=[r['mc']['p_goal'] for r in results]; pf_mc=[r['mc']['p_fail'] for r in results]
    tg_mc=[r['mc']['mean_time'] or 0 for r in results]; std_mc=[r['mc']['std_time'] or 0 for r in results]
    fig=plt.figure(figsize=(22,13),facecolor=C['bg'])
    fig.suptitle(f'Expérience 2 — Impact de l\'Incertitude ε\nGrille {cfg_name} | Plan A* fixé | N={n_sim} simulations',
                 fontsize=15,fontweight='bold',color=C['text'],y=.99)
    gs=GridSpec(2,3,figure=fig,hspace=.45,wspace=.35,top=.91,bottom=.07,left=.07,right=.97)
    ax1=fig.add_subplot(gs[0,0])
    ax1.plot(ep_v,pg_mat,'o-',color=C['a1'],lw=2.5,ms=9,label='Matriciel (n=60)')
    ax1.plot(ep_v,pg_mc,'s--',color=C['a2'],lw=2.5,ms=9,label='Monte-Carlo')
    ax1.fill_between(ep_v,pg_mat,pg_mc,alpha=.15,color='white')
    ax1.set_xlabel('ε'); ax1.set_ylabel('P(atteindre GOAL)'); ax1.set_title('Probabilité d\'atteinte de GOAL',fontweight='bold')
    ax1.legend(); ax1.grid(True,alpha=.3); ax1.set_ylim(0,1.12)
    for e,pmc in zip(ep_v,pg_mc): ax1.annotate(f'{pmc:.3f}',(e,pmc),textcoords='offset points',xytext=(0,12),ha='center',fontsize=9,color=C['a2'])
    ax2=fig.add_subplot(gs[0,1]); bw=.07
    bg2=ax2.bar(ep_v,pg_mc,bw,color=C['a3'],label='P(GOAL)',alpha=.9)
    ax2.bar(ep_v,pf_mc,bw,bottom=pg_mc,color=C['a4'],label='P(FAIL)',alpha=.9)
    ax2.set_xlabel('ε'); ax2.set_ylabel('Probabilité'); ax2.set_title('Répartition GOAL / FAIL',fontweight='bold')
    ax2.legend(); ax2.grid(axis='y',alpha=.3); ax2.set_ylim(0,1.15)
    for bar,v in zip(bg2,pg_mc): ax2.text(bar.get_x()+bar.get_width()/2,v+.02,f'{v*100:.1f}%',ha='center',fontsize=9,color=C['a3'],fontweight='bold')
    ax3=fig.add_subplot(gs[0,2])
    ax3.plot(ep_v,tg_mc,'^-',color=C['a3'],lw=2.5,ms=9)
    ax3.fill_between(ep_v,[t-s2 for t,s2 in zip(tg_mc,std_mc)],[t+s2 for t,s2 in zip(tg_mc,std_mc)],alpha=.2,color=C['a3'])
    ax3.set_xlabel('ε'); ax3.set_ylabel('Temps moyen (pas)'); ax3.set_title('Temps d\'atteinte GOAL ± std',fontweight='bold'); ax3.grid(True,alpha=.3)
    for e,t in zip(ep_v,tg_mc):
        if t>0: ax3.annotate(f'{t:.1f}',(e,t),textcoords='offset points',xytext=(0,12),ha='center',fontsize=9,color=C['a3'])
    ax4=fig.add_subplot(gs[1,0]); viz(ax4,grid,res_a['path'],s,g,f'Chemin A* planifié\nCoût={res_a["cost"]} | {res_a["nodes_expanded"]} nœuds')
    for ax_gs,eps_show in [(gs[1,1],.1),(gs[1,2],.3)]:
        ax5=fig.add_subplot(ax_gs); viz(ax5,grid,[],s,g,'',show_path=False)
        rng=np.random.default_rng(99); pol_v=build_policy(res_a['path']); n_traj=15
        for _ in range(n_traj):
            pos=list(s); traj=[tuple(pos)]; reached=False; rg2,cg2=len(grid),len(grid[0])
            for __ in range(500):
                cur=(pos[0],pos[1])
                if cur==g: reached=True; break
                action=pol_v.get(cur)
                if not action: break
                perps=_perpendicular(action); rv=rng.random()
                move=action if rv<1-eps_show else (perps[0] if rv<1-eps_show/2 else perps[1])
                nr,nc=pos[0]+move[0],pos[1]+move[1]
                if not(0<=nr<rg2 and 0<=nc<cg2) or grid[nr][nc]==1: break
                pos=[nr,nc]; traj.append(tuple(pos))
            if len(traj)>1:
                ax5.plot([p[1] for p in traj],[p[0] for p in traj],'-',
                         color=C['a3'] if reached else C['a4'],alpha=.45,lw=1.2,zorder=4)
        ax5.plot([],[],'-',color=C['a3'],alpha=.8,lw=2,label='Atteint GOAL')
        ax5.plot([],[],'-',color=C['a4'],alpha=.8,lw=2,label='Échoué (FAIL)')
        r_s=next(r for r in results if abs(r['eps']-eps_show)<.01)
        ax5.set_title(f'Trajectoires MC (ε={eps_show})\nP(GOAL)={r_s["mc"]["p_goal"]*100:.1f}% | N={n_sim}',fontweight='bold')
        ax5.legend(fontsize=8,loc='upper right')
    plt.savefig('exp2_epsilon.png',dpi=150,bbox_inches='tight',facecolor=C['bg']); plt.close()
    print('  → exp2_epsilon.png'); return results

def exp3_heuristics():
    print('\n'+'═'*65+'\n  EXP 3 — Comparaison des heuristiques\n'+'═'*65)
    hcfg=[('h=0 (UCS)',h_zero,1.,'Oui',C['a2']),('Manhattan',h_manhattan,1.,'Oui',C['a1']),
          ('Euclidienne',h_euclidean,1.,'Oui',C['a3']),('Weighted×1.5',h_manhattan,1.5,'Non',C['a4'])]
    exp3={}
    print(f'\n  {"Grille":<32} {"Heuristique":<16} {"Coût":>5} {"Nœuds":>6} {"Admissible":>11}')
    print('  '+'-'*74)
    for gname,cfg in GRIDS.items():
        exp3[gname]={}; grid=make_grid(*cfg['size'],cfg['obstacles']); s,g=cfg['start'],cfg['goal']
        for h_name,h_fn,w,adm,_ in hcfg:
            res=search(grid,s,g,h_fn,weight=w); exp3[gname][h_name]=res
            print(f'  {cfg["label"]:<32} {h_name:<16} {res["cost"]:>5.0f} {res["nodes_expanded"]:>6} {adm:>11}')
    fig,axes=plt.subplots(1,3,figsize=(18,6),facecolor=C['bg'])
    fig.suptitle('Expérience 3 — Comparaison des Heuristiques',fontsize=15,fontweight='bold',color=C['text'])
    h_names=[c[0] for c in hcfg]; hcols={c[0]:c[4] for c in hcfg}
    x=np.arange(len(GRIDS)); width=.2; glabels=[GRIDS[g]['label'].split('—')[0].strip() for g in GRIDS]
    for (metric,ylabel),ax in zip([('nodes_expanded','Nœuds développés'),('cost','Coût du chemin'),('time_ms','Temps (ms)')],axes):
        for j,h_name in enumerate(h_names):
            vals=[exp3[gn].get(h_name,{}).get(metric,0) for gn in GRIDS]; vals=[v if v!=float('inf') else 0 for v in vals]
            bars=ax.bar(x+j*width,vals,width,label=h_name,color=hcols[h_name],alpha=.85,edgecolor='white',lw=.5)
            for bar,v in zip(bars,vals):
                if v>0: ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+max(vals)*.01,
                    f'{v:.0f}' if metric!='time_ms' else f'{v:.3f}',ha='center',va='bottom',fontsize=7.5,color=C['text'])
        ax.set_xticks(x+1.5*width); ax.set_xticklabels(glabels,fontsize=10); ax.set_ylabel(ylabel)
        ax.set_title(ylabel,fontweight='bold'); ax.legend(fontsize=9); ax.grid(axis='y',alpha=.3); ax.set_facecolor(C['panel'])
    plt.tight_layout(); plt.savefig('exp3_heuristics.png',dpi=150,bbox_inches='tight',facecolor=C['bg']); plt.close()
    print('  → exp3_heuristics.png'); return exp3

def exp4_absorption(cfg_name='medium',epsilon=.1):
    print(f'\n'+'═'*65+f'\n  EXP 4 — Absorption (ε={epsilon}, {cfg_name})\n'+'═'*65)
    cfg=GRIDS[cfg_name]; grid=make_grid(*cfg['size'],cfg['obstacles']); s,g=cfg['start'],cfg['goal']; rows,cols=cfg['size']
    res=astar(grid,s,g)
    if not res['found']: print('  Chemin non trouvé'); return
    policy=build_policy(res['path']); free=[(r,c) for r in range(rows) for c in range(cols) if grid[r][c]==0 and (r,c)!=g]
    N_st=len(free); Pm,si,GI,FI=build_transition_matrix(grid,free,g,policy,epsilon); Nmat,B,t_abs=absorption_analysis(Pm,N_st)
    if s in si:
        i0=si[s]; print(f'  s₀={s}: P(GOAL)={B[i0,0]:.4f} | P(FAIL)={B[i0,1]:.4f} | Tps={t_abs[i0]:.2f} pas')
    pg_map=np.full((rows,cols),np.nan); t_map=np.full((rows,cols),np.nan)
    for pos,idx in si.items(): pg_map[pos[0],pos[1]]=B[idx,0]; t_map[pos[0],pos[1]]=t_abs[idx]
    pg_map[g[0],g[1]]=1.0
    fig,axes=plt.subplots(1,2,figsize=(16,7),facecolor=C['bg'])
    fig.suptitle(f'Expérience 4 — Analyse d\'Absorption | {cfg["label"]} | ε={epsilon}',fontsize=14,fontweight='bold',color=C['text'])
    for ax,data,cm_name,title_ax,fmt,vmax_mult in [
        (axes[0],pg_map,['#F74F8E','#F7874F','#4FF7A0'],'P(atteindre GOAL) par état','.3f',1.0),
        (axes[1],t_map,['#4F8EF7','#A44FF7','#F74F8E'],'Temps moyen absorption (pas)','.1f',1.0)]:
        ax.set_facecolor(C['panel'])
        cmap=mcolors.LinearSegmentedColormap.from_list('c',cm_name)
        masked=np.ma.masked_invalid(data)
        vmax=np.nanmax(data) if not np.all(np.isnan(data)) else 1
        im=ax.imshow(masked,cmap=cmap,origin='upper',vmin=0,vmax=vmax)
        for r in range(rows):
            for c in range(cols):
                if grid[r][c]==1: ax.add_patch(plt.Rectangle((c-.5,r-.5),1,1,color=C['obs'],zorder=2))
                elif not np.isnan(data[r,c]): ax.text(c,r,format(data[r,c],fmt),ha='center',va='center',fontsize=6,color='white',zorder=3,fontweight='bold')
        ax.plot(s[1],s[0],'o',color=C['start'],ms=14,zorder=5,markeredgecolor='white',markeredgewidth=1.5)
        ax.text(s[1],s[0],'S',ha='center',va='center',fontsize=8,fontweight='bold',color='#0F1117',zorder=6)
        ax.plot(g[1],g[0],'*',color=C['goal'],ms=18,zorder=5,markeredgecolor='white',markeredgewidth=1.5)
        plt.colorbar(im,ax=ax,fraction=.046,pad=.04); ax.set_title(f'{title_ax}\nε={epsilon}',fontweight='bold',color=C['text'],fontsize=12); ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout(); plt.savefig('exp4_absorption.png',dpi=150,bbox_inches='tight',facecolor=C['bg']); plt.close(); print('  → exp4_absorption.png')

if __name__=='__main__':
    print('\n'+'★'*65+'\n  MINI-PROJET IA — A* + Chaînes de Markov\n  Étudiant : Farahi Abderahim | SDIA\n'+'★'*65)
    r1=exp1_comparison(); r2=exp2_epsilon('medium'); r3=exp3_heuristics(); exp4_absorption('medium',.1)
    print('\n'+'★'*65+'\n  ✓ Terminé.\n'+'★'*65)
