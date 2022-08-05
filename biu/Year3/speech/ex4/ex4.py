'''
Itay Hassid 209127596   Aviv Shisman 206558157
'''

# imports:
import torch
import numpy as np
from gcommand_loader import spect_loader
import gcommand_loader as loader
from torch import nn, optim
from torch.autograd.variable import Variable
import torch.nn.functional as F
from cer import cer
import os

# params:
out_dim = 27
num_epochs = 1 # if you want train from scratch turn it to 40 and remove the loading of model

# variables:
blank = '_'
idx_2_letter = {i: chr(i + 96) for i in range(1, 27)}
idx_2_letter[0] = blank
letter_2_idx = {chr(i + 96): i for i in range(1, 27)}
letter_2_idx[blank] = 0


cuda = torch.cuda.is_available()
device = torch.device("cuda" if cuda else "cpu")


def main():
    # getting info:
    train_set, valid_set, test_set = load_data()
    idx_2_class = {value: key for key, value in train_set.dataset.class_to_idx.items()}

    # creating model:
    model = SimpleNN().to(device)

    # train ,if you want train from scratch turn off the comment
    #train(train_set, model, idx_2_class, valid_set)

    # test
    test(train_set, model)

    return


'''
loading data....
'''


def load_data():
    print('loading dataset...')
    dataset = loader.GCommandLoader('train')
    train = torch.utils.data.DataLoader(
        dataset, batch_size=100, shuffle=True,
        num_workers=20, pin_memory=True, sampler=None)

    dataset = loader.GCommandLoader('valid')
    valid = torch.utils.data.DataLoader(
        dataset, batch_size=100, shuffle=True,
        num_workers=20, pin_memory=True, sampler=None)

    dataset = loader.GCommandLoader('test')  ################
    testS = torch.utils.data.DataLoader(
        dataset, batch_size=100, shuffle=None,
        num_workers=20, pin_memory=True, sampler=None)
    print('done')

    return train, valid,testS


