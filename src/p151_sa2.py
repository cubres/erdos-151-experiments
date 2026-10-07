import random, itertools, math, sys, time
from p151_sa import max_cliques_bits, alpha_bits, H, bad_count
def sa(n, iters, seed, dcap):
    rng=random.Random(seed); h=H(n)
    subsets=[sum(1<<i for i in S) for S in itertools.combinations(range(n),h)]
    adj=[0]*n; deg=[0]*n
    # start: random graph with degree cap
    pairs=[(a,b) for a in range(n) for b in range(a+1,n)]; rng.shuffle(pairs)
    for a,b in pairs:
        if deg[a]<dcap and deg[b]<dcap and rng.random()<0.7:
            adj[a]|=1<<b; adj[b]|=1<<a; deg[a]+=1; deg[b]+=1
    cur=bad_count(adj,n,h,subsets); best=cur; bestadj=adj[:]
    T0=2.0; T=T0
    for it in range(iters):
        a,b=rng.sample(range(n),2)
        adding = not (adj[a]>>b&1)
        if adding and (deg[a]>=dcap or deg[b]>=dcap): continue
        adj[a]^=1<<b; adj[b]^=1<<a; d=1 if adding else -1; deg[a]+=d; deg[b]+=d
        new=bad_count(adj,n,h,subsets)
        if new<=cur or rng.random()<math.exp(-(new-cur)/T):
            cur=new
            if cur<best: best=cur; bestadj=adj[:]
            if cur==0: break
        else:
            adj[a]^=1<<b; adj[b]^=1<<a; deg[a]-=d; deg[b]-=d
        T=max(0.1, T0*(1-it/iters))
    return best,bestadj
ns=[int(x) for x in sys.argv[1].split(',')]; iters=int(sys.argv[2]); seeds=int(sys.argv[3])
for n in ns:
    h=H(n); t=time.time(); bestall=None
    for seed in range(seeds):
        b,adj=sa(n,iters,seed,h-1)
        if bestall is None or b<bestall[0]: bestall=(b,adj)
        if b==0: break
    b,adj=bestall
    edges=[(x,y) for x in range(n) for y in range(x+1,n) if adj[x]>>y&1]
    print(f"n={n} h={h} (deg<={h-1}): min bad = {b}/{math.comb(n,h)} alpha={alpha_bits(adj,n)} edges={len(edges)} [{time.time()-t:.0f}s]"); sys.stdout.flush()
    if b==0: print("  COUNTEREXAMPLE:", edges)
