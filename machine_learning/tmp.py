#树回归模型与标准模型的比较
from numpy import *
from CART import *

def main():
    trainMat = mat(loadDataSet('bikeSpeedVsIq_train.txt'))
    testMat = mat(loadDataSet('bikeSpeedVsIq_test.txt'))
    #回归树
    myTree = createTree(trainMat,ops = (1,20))
    yHat = createForeCast(myTree,testMat[:,0])
    print(corrcoef(yHat,testMat[:,1],rowvar=0)[0,1])
    #模型树
    myTree = createTree(trainMat,modelLeaf,modelErr,(1,20))
    yHat = createForeCast(myTree,testMat[:,0],modelTreeEval)
    print(corrcoef(yHat,testMat[:,1],rowvar=0)[0,1])
    #线性回归
    ws,X,Y = linearSolve(trainMat)
    for i in range(shape(testMat)[0]):
        yHat[i] = testMat[i,0] * ws[1,0] + ws[0,0]
    print(corrcoef(yHat,testMat[:,1],rowvar=0)[0,1])
if __name__ == '__main__':
    main()