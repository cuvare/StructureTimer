#秒の受け渡し用

class Time_converter():
    def __init__(self, h,m=None,s=None):
        if (m==None)&(s==None):
            self.total_s = h

        elif(s==None):
            self.total_s = 60*h + m

        else:
            self.total_s = s+60*m+3600*h

        self.h = self.total_s // 3600
        self.m = (self.total_s - (self.h * 3600)) // 60
        self.s = self.total_s - (self.h * 3600) - (self.m * 60)

        self.HMS = "{:0=02}:{:0=02}:{:0=02}".format(self.h, self.m, self.s)
        self.MS = "{:0=02}:{:0=02}".format(self.m, self.s)

    def __add__(self, other):
        return Time_converter(self.total_s + other.total_s)

    def __sub__(self,other):
        return Time_converter(self.total_s - other.total_s)

# a = Time_converter(1,10,4)
# print(a.total_s)
# print(Time_converter(5000).MS)