#%%
# config_module.py

import os
from osgeo import gdal
import numpy as np
import netCDF4 as nc
from datetime import datetime 
from dataclasses import dataclass

@dataclass
class Pathconfig:
    cwd: str = '/lustre/nobackup/WUR/ESG/liu297/gitrepo/VIC-WUR-GWM-1910/vic_online/'
    template_dir: str = os.path.join(cwd, 'python', 'VIC_config_file_naturalized_template_pyread_txt')
    statefile_dir: str = os.path.join(cwd , 'python', 'statefile')
    configfile_dir: str =  os.path.join(cwd , 'python', 'configfile')
    vic_executable: str = '/lustre/nobackup/WUR/ESG/liu297/vic_indus/11indus_run/99vic_offline_src/drivers/image/vic_image_gwm.exe'
    mfinput_dir: str = '/lustre/nobackup/WUR/ESG/yuan018/04Input_Indus/'
    output_dir: str = os.path.join(cwd, 'python', 'output')
    mfoutput_dir: str = os.path.join(cwd, 'python', 'mfoutput')
    mf6exe: str = '/lustre/nobackup/WUR/ESG/yuan018/mf6.4.1_linux/bin/mf6'
    clonemap: gdal.Dataset = gdal.Open(mfinput_dir + 'Clone_05min.nc')
    dem_ini: np.ndarray = gdal.Open(mfinput_dir + 'demfrom30s.nc').ReadAsArray()
    aqdepth_ini: np.ndarray = gdal.Open(mfinput_dir + 'damc_ave.nc').ReadAsArray()
    ksat_log: np.ndarray = gdal.Open(mfinput_dir + 'lkmc_ave.nc').ReadAsArray()
    cellarea: np.ndarray = gdal.Open(mfinput_dir + 'Indus_CellArea_m2_05min.nc').ReadAsArray()
    qbank: np.ndarray =gdal.Open(mfinput_dir + 'Qbank_new_average.nc') 
    riv_slope1: np.ndarray = gdal.Open(mfinput_dir+'slope05min_avgFrom30sec.nc').ReadAsArray()
    Z0_floodplain: np.ndarray = gdal.Open(mfinput_dir+'efplact_new_05min.nc').ReadAsArray()
    qaverage: np.ndarray = gdal.Open(mfinput_dir + 'mean_discharge_edwinInput.nc').ReadAsArray()
    min_dem: np.ndarray = gdal.Open(mfinput_dir+'mindem_05min.nc').ReadAsArray()
    KQ3: np.ndarray = gdal.Open(mfinput_dir + 'Recess_NEW.nc').ReadAsArray()
    conflayers: np.ndarray = gdal.Open(mfinput_dir + 'conflayers4.nc').ReadAsArray()
    ksat_l1_conf_log: np.ndarray = gdal.Open(mfinput_dir + 'kl1B_ave.nc').ReadAsArray()
    ksat_l2_conf_log: np.ndarray = gdal.Open(mfinput_dir + 'kl2B_ave.nc').ReadAsArray()
    spe_yi_inp: np.ndarray = gdal.Open(mfinput_dir+ 'StorCoeff_NEW.nc').ReadAsArray()
    #vic_output_file: nc.Dataset = nc.Dataset('/lustre/nobackup/WUR/ESG/yuan018/04Input_Indus/fluxes_Modis_GFDL-ESM4adj_historical_1970_2000_naturalized_offline_.1968-01.nc') 
    nc_boundary: nc.Dataset = nc.Dataset(mfinput_dir + 'boundary.nc')
    bdmask: np.ndarray = nc_boundary.variables['idomain'][:].data
    topl1_gwl: nc.Dataset = nc.Dataset(mfinput_dir + 'topl1_gwl_Indus_monthly_1968to2000.nc')
    gwll1: np.ndarray = topl1_gwl.variables['gwl'][:].data
    gwll1: np.ndarray = np.flip(gwll1, axis=1)
    topl2_gwl: nc.Dataset = nc.Dataset(mfinput_dir + 'topl2_gwl_Indus_monthly_1968to2000.nc')
    gwll2: np.ndarray = topl2_gwl.variables['gwl'][:].data
    gwll2: np.ndarray = np.flip(gwll2, axis=1)
    
    def set_cwd(self, cwd):
        self.cwd = cwd
    def set_template_dir(self, template_dir):
        self.template_dir = template_dir
    def set_statefile_dir(self, statefile_dir):
        self.statefile_dir = statefile_dir    
    def set_configfile_dir(self, configfile_dir): # Directory to store the vic configuration files
        self.configfile_dir = configfile_dir
    def set_vic_executable(self, vic_executable): # VIC executable
        self.vic_executable = vic_executable
    def set_startstamp(self, startstamp): # VIC start time
        self.startstamp = startstamp
    def set_output_dir(self, output_dir): # Directory to store the vic output files
        self.output_dir = output_dir
    def set_mfinput_dir(self, mfinput_dir): # raw input data directory for modflow simulation
        self.mfinput_dir = mfinput_dir
    def set_mfoutput_dir(self, mfoutput_dir): # Directory to store the modflow output files and the modflow generated inputs
        self.mfoutput_dir = mfoutput_dir
    def set_mf6exe(self, mf6exe): # modflow executable
        self.mf6exe = mf6exe
    def set_clonemap(self, clonemap): # a map to determin the extend and resolution of the MODFLOW simulation
        self.clonemap = clonemap
    def set_dem_ini(self, dem_ini):# raw dem data (modflow)
        self.dem_ini = dem_ini
    def set_aqdepth_ini(self, aqdepth_ini): # raw aquifer depth data (modflow)
        self.aqdepth_ini = aqdepth_ini
    def set_ksat_log(self, ksat_log): # raw ksat data (modflow)
        self.ksat_log = ksat_log
    def set_cellarea(self, cellarea): # cell area data (modflow, change the geographical grid in vic into orthogonal grid in modflow)
        self.cellarea = cellarea
    def set_nc_qbank(self, nc_qbank): # raw 30 year river discharge data (modflow input for RIV_bot_elevation )
        self.nc_qbank = nc_qbank
    def set_allqbank(self, allqbank): 
        self.allqbank = allqbank
    def set_riv_slope1(self, riv_slope1): # raw river slope data (modflow)
        self.riv_slope1 = riv_slope1
    def set_Z0_floodplain(self, Z0_floodplain):  # raw floodplain depth data (modflow)
        self.Z0_floodplain = Z0_floodplain
    def set_qaverage(self, qaverage): # raw mean discharge data (modflow)
        self.qaverage = qaverage
    def set_min_dem(self, min_dem): # raw minimum dem data (modflow)
        self.min_dem = min_dem
    def set_KQ3(self, KQ3): # raw KQ3 data (modflow)
        self.KQ3 = KQ3
    def set_conflayers(self, conflayers): # raw conflayers data (modflow)
        self.conflayers = conflayers
    def set_ksat_l1_conf_log(self, ksat_l1_conf_log): # raw ksat_l1 data (modflow, but it is the bottom layer))
        self.ksat_l1_conf_log = ksat_l1_conf_log 
    def set_ksat_l2_conf_log(self, ksat_l2_conf_log): # raw ksat_l2 data (modflow, but it is the top layer))
        self.ksat_l2_conf_log = ksat_l2_conf_log
    def set_spe_yi_inp(self, spe_yi_inp): # raw specific yield data (modflow)
        self.spe_yi_inp = spe_yi_inp
    def set_ts_gwrecharge(self, ts_gwrecharge): # raw groundwater recharge data from the vic simulation for modflow
        self.ts_gwrecharge = ts_gwrecharge
    def set_vic_output_file(self, vic_output_file): # vic output file for the current time step. it must be specified for each time step, the default it just a random file with vic results
        self.vic_output_file = vic_output_file
    def set_ts_discharge(self, ts_discharge):
        self.ts_discharge = ts_discharge
    def set_nc_boundary(self, nc_boundary): 
        self.nc_boundary = nc_boundary
    def set_bdmask(self, bdmask):
        self.bdmask = bdmask
    def set_topl1_gwl(self, topl1_gwl):
        self.topl1_gwl = topl1_gwl
    def set_gwll1(self, gwll1):
        self.gwll1 = gwll1
    def set_topl2_gwl(self, topl2_gwl):
        self.topl2_gwl = topl2_gwl
    def set_gwll2(self, gwll2):
        self.gwll2 = gwll2
    def set_missingvalue(self, missingvalue):
        self.missingvalue = missingvalue
    def set_idomain(self, idomain):
        self.idomain = idomain
    def set_qbank(self, qbank):
        self.qbank = qbank
    

    
