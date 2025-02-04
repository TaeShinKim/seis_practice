import glob
import numpy as np
from pathlib import Path
from obspy import read

wfBaseDir='./waveforms'
PhasenetResultDir='./results_phasenet_plus'
Path(PhasenetResultDir).mkdir(parents=True, exist_ok=True)

for fname in glob.glob(wfBaseDir+'/*/*/*Z..*.mseed'):
    stream = read(fname.replace('Z..', '?..'))
    Path('./waveforms_combined/'+fname.split('/')[-3]+'/'+fname.split('/')[-2]).mkdir(parents=True, exist_ok=True)
    out_fname = fname.replace('Z..', '..').replace('waveforms', 'waveforms_combined')
    stream.write(out_fname, 'MSEED')

mseed_path='./waveforms_combined/*/*/*.mseed'
filenames = glob.glob(mseed_path)
filenames=np.unique(filenames)
print('number of stations',len(filenames))


np.savetxt(PhasenetResultDir+'/mseed.txt', filenames, fmt='%s')
