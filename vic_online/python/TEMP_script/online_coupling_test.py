#%%
import os 
import flopy
import numpy as np
import subprocess  # for calling shell commands
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import vic_runner as vr
import support_function as sf
#%%

cwd = '/home/sliu/Documents/gitversion/VIC-WUR-GWM-1910/vic_online'
os.chdir(cwd)
filepath = os.path.join(cwd, 'python', 'VIC_config_file_template_pyread.txt')
statefile_dir = os.path.join(cwd, 'python', 'statefile')  #may change later 
configfile_dir = os.path.join(cwd, 'python', 'configfile')  #may change later

vic_executable = '/home/sliu/Documents/vic_indus/99SourceCode/VIC-WUR-GWM-1910/vic_offline/drivers/image/vic_image_gwm_offline.exe'

#%%
startstamp = datetime(1968, 1, 1)
current_date = datetime(1968,1,1)
finishdate = datetime(1975, 12, 31)

# Loop over the dates
while current_date <= finishdate:
    print("Running VIC for the time step [{}-{}]".format(current_date.year, current_date.month))
    #generate dmy for VIC run
    (startyear , startmonth , startday,
    endyear , endmonth , endday, 
    stateyear , statemonth , stateday, 
    init_date , init_datestr) = sf.prepare_dates(current_date)   
         
    # prepare VIC config file
    config_file = vr.prepare_vic(startyear, startmonth, startday, 
               endyear, endmonth, endday, 
               stateyear, statemonth, stateday, 
               init_date, init_datestr, 
               startstamp, filepath, statefile_dir, 
               configfile_dir, vic_executable)    
    #vr.run_vic(vic_executable, config_file, startyear, startmonth)    
    
    # Keep writing the PostProcessVIC() unwrapped version:
    
    