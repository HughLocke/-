from numpy import *
import random as rd
import pandas as pd
def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split(' ')) - 1
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split(' ')
        for i in range(numFeat - 1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

#错误率
def rssError(ans,Hatans):
    return (power((ans - Hatans),2)).sum()

def checkvar(var):
    n,m = shape(var)
    for i in range(n):
        for j in range(m):
            if(var[i,j] == 0):
                var[i,j] = 0.000000000000000000000000000001
#岭回归
#当特征比样例多的时候,将矩阵加上一个对角线lam其他全0的矩阵
def ridgeRegres(xMat,yMat,lam = 0.00002): #计算回归函数
    xTx = xMat.T * xMat
    denom = xTx + eye(shape(xMat)[1]) * lam
    if linalg.det(denom) == 0.0:
        print("This matrix is singular,cannot do inverse")
        return
    ws = denom.I * (xMat.T * yMat)
    return ws

def ridgeTest(xArr,yArr,numTestPts = 50): #在一组lam上测试结果
    #print(xArr);print(yArr)
    xMat = mat(xArr)
    yMat = mat(yArr).T
    #print(xMat);print(yMat)
    # 标准化:所有特征减去各自的均值并除以方差,使得所有特征有相同的重要性
    yMean = mean(yMat,0)
    yMat = yMat - yMean
    xMeans = mean(xMat,0)
    xVar = var(xMat,0) #方差
    checkvar(xVar)
    xMat = (xMat - xMeans) / xVar
    wMat = zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat

def crossValidation(dataset,ans,numVal = 30): #交叉测试岭回归
    n = len(ans)
    #print("n = ",n)
    indexList = [i for i in range(n)]
    errorMat = zeros((numVal,30))
    for i in range(numVal):
        traindata = []; trainans = []
        testdata = []; testans = []
        rd.shuffle(indexList) #打乱下标
        for j in range(n):
            if j < n * 0.9: #取出前90%作为训练集
                traindata.append(dataset[indexList[j]])
                trainans.append(ans[indexList[j]])
            else:      #剩下的10%数据作为训练集
                testdata.append(dataset[indexList[j]])
                testans.append(ans[indexList[j]])
       # print(traindata)
        wMat = ridgeTest(traindata,trainans) #一组岭回归返回的结果
        #print(wMat)
        for k in range(30): #对每个lam返回的结果进行误差分析
            #用训练集的参数将测试集标准化
            matTestdata = mat(testdata); matTraindata = mat(traindata)
            meanTrain = mean(matTraindata,0)
            varTrain = var(matTraindata,0)
            checkvar(varTrain)
            matTestdata = (matTestdata - meanTrain) / varTrain
            #利用标准化后的测试集乘以模型,然后加上训练集答案的平均值以返回预测答案
            yEst = matTestdata * mat(wMat[k,:]).T + mean(trainans)
            errorMat[i,k] = rssError(yEst.T.A,array(testans))
    #所有lam下的10组测试平均误差和
    meanErrors = mean(errorMat,0)
    minMean = float(min(meanErrors)) #找出最小误差
    bestWeights = wMat[nonzero(meanErrors == minMean)] #找出最小误差的lam对应的模型
    dataMat = mat(dataset)
    ansMat = mat(ans).T
    meanX = mean(dataMat,0)
    varX = var(dataMat,0)
    checkvar(varX)
    unReg = bestWeights/varX
    c = -1*sum(multiply(meanX,unReg)) + mean(ansMat) #计算常数项
    #print("the best model from Ridge Regression is :\n",unReg)
    #print("with constant term: ",c)
    return unReg,c

if __name__ == '__main__':
    dataset,ans = loadDataSet('../data/Account_info.txt')
    #datamat = mat(dataset)
    f = open('../data/modeltest.txt', 'w')
    w,c = crossValidation(dataset,ans)
    n,m = shape(w)
    for i in range(n):
        for j in range(m):
            f.write(str(w[i,j]) + '\t')
    f.write('\n' + str(c))
    f.close()
    Hatans = dataset * w.T + c
    print(format(rssError(ans,Hatans),'.3e'))

