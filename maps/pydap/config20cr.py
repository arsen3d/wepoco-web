#
# Michael Saunby.  August 2011.
#
# Purpose:
# Configuration for 20th Century reanalysis datasets.
# These aren't downloaded in full, subset is selected using OPeNDAP server. 

dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/" 
monthly_monolevel = dods + "Datasets20thC_ReanV2/Monthlies/gaussian/monolevel/"

precip_rate_url = dods + "Datasets20thC_ReanV2/gaussian/monolevel/prate.2008.nc"

months20cr = {};

# Conversion from monthly mean rainfall rate in mm/s  (or (kg/m2)/s if you like)
# to month total.
secs_per_month = 2592000 # Assume all months 30 days


# Not every Python version needs the 'tolist()'- not sure which do.
# Can get nasty error when converting to JSON otherwise.

months20cr['prate_mon_mean']={
    'url': monthly_monolevel + 'prate.mon.mean.nc',
    'var': 'prate',
    'convert':  lambda data: (data*secs_per_month)[:].astype('float').tolist() 
    }
months20cr['air_2m_mon_mean']={
    'url': monthly_monolevel + 'air.2m.mon.mean.nc',
    'var': 'air',
    'convert':  lambda data: (data-273.15)[:].astype('float').tolist()
    }
months20cr['tmin_2m_mon_mean']={
    'url': monthly_monolevel + 'tmin.2m.mon.mean.nc',
    'var': 'tmin',
    'convert':  lambda data: (data-273.15)[:].astype('float').tolist()
    }
months20cr['tmax_2m_mon_mean']={
    'url': monthly_monolevel + 'tmax.2m.mon.mean.nc',
    'var': 'tmax',
    'convert':  lambda data: (data-273.15)[:].astype('float').tolist()
    }