#%% 
class config:
    def __init__(self): #without specifying the input, the default input will be used as below: 
        self.paths = Pathconfig()
        self.startstamp =  datetime(1968, 1, 1)
        self.ts_gwrecharge = gdal.Open(self.paths.mfinput_dir+'gwRecharge_month_1968to2000.nc').ReadAsArray() 
        self.bdmask = self.paths.nc_boundary.variables['idomain'][:].data 
        self.humanimpact = False
        
        #from here on are some derived variables based on the variables above:
        self.missingvalue = self.paths.aqdepth_ini[0][0] 
        self.idomain = self.paths.bdmask.astype(int)
        self.Nlay = 2  # number of layers in modflow
        self.Nrow, self.Ncol = self.paths.bdmask.shape  # number of rows and columns in modflow
        self.delrow = self.paths.clonemap.GeoGeoTransform()[1]*111*1000 # cell size in y direction in modflow
        self.delcol = self.paths.clonemap.GeoGeoTransform()[5]*111*1000 # cell size in x direction in modflow

            
    def set_humanimpact(self, humanimpact): # whether to vic simulation options for human impact is turned on
        self.humanimpact = humanimpact
    def cal_aqdepth(self):
        self.aqdepth = self.paths.aqdepth_ini.copy()
        self.aqdepth[self.paths.bdmask==-1] = 200
        self.aqdepth[self.paths.bdmask==0] = 200
        self.aqdepth[self.paths.bdmask==-2] = 200
        self.aqdepth = np.where(self.aqdepth > 0, self.aqdepth, 200)
        self.aqdepth[self.aqdepth==self.missingvalue] = 200
        return self.aqdepth
    
    def cal_toplayer_elevation(self):
        combined_mask = np.logical_or(self.paths.bdmask == 1, self.paths.bdmask == 2)
        self.top_layer1 = np.where(combined_mask, self.paths.dem_ini, 0)
        self.top_layer1 = np.where(self.top_layer1== self.missingvalue, 0, self.top_layer1)
        return self.top_layer1
    
    def cal_botlayer_elevation(self):
        if not hasattr(self, 'aqdepth'): # lazy loading/ on demand loading
            self.cal_aqdepth()        
        bot_layer1 = self.top_layer1-(self.aqdepth*0.1) #second layer is 10% total thickness
        bot_layer1 = top_layer2 = np.where(bot_layer1==self.missingvalue, -20 ,bot_layer1)
        top_layer2 = np.where(top_layer2==self.missingvalue, -20 ,top_layer2)
        bot_layer2 = self.top_layer1-self.aqdepth
        bot_layer2 = np.where(bot_layer2==self.missingvalue, -200 ,bot_layer2)
        self.botm = [bot_layer1, bot_layer2]
        return self.botm
    def initial_head(self): #this is only for the first time step. 
        startinghead_layer1 = self.paths.gwll2[0]  
        startinghead_layer2 = self.paths.gwll1[0]    #why 
        
        initial_head = [startinghead_layer1, startinghead_layer2]
        return self.initial_head
    
    

        

