## ltf library
This library is supposed to be a public library of all Token Engineering tools

## Installation
```python
pip install ltf
```

## List of all packages
```python
import ltf
help(ltf)
```

## A few examples
```python
from ltf.bondingcurves import Sigmoid
# sample csv file can be found in the data folder
sbc = Sigmoid(
    csv_path='./data/bondingcurves_initial_values.csv',
    current_supply=16000000,
    zoom=1
    )
sbc.fig_builder().show()
```

> `output:`
![](./data/sbc.png)


```
import pandas as pd
df = pd.DataFrame([{'l':1, 's':1, 'm':1, 'k':1, 'steps':1000}]) 
```
