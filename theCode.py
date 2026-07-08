class Polynomial():
    def __init__(self, nomial1, operator, nomial2, atpS=False):
        self.nomial1 = nomial1
        self.operator = operator
        self.nomial2 = nomial2
        self.__atpS = atpS #attempt simplify

        #print("tried as", self.__repr__(), self.__atpS)

        if self.operator in ["+","-"] and (self.nomial1==0 or self.nomial2==0):
            self.__init__(self.nomial1==0 and self.nomial2 or self.nomial1,None,None)
        elif self.operator in ["*","/"] and (self.nomial1==1 or self.nomial2==1):
            self.__init__(self.nomial1==1 and self.nomial2 or self.nomial1,None,None)
        elif self.operator in ["**","^"] and (self.nomial2==1):
            self.__init__(self.nomial1,None,None)

        if self.operator == None and isinstance(self.nomial1, Polynomial):
            #Removing nesting, by default nomial1 is prioritized
            self.__init__(self.nomial1.nomial1, self.nomial1.operator, self.nomial1.nomial2, True)
        #Solving inner problems
        elif self.operator == "+" and not self.__atpS:
            self.__init__(self.get_nomials_sum(), None, None, True)
        elif self.operator == "-" and not self.__atpS:
            self.__init__(self.get_nomials_difference(), None, None, True)
        elif self.operator == "*" and not self.__atpS:
            self.__init__(self.get_nomials_product(), None, None, True)
        elif self.operator in ["^","**"] and not self.__atpS:
            self.__init__(self.get_nomials_powered(), None, None, True)
        else:
            self.__atpS = True

    def result(self):
        if self.operator == None:
            return self.nomial1

    def __are_nomials_numbers(self):
        return isinstance(self.nomial1,(int,float,Polynomial)) and isinstance(self.nomial2,(int,float,Polynomial))

    def __str__(self):
        #Hides unescessary stuff
        toShow = str(self.nomial1)
        if self.operator != None:
            toShow += str(self.operator)
            toShow += str(self.nomial2)
        return "(" + toShow + ")"

    def __repr__(self):
        #Doesnt hide anything
        return "(" + self.nomial1.__repr__() + str(self.operator) + self.nomial2.__repr__() + ")"

    def get_nomials_sum(self):
        if self.__are_nomials_numbers():
            return self.nomial1 + self.nomial2
        else: return Polynomial(self.nomial1,"+",self.nomial2, True)

    def get_nomials_difference(self):
        if self.__are_nomials_numbers():
            return self.nomial1 - self.nomial2
        else: return Polynomial(self.nomial1,"-",self.nomial2, True)

    def get_nomials_product(self):
        if self.__are_nomials_numbers():
            return self.nomial1 * self.nomial2
        else: return Polynomial(self.nomial1,"*",self.nomial2, True)

    def get_nomials_powered(self):
        if self.__are_nomials_numbers():
            return self.nomial1 ** self.nomial2
        else: return Polynomial(self.nomial1,"^",self.nomial2, True)


    def __add__(self, toAdd):
        #Can only add with operator being "+","-" or None
        if self.operator in [None,"+","-"]:
            try:
                return Polynomial(self.nomial1 + toAdd, self.operator, self.nomial2)
            except:
                try:
                    return Polynomial(self.nomial1, self.operator, self.nomial2 + toAdd)
                except:
                    if self.operator==None:
                        #removes parent nesting
                        return Polynomial(self.nomial1,"+",toAdd)
                    else:
                        return Polynomial(self,"+",toAdd)
        else:
            return Polynomial(self,"+",toAdd, True)

    def __radd__(self, toAdd):
        return self.__add__(toAdd)

    def __sub__(self, toSub):
        return self.__add__(-toSub)

    def __rsub__(self, toSub):
        return -self.__add__(-toSub)

    def __neg__(self):
        return self * -1

    def __mul__(self, toMul):
        #Multiplies  ONE  term if the operator is "*"
        #Multiplies BOTH terms if the operator is "+" or "-"
        #Multiplies FIRST term if the operator is "/" or None

        #print("trying to multiply", self, "by", toMul)

        firstResult = False
        try:
            if not isinstance(self.nomial1,str):
                firstResult = self.nomial1 * toMul
        except:
            if self.operator in ["+","-","/",None]:
                #needed to have first nomial calculated
                return Polynomial(self,"*",toMul)
        else:
            if firstResult and self.operator in ["/",None]:
                #got requirements
                return Polynomial(firstResult, self.operator, self.nomial2)


        secondResult = False
        try:
            if not isinstance(self.nomial2,str):
                secondResult = self.nomial2 * toMul
        except:
            if self.operator in ["+","-"]:
                #needed to have second nomial calculated
                return Polynomial(self,"*",toMul)
        else:
            if secondResult and self.operator in ["+","-"]:
                #got requirements
                return Polynomial(firstResult, self.operator, secondResult)

        #smart multiplication
        priority = isinstance(self.nomial1,(int,float)) and 1 or 2
        #print(firstResult, secondResult, priority)
        if self.operator in ["*"]:
            if firstResult and (priority==1 or not secondResult):
                return Polynomial(firstResult, self.operator, self.nomial2)
            elif secondResult and (priority==2 or not firstResult):
                return Polynomial(self.nomial1, self.operator, secondResult)
            else:
                return Polynomial(self,"*",toMul, True)

        return Polynomial(self,"*",toMul, True)


    def __rmul__(self, toMul):
        return self.__mul__(toMul)

    def __truediv__(self, toDiv):
        return self.__mul__(1/toDiv)

    def __rtruediv__(self, toDiv):
        return (self**-1).__mul__(toDiv)

    def __pow__(self, toPow):
        #Can only pow with operator being "*","/" or None
        #print("trying to power", self, "to", toPow)
        if self.operator == "^":
            return Polynomial(self.nomial1,"^",self.nomial2 * toPow)
        elif not self.operator in ["*","/",None]:
            return Polynomial(self,"^",toPow, True)

        firstResult = None
        try:
            firstResult = self.nomial1 ** toPow
        except:
            if self.nomial1 != None: #None should work
                return Polynomial(self,"^",toPow, True)

        secondResult = None
        try:
            secondResult = self.nomial2 ** toPow
        except:
            if self.nomial2 != None:
                return Polynomial(self,"^",toPow, True)

        #print("got", firstResult, secondResult)
        return Polynomial(firstResult,self.operator,secondResult,True)