#%%
config_indus_ubuntu = config()

top_layer1 = config_indus_ubuntu.cal_toplayer_elevation()
aqdepth = config_indus_ubuntu.cal_aqdepth()
botm = config_indus_ubuntu.cal_botlayer_elevation()


#%%

cwd = '/lustre/nobackup/WUR/ESG/liu297/gitrepo/VIC-WUR-GWM-1910/vic_online/'
config_indus_ubuntu.paths.set_template_dir(os.path.join(cwd, 'python', 'VIC_config_file_naturalized_template_pyread_anunna.txt'))
config_indus_ubuntu.paths.set_statefile_dir(os.path.join(cwd, 'python', 'statefile'))
config_indus_ubuntu.paths.set_configfile_dir(os.path.join(cwd, 'python', 'configfile'))
config_indus_ubuntu.paths.set_vic_executable('/lustre/nobackup/WUR/ESG/liu297/vic_indus/11indus_run/99vic_offline_src/drivers/image/vic_image_gwm.exe')
config_indus_ubuntu.paths.set_startstamp(datetime(1968, 1, 1))
config_indus_ubuntu.paths.set_mfinput_dir('/lustre/nobackup/WUR/ESG/yuan018/04Input_Indus/')
config_indus_ubuntu.paths.set_mfoutput_dir('/lustre/nobackup/WUR/ESG/liu297/gitrepo/VIC-WUR-GWM-1910/vic_online/python/mfoutput/workspace/')
config_indus_ubuntu.set_humanimpact(False)

# %%
