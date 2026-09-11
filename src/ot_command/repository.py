from pathlib import Path
import csv, json
ROOT=Path(__file__).resolve().parents[2]
def rows(rel):
    with open(ROOT/rel,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def jsonl(rel):
    with open(ROOT/rel,encoding='utf-8') as f:return [json.loads(x) for x in f if x.strip()]
