#csvファイルを読み込んで、ラウンド数とラウンドごとのBB、SB、休憩、各時間をタプルとして出力する

import csv

class StructureBB():
    def __init__(self):
        with open ("Blind.csv", 'rt',encoding="utf-8_sig") as self.f:
            self.bf = csv.reader(self.f)
            self.list_Blind = [row for row in self.bf]  # LEVEL,ANTE,BB,SB,時間（分）

    def ALLround(self):
        return len(self.list_Blind)-1

    def output(self,LEVEL):
        if not self.list_Blind[LEVEL][2]=="rest":
            return ("play",self.list_Blind[LEVEL][1],self.list_Blind[LEVEL][2],self.list_Blind[LEVEL][3],60*int(self.list_Blind[LEVEL][4]))
        else:
            return ("rest",self.list_Blind[LEVEL][1],"rest",self.list_Blind[LEVEL][3],60*int(self.list_Blind[LEVEL][4]))

#instance.output(0) = "play" or "rest"
#(1) = ANTE
#(2) = BB
#(3) = SB
#(4) = min

# a = StructureBB()
# b = a.output(1)
# print(b[2])
# print("{0} / {1}".format(a.output(2),a.output(3)))