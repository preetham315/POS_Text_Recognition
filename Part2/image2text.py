from PIL import Image, ImageDraw, ImageFont
import sys
import copy

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
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)


numbers = '0123456789'
numbers_dict = {}
symbols='(),.-!?\"\' '
symbols_dict = {}
final_result=['']*len(test_letters)
max_value=0
final_chars = {}
simple_final = {}

def find_symbols(i):
    if i not in symbols_dict.keys():
        symbols_dict[i]=dict()
        for j in simple_final[i].copy():
            if j in symbols:
                symbols_dict[i][j]=simple_final[i][j]
                del simple_final[i][j]
    
def find_numbers(i):
        if i not in numbers_dict.keys():
            numbers_dict[i]=dict()
        for j in simple_final[i].copy():
            if j in numbers:
                numbers_dict[i][j]=simple_final[i][j]
                del simple_final[i][j]

def find_chars():
    for i in simple_final.keys():
        max_val=0
        max_key=''
        max_symbol_key=''
        max_symbol_val=0
        max_number_key=''
        max_number_val=0
        
        find_symbols(i)
        find_numbers(i)      
        
        for j in simple_final[i].keys():
            if simple_final[i][j]>max_val:
                max_key=j
                max_val=simple_final[i][j]
        
        for j in numbers_dict[i].keys():
            if max_number_val<numbers_dict[i][j]:
                max_number_key=j
                max_number_val=numbers_dict[i][j]
        
        for j in symbols_dict[i].keys():
            if max_symbol_val<symbols_dict[i][j]:
                max_symbol_key=j
                max_symbol_val=symbols_dict[i][j]

        
        if max_symbol_val-max_val>=0.07:
            final_result[i]=max_symbol_key
        else:
            final_result[i]=max_key

        if max_number_val-max_val>=0.02:
            final_result[i]=max_symbol_key
        else:
            final_result[i]=max_key
        

def find_pattern(test_row, train_row,final_chars,i,j):
    for row in range(len(test_row)):
            for pixel in range(len(test_row[row])):
                if test_row[row][pixel]==train_row[row][pixel]:
                    if train_row[row][pixel]==' ':
                        if ' ' in final_chars[i][j].keys():
                            final_chars[i][j][' ']+=1
                        else:
                            final_chars[i][j][' ']=1 
                             
                    elif train_row[row][pixel]=='*':

                        if '*' in final_chars[i][j].keys():
                            final_chars[i][j]['*']+=1
                        else:
                            final_chars[i][j]['*']=1
                            
for itr in range(0,len(test_letters),1):
    if itr not in final_chars:
        final_chars[itr] = {}
    for i in train_letters:
        if i not in final_chars:
            final_chars[itr][i] ={}
        find_pattern(test_letters[itr],train_letters[i],final_chars, itr,i)
simple_final = copy.deepcopy(final_chars)
        
for i in simple_final.keys():
    for j in simple_final[i].keys():
        final_sum=sum(simple_final[i][j].values())
        simple_final[i][j]=final_sum/400

find_chars()

final_result=''.join(final_result)

# The final two lines of your output should look something like this:
print("Simple: " + final_result)
print("   HMM: " + "Sample simple result") 


