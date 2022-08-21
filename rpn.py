import re
from utils import Stack
from config import precedence 
#todo
#sort out the negatives DONE
#implement variable stored in the letters. just have them be the letters in rpn and deal with in compute
#add ability to implement functions sin cos tan asin acos atan dy/dx integrate ln log base
#create compute
#add short hand 5(6+4) and 6A


class RPN:
    def __init__(self, exp, variables):
        self.variables = variables
        self.exp = exp
        self.precedence = precedence
        self.tokens = list(self.precedence.keys())
        self.tokens.append('(')
        self.tokens.append(')')
        self.rpn = self.CreateRPN(self.exp)

    def CreateRPN(self, exp):
        
        # adapted the algorithm from https://www.andreinc.net/2010/10/05/converting-infix-to-rpn-shunting-yard-algorithm
        # tokens = ['+', '-', '*', '/', '^', '%']
        exp = exp.replace(' ', '')
        #print('exp ', exp)
        precedence = self.precedence
        tokens = self.tokens
        newExp = ''
        # split on the spaces, 3+4-> 3 + 4 so that all the symbols and numbers can be tokenised
        for token in tokens:
            for char in exp:
                if char == token:
                    # space at the start incase the symbol follows from a number, numbers wont have spaces because theyre not in the token array
                    newExp += f' {char} '
                else:
                    newExp += char  # its a number
            exp = newExp  # ready to repeat for the next character

            newExp = ''
        tokenised = exp.split(' ')  # do the split
        newTokenised = []
        # remove the unecessary blank characters from subsequent symbols, ie ')*' ->' )  * ' which makes a mess when split
        for i,t in enumerate(tokenised):
            if t != '':
                newTokenised.append(t)
        tokenised=newTokenised
        # newTokenised=[]
        # print(f'before shuffling {tokenised}')
        # skip = False
        # for i,item in enumerate(tokenised[:-1]):
            
        #     if skip == True:
        #         skip = False
        #         continue
        #     if item == '-' and tokenised[i+1]=='-':
        #         newTokenised.append('+')
        #         skip = True
        #     elif (item == '+' and tokenised[i+1]=='-') or (item == '-' and tokenised[i+1]=='+'):
        #         newTokenised.append('-')
        #         skip =True
        #     else:
        #         newTokenised.append(item)
        # newTokenised.append(tokenised[-1])
        tokenised = newTokenised
        print('tokenised 1 ',tokenised)
        newTokenised=[]
        #needs cleaning after negative numbers are fixed
        skip = False
        for i,t in enumerate(tokenised):
            if skip == True:
                skip = False
                continue 
                
            if t=='-':
                # #experimental
                #print('in if')
                newTokenised.append('0')
                newTokenised.append('+')
                newTokenised.append('(')
                newTokenised.append('0')
                newTokenised.append('-')
                newTokenised.append(str(tokenised[i+1]))
                newTokenised.append(')')
                # newTokenised.append(t)
                skip = True
            else:
                newTokenised.append(t)
            

        tokenised = newTokenised
        print(f'tokenised after shuffling {tokenised}')

        # shunting yard algorithm
        s = Stack()
        output = []
        for i, t in enumerate(tokenised):
            if t == '(':
                s.push(t)
            elif t == ')':
                while s.peek() != '(':
                    x = s.pop()
                    if x != '(':
                        output.append(x)
                s.pop()
            elif t in tokens:
                while not s.isEmpty() and s.peek() in list(precedence.keys()):
                    if precedence[t] <= precedence[s.peek()]:
                        x = s.pop()
                        output.append(x)
                    else:
                        break
                s.push(t)

                # s.pop()
            else:
                output.append(t)
        while s.isEmpty() == False:
            x = s.pop()
            print(f'also adding {x}')
            output.append(x)
        #this is in order to support negative numbers
        #example -A + B
        #comes out of rpn like 6-4+ which doesnt work
        #if it was 06-4+ that would work
        # newOuput = [] # cant work on the array were itterating over, world of hurt lol
        # for i,item in enumerate(output):
        #     if item == '-':
        #         if output [i-2] in self.precedence:
        #             #this is a negative number
        #             lastNumber = newOuput.pop()
                    
        #             newOuput.append('0')
        #             newOuput.append(lastNumber)
        #             newOuput.append('-')
        #             newOuput.append('+')
        #             continue #just move on now
        #     newOuput.append(item)


        

        # return newOuput
        newOutput = []


        return output
    def __repr__(self):
        return str(self.rpn)

if __name__ == '__main__':
    r = RPN('A-6', {})
    r = RPN('5*tan (6+5)', {})
    r=RPN('5-6*-9',{})
    print('r: ',r)
    # r = RPN('-6+4', {})

    # print('r: ',r)
