class Polynomial():
    def __init__(self, nomial1, operator, nomial2):
        self.nomial1 = nomial1
        self.operator = operator
        self.nomial2 = nomial2

        try:
            result = "Dont"
            if operator == "+":
                result = self.nomial1 + self.nomial2
            elif operator == "-":
                result = self.nomial1 - self.nomial2
            elif operator == "*":
                result = self.nomial1 * self.nomial2
            elif operator == "/":
                result = self.nomial1 / self.nomial2
            elif operator == "^" or operator == "**":
                result = self.nomial1 ** self.nomial2
        except:
            result = "Dont"

        finally:
            if result != "Dont":
                self.__init__(result, None, None)

        if type(self.nomial1) == Polynomial and self.operator in [None,False] and self.nomial2 in [None,False]:
            self.__init__(self.nomial1.nomial1, self.nomial1.operator, self.nomial1.nomial2)

    def __str__(self):
        #Printa polinômios e monômios
        return "(" + str(self.nomial1) + str(self.operator) + str(self.nomial2) + ")"

    def __repr__(self):
        #Mostra todas os atributos, sem esconder
        if self.operator == None:
            return str(self.nomial1)
        else:
            toShow = str(self.nomial1)
            toShow += self.operator and str(self.operator) or ""
            toShow += self.nomial2 and str(self.nomial2) or ""
            return "(" + toShow + ")"

    def addition(self, toAdd, ignoreFactor=0):
        result = self
        try:
            if ignoreFactor == 1:
                return False
            result = self.nomial1 + toAdd
        except TypeError as e:
            if ignoreFactor == 2:
                return False
            result = self.nomial2 + toAdd

        except TypeError as actE:
            print("WEE WOO WEE WOO (add)")
            print(actE)
            return False
        finally:
            return result

    def __radd__(self, toAdd):
        return self.__add__(toAdd)

    def __add__(self, toAdd):
        return self.addition(toAdd)

    def __rsub__(self, toSub):
        return -self.__sub__(toSub)

    def __sub__(self, toSub):
        return self.addition(-toSub)

    def __neg__(self):
        return self * -1


    def multiply(self, toMulti, ignoreFactor=0):
        esult = self
        didIt = ["idklol", None, None]

        if self.operator in ["+","-"]:
            didIt[0] = "and"
        elif self.operator in ["*"]:
            didIt[0] = "or"
        elif self.operator in ["/"]:
            didIt[0] = "onlyFirst"
        elif self.operator in [None]:
            didIt[0] = "Noner"

        try:
            didIt[1] = self.nomial1 * toMulti
        except:
            didIt[1] = None

        try:
            didIt[2] = self.nomial2 * toMulti
        except:
            didIt[2] = None

        if didIt[0] == "and" and didIt[1]!=None and didIt[2]!=None:
            return Polynomial(didIt[1], self.operator, didIt[2])
        elif didIt[0] == "or" and didIt[1]!=None:
            return Polynomial(didIt[1], self.operator, self.nomial2)
        elif didIt[0] == "or" and didIt[2]!=None:
            return Polynomial(self.nomial1, self.operator, didIt[2])
        elif didIt[0] == "onlyFirst" and didIt[1]!=None:
            return Polynomial(didIt[1], self.operator, self.nomial2)
        elif didIt[0] == "Noner" and toMulti = None:
            return Polynomial(didIt[1], self.operator, self.nomial2)
        else:
            return Polynomial(self,"*",toMulti)

    def __rmul__(self, toMulti):
        return self.__mul__(toMulti)

    def __mul__(self, toMulti):
        return self.multiply(toMulti)

    def __rdiv__(self, toDiv):
        return self ** -1

    def __div__(self, toDiv):
        return self.multiply(1/toDiv)


    def exponentiate(self, toPow, ignoreFactor=0):
        result = self
        try:
            if ignoreFactor == 1:
                return False
            result = self.nomial1 ** toPow
        except TypeError as e:
            if ignoreFactor == 2:
                return False
            result = self.nomial2 ** toPow

        except TypeError as actE:
            print("WEE WOO WEE WOO (pow)")
            print(actE)
            return False

        finally:
            return Polynomial(result,None,None)

    def __pow__(self, toPow):
        return self.exponentiate(toPow, 0)

    def __rpow__(self, toPow, recursed=False):
        try:
            if recursed:
                pass
            return toPow.exponentiate(self, 0)
        except Exception as e:
            return Polynomial(toPow, "^", self)
