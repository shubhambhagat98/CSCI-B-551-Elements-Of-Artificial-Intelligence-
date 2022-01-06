#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors:  Henish Shah
#           Shubham Bhagat
#           Ameya Dalvi
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"\' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
#print("\n".join([ r for r in train_letters['h'] ]))

# print('Train len:',len(train_letters['h']))
# print(train_letters)
# print(test_letters)
# Same with test letters. Here's what the third letter of the test data
#  looks like:
#print("\n".join([ r for r in test_letters[1] ]))
# print('Test len:',len(test_letters[1]))

op_dict=dict()

for i in range(len(test_letters)):
    temp_test_list=test_letters[i]

    if i in op_dict.keys():
        pass
    else:
        op_dict[i]=dict()
    
    for j in train_letters.keys():

        if j in op_dict[i].keys():
            pass
        else:
            op_dict[i][j]=dict()
    
        temp_train_list = train_letters[j]
        
        for row in range(len(temp_test_list)):
            for pixel in range(len(temp_test_list[row])):
                if temp_test_list[row][pixel]==temp_train_list[row][pixel]:
                    
                    if temp_train_list[row][pixel]=='*':

                        if '*' in op_dict[i][j].keys():
                            op_dict[i][j]['*']+=1
                        else:
                            op_dict[i][j]['*']=1
                    
                    elif temp_train_list[row][pixel]==' ':

                        if ' ' in op_dict[i][j].keys():
                            op_dict[i][j][' ']+=1
                        else:
                            op_dict[i][j][' ']=1   
                else:
                    pass
        
        # summ=sum(op_dict[i][j].values())
        # op_dict[i][j]=summ/400



op_dict_simplify=op_dict.copy()

for i in op_dict_simplify.keys():
    for j in op_dict_simplify[i].keys():
        summ=sum(op_dict_simplify[i][j].values())
        op_dict_simplify[i][j]=summ/400


symbols='(),.-!?\"\' '
num = '1234567890'
symbols_dict=dict()
num_dict=dict()
op_sent=['']*len(test_letters)
max_val=0



for i in op_dict_simplify.keys():
    max_val=0
    max_key=''
    max_symbol_key=''
    max_symbol_val=0
    max_num_key=''
    max_num_val=0
    
    if i not in symbols_dict.keys():
        symbols_dict[i]=dict()
    if i not in num_dict.keys():
        num_dict[i]=dict()
        
    
    
    # space_val=op_dict_simplify[i][' ']
    # del op_dict_simplify[i][' ']
    
    # if space_val-max(op_dict_simplify[i].values())>=0.02:
    #     op_sent[i]=' '
    #     continue

    for j in op_dict_simplify[i].copy():
        if j in symbols:
            symbols_dict[i][j]=op_dict_simplify[i][j]
            del op_dict_simplify[i][j]
    
    for j in op_dict_simplify[i].copy():
        if j in num:
            num_dict[i][j]=op_dict_simplify[i][j]
            del op_dict_simplify[i][j]
    
    # print(symbols_dict)
    # print(num_dict)
    # print(op_dict_simplify)
    
    for j in op_dict_simplify[i].keys():
        if op_dict_simplify[i][j]>max_val:
            max_key=j
            max_val=op_dict_simplify[i][j]
    
    for j in symbols_dict[i].keys():
        if symbols_dict[i][j]>max_symbol_val:
            max_symbol_key=j
            max_symbol_val=symbols_dict[i][j]

    for j in num_dict[i].keys():
        if num_dict[i][j]>max_num_val:
            max_num_key=j
            max_num_val=num_dict[i][j]
    

    if max_num_val-max_val>=0.03:
        op_sent[i]=max_symbol_key
    else:
        op_sent[i]=max_key
    
    if max_symbol_val-max_val>=0.07:
        op_sent[i]=max_symbol_key
    else:
        op_sent[i]=max_key

op_sent=''.join(op_sent)


# print("\n".join([ r for r in train_letters[' '] ]))
# print(train_letters[' '])
# The final two lines of your output should look something like this:
print("Simple: ", op_sent)
print("   HMM: " + "Sample simple result") 


