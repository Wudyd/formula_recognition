# s = "(3+657579)/2+7="
def cal(s):
    print(s)
    stknum= []
    stkope= []
    i = 0
    p = 0
    q = 0
    while 1:
        if p==0:
            #print "i=",i,
            ope = s[i]
            if ope>='0' and ope<='9':
                #print ope
                num = 0
                while s[i] >= '0' and s[i]<= '9':
                    num *= 10
                    num += int(s[i])
                    i =i+1
                    #print "++",
                stknum.append(float(num))
                ope = s[i]
        #print stknum,stkope,
        if len(stkope)==0 or ope == '(' or (stkope[len(stkope)-1] == '(' and ope != ')') :
            #print "kk",
            stkope.append(ope)
        elif (stkope[len(stkope)-1] == '-' or stkope[len(stkope)-1] == '+') and (ope == '*' or ope == '/'):
            stkope.append(ope)
        elif stkope[len(stkope)-1] == '(' and ope == ')':
            stkope.pop()
        else:
            num1 = stknum[len(stknum)-1]
            stknum.pop()
            num2 = stknum[len(stknum)-1]
            stknum.pop()
            val = 0
            if stkope[len(stkope)-1] == '+':
                val = num2+num1
            if stkope[len(stkope)-1] == '-':
                val = num2-num1
            if stkope[len(stkope)-1] == '*':
                val = num2 * num1
            if stkope[len(stkope)-1] == '/':
                val = num2 / num1
            stkope.pop()
            stknum.append(val)
            i =i-1

            if ope == '=':
                if len(stkope)==0:
                    #print "!!!!!",
                    print ('%.3f' %stknum[len(stknum)-1])
                    stknum.pop()
                    q = 1
                else:
                    p = 1
        #print stknum,stkope
        i = i+1
        if i==len(s):
            break
        if q==1:
            break
# cal(s)