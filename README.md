# sshBruteScan
#Batch ssh brute force based on thread pool

Premise：
pip install -r requirement

Usage:
Usage: sshBruteScan.py [options] arg

Options:
  -h, --help            show this help message and exit
  -H TGTHOST, --tgthost=TGTHOST
  -t THREADNUM, --threadnum=THREADNUM
  
Examples：
sshBruteScan.py -H 118.183.1.1 -t 100
