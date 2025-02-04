import datetime
import math
import sys
import os
import pandas as pd
import numpy as np
from obspy import UTCDateTime
import glob

events_pha = pd.read_csv('/home/hypodd/results_hypodd/hypoDD.pha', sep="\t", names=[ "lines" ])

line_idx=np.where(events_pha['lines'].apply(lambda x: x[0]=='#'))
Origintime=events_pha.iloc[line_idx]['lines'].apply(lambda x: UTCDateTime(int(x[2:6]),int(x[7:9]),int(x[10:12]),int(x[13:15]),int(x[16:18]),float(x[19:24])))
EventId=events_pha.iloc[line_idx]['lines'].apply(lambda x: x[-8:-2])

def cutwaves(Net, Sta):
    os.makedirs('/home/cc/cuts/'+Net+'.'+Sta, exist_ok=True)
    wavelist=glob.glob('/home/waveforms/'+Net+'/'+Sta+'/*.mseed')
    channel_list=np.unique([i.split('/')[-1][0:3] for i in wavelist])

    for Cha in channel_list:
        st=obspy.read('/home/waveforms/'+Net+'/'+Sta+'/'+Cha+'.*.mseed')
        st=st.sort()
        st=st.merge(fill_value=0)
        for i in range(len(Origintime)):
            try:
                evmseed=st.slice(Origintime.iloc[i]-10,Origintime.iloc[i]+50)
                if len(evmseed)>0:
                    evmseed.write('/home/cc/cuts/'+Net+'.'+Sta+'/'+EventId.iloc[i]+'.'+Net+'.'+Sta+'.'+evmseed[0].stats.channel, format='MSEED')
            except:
                print('error cut '+EventId.iloc[i])



import multiprocessing as mp
import time

pool = mp.Pool(mp.cpu_count())
for Net in ['YR']:
    stalist=glob.glob('/home/waveforms/'+Net+'/*')
    stanames=[stapath.split('/')[-1] for stapath in stalist]
    for Sta in stanames:
        pool.apply_async(cutwaves,args=(Net, Sta))
        while pool._taskqueue.qsize() > 200:
            time.sleep(1)
pool.close()
pool.join()


os.system('cp /home/hypodd/results_hypodd/hypoDD.pha /home/cc/amatrice/pha.dat')

os.chdir('/home/cc/amatrice')
os.system('pwd')
os.system('./getmseedfiles')
os.system('./getcat')


import subprocess

# ✅unpreprocess
subprocess.Popen(
    "./runpreprocess.chasZ > outZ 2>&1", 
    shell=True, executable='/bin/bash', 
    cwd="/home/cc/amatrice/preprocess/runs"
).wait()

subprocess.Popen(
    "./runpreprocess.chasH > outH 2>&1", 
    shell=True, executable='/bin/bash', 
    cwd="/home/cc/amatrice/preprocess/runs"
).wait()

# ✅uncorrel9
subprocess.Popen(
    "./runcorrel9.chasZ > outZ 2>&1", 
    shell=True, executable='/bin/bash', 
    cwd="/home/cc/amatrice/correl/runs"
).wait()

subprocess.Popen(
    "./runcorrel9.chasN > outN 2>&1", 
    shell=True, executable='/bin/bash', 
    cwd="/home/cc/amatrice/correl/runs"
).wait()

subprocess.Popen(
    "./runcorrel9.chasE > outE 2>&1", 
    shell=True, executable='/bin/bash', 
    cwd="/home/cc/amatrice/correl/runs"
).wait()

# ✅runselect
subprocess.Popen(
    "./runselect5 > select.out 2>&1", 
    shell=True, executable='/bin/bash', 
    cwd="/home/cc/amatrice/correl/runs"
).wait()

