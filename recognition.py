import os
import calculate
from PIL import Image
from model import MyModel
from skimage import io

# s = "(3+657579)/2+7="
def cal(s):
    s+="="
    # print(s)
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
                    print ('%s %.3f'%(s,stknum[len(stknum)-1]) )
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

def splitimage(src, dstpath):
    mystr=''
    img = Image.open(src)
    w, h = img.size
    colnum = int(w/100)
    # print(colnum)
    rownum = 1
    if rownum <= h and colnum <= w:
        # print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
        print('开始识别, 请稍候...')

        s = os.path.split(src)
        if dstpath == '':
            dstpath = s[0]
        fn = s[1].split('.')
        basename = fn[0]
        ext = fn[-1]

        num = 0
        rowheight = h // rownum
        colwidth = w // colnum
        for r in range(rownum):
            for c in range(colnum):
                box = (c * colwidth, r * rowheight, (c + 1) * colwidth, (r + 1) * rowheight)
                img.crop(box).save(os.path.join(dstpath, basename + '_' + str(num) + '.' + ext))
                infile = basename + '_' + str(num) + '.' + ext
                # print(infile)
                outfile = os.path.splitext(infile)[0] + ".jpg"
                try:
                    Image.open(infile).save(outfile)
                    model = MyModel()
                    singleImage = io.imread(outfile, as_grey=True)
                    # print(model.recognize(singleImage))
                    mystr+=model.recognize(singleImage)
                except IOError:
                    print("load....")

                num = num + 1


        print('图片识别完毕，共识别出 %s 个字符' % num)
    else:
        print('不合法的行列切割参数！')
    cal(mystr)


src = input('请输入图片文件路径：')
if os.path.isfile(src):
    dstpath =''
    if (dstpath == '') or os.path.exists(dstpath):
        splitimage(src, dstpath)

    # else:
    #     print('图片输出目录 %s 不存在！' % dstpath)
else:
    print('图片文件 %s 不存在！' % src)