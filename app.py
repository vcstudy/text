from flask import Flask, redirect, url_for, render_template, request
import string
import random

'''
{%...%} for conditions
{{}} expressions to print
{#...#}comments 
'''


# ----------------------code starts-----------------------------------
def stuffing(y):
    return ''.join(random.choice(string.ascii_letters) for _ in range(y))


def convert_to_number(key):
    SUM = 0
    for i in key:
        SUM = SUM + ord(i)
    return SUM


def enc_lst(key, ln):
    random.seed(key)
    lis = []
    for i in range(ln):
        lis.append(random.randint(0, ln + key))
    return lis


def get_key(pasw, ln):
    first_key = convert_to_number(pasw)
    second_key = ln
    third_key = ord(pasw[0])
    final_key = first_key + second_key + third_key
    return final_key


def encrypt_the_data(pasw, message):
    lis = enc_lst(get_key(pasw, len(message)), len(message))
    enc = stuffing(len(message))
    for i, j in zip(message, lis):
        enc = enc + chr(((ord(i) + j) % 94) + 32)
        enc = enc + chr(ord("!") + (ord(i) + j) // 94)
    enc = enc + stuffing(len(message))
    return enc


def decrypt_the_data(pasw, encmsg):
    encmsg = encmsg[(len(encmsg) // 4):-(len(encmsg) // 4)]
    lis = enc_lst(get_key(pasw, len(encmsg) // 2), len(encmsg) // 2)
    enc, ext = encmsg[::2], encmsg[1::2]
    msg = ""
    for i, j, k in zip(enc, ext, lis):
        msg = msg + chr(((ord(j) - 33) * 94) + (ord(i) - 32) - k)
    return msg


def final_enc(message, pas):
    return encrypt_the_data(pas, message)


def final_dec(message, pas):
    return decrypt_the_data(pas, message)


# -----------------------------------------code ends---------------------------------------------

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/submit', methods = ['POST', 'GET'])
def submit():
    dict = {}
    if request.method == 'POST':
        emsg = str(request.form['emsg'])
        dmsg = str(request.form['dmsg'])
        psw = str(request.form['psw'])
        if len(emsg) > 2:
            enc = final_enc(emsg, psw)
            dict = {'msg': enc}
        else:
            dec = final_dec(dmsg, psw)
            dict = {'msg': dec}

    return render_template('result.html', dict = dict)


if __name__ == '__main__':
    app.run()
