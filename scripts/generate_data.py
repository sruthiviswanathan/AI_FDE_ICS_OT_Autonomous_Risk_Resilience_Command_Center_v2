import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(); p.add_argument('--check-only',action='store_true'); p.parse_args()
    m=json.loads((ROOT/'data/manifest.json').read_text())
    missing=[x for x in m['files'] if not (ROOT/x).exists()]
    print(json.dumps({'seed':m['seed'],'missing':missing,'status':'ok' if not missing else 'missing_files'},indent=2))
    raise SystemExit(1 if missing else 0)
if __name__=='__main__': main()
