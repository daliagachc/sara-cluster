# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *

# %%
import sara_cluster.util as scu
from sara_cluster.util import *
import useful_scit.plot.plot as ucp

# %%
data_path = '../data/raw/Original_eq.20_2.nc'

# %%
ds = xr.open_dataset(data_path)

# %%
hyam     = 'hyam'
hybm     = 'hybm'
hyai     = 'hyai'
hybi     = 'hybi'
date     = 'date'
gw       = 'gw'
LANDFRAC = 'LANDFRAC'
NCONC01  = 'NCONC01'
PS       = 'PS'
lat_wg   = 'lat_wg'
NMR01    = 'NMR01'
COAGNUCL = 'COAGNUCL'
H2SO4    = 'H2SO4'
SOA_LV   = 'SOA_LV'

cols = [
    NCONC01  ,
    NMR01    ,
    H2SO4    ,
    COAGNUCL ,
    SOA_LV   ,
]

time ='time'
lev  ='lev'
lat  ='lat'
lon  ='lon'

# %%
hist_better_mult(ds,cols)

# %%
df = ds[cols].to_dataframe()

# %%
dfr = df.reset_index([lat,lev,lon])

# %%
from sklearn.preprocessing import QuantileTransformer

# %%
qts = {}
df1 = df.copy()
for c in cols:
    qt = QuantileTransformer()
    data = qt.fit_transform(df[c].values.reshape(-1,1))
    df1[c]=data.flatten()
    qts[c]= qt

# %%
from sklearn.cluster import KMeans

# %%
c2 = cols
n_c = 10
kmean = KMeans(n_clusters=n_c, random_state=0)

# %%
from random import sample 

# %%
df2 = _df = df1[c2].dropna().copy()
sam = sample(range(len(_df)),int(len(_df)/10))
dfs = _df.iloc[sam].copy()

kmean.fit(dfs.values)

labs = kmean.predict(df2)

# %%
la = 'labs'
df2[la] = labs

# %%
_df = df2[la].value_counts().sort_index()
_df = _df/_df.sum()*100
_df.plot.bar(color=ucp.cc);

# %%
_df = df2.reset_index(drop=True)
_df[la]=_df[la].astype(str)

# %%
res = _df.groupby(la).boxplot(layout=(5,2),figsize=(20,10),return_type='both',patch_artist = True,);
plt.gcf().tight_layout()
_i = 0
for row_key, (ax,row) in res.iteritems():
    for i,box in enumerate(row['boxes']):
        box.set_facecolor(ucp.cc[_i])
        box.set_edgecolor('k')
    _i +=1

# %%
ds2 = df2.to_xarray() 

# %%
_la = ds2[la].astype(int)
bb = (_la<=n_c) & (_la>=0)

# %%
ds2[la]=_la.where(bb).astype('int32')

# %%
tot100 = df2[la].count()/100

# %%
mkrs = mpl.lines.Line2D.filled_markers

# %%
_df = df2.reset_index()[[lev,la,cols[0]]]
_d1 =_df
_d2 = _d1.groupby([lev,la]).count()
_d2 = _d2.unstack(la)[cols[0]].T/_d2.unstack(la).sum(axis=1) * 100
_d3 = _d2.T
_d3 = _d3.sort_index()
# ax = _d3.plot.area(color = ucp.cc,legend=False)
ax = _d3.plot.line(color = ucp.cc,legend=False,linewidth=1)
for i, line in enumerate(ax.get_lines()):
    line.set_marker(mkrs[i])
    line.set_markevery(3)
ax.set_xscale('log')

# %%
_df = df2.reset_index()[[lat,la,cols[0]]]
_d1 =_df
_d2 = _d1.groupby([lat,la]).count()
_d2 = _d2.unstack(la)[cols[0]].T/_d2.unstack(la).sum(axis=1) * 100
_d3 = _d2.T
_d3 = _d3.sort_index()
# ax = _d3.plot.area(color = ucp.cc,legend=False)
ax = _d3.plot.line(color = ucp.cc,legend=False,linewidth=1)
for i, line in enumerate(ax.get_lines()):
    line.set_marker(mkrs[i])
    line.set_markevery(5)

# %%
_df = df2.reset_index()[[lon,la,cols[0]]]
_d1 =_df
_d2 = _d1.groupby([lon,la]).count()
_d2 = _d2.unstack(la)[cols[0]].T/_d2.unstack(la).sum(axis=1) * 100
_d3 = _d2.T
_d3 = _d3.sort_index()
ax = _d3.plot.line(color = ucp.cc,legend=False,linewidth=1,marker='d')
for i, line in enumerate(ax.get_lines()):
    line.set_marker(mkrs[i])
    line.set_markevery(5)

# %%
_df1 = _df.groupby([la,time]).count()[cols[0]].unstack(la)

ax=_df1.plot.line(color=ucp.cc,legend=False)
for i, line in enumerate(ax.get_lines()):
    line.set_marker(mkrs[i])
    line.set_markevery(1)

# %%
import cartopy.crs as ccrs
fig,axs = plt.subplots(4,3,subplot_kw={'projection':ccrs.PlateCarree()},figsize=np.array([4.5*3,2*4]))
axf = axs.flatten()
for il in range(n_c):
    col = ucp.cc[il]
    _ds = ds2.where(ds2[la]==il)
    cm = ucp.create_cmap_from_color(col)
#     fig,ax = plt.subplots(subplot_kw={'projection':ccrs.PlateCarree()},figsize=(4.5,2))
    ax = axf[il]
    _ds1=_ds[la].count([lev,time])/ds2[la].count([lev,time])*100
    _ds1.plot(ax=ax, transform=ccrs.PlateCarree(),cmap=cm)
    ax.set_global(); ax.coastlines();

# %%
_df = df2.reset_index()[[time,la,cols[0]]]
# _df1 = df2.reset_index().set_index(time)[la]
# _df = _df.resample('M').count()#/_df1.resample('M').count()*100
# _df.plot(color=[col],linewidth=2)

# %%
