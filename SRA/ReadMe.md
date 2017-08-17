## SRA RAID

This is a simple shell script that takes list of SRA accessions and downloads them using wget. 
I wrote this because prefetch was not working as expected on the server I wanted to use for downloads.
Additionally, this allows the script to run easily with nohup. A step I had to take for several SRA accessions.
give SRA_Raid.sh a file contains a series of accessions 1 per line. 
Initially, I included a sleep statement for lists containing larger SRA accessions. 
I have take that out. or SRA_Raid.sh making both scripts virtually identical.

usage:
```
SRA_Raid.sh <SRA list>.txt

```
or
```
SRA_Raid_lt1Gb.sh <SRA list>.txt

```
