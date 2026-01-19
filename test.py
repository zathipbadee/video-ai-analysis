from concurrent.futures import ProcessPoolExecutor
from p_config import *

with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
    print(executor._max_workers)
