from data_pre import data0,data1,data2,data3,data4
import random

#---------------------------------------------读取数据-----------------------------------------------------------
train_text0,label_text0,special_words0,entity_text0 = data0
train_text1,label_text1,special_words1,entity_text1 = data1
train_text2,label_text2,special_words2,entity_text2 = data2
train_text3,label_text3,special_words3,entity_text3 = data3
train_text4,label_text4,special_words4,entity_text4 = data4
train_text = train_text0+train_text1+train_text2+train_text3+train_text4
label_text = label_text0+label_text1+label_text2+label_text3+label_text4
#special_words = special_words0+special_words1+special_words2+special_words3+special_words4
entity_text = entity_text0+entity_text1+entity_text2+entity_text3+entity_text4

#-------------------------------------------训练数据预处理--------------------------------------------------------

#----------------------------------------jieba用userdict给每句话分词-----------------------------------------------
import jieba
jieba.load_userdict('./ie_employee/special_words.txt')
for i in range(len(train_text)):
    train_text[i] = list(jieba.cut(train_text[i],cut_all=False))

#------------------------------------------分完词用postagger------------------------------------------------------
from pyltp import Postagger
post_path = "D:/ltp_models/ltp_data_v3.4.0/pos.model"
postagger = Postagger()
postagger.load_with_lexicon(post_path,'./ie_employee/entity_text.txt')


#-------------------------------------生成对应的训练集/测试集,或测试准确率等---------------------------------------------
GRU_model_path = ""

def generate():
    data = zip(train_text,label_text)
    assert len(train_text)==len(label_text)
    training_corpus = []
    for i in data:
        text,label = i
        label_dict = []
        post = list(postagger.postag(text))
        for tmp in label:
            """对每个tmp生成一条训练语料"""
            try:
                ssleft = text.index(tmp[0])
                ssright = text.index(tmp[1])
                #print(ssleft,ssright,tmp[0],tmp[1])
                if ssleft>ssright:
                    ssleft,ssright = ssright,ssleft
                """然后生成label 对"""
                label_dict.append([ssleft,ssright,tmp[2]])
            except:
                pass
        #print(label_dict)
        for left in range(len(text)):
            for right in range(left+1, len(text)):
                if (post[left],post[right]) == ('ni','nh') or  (post[left],post[right]) == ('nh','ni'):
                    lf = left-5 if left-5>0 else 0
                    rf = right+5 if right+5<len(text) else len(text)
                    select_dict = []

                    #新的select的方式，周围十个词，然后中间任取十个词，搞数据增强？？？我觉得任取更正确一点。然后对于关系N就任取
                    if right-left<15:
                        for tmp in range(lf,rf):
                            select_dict.append(text[tmp])

                    else:
                        for tmp in range(lf,left+5):
                            select_dict.append(text[tmp])

                        for tmp in range(left+5,right-5):
                            if post[tmp] in ['nr','nh','ni','v','wp']:
                                if random.random() < float((right-left-10))/(right-left):
                                    select_dict.append(text[tmp])

                        for tmp in range(right-5,rf):
                            select_dict.append(text[tmp])

                    """
                    for j in range(lf,rf):
                        select_dict.append(text[j])
                        if (post[j] == 'ni' or post [j] == 'nh') and j!=left and j!=right:
                            continue
                        else:
                            select_dict.append(text[j])
                    """
                    #print(text[left],text[right])
                    relation = 'N'
                    if ([left,right,'I']) in label_dict:
                        relation = 'I'
                        #print(left,right,'I')
                    elif ([left,right,'B']) in label_dict:
                        relation = 'I'
                    elif ([left,right,'E']) in label_dict:
                        relation = 'N'
                    elif ([left,right,'P']) in label_dict:
                        relation = 'N'
                    else:
                        pass
                        #print(left,right,'N')
                    training_corpus.append(text[left]+" "+text[right]+" "+relation+" "+"".join(select_dict))
    random.shuffle(training_corpus)
    for i in training_corpus:
        print(i)
    return training_corpus

def test():
    pass



#-----------------------------------------------------------------------------------------------------------------
is_generate = True
if is_generate:
    trainfile = open("./train.txt",'w')
    testfile = open("./test.txt",'w')
    data = generate()
    for i in data:
        if random.random()<0.2:
            testfile.write(i+"\n")
        else:
            a = i.split()
            if a[2] == 'N':
                #按0.1的概率抽取算了
                if random.random()<0.2:
                    trainfile.write(i+"\n")
            else:
                trainfile.write(i+"\n")
else:
    test()

#----------------------------------------------------------------------------------------------------------------