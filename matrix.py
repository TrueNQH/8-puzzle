from random import randint
from copy import deepcopy
import numpy as np

# Định nghĩa class Matrix
class Matrix():

    # Hàm khởi tạo, tạo ma trận với số hàng và số cột cho trước
    def __init__(self, lins, cols):
        self.matrix = np.zeros((lins, cols), dtype=int)
        self.dist = 0
        self.previous = None
        self.move = ""
        self.cost = 0

    # Hàm kiểm tra tính hợp lệ của các số trong ma trận
    def validNumbers(self, numbers):
        valid = False
        if len(numbers) == 9:
            ref = list(range(9))
            valid = True
            for i in numbers:
                if int(i) not in ref:
                    valid = False
                else: 
                    ref.remove(int(i))
        return valid

    # Hàm xây dựng ma trận từ một chuỗi
    def buildMatrix(self, str):
        numbers = str.split(",")
        if self.validNumbers(numbers):
            i = 0
            for k in range(3):
                for j in range(3):
                    self.matrix[k][j] = int(numbers[i])
                    i += 1

    # Hàm tìm vị trí của một số trong ma trận
    def searchBlock(self, value):
        for k in range(3):
            for j in range(3):
                if self.matrix[k][j] == value:
                    return (k, j)

    # Các hàm di chuyển ô trống lên, xuống, sang trái, sang phải
    def moveup(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]-1][zero[1]]
        self.matrix[zero[0]-1][zero[1]] = 0

    def movedown(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]+1][zero[1]]
        self.matrix[zero[0]+1][zero[1]] = 0

    def moveright(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]][zero[1]+1]
        self.matrix[zero[0]][zero[1]+1] = 0

    def moveleft(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]][zero[1]-1]
        self.matrix[zero[0]][zero[1]-1] = 0

    # Hàm trả về các nút có thể đi từ trạng thái hiện tại
    def getPossibleNodes(self, moves):
        zero = self.searchBlock(0)
        possibleNodes = []
        if zero[0] > 0:
            self.moveup(zero)
            moves.append("up")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.movedown(zero)
            zero = self.searchBlock(0)
        if zero[0] < 2:
            self.movedown(zero)
            moves.append("down")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveup(zero)
            zero = self.searchBlock(0)
        if zero[1] > 0:
            self.moveleft(zero)
            moves.append("left")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveright(zero)
            zero = self.searchBlock(0)
        if zero[1] < 2:
            self.moveright(zero)
            moves.append("right")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveleft(zero)
            zero = self.searchBlock(0)
        return possibleNodes

    # Hàm trả về tọa độ (x, y) của một giá trị trong ma trận
    def getXY(self, value, matFinal=[[1, 2, 3], [4, 5, 6], [7, 8, 0]]):
        for x in range(3):
            for y in range(3):
                if value == matFinal[x][y]:
                    return (x, y)

    # Hàm tính khoảng cách Manhattan giữa ma trận hiện tại và trạng thái cuối cùng
    def manhattanDist(self):
        res = 0
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != 0:
                    fi, fj = self.getXY(self.matrix[i][j])
                    res += abs(fi - i) + abs(fj - j)
        self.dist = res
        return res

    # Hàm tính chi phí theo khoảng cách Manhattan đối với trạng thái cuối cùng
    def manhattanDistCost(self, Final):
        res = 0
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != 0:
                    fi, fj = self.getXY(self.matrix[i][j], Final.matrix)
                    res += abs(fi - i) + abs(fj - j)
        return res

    # Hàm trả về ma trận
    def getMatrix(self):
        return self.matrix

    # Hàm kiểm tra hai ma trận có giống nhau không
    def isEqual(self, matrix):
        return (self.matrix == matrix).all()

    # Hàm thiết lập ma trận trước đó
    def setPrevious(self, p):
        self.previous = p

    # Các hàm so sánh giúp sắp xếp các ma trận trong các thuật toán tìm kiếm
    def __cmp__(self, other):
        return self.dist == other.dist

    def __lt__(self, other):
        return self.dist < other.dist
