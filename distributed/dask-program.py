## import dependencies
import pandas as pd
import dask.dataframe as dd
import time

pd_start = time.process_time()
## read data into the pandas dataframe
pandas_dataframe = pd.read_csv('Sunspots.csv')

## calculate mean of a column
print(pandas_dataframe['Monthly Mean Total Sunspot Number'].mean())
print(f"time taken by pandas data frame computation is: {time.process_time()-pd_start}")


ddf_start = time.process_time()
# Read data into dask dataframe
dask_dataframe = dd.read_csv('Sunspots.csv')

# calculate mean of a column
print(dask_dataframe['Monthly Mean Total Sunspot Number'].mean().compute())
print(f"time taken by pandas data frame computation is: {time.process_time()-ddf_start}")