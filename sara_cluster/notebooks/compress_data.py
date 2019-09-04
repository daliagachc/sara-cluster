# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *

# %%
path = '../data/raw/'

# %%
files = glob.glob(os.path.join(path,'*.nc'))

# %%
files

# %%
f = files[0]

# %%
ds = xr.open_dataset(f)

# %%
za.compressed_netcdf_save(ds,'/tmp/ar.nc')

# %%
