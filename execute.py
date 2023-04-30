# -*- coding:utf-8 -*-
from asyncio.windows_events import NULL
import os
import sys
import time
import torch
import seq2seqModel
from config import getConfig
import io
from torch import optim
import nltk

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

gConfig = {}
gConfig= getConfig.get_config()
units=gConfig['layer_size']
BATCH_SIZE=gConfig['batch_size']
EOS_token=1
SOS_token=0
MAX_LENGTH=gConfig['max_length']
hidden_size  =256


"""
format the input sentence
"""
def modify_input(sen ):
    sen = nltk.word_tokenize(sen)
    sen = [''.join([i for i in s if not i.isdigit()]) for s in sen]
    sen = ' '.join([s.lower() for s in sen])
    return sen


def undestanding_ratio(lang, sen):
    count = 0 
    senL = sen.split(" ")
    for word in senL:
        if word not in lang.word2index:
            count +=1
    return (float)(count/len(senL))
"""
input_lang: a Lang class to hold all words appear in answer
output_lang: a Lang class to hold all words appear in ask
pairs: a list of tuple hold all ask and answer as [(answer, ask)....] 
"""
def create_dataset(path, num_examples):
    lines = io.open(path, encoding='UTF-8').read().strip().split('\n')
    pairs = [l.split('=>') for l in lines[:num_examples]]
    lang=Lang("dict")
    #pairs = [list(reversed(p)) for p in pairs]
    #print(pairs)
    for pair in pairs:
        lang.addSentence(pair[0])
        lang.addSentence(pair[1]) 
    
    return lang,pairs

def max_length(tensor):
    return max(len(t) for t in tensor)


"""
database:
    name: the name of the database
    word2index: {(w: the number of words database has when w enter the database)...}
    word2count: {(w: the appreance count of w)...}
    index2word: reverse version of word2index 
"""
class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {}
        self.n_words = 0  # Count start and end

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1
            
    
    def print_stucture(self):
        for i in range(self.n_words):
            word =self.index2word[i]
         
            print(self.index2word[i]+ ": "+"count: "+ str(self.word2count[word])+ "   index: "+ str(self.word2index[word]) +"\n" )

"""
convert a sentence to a list of indexes of words
the index is the number of words in database when the word enter, store in self.word2index
then the return is the tensor of the indexes list
"""
def indexesFromSentence(lang, sentence):
    #change after
    L = [lang.word2index[word] if word in lang.word2index else 0 for word in sentence.split(' ')]
    #print(len(L))
    return L

def tensorFromSentence(lang, sentence):

    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)

    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)


"""
read from data file, create database. Then convert each ask to indexes tensor, 
and then put all ask index tensor together to target_tensor
Then do same things to answer and then have input_tensor

return:
    input_tensors: answer index tensor for each answer
    input_lang: answer word database
    target_tensors: ask index tensor for each ask
    target_lang: ask word database
"""
def read_data(path,num_examples):
    input_tensors=[]
    target_tensors=[]
    lang,pairs=create_dataset(path,num_examples)
    
    limit = 0
    if(num_examples - 1 > len(pairs)):
        limit = len(pairs)
    else:
        limit = num_examples -1

    for i in range(0,limit):
        input_tensor = tensorFromSentence(lang, pairs[i][0])
        target_tensor = tensorFromSentence(lang, pairs[i][1])
        input_tensors.append(input_tensor)
        target_tensors.append(target_tensor)
    
    return lang, input_tensors,target_tensors




def train(input_lang, target_lang, input_tensor, target_tensor):
    
    # 
    print("Preparing data in %s" % gConfig['train_data'])
    steps_per_epoch = len(input_tensor) // gConfig['batch_size']
    #print(steps_per_epoch)
    checkpoint_dir = gConfig['model_data']

    # initialize model
    epoch_c = 0
    start_time = time.time()
    encoder = seq2seqModel.Encoder(input_lang.n_words, hidden_size).to(device)
    decoder = seq2seqModel.AttentionDencoder(hidden_size, target_lang.n_words, dropout_p=0.1).to(device)
    # check if there is available model
    if os.path.exists(checkpoint_dir):
        print("Load existed model")
        checkpoint = torch.load(checkpoint_dir)
        encoder.load_state_dict(checkpoint['modelA_state_dict'])
        decoder.load_state_dict(checkpoint['modelB_state_dict'])
        epoch_c=checkpoint['epoch']


    max_data=gConfig['max_train_data_size']

    # check the data size with max data size 
    limit = 0 
    if(len(input_tensor)>max_data):
        limit = max_data
    else:
        limit = len(input_tensor)

    
   
    total_loss = 0
    batch_loss=1
    step_loss =100

    print("Total Steps :"+str(limit//BATCH_SIZE))
    # train until reach the desired loss
    while step_loss>gConfig['min_loss']:
        #start_time_epoch = time.time()
        print("Start " + str(epoch_c)+" epoch: ")
        # train the model with all the data in dataset Lang according to BATCH_SIZE
        for i in range(1,limit//BATCH_SIZE):
            # seperate data by batch size
            inp=input_tensor[(i-1)*BATCH_SIZE:i*BATCH_SIZE]
            targ=target_tensor[(i-1)*BATCH_SIZE:i*BATCH_SIZE]
            # train function in model class
            batch_loss = seq2seqModel.train_step(inp, targ,encoder,decoder,optim.SGD(encoder.parameters(),lr=0.001),optim.SGD(decoder.parameters(),lr=0.01))
            total_loss += batch_loss
            if i%100 ==0:
                print('Total Steps:{} | New Step Loss {:.4f}'.format(i,batch_loss ))
        
        #calculate loss and time for this epoch, and format output
      
        step_loss = total_loss / steps_per_epoch
        current_steps = +steps_per_epoch
        print('Total Steps: {} | Most Recent loss {:.4f} | Average Loss {:.4f}'.format(current_steps,
                                                                      batch_loss, step_loss))
        total_loss = 0
        epoch_c += 1
        # After each epoch, store the data and model
        torch.save({'modelA_state_dict': encoder.state_dict(),
                    'modelB_state_dict': decoder.state_dict(),
                    'epoch': epoch_c
                    },
                     checkpoint_dir)
        sys.stdout.flush()
        




if __name__ == '__main__':
    model_dir = gConfig['model_data']
    data_dir = gConfig['running_data']
    input_tensor = NULL
    input_lang= NULL
    target_tensor= NULL
    target_lang =NULL
    lang = NULL
    
    print("Load existed data ..." , end = "   ")  
    data = torch.load(gConfig['running_data'])
    input_lang = data['lang']
    target_lang = input_lang
    input_tensor = data['input_tensor']
    target_tensor = data['target_tensor']
    print("Success!") 



    train(input_lang,target_lang,input_tensor,target_tensor)

    #input_lang.print_stucture()

    