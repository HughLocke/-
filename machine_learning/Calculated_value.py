import numpy as np
from regression import loadDataSet as ld1
from Get_Account import Get_Attribute
def Reg():
    w = []
    f = open('../data/model.txt')
    text = f.readlines()
    Line = text[0].strip().split('\t')
    for i in Line: w.append(float(i))
    c = float(text[1])
    wmat = np.mat(w)
    dataset, ans = ld1('../data/Account_tmp.txt')
    Hatans = dataset * wmat.T + c
    for i in range(0, 300):
        if ans[i] * 20 < Hatans[i,0]:
            print(dataset[i])
    n, m = np.shape(wmat)
    AttributeIndex = Get_Attribute()
    IndexAttribute = {}
    for key in AttributeIndex:
        IndexAttribute[int(AttributeIndex[key])] = key
    sorted_nums = sorted(enumerate(w), key=lambda x: x[1])
    idx = [i[0] for i in sorted_nums]
    nums = [i[1] for i in sorted_nums]
    # print(idx)
    #for i in idx:
        #print(IndexAttribute[i],'   ',w[i])
        #print(IndexAttribute[i])


from TreeReg import loadDataSet as ld2
from TreeReg import treeForeCast
from TreeReg import isTree
import json

IndexAttribute = {}
def REPLACE(Tree):
    Tree['spInd'] = IndexAttribute[Tree['spInd']]
    if isTree(Tree['left']):
        REPLACE(Tree['left'])
    if isTree(Tree['right']):
        REPLACE(Tree['right'])
def tReg():
    f = open("../data/treemodel.txt")
    dataset = ld2('../data/Account_tmp.txt')
    m = len(dataset)
    text = f.readlines()[0]
    text = text.replace("'",'"')
    Tree = json.loads(text)
    AttributeIndex = Get_Attribute()
    for key in AttributeIndex:
        IndexAttribute[int(AttributeIndex[key])] = key
    REPLACE(Tree)
    print(Tree)
if __name__ == '__main__':
    Reg()
    #tReg()