def train(train_set, model, dic, valid_set):
    checkpoint = torch.load('latestmodel0.3036', map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    loss_func = nn.CTCLoss()
    model.train()

    # Total number of epochs to train
    for epoch in range(num_epochs):
        print('epoch:{}'.format(epoch + 1))
        total_loss = 0
        counter = 0
        for i, (batch_inputs, batch_labels) in enumerate(train_set):
            model.train()

            for j, (example, label) in enumerate(zip(batch_inputs, batch_labels)):
                example, label = example.to(device), label.to(device)
                optimizer.zero_grad()

                # predict
                probs = model(example, True)

                # calc ctc loss
                output = probs
                output = output.unsqueeze(dim=1)
                word = dic[label.item()]
                vec = torch.FloatTensor(get_word_idx(word)).to(device)
                vec = vec.unsqueeze(dim=0).type(dtype=torch.int)

                input_length = torch.as_tensor([50]).to(device)
                target_length = torch.as_tensor([len(word)]).to(device)
                loss = loss_func(output, vec, input_length, target_length)
                total_loss += loss.item()
                counter += 1

                # back-prop
                loss.backward()

                # update parameters.
                optimizer.step()

            if i%15 ==0:
                print('batch:{}, '.format(i),end='')
                print('current average loss: ', 1.0 * total_loss / counter)
                total_loss = 0
                counter = 0
        if epoch % 1 == 0:
            validation(valid_set, model, dic,loss_func)
            torch.save({
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                }, 'latestmodel')
    return


def validation(valid_set, model, dic,loss_func):
    total_cer = 0
    total_ctc = 0
    counter = 0

    model.eval()
    print('Validation:')
    for i, (batch_inputs, batch_labels) in enumerate(valid_set):
        if i % 5 == 0:
            print('batch:{}'.format(i + 1))
        for example, label in zip(batch_inputs, batch_labels):
            example, label = example.to(device), label.to(device)
            probs = model(example, False)
            output=[]
            for row in range(probs.shape[0]):
                current = probs[row]
                value = current.max(0, keepdim=True)[1].item()
                output.append(idx_2_letter[value])

            # calc loss:
            probs= probs.unsqueeze(dim=1)
            word = dic[label.item()]
            vec = torch.FloatTensor(get_word_idx(word)).to(device)
            vec = vec.unsqueeze(dim=0).type(dtype=torch.int)
            input_length = torch.as_tensor([50]).to(device)
            target_length = torch.as_tensor([len(word)]).to(device)
            loss = loss_func(probs, vec, input_length, target_length)
            total_ctc += loss.item()
            counter +=1

            # predict
            our_word = remove_reps(output)
            word = dic[label.item()]
            total_cer += cer(list(word),list(our_word))

    print('average cer: ', total_cer / counter)
    print('current average loss: ', 1.0 * total_ctc / counter)


def test(test_set, model):
    checkpoint = torch.load('latestmodel0.3036', map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    model.eval()
    print('test:')
    counter =0
    outFile = open('test_y','w')
    counter =0
    for file in os.listdir('test/test'):

        if ".DS_Store" in file:
            continue
        path = os.path.join('test/test',file)
        example = spect_loader(path,.02,.01,'hamming',normalize=True,max_len=101)

        probs = model(example, False)
        output = []
        for row in range(probs.shape[0]):
            current = probs[row]
            value = current.max(0, keepdim=True)[1].item()
            output.append(idx_2_letter[value])


        # predict
        our_word = remove_reps(output)


        our_word = remove_reps(output)
        outFile.write(file+ ', ' + our_word + '\n')
        counter += 1
    outFile.close()


# get string, return list
def get_word_idx(word):
    return [letter_2_idx[letter] for letter in word]


# example: hheeell_llo -> hello
def remove_reps(chr_vec):
    start = [chr_vec[0]]
    for i in range(1, len(chr_vec)):
        if chr_vec[i - 1] != chr_vec[i]:
            start.append(chr_vec[i])
    return ''.join(start).replace(blank, '')


'''
model 1
'''
class SimpleNN(torch.nn.Module):
    """
    A three hidden-layer generative neural network
    """

    def __init__(self):
        super(SimpleNN, self).__init__()

        self.conv1d = nn.Sequential(
            nn.Conv1d(101, 120, 10, padding=3),
            nn.SELU(),
            # nn.MaxPool1d(2, 2),
            nn.Conv1d(120, 90, 7, padding=3),
            nn.SELU(),
            nn.AvgPool1d(2),
        )
        self.lstm = nn.LSTM(79, 79, 3, dropout=0.4)
        self.hidden0 = nn.Sequential(

            nn.Linear(79, 90),
            nn.Dropout(0.5),
            nn.SELU(),
            # nn.BatchNorm1d(128),
            nn.Linear(90, 32),
            nn.Dropout(0.1),
            nn.SELU(),

            # nn.BatchNorm1d(64),
        )

        self.out = nn.Sequential(
            nn.Linear(32, out_dim),
            nn.SELU()
        )

    def lstm_forward(self, input):
        # Forward pass through LSTM layer
        # shape of lstm_out: [input_size, batch_size, hidden_dim]
        # shape of self.hidden: (a, b), where a and b both
        # have shape (num_layers, batch_size, hidden_dim).
        # lstm_out, self.hidden = self.lstm(input.view(len(input), 1, -1))
        lstm_out, self.hidden = self.lstm(input)
        return lstm_out
        # Only take the output from the final timetep
        # Can pass on the entirety of lstm_out to the next layer if it is a seq2seq prediction
        # y_pred = self.linear(lstm_out[-1].view(self.batch_size, -1))
        # return y_pred.view(-1)

    def forward(self, x, train=True):
        if train:
          x += Variable(x.data.new(x.size()).normal_(0, 1.1))
        x = x.permute(0,2,1)
        x = self.conv1d(x)
        x = x.permute(1,0,2)
#         x = self.lstm_forward(x)
        x, hidden = self.lstm(x)
        x = x.squeeze(1)
        x = self.hidden0(x)
        x = self.out(x)
        x = F.log_softmax(x, dim=1)
        return x


if __name__ == '__main__':
    main()


