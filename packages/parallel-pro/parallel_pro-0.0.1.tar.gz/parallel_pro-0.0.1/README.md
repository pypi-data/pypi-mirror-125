# parallel_pro
parallel_pro is a simple package for parallel processing.

# Installation
```bash
pip install parallel_pro
```

# How to use
```python
from parallel_pro import run_parallel
from datetime import datetime


def test(data):
    ss = list()
    for i in data:
        ss.append(i * 2)
    return ss


def main():
    start = datetime.now()
    data = run_parallel(list_of_data=list(range(100)), process_fun=test,workers=4,
                        verbose=False)
    end = datetime.now()
    # print(data)
    diff = end - start
    print(diff.total_seconds() / 60)
```