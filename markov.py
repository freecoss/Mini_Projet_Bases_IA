import numpy as np
from typing import List,Tuple,Dict,Optional

def build_policy(path):
    policy={}
    for i in range(len(path)-1):
        s,s_next=path[i],path[i+1]
        policy[s]=(s_next[0]-s[0],s_next[1]-s[1])
    return policy

def _perpendicular(action):
    dr,dc=action
    return [(-1,0),(1,0)] if dr==0 else [(0,-1),(0,1)]

def build_transition_matrix(grid,states,goal,policy,epsilon=0.1):
    rows_g,cols_g=len(grid),len(grid[0])
    state_idx={s:i for i,s in enumerate(states)}
    N=len(states); GOAL_IDX,FAIL_IDX=N,N+1
    P=np.zeros((N+2,N+2))
    P[GOAL_IDX,GOAL_IDX]=1.0; P[FAIL_IDX,FAIL_IDX]=1.0
    def dest(pos):
        nr,nc=pos
        if not(0<=nr<rows_g and 0<=nc<cols_g) or grid[nr][nc]==1: return FAIL_IDX
        if pos==goal: return GOAL_IDX
        return state_idx.get(pos,FAIL_IDX)
    for i,s in enumerate(states):
        action=policy.get(s,(0,0))
        if action==(0,0): P[i,FAIL_IDX]+=1.0; continue
        r,c=s
        P[i,dest((r+action[0],c+action[1]))] += (1.0-epsilon)
        for pdir in _perpendicular(action):
            P[i,dest((r+pdir[0],c+pdir[1]))] += epsilon/2.0
    assert np.allclose(P.sum(axis=1),1.0)
    return P,state_idx,GOAL_IDX,FAIL_IDX

def markov_distribution(P,pi0,n_steps):
    return pi0@np.linalg.matrix_power(P,n_steps)

def initial_distribution(state_idx,start,size):
    pi0=np.zeros(size)
    if start in state_idx: pi0[state_idx[start]]=1.0
    return pi0

def absorption_analysis(P,N):
    Q,R=P[:N,:N],P[:N,N:]
    try: Nmat=np.linalg.inv(np.eye(N)-Q)
    except: Nmat=np.linalg.pinv(np.eye(N)-Q)
    return Nmat,Nmat@R,Nmat@np.ones(N)

def monte_carlo(grid,states,state_idx,policy,goal,epsilon,n_sim=5000,max_steps=1000,start=None,seed=42):
    rows_g,cols_g=len(grid),len(grid[0])
    rng=np.random.default_rng(seed)
    if start is None: start=states[0]
    rg,rf,tg=0,0,[]; perp_cache={}
    for _ in range(n_sim):
        s=list(start); done=False
        for step in range(max_steps):
            pos=(s[0],s[1])
            if pos==goal: rg+=1; tg.append(step); done=True; break
            action=policy.get(pos)
            if not action or action==(0,0): rf+=1; done=True; break
            if action not in perp_cache: perp_cache[action]=_perpendicular(action)
            perps=perp_cache[action]; rv=rng.random()
            move=action if rv<1-epsilon else (perps[0] if rv<1-epsilon/2 else perps[1])
            nr,nc=s[0]+move[0],s[1]+move[1]
            if not(0<=nr<rows_g and 0<=nc<cols_g) or grid[nr][nc]==1: rf+=1; done=True; break
            s=[nr,nc]
        if not done: rf+=1
    return {'p_goal':rg/n_sim,'p_fail':rf/n_sim,
            'mean_time':float(np.mean(tg)) if tg else None,
            'std_time':float(np.std(tg)) if tg else None,'n_sim':n_sim}
