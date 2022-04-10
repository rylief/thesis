import numpy as np
import imagePipes as iP
import matplotlib.image as mpimg


hurricanes = [('2000', '08', '03', '2000', '08', '23', '1200x1200+0+0'),
              ('2000', '08', '19', '2000', '08', '24', '1200x1200+0+0'),
              ('2000', '09', '10', '2000', '09', '17', '1200x1200+0+0'),
              ('2000', '09', '14', '2000', '09', '18', '1200x1200+0+0'),
              ('2000', '09', '25', '2000', '10', '02', '1200x1200+0+0'),
              ('2000', '09', '28', '2000', '10', '06', '1200x1200+0+0'),
              ('2000', '10', '17', '2000', '10', '19', '1200x1200+0+0'),
              ('2001', '09', '01', '2001', '09', '15', '1200x1200+0+0'),
              ('2001', '09', '11', '2001', '09', '19', '1200x1200+0+0'),
              ('2001', '09', '21', '2001', '09', '27', '1200x1200+0+0'),
              ('2001', '10', '04', '2001', '10', '09', '1200x1200+0+0'),
              ('2001', '10', '29', '2001', '11', '05', '1200x1200+0+0'),
              ('2001', '11', '04', '2001', '11', '06', '1200x1200+0+0'),
              ('2001', '11', '24', '2001', '12', '04', '1200x1200+0+0'),
              ('2002', '09', '08', '2002', '09', '12', '1200x1200+0+0'),
              ('2002', '09', '14', '2002', '09', '27', '1200x1200+0+0'),
              ('2002', '09', '20', '2002', '10', '12', '1200x1200+0+0'),
              ('2002', '09', '21', '2002', '10', '04', '1200x1200+0+0')]

fname = 'C:/Users/DELL/PycharmProjects/thesisIdeas/'
picname = 'ir_scale.jpg'
scale = pic = mpimg.imread(fname + picname)

paths = ['training_pics/hurricanes/', 'training_pics/non-hurricanes/']

for m, path in enumerate(paths):
    nscale = np.unique(np.array(scale[0]), axis=0)
    snapshots = iP.getpics(path, 1, nscale)
    print(path)
    snapshots = snapshots / np.amax(snapshots)
    for n, snapshot in enumerate(snapshots):
        filename = ''
        if m == 0:
            filename = f'hurricane_{n}'
        if m == 1:
            filename = f'non-hurricane_{n}'
        np.save(f'training_data/{filename}', snapshot)
