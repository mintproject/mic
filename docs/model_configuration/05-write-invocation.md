## MINT wrapper

You must add the invocation line of your model,

### Types

An invocation can be one line.

For example, FloodSeverityIndex model. [Example](https://github.com/mintproject/MINT-WorkflowDomain/blob/master/WINGSWorkflowComponents/fsi-1.0.0/src/run#L19)

```bash
python FloodSeverityIndex.py ./ GloFAS_FloodThreshold.nc [23,48,3,15] [2016,2017] True
```

Or multiple lines as the HAND model. [Example](https://github.com/mintproject/HAND-TauDEM/blob/master/hand_v2_mint_component/src/run#L27)


```bash
...
pitremove -z $1 -fel demfel.tif
dinfflowdir -fel demfel.tif -ang demang.tif -slp demslp.tif
d8flowdir -fel demfel.tif -p demp.tif -sd8 demsd8.tif
aread8 -p demp.tif -ad8 demad8.tif -nc
areadinf -ang demang.tif -sca demsca.tif -nc

## Skeleton
slopearea -slp demslp.tif -sca demsca.tif -sa demsa.tif
d8flowpathextremeup -p demp.tif -sa demsa.tif -ssa demssa.tif -nc
python3 hand-thresh.py --resolution demfel.tif --output demthresh.txt
threshold -ssa demssa.tif -src demsrc.tif -thresh 500

streamnet -fel demfel.tif -p demp.tif -ad8 demad8.tif -src demsrc.tif -ord demord.tif -tree demtree.dat -coord demcoord.dat -net demnet.shp -w demw.tif -sw

connectdown -p demp.tif -ad8 demad8.tif -w demw.tif -o outlets.shp -od movedoutlets.shp

python3 hand-heads.py --network demnet.shp --output dangles.shp
python3 hand-weights.py --shapefile dangles.shp --template demfel.tif --output demwg.tif
```

What is the best option? That's is your decision. We provide flexibility.




### Adding your invocation line

!!! info
    The language of the run file is bash.


1. Open the file `src/run` 
2. Add the invocation line(s) after the comment `# WRITE THE COMMAND LINE INVOCATION HERE.`


```
# WRITE THE COMMAND LINE INVOCATION HERE
python FloodSeverityIndex.py ./ GloFAS_FloodThreshold.nc [23,48,3,15] [2016,2017] True
```


On the next page, we are going to learn how to pass the parameters to your model.