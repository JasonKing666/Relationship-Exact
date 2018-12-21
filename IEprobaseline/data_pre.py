import os
import re

data_root = r"./ie_employee"
data_files =[r"LabeledData.1.txt",r"LabeledData.2.txt",r"LabeledData.3.txt",r"LabeledData.4.txt",r"LabeledData.5.txt"]

t = r"\{.+\\n.\}"


def process_datafiles(filepath,savepath,i):
    print(filepath)
    f = open(filepath).read().splitlines()
    if not os.path.exists(os.path.join(savepath,str(i))):
        os.mkdir(os.path.join(savepath,str(i)))
    sp = os.path.join(savepath,str(i))
    trainingdict = []
    words = []
    for j in f:
        if j =="":
            trainingdict.append(words)
            words=[]
        else:
            words.append(j)

    train_text = []
    train_text_file = open(os.path.join(sp,"train_text.txt"),'w')
    entity_text = []
    entity_text_file = open(os.path.join(sp,"entity_text.txt"),'w')
    label_text = []
    label_text_file = open(os.path.join(sp,'label_text_file.txt'),'w')
    special_words = {}
    spwords_file = open(os.path.join(sp,"special_words.txt"),'w')
    for j in trainingdict:
        label_dict = []
        for tmp in range(1,len(j)):
            ss = str.split(j[tmp],'|')
            ss = ss[0:3]
            try:
                special_words[ss[0]] = special_words[ss[0]]
            except:
                special_words[ss[0]] = 1
            try:
                special_words[ss[1]] = special_words[ss[1]]
            except:
                try:
                    special_words[ss[1]] =1
                except:
                    pass
            label_dict.append(ss)
        label_text.append(label_dict)
        tmp_entity = ""
        flag = False
        for tmp in j[0]:
            if tmp=='{':
                flag = True
                continue
            if flag and tmp!='}':
                if tmp == '/':
                    tmp_entity = tmp_entity+" "
                else:
                    tmp_entity = tmp_entity+tmp
            elif tmp == '}':
                flag = False
                if tmp_entity not in entity_text:
                    entity_text.append(tmp_entity)
                tmp_entity = ""

        text = j[0]
        texts = re.sub(r'{','',text)
        texts = re.sub(r'/nr}','',texts)
        texts = re.sub(r'/ns}','',texts)
        texts = re.sub(r'/nt}','',texts)
        texts = re.sub(r'/nz}','',texts)
        train_text.append(texts)
    for i in train_text:
        train_text_file.write(i)
        train_text_file.write('\n')
    for i in label_text:
        for  tmp in i:
            label_text_file.write(" ".join(tmp))
            label_text_file.write('\n')
        label_text_file.write('\n')
    for i in special_words:
        spwords_file.write(i)
        spwords_file.write(" "+str(100))
        spwords_file.write('\n')
    for i in entity_text:
        entity_text_file.write(i)
        entity_text_file.write('\n')
    return train_text,label_text,special_words,entity_text



#----------------------------------------------读取数据-----------------------------------------------------------
data0 = process_datafiles(os.path.join(data_root,data_files[0]),data_root,0)
data1 = process_datafiles(os.path.join(data_root,data_files[1]),data_root,1)
data2 = process_datafiles(os.path.join(data_root,data_files[2]),data_root,2)
data3 = process_datafiles(os.path.join(data_root,data_files[3]),data_root,3)
data4 = process_datafiles(os.path.join(data_root,data_files[4]),data_root,4)



