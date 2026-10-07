import random, itertools, math, sys, time
R3 = {2:3,3:6,4:9,5:14,6:18,7:23,8:28,9:36}
def H(n): return max(h for h,r in R3.items() if r<=n)

def max_cliques_bits(adj, n):
    # adj: list of int bitmasks. Bron-Kerbosch with pivot on bitmasks
    out=[]
    def bk(R, P, X):
        if P==0 and X==0:
            if bin(R).count('1')>=2: out.append(R)
            return
        PX=P|X
        # pivot: vertex in PX maximizing |P & adj[u]|
        best=-1; u=-1; t=PX
        while t:
            v=(t&-t).bit_length()-1; t&=t-1
            c=bin(P&adj[v]).count('1')
            if c>best: best=c; u=v
        cand=P & ~adj[u]
        while cand:
            v=(cand&-cand).bit_length()-1; cand&=cand-1
            bk(R|(1<<v), P&adj[v], X&adj[v]); P&=~(1<<v); X|=(1<<v)
    bk(0,(1<<n)-1,0)
    return out

def bad_count(adj, n, h, subsets, cliques=None):
    if cliques is None: cliques=max_cliques_bits(adj,n)
    bad=0
    for S in subsets:
        ok=False
        for c in cliques:
            if c & ~S == 0: ok=True; break
        if not ok: bad+=1
    return bad

def alpha_bits(adj,n):
    co=[((1<<n)-1) & ~adj[v] & ~(1<<v) for v in range(n)]
    return max(bin(c).count('1') for c in max_cliques_bits(co,n)) if n>1 else 1

def sa(n, iters=20000, seed=0, p0=0.5, T0=1.0, verbose=True):
    rng=random.Random(seed); h=H(n)
    subsets=[sum(1<<i for i in S) for S in itertools.combinations(range(n),h)]
    adj=[0]*n
    for a in range(n):
        for b in range(a+1,n):
            if rng.random()<p0: adj[a]|=1<<b; adj[b]|=1<<a
    cur=bad_count(adj,n,h,subsets); best=cur; bestadj=adj[:]
    T=T0
    for it in range(iters):
        a,b=rng.sample(range(n),2)
        adj[a]^=1<<b; adj[b]^=1<<a
        new=bad_count(adj,n,h,subsets)
        if new<=cur or rng.random()<math.exp(-(new-cur)/T):
            cur=new
            if cur<best: best=cur; bestadj=adj[:]
            if cur==0: break
        else:
            adj[a]^=1<<b; adj[b]^=1<<a
        T=max(0.05, T0*(1-it/iters))
    return best, bestadj

if __name__=='__main__':
    ns=[int(x) for x in sys.argv[1].split(',')] if len(sys.argv)>1 else [8,9,10,13]
    iters=int(sys.argv[2]) if len(sys.argv)>2 else 20000
    for n in ns:
        t=time.time(); h=H(n); tot=math.comb(n,h)
        bestall=None
        for seed in range(4):
            best,adj=sa(n,iters=iters,seed=seed)
            if bestall is None or best<bestall[0]: bestall=(best,adj)
            if best==0: break
        best,adj=bestall
        edges=[(a,b) for a in range(n) for b in range(a+1,n) if adj[a]>>b&1]
        print(f"n={n} h={h}: min #bad {h}-sets found = {best} / {tot}   alpha={alpha_bits(adj,n)} maxdeg={max(bin(x).count('1') for x in adj)} edges={len(edges)}  [{time.time()-t:.0f}s]")
        if best==0: print("  COUNTEREXAMPLE edges:", edges)
        sys.stdout.flush()
