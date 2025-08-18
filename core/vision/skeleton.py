import numpy as np, cv2
from skimage.morphology import skeletonize

NEIGH8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def to_skeleton(bin_img: np.ndarray) -> np.ndarray:
    s = skeletonize((bin_img>0).astype(bool)).astype(np.uint8)*255
    return s

def longest_path_polyline(skel: np.ndarray) -> list[tuple[int,int]]:
    ys, xs = np.where(skel>0)
    if len(xs)==0: return []
    S = set(zip(xs,ys))
    def neighbors(p):
        x,y=p
        for dx,dy in NEIGH8:
            q=(x+dx,y+dy)
            if q in S: yield q
    ends = [p for p in S if sum(1 for _ in neighbors(p))==1]
    if len(ends)<2: ends = list(S)[:2]
    import heapq
    def dists_path(a,b):
        INF=10**9; dist={a:0.0}; prev={a:None}; pq=[(0.0,a)]
        while pq:
            d,u=heapq.heappop(pq)
            if u==b: break
            if d>dist[u]: continue
            for v in neighbors(u):
                step = 1.4142 if (v[0]!=u[0] and v[1]!=u[1]) else 1.0
                nd=d+step
                if nd<dist.get(v,INF): dist[v]=nd; prev[v]=u; heapq.heappush(pq,(nd,v))
        path=[]; cur=b
        if b not in prev and b!=a: return [], float('inf')
        while cur is not None:
            path.append(cur); cur=prev.get(cur)
        path.reverse(); return path, dist.get(b,float('inf'))
    best=[]; L=-1
    for i in range(len(ends)):
        for j in range(i+1,len(ends)):
            p, l = dists_path(ends[i], ends[j])
            if np.isfinite(l) and l>L:
                L=l; best=p
    return [(int(x),int(y)) for x,y in best]
