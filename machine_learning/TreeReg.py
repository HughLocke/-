from numpy import *

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for Line in fr.readlines():
        curLine = Line.strip().split(' ')
        fltLine = []
        for i in curLine:
            fltLine.append(float(i))
        dataMat.append(fltLine)
    return dataMat

#二元切分数据集
#将数据集上所有在feature特征的数据以value为界限划分为mat0和mat1
def binSplitDataSet(dataSet,feature,value):
    mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0],:]
    mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:]
    return mat0,mat1

def regLeaf(dataSet):
    return mean(dataSet[:,-1])

def regErr(dataSet):
    return var(dataSet[:,-1]) * shape(dataSet)[0]
#线性回归
def linearSolve(dataSet):
    n,m = shape(dataSet)
    X = mat(ones((n,m))); Y = mat(ones((n,1)))
    X[:,1:m] = dataSet[:,0:m-1]; Y = dataSet[:,-1]
    xTx = X.T * X
    if linalg.det(xTx) == 0.0:
        print(dataSet)
        raise NameError("This matrix is singular,connot do inverse,try increasing the second value of ops")
    ws = xTx.I * (X.T * Y)
    return ws,X,Y
#负责生成叶子节点的模型
def modelLeaf(dataSet):
    ws,X,Y = linearSolve(dataSet)
    return ws
#负责计算叶子节点模型的误差
def modelErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y - yHat,2))

#选出划分特征的下标和划分的值
def chooseBestSplit(dataSet,leafType = regLeaf,errType=regErr,ops=(1,4)):
    tolS = ops[0]; tolN = ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1: #这个特征下全是相同的值
        return None,leafType(dataSet)
    m,n = shape(dataSet)
    S = errType(dataSet)
    bestS = inf;bestIndex = 0;bestValue = 0
    for featIndex in range(n - 1): #遍历所有属性
        for splitVal in set(dataSet[:,featIndex].T.tolist()[0]): #遍历这个属性下所有可能的值
            mat0,mat1 = binSplitDataSet(dataSet,featIndex,splitVal) #尝试划分的两个矩阵
            if(shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue #划分之后其中一个数据集过小,则不考虑
            newS = errType(mat0) + errType(mat1) #重新计算误差
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    if (S - bestS) < tolS: #降低误差的范围小到一定程度,就不管了
        return None,leafType(dataSet)
    mat0,mat1 = binSplitDataSet(dataSet,bestIndex,bestValue)
    if(shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): #无法划分出满足另一个数据集条件的情况,也不管了
        return None,leafType(dataSet)
    return bestIndex,bestValue
#数据集.建立叶节点的函数,误差计算函数,包含树构建所需其他参数的元祖
def createTree(dataSet,leafType = regLeaf,errType = regErr,ops = (1,4)):
    feat,val = chooseBestSplit(dataSet,leafType,errType,ops)
    if feat == None: return val #不需要划分,直接返回这个叶子节点的答案
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet,rSet = binSplitDataSet(dataSet,feat,val)
    retTree['left'] = createTree(lSet,leafType,errType,ops)
    retTree['right'] = createTree(rSet,leafType,errType,ops)
    return retTree
#后剪枝
#通过判断儿子是不是字典来判断是树还是值
def isTree(obj):
    return (type(obj).__name__ == 'dict')
#合并两树
def getMean(tree):
    if isTree(tree['right']): tree['right'] = getMean(tree['right'])
    if isTree(tree['left']): tree['left'] = getMean(tree['left'])
    return (tree['left'] + tree['right']) / 2.0
#使用测试集testData给树剪枝
def prune(tree,testData):
    if shape(testData)[0] == 0.0: return getMean(tree) #如果测试集已经不包含数据 则直接将整颗子树合并
    # 如果左右节点有一棵是树,则将测试集按照节点信息划分,递归进入子树尝试剪枝
    if (isTree(tree['right']) or isTree(tree['left'])):
        lSet,rSet = binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if isTree(tree['left']): tree['left'] = prune(tree['left'],lSet)
    if isTree(tree['right']): tree['right'] = prune(tree['right'],rSet)
    #子树剪枝完成后,如果两孩子都是叶子节点,则尝试给这个节点剪枝,否则直接返回
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet,rSet = binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        errorNoMerge = sum(power(lSet[:,-1] - tree['left'],2)) + \
                       sum(power(rSet[:,-1] - tree['right'],2)) #测试集在剪枝状态下的表现
        treeMean = (tree['left'] + tree['right']) / 2
        errorMerge = sum(power(testData[:,-1] - treeMean,2)) #测试集在不剪枝情况下的误差表现
        if errorMerge < errorNoMerge: #如果不切分误差反而更低,则剪枝
            print("merging")
            return treeMean
        else: return tree
    else:return tree
#回归树返回i叶子节点
def regTreeEval(model,inDat):
    return float(model)
#模型树返回叶子节点
def modelTreeEval(model,inDat):
    n = shape(inDat)[1]
    X = mat(ones((1,n + 1)))
    X[:,1:n + 1]=inDat
    return float(X*model)

#将树和测试数据带入,得出结果
def treeForeCast(tree,inData,modelEval=regTreeEval):
    if not isTree(tree): return modelEval(tree,inData)
    if inData[0,tree['spInd']] > tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inData,modelEval)
        else:
            return modelEval(tree['left'],inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'],inData,modelEval)
        else:
            return modelEval(tree['right'],inData)

#将数据集代入树,得出预测集
def createForeCast(tree,testData,modelEval = regTreeEval):
    m = len(testData)
    yHat = mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0] = treeForeCast(tree,mat(testData[i]),modelEval)
    return yHat

def main():
    dataset = loadDataSet('../data/Account_info.txt')
    dataMat = mat(dataset)
    testSet = loadDataSet('../data/Account_tmp.txt')
    testMat = mat(testSet)
    Tree = createTree(dataMat,ops = (2,10))
    yHat = createForeCast(Tree,testSet)

    f = open('../data/treemodel.txt', 'w')
    f.write(str(Tree))
    m = len(testSet)
    for i in range(m):
        print(yHat[i,0],' ',mat(testSet[i])[0,-1])
if __name__ == '__main__':
    main()