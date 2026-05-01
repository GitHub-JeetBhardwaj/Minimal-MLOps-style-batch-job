import argparse
import yaml
import pandas as pd
import numpy as np
import logging
import json
import time
import sys
import os

__author__="Jeet Bhardwaj"

def setup_log(log_path):
    os.makedirs(os.path.dirname(os.path.abspath(log_path)),exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s-%(levelname)s-%(message)s',
        handlers=[logging.FileHandler(log_path),logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger("Jeet_BatchJob")
def main():
    t0=time.time()
    
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",required=True)
    parser.add_argument("--config",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--log-file",required=True)
    args=parser.parse_args()

    log=setup_log(args.log_file)
    log.info(f"Starting job run by {__author__}")
    
    version="unknown"

    try:
        if not os.path.exists(args.config): raise FileNotFoundError("Config missing")
        with open(args.config,'r') as f:
            cfg=yaml.safe_load(f)
            
        version=str(cfg.get('version','unknown'))
        seed=int(cfg['seed'])
        window=int(cfg['window'])
        np.random.seed(seed)
        log.info(f"Config OK - ver:{version} seed:{seed} win:{window}")

        if not os.path.exists(args.input): raise FileNotFoundError("No data file")
        if os.path.getsize(args.input)==0: raise ValueError("Empty data file")
        
        df=pd.read_csv(args.input)
        if not os.path.exists(args.input): raise FileNotFoundError("No data file")
        if os.path.getsize(args.input)==0: raise ValueError("Empty data file")
        
        df = pd.read_csv(args.input, sep=r'[,;\t]', engine='python', quoting=3)
        
        df.columns = df.columns.str.replace('"', '').str.replace("'", "").str.lower().str.strip()
        
        if 'close' not in df: 
            raise ValueError(f"Missing 'close' col. Columns found: {df.columns.tolist()}")
        
        df['close']=pd.to_numeric(df['close'],errors='coerce')
        if df['close'].isna().all(): raise ValueError("Bad close data")
        log.info(f"Data loaded - {len(df)} rows")
        
        
        df['close']=pd.to_numeric(df['close'],errors='coerce')
        if df['close'].isna().all(): raise ValueError("Bad close data")
        log.info(f"Data loaded - {len(df)} rows")

        log.info("Calculating rolling mean & signals")
        df['rmean']=df['close'].rolling(window).mean()
        df['signal']=(df['close']>df['rmean']).astype(int)

        valid=df['signal'][df['rmean'].notna()]
        rate=float(valid.mean()) if not valid.empty else 0.0
        ms=int((time.time()-t0)*1000)

        out={
            "version":version,
            "rows_processed":len(df),
            "metric":"signal_rate",
            "value":round(rate,4),
            "latency_ms":ms,
            "seed":seed,
            "status":"success"
        }

        with open(args.output,'w') as f:
            json.dump(out,f,indent=4)
            
        print(json.dumps(out,indent=4))
        log.info(f"Done in {ms}ms")

    except Exception as e:
        log.error(str(e))
        err={
            "version":version,
            "status":"error",
            "error_message":str(e)
        }
        with open(args.output,'w') as f:
            json.dump(err,f,indent=4)
        print(json.dumps(err,indent=4))
        sys.exit(1)

if __name__=="__main__":
    main()