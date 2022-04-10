import os
import time
import numpy as np
import imagePipes as iP
import csv
import dftTest as fT
import podTest as pT
import dmdTest as dT
import hurricaneNets as hN
from matplotlib import pyplot as plt


# General test


def classfierTest(f, pics, maxrank):
    times = []
    testmeans = []
    testvars = []
    for k in range(maxrank):
        # timing the data reconstruction for rank k
        recs = []
        t0 = time.perf_counter()
        for pic in pics:
            recs.append(f(pic, k))
        t1 = time.perf_counter()
        t = (t1-t0)/len(pics)
        times.append(t)
        # testing cnn accuracy on the reconstructed dataset
        for num, rec in enumerate(recs):
            if num < len(recs) // 2:
                np.save(f'temp_data/hurricane_{num}', rec)
            else:
                np.save(f'temp_data/non-hurricane_{num - len(recs) // 2}', rec)
        testmean, testvar = hN.test_data('temp_data')
        testmeans.append(testmean)
        testvars.append(testvar)
        for file in os.listdir('temp_data'):
            os.remove(f'temp_data/{file}')
    return times, testmeans, testvars


def vidTest(type, snapshots, skip, ranks, savename, trainTo):
    if not os.path.isdir(savename):
        os.mkdir(savename)
        os.mkdir(f'{savename}/vids-skip_{skip}')
        os.mkdir(f'{savename}/vids_reconstructed-skip_{skip}')
        os.mkdir(f'{savename}/time_errors')
        os.mkdir(f'{savename}/modes')
        os.mkdir(f'{savename}/mode_errors/')
        for rank in ranks:
            os.mkdir(f'{savename}/mode_errors/time_errors-rank_{rank}')
        os.mkdir(f'{savename}/dynamics')

    if type == 'POD':
        pT.recreate_video(snapshots, skip, ranks, savename)
    if type == 'DMD':
        dT.recreate_video(snapshots, skip, ranks, savename, trainTo)


# Run


if __name__ == "__main__":

    maxrank = 10
    path = f'training_data'
    files = os.listdir(path)
    pics = []
    times = []
    for file in files:
        data = np.load(f'training_data/{file}')
        pics.append(data)

    pic = pics[0]

    f, arrax = plt.subplots(2, 3)
    arrax[0, 0].imshow(pic)
    arrax[0, 0].set_title("IR scan of a hurricane")
    arrax[0, 0].tick_params(left=False, right=False, labelleft=False,
                labelbottom=False, bottom=False)


    arrax[0, 1].imshow(fT.recreate_image(pic, 1))
    arrax[0, 1].set_title("Rank 1 DFT recreation")
    arrax[0, 1].tick_params(left=False, right=False, labelleft=False,
                            labelbottom=False, bottom=False)

    arrax[0, 2].imshow(fT.recreate_image(pic, 5))
    arrax[0, 2].set_title("Rank 5 DFT recreation")
    arrax[0, 2].tick_params(left=False, right=False, labelleft=False,
                            labelbottom=False, bottom=False)

    arrax[1, 0].imshow(fT.recreate_image(pic, 10))
    arrax[1, 0].set_title("Rank 10 DFT recreation")
    arrax[1, 0].tick_params(left=False, right=False, labelleft=False,
                            labelbottom=False, bottom=False)

    arrax[1, 1].imshow(fT.recreate_image(pic, 25))
    arrax[1, 1].set_title("Rank 25 DFT recreation")
    arrax[1, 1].tick_params(left=False, right=False, labelleft=False,
                            labelbottom=False, bottom=False)

    arrax[1, 2].imshow(fT.recreate_image(pic, 125))
    arrax[1, 2].set_title("Rank 125 DFT recreation")
    arrax[1, 2].tick_params(left=False, right=False, labelleft=False,
                            labelbottom=False, bottom=False)

    plt.show()
    '''
    base_mean, base_var = hN.test_data('training_data')
    dft_times, dft_means, dft_vars = classfierTest(fT.recreate_image, pics, maxrank)
    pod_times, pod_means, pod_vars = classfierTest(pT.recreate_image, pics, maxrank)
    dmd_times, dmd_means, dmd_vars = classfierTest(dT.recreate_image, pics, maxrank)

    fig = plt.figure()
    ax0 = fig.add_subplot(111)
    ax0.set(xlabel='recreation_rank')
    ax0.set(ylabel='recreation_time (seconds)')
    ax0.plot(dft_times)
    ax0.plot(pod_times)
    ax0.plot(dmd_times)
    ax0.legend(['dft', 'pod', 'dmd'])
    plt.show()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set(xlabel='recreation_rank')
    ax1.set(ylabel='cnn_accuracy_mean')
    ax1.plot(base_mean*np.ones(maxrank))
    ax1.plot(dft_means)
    ax1.plot(pod_means)
    ax1.plot(dmd_means)
    ax1.legend(['base', 'dft', 'pod', 'dmd'])
    plt.show()

    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    ax2.set(xlabel='recreation_rank')
    ax2.set(ylabel='cnn_accuracy_variance')
    ax2.plot(base_var * np.ones(maxrank))
    ax2.plot(dft_vars)
    ax2.plot(pod_vars)
    ax2.plot(dmd_vars)
    ax2.legend(['base', 'dft', 'pod', 'dmd'])
    plt.show()
    '''