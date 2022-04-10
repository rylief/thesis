from modulo.modulo import MODULO as mdl
import csv
import imagePipes as ip
import numpy as np
from matplotlib import pyplot as plt


def recreate_image(data, rank):
    m = mdl(data=data, n_Modes=rank)
    pod = m.compute_POD()
    sig = np.zeros(data.shape)
    for i in range(rank):
        sig[i][i] = pod[2][i]
    modes = np.zeros(data.shape)
    modes[:rank] = pod[0].T
    dynamics = np.zeros(data.shape)
    dynamics[:rank] = pod[1].T
    return np.matmul(np.matmul(modes.T, sig), dynamics)


def recreate_video(snapshots, skip=4, ranks=range(1, 10, 1), savename=''):
    shp = np.shape(snapshots[0])
    ip.makevid(snapshots, "Original frames", f'{savename}/vids-skip_{skip}')
    diffs = []

    with open(f'{savename}/rank_errors.csv', 'w') as g:
        rankWriter = csv.DictWriter(g, fieldnames=['rank', 'error'])
        for n in ranks:
            rank = str(n)
            m = mdl(data=snapshots)
            pod = m.compute_POD()
            frames = []
            sig = np.zeros(snapshots.shape)
            for i in range(n):
                sig[i][i] = pod[2][i]
            modes = np.zeros(snapshots.shape)
            modes[0: rank] = pod[0].T
            dynamics = np.zeros(snapshots.shape)
            dynamics[0: rank] = pod[1].T
            newSnapshots = np.matmul(np.matmul(modes.T, sig), dynamics)
            for frame in newSnapshots:
                frames.append(np.reshape(frame, shp))
            ip.makevid(frames, f"Reconstructed frames from {rank} mode(s)", f'{savename}/vids_reconstructed-skip_{skip}')
            fdiffs = []
            sdiffs = []
            diff = 0
            with open(f'{savename}/time_errors/time_error-{n}.csv', 'w') as f:
                writer = csv.DictWriter(f, fieldnames=['error'])
                for i, frame in enumerate(frames):
                    snap=np.reshape(snapshots[i],shp)
                    fdiff=snap-frame
                    fdiffs.append(fdiff)
                    norm=ip.fnorm(fdiff)
                    writer.writerow({'error':str(norm)})
                    diff=diff+norm
                    sdiffs.append((i, norm))
            plt.scatter(*zip(*sdiffs))
            plt.title(f"Norm vs Time at {rank} modes")
            plt.savefig(f'{savename}/Norm_vs_Time_at_{rank}_modes')
            ip.makevid(fdiffs, f"Original frames - Reconstructed frames from rank {rank} svd", f'{savename}\diffs-skip_{skip}')
            rankWriter.writerow({'rank':str(rank),'error': str(norm)})
            diffs.append((n, diff))
    plt.scatter(*zip(*diffs))
    plt.title("Norm vs Rank")
    plt.savefig(f'{savename}/Norm_vs_Rank')
    plt.close()