import argparse, json
from .diagnostics import run_diagnostics

def main():
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['diagnostics']); a=p.parse_args()
    if a.command=='diagnostics': print(json.dumps(run_diagnostics(),indent=2))
if __name__=='__main__': main()
