import os
from config import getConfig

import nltk
from nltk.stem.porter import PorterStemmer

from asyncio.windows_events import NULL
import torch
from config import getConfig
import execute


gConfig = {}
gConfig= getConfig.get_config()

def read_sen():
    
    conv_path = gConfig['resource_data']
    assert os.path.isfile(conv_path)
    file = open(conv_path,encoding='utf-8')
    Lines = file.readlines()

    all_sen = []

    
    for line in Lines:
        paragraph = []
        for sen in line.split("__eou__"):
            token = nltk.word_tokenize(sen)
            token = [''.join([i for i in s if not i.isdigit()]) for s in token]
            token = [s.lower() for s in token]
            if(len(token)!=0):
                paragraph.append(token)
        if(len(paragraph)!=0):
            all_sen.append(paragraph)

    file.close()
    seq_train = open(gConfig['seq_data'],'w',encoding='utf-8')

    for para in all_sen:
        sen_idx = 0
        while sen_idx < len(para) -1 :
            if sen_idx + 1 < len(para):
                for word in para[sen_idx]:
                    seq_train.write(word+' ')
                
                seq_train.write("=> ")
                sen_idx  = sen_idx + 1
                for word in para[sen_idx]:
                    seq_train.write(word+' ')
                    #print(word,end =" ")
            seq_train.write('\n')
    seq_train.close()
    print("finish create data file")


def create_dataset():
    data_dir = gConfig['running_data']
    input_tensor = NULL
    input_lang= NULL
    target_tensor= NULL
    target_lang =NULL


    
    lang, input_tensor,target_tensor= execute.read_data(gConfig['seq_data'], gConfig['max_train_data_size'])

    dict = gConfig['dict']
    file = open(dict,encoding='utf-8')
    Lines = file.readlines()

    print("Total words after loading seq_data: "+str(lang.n_words))
    for line in Lines:
        word = line.strip(" ").strip("\n")
        lang.addWord(word)
    print("Total words after loading dict: "+str(lang.n_words))
    torch.save({
                'lang': lang,
                'input_tensor': input_tensor,
                'target_tensor': target_tensor},
                data_dir)



if __name__ == '__main__':
    #read_sen();
    create_dataset();
    
