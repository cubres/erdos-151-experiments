import sys, itertools, subprocess
from p151_sa import max_cliques_bits, alpha_bits, H
def g6_to_adj(s):
    s=s.strip(); n=ord(s[0])-63; bits=[]
    for ch in s[1:]:
        v=ord(ch)-63
        bits.extend((v>>k)&1 for k in range(5,-1,-1))
    adj=[0]*n; k=0
    for j in range(1,n):
        for i in range(j):
            if bits[k]: adj[i]|=1<<j; adj[j]|=1<<i
            k+=1
    return n, adj
n=int(sys.argv[1]); h=H(n)
subsets=[sum(1<<i for i in S) for S in itertools.combinations(range(n),h)]
proc=subprocess.Popen(['./nauty/geng','-q','-D'+str(h-1),str(n)],stdout=subprocess.PIPE,text=True)
tot=0; passed_alpha=0; found=[]
for line in proc.stdout:
    tot+=1
    _,adj=g6_to_adj(line)
    if alpha_bits(adj,n)>=h: continue
    passed_alpha+=1
    cl=max_cliques_bits(adj,n)
    ok=True
    for S in subsets:
        if not any(c & ~S==0 for c in cl): ok=False; break
    if ok:
        found.append(line.strip())
print(f"n={n} h={h}: graphs with maxdeg<={h-1}: {tot}; with also alpha<={h-1}: {passed_alpha}; COUNTEREXAMPLES: {len(found)}")
for g in found[:20]: print("  ", g)
