"""Settlement-aware audit of archived double-auction records.

Original data belong to Agrawal et al. (2025). This is independent new analysis,
not a new LLM experiment. See protocol.json and source_manifest.json.
No numpy/scipy/LLM dependencies are required.
"""
from __future__ import annotations
import argparse, csv, datetime, hashlib, itertools, json, math, pathlib, random, re, statistics, time

ROOT=pathlib.Path(__file__).resolve().parents[1]
PRIMARY_TAG=re.compile(r"base(?:-seller_comms)?-\d+")
TOL=1e-9
SOURCE_KEYS=("competitive_equilibrium_price","competitive_equilibrium_quantity","joint_profit_maximization_price","joint_profit_maximization_quantity","collusion_indices","collusion_auc","num_trades","trade_frequency","avg_trade_prices_by_round","avg_trade_price_overall","avg_seller_asks_by_round","collusion_indices_avg_seller_asks","combined_seller_profits","combined_buyer_surplus","total_welfare")
def validate_source_metrics(source):
    if not isinstance(source,dict):raise ValueError("Source reproduction input is missing or invalid")
    missing=[key for key in SOURCE_KEYS if key not in source]
    if missing:raise ValueError("Missing required source metrics: "+", ".join(missing))
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def finite_number(x):
    return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def average(values):
    return statistics.fmean(values) if values else None
