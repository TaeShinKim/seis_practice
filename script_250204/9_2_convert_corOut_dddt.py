import os
from pathlib import Path


os.chdir('/home/cc/convcc')
Path('/home/cc/convcc/select').mkdir(parents=True, exist_ok=True)

os.system('cp /home/hypodd/results_hypodd/hypoDD.pha pha.all')
os.system('cp /home/cc/amatrice/corr/corr.Pwaves/select/*.P /home/cc/convcc/select/.')
os.system('cp /home/cc/amatrice/corr/corr.Swaves/select/*.S /home/cc/convcc/select/.')
os.system('./convcc.sh ./select pha.all pha.all 3') 
os.system('cp /home/cc/convcc/dt.cc.P5 /home/hypodd/results_hypodd/dt.cc')
