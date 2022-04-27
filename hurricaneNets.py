import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os
import statistics
from threading import Thread


class HurricaneDataset(Dataset):
    def __init__(self, root, files):
        self.root = root
        self.data = []
        for file in files:
            fileclass = file.split('/')[-1]
            fileclass = fileclass.split('_')[0]
            self.data.append([file, fileclass])
        self.class_map = {'non-hurricane': 0, 'hurricane': 1}
        self.img_dim = (160, 160)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, k):
        item_name, item_class = self.data[k]
        arr = np.load(f'{self.root}/{item_name}')
        item_data = torch.from_numpy(arr)
        item_class_id = self.class_map[item_class]
        return item_data, np.eye(2)[item_class_id]


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 1, 3)
        self.fc1 = nn.Linear(79*79, 64)
        self.fc2 = nn.Linear(64, 8)
        self.fc3 = nn.Linear(8, 2)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.softmax(x, dim=1)


def netScore(data):
    m = statistics.mean(data)
    v = statistics.variance(data, m)
    return m, v


def train(train_data, test_data, outlist, index):

    print(f'Training on fold {index}')

    net = Net()

    net = net.float()

    train_set = DataLoader(train_data, batch_size=10, shuffle=True)
    test_set = DataLoader(test_data, batch_size=len(test_data), shuffle=True)

    optimizer = optim.Adam(net.parameters(), lr=0.0001)
    loss_function = nn.MSELoss()

    EPOCHS = 800
    epoch_accuracies = []
    losses = []
    for epoch in range(EPOCHS):
        if epoch % 40 == 0:
            print(index, epoch)
        epoch_losses = []
        for data in train_set:
            x, y = data
            y = torch.tensor(y, dtype=torch.float)
            net.zero_grad()
            output = net((x.view(-1, 1, 160, 160).float()))
            loss = (loss_function(output, y))
            epoch_losses.append(float(loss))
            loss.backward()
            optimizer.step()
        losses.append(statistics.mean(epoch_losses))
        correct = 0
        total = 0
        for i, data in enumerate(test_set):
            x, y = data
            y = torch.tensor(y, dtype=torch.float)
            output = net((x.view(-1, 1, 160, 160).float()))
            for j, guess in enumerate(output):
                if torch.argmax(guess) == torch.argmax(y[j]):
                    correct += 1
                total += 1
        epoch_accuracies.append(correct / total)
    outlist[index] = statistics.mean(epoch_accuracies)


def test_data(root):
    k_fold = 8
    fold_accuracies = [0.0]*8
    train_ratio = 1 - 1 / k_fold
    test_ratio = 1 - train_ratio

    files = os.listdir(root)
    arr = np.arange(len(files))
    np.random.shuffle(arr)
    files = [files[k] for k in arr]

    train_data = []
    test_data = []
    threads = [None] * 8

    for fold in range(k_fold):
        test_start = int((len(files)*test_ratio*fold))
        test_end = test_start + int(len(files)*test_ratio)
        train_files = files[:test_start] + files[test_end:]
        test_files = files[test_start:test_end]

        train_data = HurricaneDataset(root, train_files)
        test_data = HurricaneDataset(root, test_files)

        # Train the net on 8 folds with multithreading

        threads[fold] = Thread(target=train, args=(train_data, test_data, fold_accuracies, fold))
        threads[fold].start()

    for fold in range(k_fold):
        threads[fold].join()

    return netScore(fold_accuracies)
