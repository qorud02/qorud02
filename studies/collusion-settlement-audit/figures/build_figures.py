"""Build publication figures from completed primary-analysis outputs.
Requires bundled ReportLab only. Figures are independent vector PDF files.
"""
import hashlib,json,pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"figures";OUT.mkdir(exist_ok=True)
W=468.;H=270.
BLUE=HexColor("#235B7A");ORANGE=HexColor("#B76417");INK=HexColor("#182B3A");GRID=HexColor("#DEE5E9");GRAY=HexColor("#60717D")
def txt(c,x,y,s,size=9,font="Helvetica",align="left",color=INK):
 c.setFillColor(color);c.setFont(font,size)
 {"left":c.drawString,"center":c.drawCentredString,"right":c.drawRightString}[align](x,y,s)
def axes(c,x0,y0,x1,y1,lo,hi,ticks):
 def fy(v):return y0+(v-lo)/(hi-lo)*(y1-y0)
 for t in ticks:
  y=fy(t);c.setStrokeColor(GRID);c.setLineWidth(.5);c.line(x0,y,x1,y)
  txt(c,x0-8,y-3,str(t),9,align="right",color=GRAY)
 c.setStrokeColor(INK);c.setLineWidth(.8);c.line(x0,y0,x0,y1);c.line(x0,y0,x1,y0)
 return fy
def point(c,x,y,color,r=3.1):
 c.setFillColor(color);c.setStrokeColor(color);c.circle(x,y,r,stroke=1,fill=1)
def make1(sessions):
 p=OUT/"figure1_sessions.pdf";c=canvas.Canvas(str(p),pagesize=(W,H))
 c.setTitle("Unsettled positive signals by session");c.setAuthor("Kyunghan Bae")
 txt(c,W/2,H-17,"Unsettled positive signals by session",11,"Helvetica-Bold","center")
 fy=axes(c,62,64,453,228,0,35,[0,5,10,15,20,25,30,35])
 c.saveState();c.translate(16,146);c.rotate(90);txt(c,0,0,"Rounds with positive bid index and no trade (%)",9,align="center");c.restoreState()
 groups=[("no_communication",169,BLUE,["No seller","communication"]),("communication",349,ORANGE,["Seller","communication"])]
 values={}
 for name,x,color,label in groups:
  rows=[r for r in sessions if r["primary_group"]==name]
  vals=[r["unsettled_positive_signal_share"]*100 for r in rows];values[name]=vals
  if len(vals)!=10:raise ValueError("Expected ten independent sessions per group")
  # Distribute horizontally within exact-value ties; preserve every y value.
  for val in sorted(set(vals)):
   tied=[(i,r) for i,r in enumerate(rows) if r["unsettled_positive_signal_share"]*100==val]
   for rank,_ in enumerate(tied):
    jitter=(rank-(len(tied)-1)/2)*6.2
    point(c,x+jitter,fy(val),color,2.8)
  mean=sum(vals)/len(vals)
  c.setStrokeColor(INK);c.setLineWidth(2);c.line(x-25,fy(mean),x+25,fy(mean))
  # Place the mean label above the baseline cluster and below isolated high values.
  txt(c,x,fy(mean)+11,"Mean "+f"{mean:.3f}"+"%",9.5,"Helvetica-Bold","center")
  txt(c,x,44,label[0],10,align="center");txt(c,x,31,label[1],10,align="center")
  txt(c,x,16,"n = 10 sessions",9,align="center",color=GRAY)
 point(c,88,213,GRAY,2.6);txt(c,97,210,"One session",9,color=GRAY)
 c.setStrokeColor(INK);c.setLineWidth(2);c.line(88,196,102,196);txt(c,108,193,"Group mean",9,color=GRAY)
 c.showPage();c.save()
 return values
def make2(summary):
 p=OUT/"figure2_thresholds.pdf";c=canvas.Canvas(str(p),pagesize=(W,H))
 c.setTitle("Threshold sensitivity of the session-mean contrast");c.setAuthor("Kyunghan Bae")
 txt(c,W/2,H-17,"Threshold sensitivity of the session-mean contrast",11,"Helvetica-Bold","center")
 fy=axes(c,72,59,453,230,-2,16,[-2,0,2,4,6,8,10,12,14,16])
 c.saveState();c.translate(18,145);c.rotate(90)
 txt(c,0,1,"Communication - no communication",9,align="center")
 txt(c,0,-11,"(percentage points)",9,align="center");c.restoreState()
 c.setDash(3,2);c.setStrokeColor(GRAY);c.setLineWidth(.8);c.line(72,fy(0),453,fy(0));c.setDash()
 contrasts=[summary["primary_contrast"],summary["secondary_contrasts"]["unsettled_positive_gt_025_share"],summary["secondary_contrasts"]["unsettled_positive_gt_050_share"]]
 values=[]
 for x,th,a in zip([132,262,392],[0,.25,.5],contrasts):
  d,low,high=(a[k]*100 for k in ("difference","ci_low","ci_high"));values.append({"strict_threshold":th,"difference_pp":d,"ci_low_pp":low,"ci_high_pp":high})
  c.setStrokeColor(BLUE);c.setLineWidth(1.4);c.line(x,fy(low),x,fy(high));c.line(x-5,fy(low),x+5,fy(low));c.line(x-5,fy(high),x+5,fy(high))
  point(c,x,fy(d),BLUE,3.4);txt(c,x+11,fy(d)-3,f"{d:.2f}",9.5,"Helvetica-Bold")
  txt(c,x,42,f"{th:.2f}",10,align="center")
 txt(c,262,23,"Strict bid-index threshold (I > threshold)",9.5,align="center")
 txt(c,83,236,"Points: mean contrast; bars: 95% session-bootstrap intervals",9,color=GRAY)
 c.showPage();c.save()
 return values
def main():
 sessions=json.loads((ROOT/"results/sessions_primary.json").read_text(encoding="utf-8"))
 summary=json.loads((ROOT/"results/summary_primary.json").read_text(encoding="utf-8"))
 one=make1(sessions);two=make2(summary)
 meta={"dimensions":{"width_inches":6.5,"height_inches":3.75,"minimum_font_pt":9},"source_files":["results/sessions_primary.json","results/summary_primary.json"],
 "input_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ["results/sessions_primary.json","results/summary_primary.json"]},
 "figure1":{"pdf":"figure1_sessions.pdf","caption":"Unsettled positive signals by independent session. Each dot is the percentage of 30 rounds with a positive highest-buyer-bid index and no executed trade. Horizontal jitter separates ties without changing values; thick marks show group means (0.667% and 8.000%). Each condition contains ten independent sessions. A no-trade positive signal is not a ground-truth collusion false positive.","points_percent":one},
 "figure2":{"pdf":"figure2_thresholds.pdf","caption":"Threshold sensitivity of the session-mean contrast (seller communication minus no seller communication). Points show percentage-point differences in the share of rounds with I above the strict threshold and no executed trade. Bars are separate 95% percentile intervals from 20,000 within-condition session bootstrap resamples. The fixed primary threshold is zero; higher thresholds are descriptive secondary checks. Both effect size and evidential strength weaken at higher thresholds.","values":two}}
 meta["pdf_sha256"]={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob("figure*.pdf")}
 (OUT/"captions.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
 print(json.dumps({"figures":2,"dimensions_inches":[6.5,3.75],"minimum_font_pt":9,"figure2_values":two}))
if __name__=="__main__":main()
