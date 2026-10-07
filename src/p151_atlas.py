import networkx as nx, itertools
from networkx.generators.atlas import graph_atlas_g
R3 = {2:3,3:6,4:9,5:14,6:18,7:23,8:28,9:36}
def H(n): return max(h for h,r in R3.items() if r<=n)
def tau_ok(G):
    n=G.number_of_nodes(); h=H(n)
    cl=[frozenset(c) for c in nx.find_cliques(G) if len(c)>=2]
    for S in itertools.combinations(G.nodes(),h):
        S=frozenset(S)
        if not any(c<=S for c in cl): return True  # conjecture holds for G
    return False
cnt={}; bad=[]
for G in graph_atlas_g():
    n=G.number_of_nodes()
    if n<3: continue
    cnt[n]=cnt.get(n,0)+1
    if not tau_ok(G): bad.append((n, list(G.edges())))
print("graphs checked per n:", cnt)
print("counterexamples (tau(G) > n-H(n)) among all graphs on <=7 vertices:", len(bad))
for n,e in bad[:10]: print(n,e)
