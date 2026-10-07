import itertools, sys
# H(n) = max h with R(3,h) <= n, using known R(3,h): 3,6,9,14,18,23,28,36
R3 = {2:3,3:6,4:9,5:14,6:18,7:23,8:28,9:36}
def H(n):
    return max(h for h,r in R3.items() if r<=n)

def maximal_cliques(adj, n):
    # Bron-Kerbosch
    out=[]
    def bk(Rset, P, X):
        if not P and not X:
            out.append(Rset); return
        u = max(P|X, key=lambda v: len(adj[v]&P))
        for v in list(P - adj[u]):
            bk(Rset|{v}, P&adj[v], X&adj[v]); P=P-{v}; X=X|{v}
    bk(frozenset(), set(range(n)), set())
    return [c for c in out if len(c)>=2]

def contains_max_clique(S, cliques):
    return any(c<=S for c in cliques)

def tau(adj, n):
    cl = maximal_cliques(adj, n)
    # tau = n - max |S| with S containing no maximal clique
    # search from large |S| downward
    best=0
    for s in range(n, 0, -1):
        for S in itertools.combinations(range(n), s):
            if not contains_max_clique(frozenset(S), cl):
                return n - s, cl
    return n, cl

def every_hset_contains_maxclique(adj, n, h):
    cl = maximal_cliques(adj, n)
    for S in itertools.combinations(range(n), h):
        if not contains_max_clique(frozenset(S), cl): return False, S
    return True, None

def complement(adj, n):
    return [set(range(n)) - adj[v] - {v} for v in range(n)]

def from_edges(n, edges):
    adj=[set() for _ in range(n)]
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    return adj

def circulant(n, jumps):
    return from_edges(n, [(i,(i+j)%n) for i in range(n) for j in jumps])

def is_triangle_free(adj,n):
    return all(not (adj[a]&adj[b]) for a in range(n) for b in adj[a] if a<b)
def alpha(adj,n):
    # independence number via maximal cliques of complement
    co=complement(adj,n); cl=maximal_cliques(co,n)
    return max((len(c) for c in cl), default=1)

# Clebsch graph: vertices = 0..15 as 4-bit vectors; adjacent iff differ in 1 bit or all 4 bits
def clebsch():
    n=16; edges=[]
    for a in range(16):
        for b in range(a+1,16):
            d=bin(a^b).count('1')
            if d==1 or d==4: edges.append((a,b))
    return from_edges(n, edges)

cands = {
 'C5 (n=5)': circulant(5,[1]),
 'Wagner/Mobius C8(1,4) (n=8)': circulant(8,[1,4]),
 'C8(1,3)? (n=8)': circulant(8,[1,3]),
 'C13(1,5) (n=13)': circulant(13,[1,5]),
 'Clebsch (n=16)': clebsch(),
 'C17(1,2,4,8) Paley? triangle? (n=17)': circulant(17,[1,2,4,8]),
}
for name, T in cands.items():
    n=len(T)
    tf=is_triangle_free(T,n); a=alpha(T,n); h=H(n)
    G=complement(T,n)
    ok, witness = every_hset_contains_maxclique(G, n, h)
    print(f"{name}: triangle-free={tf} alpha(T)={a} H(n)={h} | complement G: every {h}-set contains a maximal clique? {ok}  -> {'COUNTEREXAMPLE tau(G)>=n-H+1' if ok else 'no (witness S='+str(witness)+')'}")
    sys.stdout.flush()
