# project name: sara-cluster
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
from useful_scit.imps import *

def hist_better(ds,col,**dp_qwargs):
    # col = NCONC01
    ds1 = ds[[col]].to_dataframe()

    ds2 = ds1.dropna()

    q1,q2 = ds2.quantile([.02,.98]).values

    lg = np.logspace(np.log10(q1),np.log10(q2),20)
    ax = sns.distplot(
        ds2[q1<ds2][q2>ds2].dropna(),bins=lg.flatten(),kde=False,
        **dp_qwargs
    )
    ax.set_xscale('log')
    ax.set_title(col)


def hist_better_mult(ds,cols):
    lc = len(cols)
    f, axs = plt.subplots(1, lc, figsize=(5 * lc, 3), sharey=True)
    axs = axs.flatten()
    for c in range(lc):
        hist_better(ds, cols[c], ax=axs[c])

class MadeUp:
    def __init__(self,col:str,df:pd.DataFrame):
        # self.custom_winsorize(col, df)
        pass


def custom_winsorize(df:pd.DataFrame, col:str, quan=0.05):
    df1 = df
    # col = NCONC01
    _df = df[col]
    # quan = .05
    q1, q2 = _df.quantile([quan, 1 - quan])
    b1 = (_df > q1)
    b2 = (_df < q2)
    b3 = b1 & b2
    df1[col] = _df.where(b3)
    return df1