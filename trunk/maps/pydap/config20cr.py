#
# Michael Saunby.  August 2011.
#
# Purpose:
# Configuration for 20th Century reanalysis datasets.
# These aren't downloaded in full, subset is selected using OPeNDAP server. 

dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/" 
monthly_monolevel = dods + "Datasets20thC_ReanV2/Monthlies/gaussian/monolevel/"
monthly_sprd = dods + "Datasets20thC_ReanV2/Monthlies/gaussian_sprd/monolevel/"
ncep_derived = dods + "Datasets/ncep.reanalysis.derived/surface_gauss/"


# Would like to extend this to other data, e.g.
precip_rate_url = dods + "Datasets20thC_ReanV2/gaussian/monolevel/prate.2008.nc"


# Conversion from monthly mean rainfall rate in mm/s  (or (kg/m2)/s if you like)
# to month total.
secs_per_month = 2592000 # Assume all months 30 days


# Not every Python version needs the 'tolist()'- not sure which do.
# Can get nasty error when converting to JSON otherwise.


months20cr = {}

months20cr['ncep_prate_sfc_mon_mean']={
    'url': ncep_derived + 'prate.sfc.mon.mean.nc',
    'var': 'prate',
    'en':'precip mm',
    'convert':  lambda data: (data*secs_per_month)[:].astype('float').tolist() 
    }
months20cr['prate_mon_mean']={
    'url': monthly_monolevel + 'prate.mon.mean.nc',
    'var': 'prate',
    'en':'precip mm',
    'convert':  lambda data: (data*secs_per_month)[:].astype('float').tolist() 
    }
months20cr['sprd_prate_mon_mean']={
    'url': monthly_sprd + 'prate.mon.mean.nc',
    'var': 'prate',
    'en':'precip spread mm',
    'convert':  lambda data: (data*secs_per_month)[:].astype('float').tolist() 
    }
months20cr['ncep_air_2m_mon_mean']={
    'url': ncep_derived + 'air.2m.mon.mean.nc',
    'var': 'air',
    'en':'2m air temp C',
    'convert':  lambda data: (data-273.15)[:].astype('float').tolist()
    }
months20cr['air_2m_mon_mean']={
    'url': monthly_monolevel + 'air.2m.mon.mean.nc',
    'var': 'air',
    'en':'2m air temp C',
    'convert':  lambda data: (data-273.15)[:].astype('float').tolist()
    }
months20cr['sprd_air_2m_mon_mean']={
    'url': monthly_sprd + 'air.2m.mon.mean.nc',
    'var': 'air',
    'en':'2m air temp spread C',
    'convert':  lambda data: data[:].astype('float').tolist()
    }
months20cr['tmin_2m_mon_mean']={
    'url': monthly_monolevel + 'tmin.2m.mon.mean.nc',
    'var': 'tmin',
    'en':'2m t-min C', 
    'convert':  lambda data: (data-273.15)[:].astype('float').tolist()
    }
months20cr['tmax_2m_mon_mean']={
    'url': monthly_monolevel + 'tmax.2m.mon.mean.nc',
    'var': 'tmax',
    'en':'2m t-max C',
    'convert':  lambda data: (data-273.15)[:].astype('float').tolist()
    }
months20cr['wspd_10m_mon_mean']={
    'url': monthly_monolevel + 'wspd.10m.mon.mean.nc',
    'var': 'wspd',
    'en':'10m wind speed m/s',
    'convert':  lambda data: data[:].astype('float').tolist()
    }
months20cr['sprd_wspd_10m_mon_mean']={
    'url': monthly_sprd + 'wspd.10m.mon.mean.nc',
    'var': 'wspd',
    'en':'10m wind speed spread m/s',
    'convert':  lambda data: data[:].astype('float').tolist()
    }

