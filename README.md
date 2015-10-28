# Merge Graph
## Visualize your fastq merge

### Usage
```
usage: merge_graph.py [-h] [-f FORWARD] [-r REVERSE] [-i RUN_FOLDER] -a
                      AMPLICON -o OUTFILE

Visualize your merges

optional arguments:
  -h, --help            show this help message and exit
  -f FORWARD, --forward FORWARD
                        Forward read fastq file
  -r REVERSE, --reverse REVERSE
                        Reverse read fastq file
  -i RUN_FOLDER, --run RUN_FOLDER
                        A directory of fastqs
  -a AMPLICON, --amplicon AMPLICON
                        The desired amplicon length
  -o OUTFILE, --output OUTFILE
                        The name of the output PNG
```
### Example Usage
Individual fastqs
`merge_graph.py -f fastqs/v3/MYFASTQ_S42_L001_R1_001.fastq -r fastqs/v3/MYFASTQ__S42_L001_R2_001.fastq -a 292 -o fastqs/graph.png`
Directory of fastqs
`merge_graph.py -i fastqs/v3/ -a 292 -o fastqs/graph.png`

### Output 
A beautiful graph
![What a beaut!](https://raw.githubusercontent.com/gblanchard4/merge_graph/master/merge.png "Snazzy!")
