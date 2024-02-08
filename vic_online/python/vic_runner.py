#%%
from os.path import join
import os
os.chdir('/lustre/nobackup/WUR/ESG/yuan018/vic_from_sida/VIC-WUR-GWM-1910/vic_online/python')
import subprocess
from datetime import datetime, timedelta
import config_module
import netCDF4 as nc
import numpy as np
import support_function as sf
import calendar

#%%
def prepare_vic(startyear, startmonth, startday, endyear, endmonth, endday, 
            stateyear, statemonth, stateday, init_date, init_datestr,
            config):
    print("startyear,month, day is {},{},{}".format(startyear, startmonth, startday))
    print("end year, month, day is {},{},{}".format(endyear, endmonth, endday))
    print("statefile wll be save for {},{},{}".format(stateyear, statemonth, stateday))
    prefixes_firststep = {
    "STARTYEAR": startyear,    "STARTMONTH": startmonth,    "STARTDAY": startday,
    "ENDYEAR": endyear,    "ENDMONTH": endmonth,    "ENDDAY": endday,
    "STATENAME":  os.path.join(config.paths.statefile_dir, "state_file_"),
    "STATEYEAR": stateyear,    "STATEMONTH": statemonth,    "STATEDAY": stateday, 
    # Add other prefixes and their corresponding values here later if necessary
    }
    prefixes = {
    "STARTYEAR": startyear,    "STARTMONTH": startmonth,    "STARTDAY": startday,
    "ENDYEAR": endyear,    "ENDMONTH": endmonth,    "ENDDAY": endday,
    "INIT_STATE": os.path.join(config.paths.statefile_dir, f"state_file_.{init_datestr}_00000.nc"),
    "STATENAME":  os.path.join(config.paths.statefile_dir, "state_file_"),
    "STATEYEAR": stateyear,    "STATEMONTH": statemonth,    "STATEDAY": stateday,
    # Add other prefixes and their corresponding values here later if necessary
    }
    current_date = datetime(startyear, startmonth, startday)
    # Determine which prefixes to use
    if current_date ==  config.startstamp:
        current_prefixes = prefixes_firststep
    else:
        current_prefixes = prefixes
    # Update the prefixes with the current date
    current_prefixes["STARTYEAR"] = startyear
    current_prefixes["STARTMONTH"] = startmonth
    current_prefixes["STARTDAY"] = startday
    current_prefixes["ENDYEAR"] = endyear
    current_prefixes["ENDMONTH"] = endmonth
    current_prefixes["ENDDAY"] = endday
    current_prefixes["STATENAME"] = os.path.join(config.paths.statefile_dir, "state_file_")
    current_prefixes["STATEYEAR"] = stateyear
    current_prefixes["STATEMONTH"] = statemonth
    current_prefixes["STATEDAY"] = stateday
    if "INIT_STATE" in current_prefixes:
        current_prefixes["INIT_STATE"] = os.path.join(config.paths.statefile_dir, f"state_file_.{init_datestr}_00000.nc")
    
    with open(config.paths.template_dir, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        for prefix, value in current_prefixes.items():
            if prefix in line:
                lines[i] = f"{prefix}               {value}\n"
                break    
    # Write the modified lines back to the file
    config_file = os.path.join(config.paths.configfile_dir, f"config_{startyear}_{startmonth}.txt")
    with open(config_file, 'w') as file:
        file.writelines(lines)
        
    return config_file

#%%
def run_vic(config, config_file, startyear, startmonth):
    vic_executable = config.paths.vic_executable
  
    try:
        command = 'bash -c "{} -g {}"'.format(vic_executable, config_file)
        subprocess.run(command, check=True, shell=True)
        print("VIC-WUR run successfully for time step [{}-{}]".format(startyear, startmonth))
    except subprocess.CalledProcessError:
        raise SystemExit("Stopping the simulation due to failure in VIC execution.")
#%%    
def PostProcessVIC(config, startyear, startmonth):
    # Read the VIC output
    if config.humanimpact:
        human_or_nat = "human"
    else:
        human_or_nat = "naturalized"
    output_dir = config.paths.output_dir
    output_file = os.path.join(output_dir, f"fluxes_{human_or_nat}_gwm_.{startyear}-{startmonth:02d}.nc")

    vicout = nc.Dataset(output_file, 'r')
    print('Do a check if it is a coupling run(check if there is baseflow reported from VIC:)')
    if vicout.variables['OUT_BASEFLOW'][:,:,:].sum() == 0:
        print("baseflow is all 0")
    else:
    #stop the program
        print("there is baseflow reported,probably means it is not a coupling run, GWM.options is set incorrectly.")
        print("program will be stopped, please check the VIC configuration file")
        exit()   
    
    ts_gwrecharge = vicout.variables['OUT_GWRECHARGE'][:,:,:] /1000 # mm/day to m/day # with size of 1*180*204
    ts_discharge = vicout.variables['OUT_DISCHARGE'][:,:,:]  # keep it as m3/s

    current_sp = config.stress_period + 1
    if config.humanimpact: 
        # ts_gwabstract = ts_gwabstract.reshape(1, 180, 204) 
        well_flux = vicout.variables['OUT_WI_NREN_SECT'][:]
        well_flux_sum_wuclass = np.sum(well_flux, axis=1)
        well_flux_flip = np.flip(well_flux_sum_wuclass, axis=1)
        ts_gwabstract = well_flux_flip
    else:
        ts_gwabstract = np.zeros_like(ts_gwrecharge)
    
    return ts_gwrecharge, ts_discharge, ts_gwabstract
#%%
# def update_statefile(current_date,stateyear,statemonth,stateday,cpr_mm_month,config):  #TODO
    
#     max_moist_file = config.paths.vic_derived_param
#     #read the parameter file to get the fraction for each veg class
#     with nc.Dataset(param_file,'r') as param:
#         veg_class_fraction = param.variables['Cv'][:]
#     with nc.Dataset(max_moist_file,'r') as max_moist:
#         max_moisture = max_moist.variables['max_moist'][:]
    
#     # split the 
    
    
    
#     # Read the state file
#     statefile_dir = config.paths.statefile_dir
#     state_file = os.path.join(statefile_dir, f"state_file_.{stateyear}_{statemonth}_{stateday}_00000.nc")
#     stateout = nc.Dataset(state_file, 'r')
#     # read the 3 soil moisture layers 
#     soil_moisture = stateout.variables['OUT_SOIL_MOIST'][14,0,:,:]
#     # uadd the cpr_mm_month first 






#     print("updated the state file for the next time step")
# %%
