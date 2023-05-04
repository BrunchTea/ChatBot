import jieba
import requests
import train_eval
from flask import Flask, render_template, request,jsonify
from zhon.hanzi import punctuation
import re
from QA_data import QA_test
from config import Config

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/_get_reply')
def get_reply(**kwargs):
#从请求中获取输入信息
    opt = Config()
    for k, v in kwargs.items(): #设置参数
        setattr(opt, k, v)
    searcher, sos, eos, unknown, word2ix, ix2word = train_eval.test(opt)
    req_msg = request.args.get('message', '__silence__', type=str)

#将语句使用结巴分词进行分词
    req_msg = re.sub(r"[%s]+" % punctuation, "", req_msg)
    req_msg = " ".join(jieba.cut(req_msg))
    req_msg = 'start ' + req_msg + ' end'
#调用decode_line对生成回答信息
    res_msg = train_eval.output_answer(req_msg,searcher,sos,eos,unknown,opt,word2ix,ix2word)
    if res_msg == '</UNK>': res_msg = '啥玩意儿'
    return jsonify(result=res_msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)