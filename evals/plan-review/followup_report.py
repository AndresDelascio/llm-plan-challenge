"""Print the counts for follow-up tests 1 and 2 from the saved runs. Run from the repository root.
Rules: followup.md. Tests 3 and 4 are read directly from runs.jsonl and the one-word replies."""

# --- Test 1: final plans per arm ---
import json, collections, glob
from pathlib import Path
from statistics import median
R=Path("runs"); S=R/"followup-score"
def tok(u):
    x=u["usage"]
    if u["provider"]=="codex": return x["input_tokens"]+x["output_tokens"]
    return x["input_tokens"]+x.get("cache_read_input_tokens",0)+x.get("cache_creation_input_tokens",0)+x["output_tokens"]
J={}
for f in sorted([S/"judgments.jsonl"]):
    for l in open(f,encoding="utf-8"):
        if l.strip(): r=json.loads(l); assert r["blind_id"] not in J; J[r["blind_id"]]=r
M=json.load(open(S/"mapping.json")); assert len(J)==len(M)==93,(len(J),len(M))
key={json.loads(l)["id"]:json.loads(l) for l in open("evals/plan-review/answer-key.jsonl")}
flawed={c for c,k in key.items() if k["seeds"]}
ARM={"followup-better-claude":"A-Claude","followup-better-codex":"A-Codex","followup-revise-codex":"B","followup-revise-claude":"C"}
SRC={"B":"portfolio-full-codex","C":"portfolio-full-claude"}
a=collections.defaultdict(lambda: collections.defaultdict(list))
for m in M:
    arm=ARM[m["run_dir"]]; j=J[m["blind_id"]]; d=a[arm]; stem=m["file"][:-3]
    assert j["case"]==m["case"]
    u=json.load(open(R/m["run_dir"]/(stem+".usage.json"))); t,w=tok(u),u["wall_ms"]
    if arm in SRC:
        case,_,rev,rep=stem.split("-"); s=json.load(open(R/SRC[arm]/f"{case}-{rev}-{rep}.usage.json")); t+=tok(s); w+=s["wall_ms"]
    d["tok"].append(t); d["wall"].append(w); d["words"].append(len((R/m["run_dir"]/m["file"]).read_text(encoding="utf-8").split()))
    d["new"].append(bool(j["new_defect"]))
    v=list(j["seeds"].values())
    if m["case"] in flawed:
        assert set(j["seeds"])=={s["id"] for s in key[m["case"]]["seeds"]},j
        d["fixed"]+= [x=="fixed" for x in v]; d["bothfixed"].append(all(x=="fixed" for x in v))
    else:
        d["reg"].append(any(x=="regressed" for x in v))
ow=median(len(p.read_text(encoding="utf-8-sig").split()) for p in Path("evals/plan-review/plans").glob("p*.md"))
print("original plan median words",ow)
for arm in ("A-Claude","A-Codex","B","C"):
    d=a[arm]
    print(arm,"plans",len(d["tok"]),"fixed",sum(d["fixed"]),"/",len(d["fixed"]),"plans both fixed",sum(d["bothfixed"]),"/",len(d["bothfixed"]),
          "regress",sum(d["reg"]),"/",len(d["reg"]),"new_defect",sum(d["new"]),"/",len(d["new"]),
          "words",median(d["words"]),"tok",median(d["tok"]),"wall_s",round(median(d["wall"])/1000,1))

# --- Test 2: same model twice against one of each ---
import json, collections
rows=json.load(open("runs/portfolio-score/mapping.json"))
m={r["blind_id"]:r for r in rows if r.get("blind_id")}
cl=[json.loads(l) for l in open("runs/followup-score/clusters.jsonl")]
done=collections.defaultdict(set)
for r in m.values(): done[r["case"]].add((r["provider"],r["repeat"]))
sets=collections.defaultdict(set)
for c in cl:
    r=m[c["blind_id"]]; sets[(r["case"],r["provider"],r["repeat"])].add(c["cluster"])
tot=collections.Counter(); n=0
for case in sorted(done):
    if len(done[case])<4: print(case,"skipped",len(done[case])); continue
    g=lambda p,r: sets[(case,p,r)]
    cc=len(g("codex",1)|g("codex",2)); kk=len(g("claude",1)|g("claude",2))
    x=sum(len(g("codex",a)|g("claude",b)) for a in (1,2) for b in (1,2))/4
    al=len(cc and g("codex",1)|g("codex",2)|g("claude",1)|g("claude",2) or g("claude",1)|g("claude",2))
    print(case,"codex x2",cc,"claude x2",kk,"cross",x,"all4",al)
    tot.update({"cc":cc,"kk":kk,"x":x,"all4":al,"s1c":(len(g("codex",1))+len(g("codex",2)))/2,"s1k":(len(g("claude",1))+len(g("claude",2)))/2}); n+=1
print(n,dict(tot))