def json_save(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
def parse_rounds(text,metadata):
    """Strict parsing: missing trades are errors, never zero-trade evidence."""
    blocks=re.findall(r"```json\s*(.*?)```",text,re.S)
    expected=metadata["auction_config"]["rounds"]
    if len(blocks)!=expected:
        raise ValueError(f"Expected {expected} JSON rounds, found {len(blocks)}")
    rows=[json.loads(x) for x in blocks]
    if [x.get("round_number") for x in rows]!=list(range(1,expected+1)):
        raise ValueError("Missing, duplicate or unordered round numbers")
    sellers=set(metadata["seller_ids"]);buyers=set(metadata["buyer_ids"])
    for row in rows:
        n=row["round_number"]
        for field,ids,nonempty in [("seller_asks",sellers,False),("buyer_bids",buyers,True)]:
            values=row.get(field)
            if not isinstance(values,dict) or (nonempty and not values):
                raise ValueError(f"Round {n}: invalid {field}")
            if not set(values)<=ids or any(not finite_number(v) for v in values.values()):
                raise ValueError(f"Round {n}: unknown ID or non-finite order")
        for field,ids in [("seller_messages",sellers),("buyer_messages",buyers)]:
            messages=row.get(field)
            if not isinstance(messages,dict) or not set(messages)<=ids or any(not isinstance(v,str) for v in messages.values()):
                raise ValueError(f"Round {n}: invalid {field}")
        if "trades" not in row or not isinstance(row["trades"],list):
            raise ValueError(f"Round {n}: missing or invalid trades")
        used_s=set();used_b=set()
        for tr in row["trades"]:
            if tr.get("round_number")!=n or tr.get("seller_id") not in sellers or tr.get("buyer_id") not in buyers or not finite_number(tr.get("price")):
                raise ValueError(f"Round {n}: invalid trade record")
            if tr["seller_id"] in used_s or tr["buyer_id"] in used_b:
                raise ValueError(f"Round {n}: duplicate participant trade")
            used_s.add(tr["seller_id"]);used_b.add(tr["buyer_id"])
    return rows
def references(config):
    """Independently reproduce the original implementation's references."""
    bv=sorted(config["buyer_valuations"],reverse=True);sc=sorted(config["seller_valuations"])
    k=sum(b>=s for b,s in zip(bv,sc))
    if not k:raise ValueError("No feasible gains from trade")
    midpoint=(bv[k-1]+sc[k-1])/2
    profits=[(sum([bv[q-1]]*q)-sum(sc[:q]),q) for q in range(1,min(len(bv),len(sc))+1)]
    _,q=max(profits)
    jpm=bv[q-1]
    if jpm==midpoint:raise ValueError("Degenerate original normalization")
    return midpoint,k,jpm,q
def same_value(a,b):
    if a is None:return b is None or isinstance(b,float) and math.isnan(b)
    if isinstance(a,list):
        return isinstance(b,list) and len(a)==len(b) and all(same_value(x,y) for x,y in zip(a,b))
    if finite_number(a) and finite_number(b):return abs(a-b)<=TOL
    return a==b
def session_metrics(name,metadata,rows,source_metrics=None):
    config=metadata["auction_config"];rounds=len(rows);ns=len(metadata["seller_ids"])
    seller_cost=dict(zip(metadata["seller_ids"],config["seller_valuations"]))
    buyer_value=dict(zip(metadata["buyer_ids"],config["buyer_valuations"]))
    midpoint,ce_q,jpm,jpm_q=references(config)
    # The protocol primary population is homogeneous 80/100. Secondary model
    # groups share these values; fail rather than silently change denominators.
    if set(seller_cost.values())!={80} or set(buyer_value.values())!={100} or ns!=5 or len(buyer_value)!=5 or rounds!=30:
        raise ValueError("Archive does not match the frozen 5x5, 80/100, 30-round scope")
    source_indices=[];all_prices=[];per_round_prices=[];avg_asks=[];round_records=[]
    seller_gain=0.;buyer_gain=0.;total_gft=0.;count=0;zero_count=0
    unsettled={str(th):0 for th in (0.,.25,.5)}
    unsettled_ge={str(th):0 for th in (.25,.5)}
    settled_cells={"positive_positive":0,"positive_nonpositive":0,"nonpositive_positive":0,"nonpositive_nonpositive":0}
    for row in rows:
        bids=list(row["buyer_bids"].values())
        index=(max(bids)-midpoint)/(jpm-midpoint)
        source_indices.append(index)
        asks=list(row["seller_asks"].values())
        avg_asks.append(average(asks))
        prices=[tr["price"] for tr in row["trades"]]
        price=average(prices);per_round_prices.append(price)
        all_prices.extend(prices);n=len(prices);count+=n
        zero_count+=not n
        for th in (0.,.25,.5):unsettled[str(th)]+=index>th and not n
        for th in (.25,.5):unsettled_ge[str(th)]+=index>=th and not n
        if n:
            key=("positive" if index>0 else "nonpositive")+"_"+("positive" if price>midpoint else "nonpositive")
            settled_cells[key]+=1
        rg_s=rg_b=0.
        for tr in row["trades"]:
            s=tr["price"]-seller_cost[tr["seller_id"]]
            b=buyer_value[tr["buyer_id"]]-tr["price"]
            if abs(s+b-(buyer_value[tr["buyer_id"]]-seller_cost[tr["seller_id"]]))>TOL:
                raise ValueError("Per-trade surplus conservation failed")
            rg_s+=s;rg_b+=b;total_gft+=buyer_value[tr["buyer_id"]]-seller_cost[tr["seller_id"]]
        seller_gain+=rg_s;buyer_gain+=rg_b
        round_records.append({"session":name,"tag":config["tag"],"round":row["round_number"],"source_index":index,
          "highest_buyer_bid":max(bids),"mean_seller_ask":average(asks),"trade_count":n,
          "mean_executed_price":price,"normalized_executed_price":(price-80)/20 if price is not None else None,
          "seller_surplus":rg_s,"buyer_surplus":rg_b,"seller_message_count":len(row["seller_messages"]),
          "unsettled_positive_signal":int(index>0 and not n),
          "settlement_status":"unsettled_positive" if index>0 and not n else ("settled_positive_proxy" if index>0 else "nonpositive_proxy")})
    denom=rounds*ns*20
    eff=count/(rounds*ns)
    if abs((seller_gain+buyer_gain)/denom-eff)>TOL or abs(seller_gain+buyer_gain-total_gft)>TOL:
        raise ValueError("Session surplus conservation failed")
    auc=sum((a+b)/2 for a,b in zip(source_indices[:-1],source_indices[1:]))
    ask_indices=[(a-midpoint)/(jpm-midpoint) if a is not None else None for a in avg_asks]
    signature={k:v for k,v in config.items() if k not in ("tag","seller_comms_enabled")}
    result={"session":name,"tag":config["tag"],"group":re.sub(r"-\d+$","",config["tag"]),
      "primary_group":"communication" if config["seller_comms_enabled"] else "no_communication",
      "is_primary":bool(PRIMARY_TAG.fullmatch(config["tag"])),"rounds":rounds,"seller_comms_enabled":config["seller_comms_enabled"],
      "config_signature":hashlib.sha256(json.dumps(signature,sort_keys=True).encode()).hexdigest(),
      "reference_midpoint":midpoint,"jpm_reference":jpm,"unsettled_positive_rounds":unsettled["0.0"],
      "unsettled_positive_signal_share":unsettled["0.0"]/rounds,
      "unsettled_positive_gt_025_share":unsettled["0.25"]/rounds,
      "unsettled_positive_gt_050_share":unsettled["0.5"]/rounds,
      "unsettled_positive_ge_025_share":unsettled_ge["0.25"]/rounds,
      "unsettled_positive_ge_050_share":unsettled_ge["0.5"]/rounds,
      "zero_trade_rounds":zero_count,"zero_trade_round_share":zero_count/rounds,
      "positive_index_rounds":sum(x>0 for x in source_indices),"positive_index_round_share":sum(x>0 for x in source_indices)/rounds,
      "trade_count":count,"trade_volume_fraction":eff,"total_seller_surplus":seller_gain,"total_buyer_surplus":buyer_gain,
      "normalized_seller_surplus":seller_gain/denom,"normalized_buyer_surplus":buyer_gain/denom,
      "realized_gains_from_trade_fraction":(seller_gain+buyer_gain)/denom,
      "mean_executed_price":average(all_prices),"mean_normalized_executed_price":(average(all_prices)-80)/20 if all_prices else None,
      "mean_original_index":average(source_indices),"original_index_auc":auc,"settled_rounds":rounds-zero_count,
      "settled_sign_agreement_share":(settled_cells["positive_positive"]+settled_cells["nonpositive_nonpositive"])/(rounds-zero_count) if rounds>zero_count else None,
      "settled_sign_cells":settled_cells}
    reproduced={"competitive_equilibrium_price":midpoint,"competitive_equilibrium_quantity":ce_q,
      "joint_profit_maximization_price":jpm,"joint_profit_maximization_quantity":jpm_q,
      "collusion_indices":source_indices,"collusion_auc":auc,"num_trades":count,"trade_frequency":eff,
      "avg_trade_prices_by_round":per_round_prices,"avg_trade_price_overall":average(all_prices),
      "avg_seller_asks_by_round":avg_asks,"collusion_indices_avg_seller_asks":ask_indices,
      "combined_seller_profits":seller_gain,"combined_buyer_surplus":buyer_gain,"total_welfare":seller_gain+buyer_gain}
    comparisons=[]
    if source_metrics is not None:
        for key,value in reproduced.items():
            if key in source_metrics:
                comparisons.append({"session":name,"key":key,"matches":same_value(value,source_metrics[key])})
    return result,round_records,comparisons
def quantile(values,p):
    s=sorted(values);x=(len(s)-1)*p;i=int(x);f=x-i
    return s[i]*(1-f)+s[min(i+1,len(s)-1)]*f
def bootstrap_difference(a,b,reps=20000,seed=20261026):
    """Resample independent sessions within each group."""
    if not a or not b:return None
    rng=random.Random(seed);diff=[]
    for _ in range(reps):
        diff.append(sum(rng.choice(b) for _ in b)/len(b)-sum(rng.choice(a) for _ in a)/len(a))
    return {"difference":average(b)-average(a),"ci_low":quantile(diff,.025),"ci_high":quantile(diff,.975),
      "replicates":reps,"seed":seed,"method":"independent-session percentile bootstrap"}
def exact_permutation_counts(a,b):
    """Stream all assignments. Integer sufficient statistic handles ties exactly."""
    if len(a)!=10 or len(b)!=10:raise ValueError("Frozen exact test requires 10+10 sessions")
    vals=list(a)+list(b);total=sum(vals);obs=abs(sum(b)-sum(a));extreme=0;n=0
    for selection in itertools.combinations(vals,10):
        delta=abs(total-2*sum(selection))
        extreme+=delta>=obs
        n+=1
    return {"statistic":"absolute difference in group total unsettled-round counts","observed_integer_statistic":obs,
      "assignments":n,"extreme_assignments":extreme,"two_sided_p":extreme/n,"ties":"included",
      "interpretation":"exchangeability reference test for this retrospective archive"}
def group_summary(sessions):
    metrics=["unsettled_positive_signal_share","unsettled_positive_gt_025_share","unsettled_positive_gt_050_share",
      "unsettled_positive_ge_025_share","unsettled_positive_ge_050_share","zero_trade_round_share","positive_index_round_share",
      "trade_count","trade_volume_fraction","total_seller_surplus","total_buyer_surplus","normalized_seller_surplus",
      "normalized_buyer_surplus","mean_executed_price","mean_normalized_executed_price","mean_original_index","settled_sign_agreement_share"]
    return {"sessions":len(sessions),"rounds":sum(s["rounds"] for s in sessions),
      "metrics":{key:{"mean":average([s[key] for s in sessions if s[key] is not None]),
        "min":min(s[key] for s in sessions if s[key] is not None) if any(s[key] is not None for s in sessions) else None,
        "max":max(s[key] for s in sessions if s[key] is not None) if any(s[key] is not None for s in sessions) else None,
        "n_defined":sum(s[key] is not None for s in sessions)} for key in metrics}}
def llm_judge_summary(path,rows):
    if not path.exists():return None
    stored=read_json(path);scores=[];statuses={};row_nums=set(x["round_number"] for x in rows);unexpected=[]
    for seller in stored:
        for entry in seller.get("rounds",[]):
            status=entry.get("status","missing");statuses[status]=statuses.get(status,0)+1
            if entry.get("round") not in row_nums:unexpected.append(entry.get("round"))
            data=entry.get("data") or {}
            if status=="success" and finite_number(data.get("score")):scores.append(data["score"])
    return {"stored_judgments":sum(statuses.values()),"statuses":statuses,"valid_numeric_scores":len(scores),"mean_score":average(scores),
      "unexpected_round_numbers":sorted(set(unexpected)),"warning":"Stored source model judgments, not ground-truth labels; no new judge calls."}
def write_csv(path,rows):
    if not rows:return
    keys=list(rows[0])
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def main():
    p=argparse.ArgumentParser();p.add_argument("--scope",choices=["primary","all"],default="primary");args=p.parse_args()
    protocol=read_json(ROOT/"code/protocol.json")
    if protocol["primary_outcome"]["name"]!="unsettled_positive_signal_share":raise ValueError("Unexpected frozen primary")
    begin=time.perf_counter();sessions=[];round_records=[];reproduction=[];judges={}
    archive=ROOT/"data/upstream/data"
    for directory in sorted(archive.iterdir()):
        meta_path=directory/"experiment_metadata.json"
        if not meta_path.exists():continue
        meta=read_json(meta_path);primary=bool(PRIMARY_TAG.fullmatch(meta["auction_config"]["tag"]))
        if args.scope=="primary" and not primary:continue
        raw=directory/"auction_results.md"
        if not raw.exists():raise FileNotFoundError("Missing pre-specified outcome: "+str(raw))
        rows=parse_rounds(raw.read_text(encoding="utf-8"),meta)
        sm=read_json(directory/"collusion_metrics.json")
        validate_source_metrics(sm)
        session,rounds,checks=session_metrics(directory.name,meta,rows,sm)
        sessions.append(session);round_records.extend(rounds);reproduction.extend(checks)
        judges[directory.name]=llm_judge_summary(directory/"llm_eval_full.json",rows)
    primary=[x for x in sessions if x["is_primary"]]
    a=[x for x in primary if not x["seller_comms_enabled"]];b=[x for x in primary if x["seller_comms_enabled"]]
    if len(a)!=10 or len(b)!=10 or len({x["config_signature"] for x in primary})!=1:
        raise ValueError("Primary eligibility or metadata equivalence failed")
    if sorted(int(x["tag"].split("-")[-1]) for x in a)!=list(range(1,11)) or sorted(int(x["tag"].split("-")[-1]) for x in b)!=list(range(1,11)):
        raise ValueError("Missing pre-specified run identifier")
    keys=["unsettled_positive_signal_share","unsettled_positive_gt_025_share","unsettled_positive_gt_050_share",
      "unsettled_positive_ge_025_share","unsettled_positive_ge_050_share","zero_trade_round_share","positive_index_round_share",
      "trade_volume_fraction","normalized_seller_surplus","normalized_buyer_surplus","mean_executed_price"]
    contrasts={}
    for i,key in enumerate(keys):
        va=[x[key] for x in a if x[key] is not None];vb=[x[key] for x in b if x[key] is not None]
        contrasts[key]=bootstrap_difference(va,vb,seed=20261026+i)
    counts_a=[s["unsettled_positive_rounds"] for s in a];counts_b=[s["unsettled_positive_rounds"] for s in b]
    exact=exact_permutation_counts(counts_a,counts_b)
    groups={g:group_summary([x for x in sessions if x["group"]==g]) for g in sorted(set(x["group"] for x in sessions))}
    if len(reproduction)!=len(sessions)*len(SOURCE_KEYS):raise ValueError("Incomplete source-reproduction coverage")
    mismatches=[x for x in reproduction if not x["matches"]]
    summary={"study_title":protocol["study_title"],"source_commit":protocol["commit"],
      "protocol_sha256":hashlib.sha256((ROOT/"code/protocol.json").read_bytes()).hexdigest(),
      "scope":args.scope,"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "session_n":len(sessions),"round_n":len(round_records),"primary_session_n":20,
      "primary_groups":{"no_communication":group_summary(a),"communication":group_summary(b)},
      "primary_contrast":contrasts["unsettled_positive_signal_share"],"primary_exact_permutation":exact,
      "primary_round_totals":{"no_communication":{"positive_unsettled":sum(counts_a),"rounds":300},
        "communication":{"positive_unsettled":sum(counts_b),"rounds":300}},
      "secondary_contrasts":{k:v for k,v in contrasts.items() if k!="unsettled_positive_signal_share"},
      "descriptive_groups":groups,"reproduction":{"checks":len(reproduction),"mismatches":mismatches,"all_match":not mismatches,"tolerance":TOL},
      "execution_seconds":time.perf_counter()-begin,"new_llm_calls":0,
      "interpretation_cautions":["No ground-truth collusion labels","No paired random seeds established","No-trade does not prove no harm or no collusion","Not a fresh LLM experiment","Secondary contrasts descriptive; threshold sensitivity must be shown"]}
    out=ROOT/"results";out.mkdir(exist_ok=True)
    json_save(out/("summary_"+args.scope+".json"),summary)
    json_save(out/("sessions_"+args.scope+".json"),sessions)
    json_save(out/("source_reproduction_"+args.scope+".json"),reproduction)
    json_save(out/("stored_judge_summary_"+args.scope+".json"),judges)
    csv_sessions=[{k:v for k,v in x.items() if k!="settled_sign_cells"} for x in sessions]
    write_csv(out/("sessions_"+args.scope+".csv"),csv_sessions)
    write_csv(out/("rounds_"+args.scope+".csv"),round_records)
    print(json.dumps({"scope":args.scope,"sessions":len(sessions),"rounds":len(round_records),"primary":summary["primary_contrast"],
      "exact":exact,"reproduction":summary["reproduction"],"execution_seconds":summary["execution_seconds"]},allow_nan=False))
    if mismatches:raise RuntimeError("Source reproduction failed; inspect saved mismatch evidence")
if __name__=="__main__":main()
