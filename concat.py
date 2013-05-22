#[2013-04-25 04:35:52.348] [020800\00]1/RnhLmCellCPT rlibTraceTraceFunctions.cc:205 INFO:< Segmenting traces for key 117860156802909, 4 parts will follow >
#[2013-04-25 04:35:52.348] [020800\00]1/RnhLmCellCPT rlibTraceTraceFunctions.cc:214 INFO:<key 117860156802909 part 1>"rnhAdmC[cellFroId 295]: AdmReq: RnhIfCellAdmissionReqD{cellFroId 295,ueRef 5803,rncModuleId 16,cause"RRCConnectionEstablishment",establishmentCause"rnhIfCellAdmEstCause_OriginatingInteractiveCall",admissionClass"rnhIfCellAdm_Other",requestClassDl"rnhIfCellAdm_guaranteed",requestClassUl"rnhIfCellAdm_guaranteed",reqPriority""
#[2013-04-25 04:35:52.348] [020800\00]1/RnhLmCellCPT rlibTraceTraceFunctions.cc:214 INFO:<key 117860156802909 part 2>"rnhIfCellArp_level1",lowestPriorityLevel"rnhIfCellArp_level3",preemptionCapability"shallNotTriggerPreemption",currentAseDl 0,reqAseDl 49,currentAseUl 0,reqAseUl 49,reqActiveSetSize 1,selectedRLinRLs 1,currentSfDl 0,reqSfDl 128,currentCodeNo -1,currentTimePosition -1,reqTimePosition -1,nonPreferredTimePosition 0,slotFormatC"
#[2013-04-25 04:35:52.348] [020800\00]1/RnhLmCellCPT rlibTraceTraceFunctions.cc:214 INFO:<key 117860156802909 part 3>"apable"slotFormat_NotValid",currentSfUl 0,reqSfUl 64,currentSfUlEdch 0,reqSfUlEdch 0,compModeRes 0,physicalHsChan 0,eulCellType"rnhIfCellEul_NotValid",currentConnIs2msEul false,lowestDchRateAtEulConges -tion 0,currentIubGbrBandwidthDl 0,reqIubGbrBandwidthDl 29,currentIubGbrBandwidthUl 0,reqIubGbrBandwidthUl 31,speechOnly"spe"
#[2013-04-25 04:35:52.348] [020800\00]1/RnhLmCellCPT(1/ADMISSION_REJECT_CELL) ../RnhAdmC.cpp:888 TRACE5:[cellFroId 295] <key 117860156802909 part 4>"echNotValid",currentRcState 0,reqRcState 1,gbrDl 0,gbrUl 0,eSrbIndex -1,reqConnIsHs 0}: RejectReason: RbsDlHwResources, pmEventValueAtFailure 0, pmEventAdmPolicyLevel 10000"
#[2013-04-25 04:35:52.348] [020800\00]1/RnhLmCellCPT(1/ADMISSION_CELL) ../RnhAdmC.cpp:4010 TRACE7:[cellFroId 295] rnhAdmC[cellFroId 295]: signal data: int 867583522

#------------------------------------------------------------------------------------------------------------------------------------
#
# script to concatenate ericssons segmented traces
# Author: declan roche
# Date: 17/05/13
# version: 1
# usage python concat.py infile outfile
#
#-----------------------------------------------------------------------------------------------------------------------------------

# TTD
# - could add a verbose/debug flag


import re
import sys
import os.path
import datetime


def main():
  start  = datetime.datetime.now()  
  if len(sys.argv) != 3:
    print "Usage: python concat.py <infile> <outfile>"
    sys.exit()
  infile = sys.argv[1]
  outfile = sys.argv[2]
  print "\nConcatenate segmented traces \ninfile: %s \noutfile: %s"%(infile,outfile)
  if  not(os.path.exists(infile)):
    print "infile does not exist !!"
    sys.exit() 
     
  concat(infile,outfile)
  end = datetime.datetime.now()
  print "\nstarting: %s" %(start)
  print "finished: %s" %(end)
  print "duration: %s" % (end - start)
 


def concat(infile,outfile ):
  out=open(outfile,'w')
  f= open(infile,'r')
  reSeg = re.compile('Segmenting traces for key (\d*), (\d+)')  
  
  for line in f:
    match = reSeg.search(line)
    if match:
      key = match.group(1)
      times = int(match.group(2))
      str = ""
      errorStr = ''
      
      for n in range(times):
        li = f.next()
	
	# chk 1 - check for unexpected start line 
	if 'Segmenting traces for key' in li:
	  errorStr = "Error: unexpected start line"
	  # to do:rollback line, potential fault if two seg lines
	  # together will lose 2nd trace
	  break
	
	
	# chk 2 - check for missing key
	if key not in li:
	  errorStr = "Error: missing key"
	  break	  
        
	
	# chk 3 - check for correct part
	try:
          ind = li.index('>')	  
	except ValueError:          
	  errorStr = "Error: ValueError (>)"
	  break  
	if ind > 1000:
	  errorStr = "Error: ind >1000 (pre-chks)"
	  break
	if li[ind-1] in ['0','1','2','3','4','5']:
	  if int(li[ind-1]) != n+1:
	    errorStr = "Error: unexpected part no"
	    break  
	else:
	  errorStr = "Error: unexpected part"
	  break
	
	
	# extract segmented text for each line
	try:
          ind = li.index('"')
        except ValueError:          
	  errorStr = "Error: ValueError (\")"
	  break
	if ind > 200:
	  errorStr = "Error: ind >200 (extraction)"
	  break
	
	# concatenate lines  
	str = str + li[ind+1:-3]        	   
      
      
      if not errorStr:
        # add timestamp, module,etc info from last part
	xtra = li[:(li.find('TRACE')+7)]    
        out.write( xtra + str + "\n")
      else:
        print errorStr + "\n" + li + "\n"
      
    
if __name__ == '__main__':
    main()    
    


