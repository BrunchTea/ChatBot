import subprocess

import torch

import execute
import seq2seqModel
from config import getConfig

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
gConfig = {}
gConfig = getConfig.get_config()

if device.type == 'cuda':
    data = torch.load(gConfig['running_data'])
else:
    data = torch.load(gConfig['running_data'], map_location=torch.device('cpu'))

input_lang = data['lang']
target_lang = input_lang
hidden_size = 256
print("Loading data Successfully!!!")

max_length_tar = execute.MAX_LENGTH
encoder = seq2seqModel.Encoder(input_lang.n_words, hidden_size).to(device)
decoder = seq2seqModel.AttentionDencoder(hidden_size, target_lang.n_words, dropout_p=0.1).to(device)
checkpoint_dir = gConfig['model_data']
if device == "cuda":
    checkpoint = torch.load(checkpoint_dir)
else:
    checkpoint = torch.load(checkpoint_dir, map_location=torch.device('cpu'))
encoder.load_state_dict(checkpoint['modelA_state_dict'])
decoder.load_state_dict(checkpoint['modelB_state_dict'])

print("Loading model Successfully!!!")


def predict(sentence):
    sentence = execute.modify_input(sentence)
    # print(sentence)
    ratio = execute.undestanding_ratio(input_lang, sentence)
    # print(ratio)
    if (ratio > 0.5):
        return "Sorry, I don't get it"

    # print(sentence)
    # sentence = execute.preprocess_sentence(sentence)
    input_tensor = execute.tensorFromSentence(input_lang, sentence)

    # print(input_tensor.size())
    input_length = input_tensor.size()[0]
    result = ''
    max_length = execute.MAX_LENGTH
    encoder_hidden = encoder.initHidden()
    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)
    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                 encoder_hidden)
        encoder_outputs[ei] += encoder_output[0, 0]

    dec_input = torch.tensor([[execute.SOS_token]], device=device)  # SOS
    dec_hidden = encoder_hidden
    # decoder_attentions = torch.zeros(max_length, max_length)
    for t in range(max_length_tar):
        predictions, dec_hidden, decoder_attentions = decoder(dec_input, dec_hidden, encoder_outputs)
        predicted_id, topi = predictions.data.topk(1)

        if topi.item() == execute.EOS_token:
            result += '<EOS>'
            break
        else:
            result += target_lang.index2word[topi.item()] + ' '
        dec_input = topi.squeeze().detach()
    return result


subprocess.run(["javac", "./ChatApp/window.java", "./ChatApp/ChatTag.java"])
proc = subprocess.Popen(["java", "ChatApp/window"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
count = 0
while (True):
    output = proc.stdout.readline()
    if len(output) > 0:
        out = output.rstrip().decode("utf-8")
        # print("Q:  " + out)
        ans = predict(out)
        proc.stdin.write("{}\n".format(ans).encode("utf-8"))
        proc.stdin.flush()
        proc.stdout.flush()

    poll = proc.poll()
    if poll is not None:
        print(poll)
        exit()

'''
input_sen = []

with open("input",encoding='utf-8') as f:
    for line in f:
        line = line.strip('\n').strip(' ')
        input_sen.append(line)

for sen in input_sen:
    print("Q:  "+sen)
    print("A:  " + predict(sen))
    print("----------------")

'''
