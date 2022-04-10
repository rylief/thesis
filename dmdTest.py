import csv
import imagePipes as ip
import numpy as np
from matplotlib import pyplot as plt
from pydmd import DMD


def recreate_image(data, rank):
    dmd = DMD(svd_rank=rank)
    dmd.fit(data)
    return dmd.reconstructed_data.real


def recreate_video(snapshots, skip: object = 4, ranks=range(5, 185, 5), savename='', trainTo=0):
    shape = snapshots[0].shape
    ip.makevid(snapshots, "Original frames", f'{savename}/vids-skip_{skip}')
    diffs=[]

    with open(f'{savename}/rank_errors.csv', 'w') as g:
        rankWriter = csv.DictWriter(g, fieldnames=['rank', 'error'])
        for n in ranks:
            rank = str(n)
            dmd = DMD(svd_rank=n)
            if trainTo==0:
                dmd.fit(snapshots)
            else:
                print(1+(len(snapshots)-trainTo)/trainTo)
                dmd.fit(snapshots[:trainTo,:])
                dmd.dmd_time['tend']*=1+(len(snapshots)-trainTo)/trainTo
            print(f"Generating Eigenvalues with rank {rank} svd")
            # Make a place to just save this
            dmd.plot_eigs(show_axes=True, show_unit_circle=True, filename=f'{savename}/Eigenvalues')
            plt.close()
            mdiffs = []
            for i, mode in enumerate(dmd.modes.T):
                product = []
                ip.plotSave(mode.real, shape, f'{savename}/modes/mode_{i}', f'mode_{i}')
                for weight in dmd.dynamics[i]:
                    product.append((np.reshape(mode, shape) * weight).real)
                ip.makevid(product, f"Product of Mode {i} and its Dynamics", f'{savename}/modes')
                mdiffs.append((i, ip.errordata(snapshots, product, f'{savename}/mode_errors/time_errors-rank_{rank}', f'time_error-mode_{i}',
                          f'{savename}\mode_errors/time_errors-rank_{rank}', f'Original frames - Mode {i} of Reconstruction')))
            for j, dynamic in enumerate(dmd.dynamics):
                plt.plot(dynamic.real)
                plt.title(f'dynamic_{j}')
                plt.savefig(f'{savename}/dynamics/dynamic_{j}')
                plt.close()
            frames = []
            for i, frame in enumerate(dmd.reconstructed_data.T):
                picframe = np.reshape(snapshots[i], shape)
                frames.append(picframe)
            ip.makevid(frames, f"Reconstructed frames from rank {rank} svd", f'{savename}/vids_reconstructed-skip_{skip}')
            diff = ip.errordata(snapshots, frames, f'{savename}/time_errors', f'time_error-rank_{n}',
                             f'{savename}/time_errors', f'Original frames - Reconstructed frames from rank {rank} svd')
            rankWriter.writerow({'rank':str(rank),'error': str(diff)})
        diffs.append((n, diff))
        plt.scatter(*zip(*mdiffs))
        plt.title("Norm vs Mode")
        plt.savefig(f'{savename}/mode_errors-rank_{rank}')
        plt.close()
    plt.scatter(*zip(*diffs))
    plt.title("Norm vs Rank")
    plt.savefig(f'{savename}/Norm_vs_Rank')
    plt.close()
