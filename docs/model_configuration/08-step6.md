Now that your component is ready, let’s edit and build the Docker image that will capture the dependencies of your component.

By typing `mic encapsulate step6`, MIC will attempt to build and test the resultant image, running your component. For example, for our SWAT example you should see the following on your terminal:

```
MIC has created the execution directory /Users/mosorio/tmp/swat_simulation/executions/05_29_15_15_24/src

Added: TxtInOut into the execution directory
Running
 ./run   -i1 /Users/mosorio/tmp/swat_simulation/swat_simulation/data/TxtInOut  -p1 1993 -p2 1
cd TxtInOut'
cp ../swat670 .
chmod +x ./swat670'
./swat670'
                SWAT2018               
               Rev. 670               
      Soil & Water Assessment Tool    
               PC Version             
 Program reading from file.cio . . . executing

                SWAT2018               
               Rev. 670               
      Soil & Water Assessment Tool    
               PC Version             
 Program reading from file.cio . . . executing

                SWAT2018               
               Rev. 670               
      Soil & Water Assessment Tool    
               PC Version             
 Program reading from file.cio . . . executing

                SWAT2018               
               Rev. 670               
      Soil & Water Assessment Tool    
               PC Version             
 Program reading from file.cio . . . executing

                SWAT2018               
               Rev. 670               
      Soil & Water Assessment Tool    
               PC Version             
 Program reading from file.cio . . . executing

                SWAT2018               
               Rev. 670               
      Soil & Water Assessment Tool    
               PC Version             
 Program reading from file.cio . . . executing

  Executing year    1
                SWAT2018               
               Rev. 670               
      Soil & Water Assessment Tool    
               PC Version             
 Program reading from file.cio . . . executing


 Execution successfully completed 
+ set -e
+ cd .
+ . ./output.sh
./run: line 27: ./output.sh: No such file or directory
Success
The model has generated the following files
TxtInOut/output.rsv
TxtInOut/file.cio.bk
TxtInOut/output.rch
TxtInOut/output.sub
TxtInOut/hyd.out
TxtInOut/chan.deg
TxtInOut/bmp-sedfil.out
TxtInOut/septic.out
TxtInOut/swat670
TxtInOut/bmp-ri.out
TxtInOut/output.sed
TxtInOut/output.std
TxtInOut/output.hru
TxtInOut/file.cio
TxtInOut/input.std
TxtInOut/fin.fin
TxtInOut/watout.dat
Added: txtinoutoutput_rsv as a output
Added: txtinoutfile_cio_bk as a output
Added: txtinoutoutput_rch as a output
Added: txtinoutoutput_sub as a output
Added: txtinouthyd_out as a output
Added: txtinoutchan_deg as a output
Added: txtinoutbmp-sedfil_out as a output
Added: txtinoutseptic_out as a output
Added: txtinoutswat670 as a output
Added: txtinoutbmp-ri_out as a output
Added: txtinoutoutput_sed as a output
Added: txtinoutoutput_std as a output
Added: txtinoutoutput_hru as a output
Added: txtinoutfile_cio as a output
Added: txtinoutinput_std as a output
Added: txtinoutfin_fin as a output
Added: txtinoutwatout_dat as a output
```
MIC creates an `executions` folder where you will be able to see the results of the executed model, which in this case correspond to all the `Added` files listed in the command above.

### Expected results 
After this step, you will have created and validated your executable component. Congratulations! Now all that remains is make it available online
