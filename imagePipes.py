import os
import csv
import numpy as np
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1 import make_axes_locatable
from celluloid import Camera
from IPython.display import HTML
from matplotlib import pyplot as plt


def fnorm(x):
    s = 0
    for i in range(0, len(x)):
        for j in range(0, len(x[0])):
            s = s + x[i][j] ** 2
    return np.sqrt(s)


def reqpics(a, b, c, d, e, f, crop, file='earth_pics'):
    filename = f'C:{file}/{a}-{b}-{c}_{d}-{e}-{f}-IR/'
    #if not os.path.isdir(filename):
    #    os.mkdir(filename)
    if b.find('0') == 0:
        b = b.partition('0')[2]
    if c.find('0') == 0:
        c = c.partition('0')[2]
    if e.find('0') == 0:
        e = e.partition('0')[2]
    if f.find('0') == 0:
        f = f.partition('0')[2]
    command = f'req_earth {a} {b} {c} {d} {e} {f} {crop}'
    os.system(f'cmd /c {command}')
    return filename


def pixelread(pixel, nscale):
    if not isinstance(pixel, np.ndarray):
        if pixel == 255:
            return 0
        for i in range(0, len(nscale)):
            if float(int(pixel) - int(nscale[i][0])) / 255 < 0.15:
                return float(i) / len(nscale)
    if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
        return 0
    for i in range(0, len(nscale)):
        if ((float(int(pixel[0]) - int(nscale[i][0])) / 255) ** 2
            + (float(int(pixel[1]) - int(nscale[i][1])) / 255) ** 2
            + (float(int(pixel[2]) - int(nscale[i][2])) / 255) ** 2) < 0.15:
            return float(i) / len(nscale)
    return 0


def picread(filename, picname, nscale, skip):
    print('Reading ' + picname)
    pic = mpimg.imread(filename + picname)
    npic = np.array(pic)
    m = len(npic) // skip
    n = len(npic[0]) // skip
    rpic = np.ndarray(shape=(m, n), dtype=float)
    for i in range(0, m):
        for j in range(0, n):
            rpic[i][j] = pixelread(npic[skip * i][skip * j], nscale)
    return (rpic)


def getpics(filename, skip, nscale):
    snapshots = [picread(filename, picname, nscale, skip)
                 for picname in os.listdir(filename)]
    return (snapshots)


def flatpics(filename, skip, nscale):
    list = os.listdir(filename)
    shp = np.shape(picread(filename, list[0], nscale, skip))
    snapshots = [picread(filename, picname, nscale, skip).flatten()
                 for picname in list]
    return (snapshots, shp)


def plotSave(vec, shape, fname, title):
    m = np.reshape(vec, shape)
    ax = plt.subplot(111)
    im = ax.imshow(m.real)
    plt.title(title)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    plt.colorbar(im, cax=cax)
    plt.savefig(f'{fname}.jpg')
    plt.close()


def makevid(snapshots, title='animation', loc=r'C:\Users\DELL\OneDrive\Desktop'):
    camera = Camera(plt.figure())
    for snapshot in snapshots:
        ax = plt.subplot(111)
        im = ax.imshow(snapshot)
        plt.title(title)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        plt.colorbar(im, cax=cax)
        camera.snap()
    ani = camera.animate(60)
    HTML(ani.to_html5_video())
    ani.save(rf'{loc}/{title}.mp4')
    plt.close()


def errordata(original, reconstructed, savename, filename, vidfile, title):
    fdiffs = []
    sdiffs = []
    diff = 0

    with open(f'{savename}/{filename}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['error'])
        for i, rframe in enumerate(reconstructed):
            fdiff = original[i] - rframe
            fdiffs.append(fdiff)
            norm = fnorm(original[i] - rframe)
            writer.writerow({'error': str(norm)})
            diff = diff + norm
            sdiffs.append((i, norm))

    plt.scatter(*zip(*sdiffs))
    plt.title(f'{title}')
    plt.savefig(f'{savename}/{filename}-fig')
    plt.close()

    makevid(fdiffs, f"{filename}_diffs_video", f'{vidfile}')

    return diff