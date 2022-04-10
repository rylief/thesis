import numpy as np
from mydft import DFT


def recreate_image(data, rank):
    dim = (data.shape[0], data.shape[1])
    dft = DFT(data_dimension=dim, dft_rank=rank)
    return dft.fit(data)

