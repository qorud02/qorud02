"""Pinned public GitHub downloader. No LLM inference calls."""
import argparse, concurrent.futures, datetime, hashlib, json, os, pathlib, tempfile, time, urllib.request, urllib.parse, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
def git_hash(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument("--phase",choices=["metadata","primary","all"],default="metadata");a=p.parse_args()
 manifest=json.loads((ROOT/"data/source_manifest.json").read_text(encoding="utf-8"));files=manifest["files"]
 extra=ROOT/"data/outcome_manifest.json"
 if a.phase!="metadata":
  if not (ROOT/"code/protocol.json").exists():raise RuntimeError("Freeze protocol before outcomes")
  files+=json.loads(extra.read_text(encoding="utf-8"))["files"]
 selected=[f for f in files if not f["path"].startswith("data/") or f["path"].endswith("/experiment_metadata.json") or a.phase=="all" or re.match(r"data/\d{8}_\d{6}_base(?:-seller_comms)?-\d+/",f["path"])]
 def one(f):
  dest=ROOT/"data/upstream"/f["path"];dest.parent.mkdir(parents=True,exist_ok=True)
  if dest.exists():
   b=dest.read_bytes()
   if git_hash(b)!=f["git_blob_sha1"]:raise ValueError("Existing source hash mismatch: "+f["path"])
  else:
   url="https://raw.githubusercontent.com/"+manifest["repository"]+"/"+manifest["commit"]+"/"+urllib.parse.quote(f["path"],safe="/")
   for attempt in range(3):
    try:
     with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"CollusionEvidenceAudit/1.0"}),timeout=30) as response:b=response.read()
     if git_hash(b)!=f["git_blob_sha1"] or len(b)!=f["size"]:raise ValueError("Source hash/size mismatch: "+f["path"])
     fd,tmp=tempfile.mkstemp(prefix=".download-",dir=str(dest.parent))
     try:
      with os.fdopen(fd,"wb") as stream:stream.write(b)
      if dest.exists():raise FileExistsError(str(dest))
      os.replace(tmp,dest)
     finally:
      if os.path.exists(tmp):os.unlink(tmp)
     break
    except Exception:
     if attempt==2:raise
     time.sleep(attempt+1)
  return {"path":f["path"],"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"git_verified":True}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(one,selected))
 records.sort(key=lambda r:r["path"])
 result={"repository":manifest["repository"],"commit":manifest["commit"],"phase":a.phase,"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"files":records}
 (ROOT/"data"/("download_"+a.phase+"_verified.json")).write_text(json.dumps(result,indent=2),encoding="utf-8")
 print(json.dumps({"phase":a.phase,"files":len(records),"bytes":sum(x["bytes"] for x in records),"all_git_hashes_verified":True}))
if __name__=="__main__":main()
