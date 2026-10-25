"""Behavioral integrity tests using explicitly synthetic diagnostic fixtures."""
import copy, hashlib, importlib.util, json, pathlib, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("audit",ROOT/"code/analyze.py")
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
def fixture(bid=92.5,trade=False):
    meta={"auction_config":{"rounds":30,"seller_valuations":[80]*5,"buyer_valuations":[100]*5,
      "tag":"base-1","seller_comms_enabled":False},"seller_ids":["s"+str(i) for i in range(5)],
      "buyer_ids":["b"+str(i) for i in range(5)]}
    rows=[{"round_number":i,"seller_asks":{s:95 for s in meta["seller_ids"]},
      "buyer_bids":{b:bid for b in meta["buyer_ids"]},"seller_messages":{},"buyer_messages":{},
      "trades":[{"round_number":i,"seller_id":"s0","buyer_id":"b0","price":90}] if trade else []} for i in range(1,31)]
    return meta,rows
def md(rows):
    return "\n".join("\n```json\n"+json.dumps(r)+"\n```\n" for r in rows)
class IntegrityTests(unittest.TestCase):
    def test_no_trade_price_is_missing_not_zero(self):
        meta,rows=fixture();result,rr,_=audit.session_metrics("synthetic",meta,rows)
        self.assertIsNone(result["mean_executed_price"]);self.assertEqual(result["trade_volume_fraction"],0)
        self.assertEqual(result["unsettled_positive_signal_share"],1)
        self.assertTrue(all(x["mean_executed_price"] is None for x in rr))
    def test_threshold_boundaries_are_explicit(self):
        meta,rows=fixture(92.5);s,_,_=audit.session_metrics("synthetic",meta,rows)
        self.assertEqual(s["unsettled_positive_gt_025_share"],0);self.assertEqual(s["unsettled_positive_ge_025_share"],1)
        meta,rows=fixture(95);s,_,_=audit.session_metrics("synthetic",meta,rows)
        self.assertEqual(s["unsettled_positive_gt_050_share"],0);self.assertEqual(s["unsettled_positive_ge_050_share"],1)
        meta,rows=fixture(90);s,_,_=audit.session_metrics("synthetic",meta,rows)
        self.assertEqual(s["unsettled_positive_signal_share"],0)
    def test_volume_surplus_conservation_and_sign_disagreement(self):
        meta,rows=fixture(trade=True);s,rr,_=audit.session_metrics("synthetic",meta,rows)
        self.assertEqual(s["trade_count"],30);self.assertEqual(s["mean_executed_price"],90)
        self.assertAlmostEqual(s["normalized_seller_surplus"],.1);self.assertAlmostEqual(s["normalized_buyer_surplus"],.1)
        self.assertAlmostEqual(s["realized_gains_from_trade_fraction"],.2)
        self.assertEqual(s["settled_sign_agreement_share"],0);self.assertEqual(s["settled_sign_cells"]["positive_nonpositive"],30)
    def test_missing_trade_key_is_not_interpreted_as_no_trade(self):
        meta,rows=fixture();del rows[0]["trades"]
        with self.assertRaises(ValueError):audit.parse_rounds(md(rows),meta)
    def test_truncated_missing_and_duplicate_rounds_fail(self):
        meta,rows=fixture()
        with self.assertRaises(ValueError):audit.parse_rounds(md(rows[:-1]),meta)
        rows[1]["round_number"]=1
        with self.assertRaises(ValueError):audit.parse_rounds(md(rows),meta)
    def test_malformed_json_fails(self):
        meta,rows=fixture();text=md(rows).replace('"round_number": 1','"round_number": nope',1)
        with self.assertRaises(json.JSONDecodeError):audit.parse_rounds(text,meta)
    def test_unknown_ids_and_nonfinite_bids_fail(self):
        meta,rows=fixture();rows[0]["buyer_bids"]={"intruder":92}
        with self.assertRaises(ValueError):audit.parse_rounds(md(rows),meta)
        meta,rows=fixture();rows[0]["buyer_bids"]["b0"]=float("nan")
        with self.assertRaises(ValueError):audit.parse_rounds(md(rows),meta)
    def test_duplicate_seller_trade_fails(self):
        meta,rows=fixture(trade=True);rows[0]["trades"].append({"round_number":1,"seller_id":"s0","buyer_id":"b1","price":91})
        with self.assertRaises(ValueError):audit.parse_rounds(md(rows),meta)
    def test_finite_negative_surpluses_are_preserved(self):
        meta,rows=fixture(trade=True)
        for row in rows:row["trades"][0]["price"]=79
        s,_,_=audit.session_metrics("synthetic",meta,rows)
        self.assertLess(s["normalized_seller_surplus"],0)
        self.assertAlmostEqual(s["normalized_seller_surplus"]+s["normalized_buyer_surplus"],s["trade_volume_fraction"])
    def test_source_tampering_is_detected(self):
        meta,rows=fixture();_,_,checks=audit.session_metrics("synthetic",meta,rows,{"num_trades":1})
        self.assertEqual(checks,[{"session":"synthetic","key":"num_trades","matches":False}])
    def test_exact_permutation_ties_are_counted(self):
        p=audit.exact_permutation_counts([0]*10,[0]*10)
        self.assertEqual(p["assignments"],184756);self.assertEqual(p["two_sided_p"],1)
        p=audit.exact_permutation_counts([0]*10,[30]*10)
        self.assertEqual(p["extreme_assignments"],2);self.assertEqual(p["two_sided_p"],2/184756)
    def test_missing_source_input_cannot_pass_vacuously(self):
        with self.assertRaises(ValueError):audit.validate_source_metrics(None)
        with self.assertRaises(ValueError):audit.validate_source_metrics({})
    def test_missing_one_source_metric_fails(self):
        valid={key:0 for key in audit.SOURCE_KEYS};audit.validate_source_metrics(valid)
        del valid["collusion_indices"]
        with self.assertRaises(ValueError):audit.validate_source_metrics(valid)
    def test_bootstrap_seed_is_reproducible(self):
        a=[0,1,2];b=[2,3,4]
        self.assertEqual(audit.bootstrap_difference(a,b,100,123),audit.bootstrap_difference(a,b,100,123))
    def test_pinned_download_bytes_match_source_manifest(self):
        for path in ("source_manifest.json","outcome_manifest.json"):
            m=json.loads((ROOT/"data"/path).read_text(encoding="utf-8"))
            for entry in m["files"]:
                local=ROOT/"data/upstream"/entry["path"]
                if not local.exists():continue
                b=local.read_bytes();actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
                self.assertEqual(actual,entry["git_blob_sha1"]);self.assertEqual(len(b),entry["size"])
    def test_completed_analysis_has_full_denominators_and_source_match(self):
        result=json.loads((ROOT/"results/summary_primary.json").read_text(encoding="utf-8"))
        self.assertEqual(result["primary_session_n"],20);self.assertEqual(result["round_n"],600)
        self.assertEqual(result["primary_round_totals"]["no_communication"]["rounds"],300)
        self.assertEqual(result["primary_round_totals"]["communication"]["rounds"],300)
        self.assertTrue(result["reproduction"]["all_match"])
if __name__=="__main__":unittest.main(verbosity=2)
