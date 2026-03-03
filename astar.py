import heapq, time
from typing import List, Tuple, Dict, Callable, Optional

def make_grid(rows, cols, obstacles):
    grid = [[0]*cols for _ in range(rows)]
    for (r,c) in obstacles:
        if 0<=r<rows and 0<=c<cols: grid[r][c]=1
    return grid

def get_neighbors(grid, pos):
    r,c=pos; rows,cols=len(grid),len(grid[0]); result=[]
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr,nc=r+dr,c+dc
        if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0: result.append((nr,nc))
    return result

def h_manhattan(p,goal): return abs(p[0]-goal[0])+abs(p[1]-goal[1])
def h_zero(p,goal): return 0.0
def h_euclidean(p,goal): return ((p[0]-goal[0])**2+(p[1]-goal[1])**2)**0.5

def search(grid, start, goal, heuristic, weight=1.0):
    t0=time.perf_counter()
    open_heap=[]; counter=0
    heapq.heappush(open_heap,(0.0,0.0,counter,start))
    came_from={start:None}; g_score={start:0.0}; closed=set()
    nodes_expanded=0; max_open=1
    while open_heap:
        f,g,_,current=heapq.heappop(open_heap)
        if current in closed: continue
        closed.add(current); nodes_expanded+=1
        if current==goal:
            path=[]; node=goal
            while node is not None: path.append(node); node=came_from[node]
            path.reverse()
            return {'path':path,'cost':g_score[goal],'nodes_expanded':nodes_expanded,
                    'max_open':max_open,'time_ms':(time.perf_counter()-t0)*1000,'found':True}
        for nb in get_neighbors(grid,current):
            new_g=g_score[current]+1
            if nb not in g_score or new_g<g_score[nb]:
                g_score[nb]=new_g; h=heuristic(nb,goal); f_val=new_g+weight*h
                counter+=1; heapq.heappush(open_heap,(f_val,new_g,counter,nb))
                came_from[nb]=current; max_open=max(max_open,len(open_heap))
    return {'path':[],'cost':float('inf'),'nodes_expanded':nodes_expanded,
            'max_open':max_open,'time_ms':(time.perf_counter()-t0)*1000,'found':False}

def astar(grid,start,goal): return search(grid,start,goal,h_manhattan,1.0)
def ucs(grid,start,goal):   return search(grid,start,goal,h_zero,1.0)
def greedy(grid,start,goal):return search(grid,start,goal,h_manhattan,float('inf'))
def weighted_astar(grid,s,g,w=1.5): return search(grid,s,g,h_manhattan,w)
