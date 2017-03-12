#-*- coding: utf-8 -*-

class A(object):

    def __init__(self):

        self.a = 0


    def run(self):
        self.step1()
        self.step2()


    def step1(self):
        self.sb1()


    def step2(self):
        self.sb2()




class B1(A):

    def __init__(self):

        super(B1, self).__init__()
        self.b1 = 1


    def step1(self):
        super(B1, self).step1()


    def sb1(self):
        self.b1 += 1




class B2(A):

    def __init__(self):

        super(B2, self).__init__()
        self.b2 = 2


    def step2(self):
        super(B2, self).step2()


    def sb2(self):
        self.b2 += 1




class C(B1, B2):

    def __init__(self):

        super(C, self).__init__()
        self.c = 3


    def step1(self):
        super(C, self).step1()


    def step2(self):
        super(C, self).step2()
