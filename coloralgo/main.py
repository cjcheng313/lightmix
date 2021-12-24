from itertools import combinations

import colormath
import numpy as np
import xlsxwriter
import pymysql
from colormath.color_objects import LabColor, XYZColor
from colormath.color_conversions import convert_color
from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color



bulbR = [[2.2622, 1.0000, 0.0026]]
bulbG = [[0.1988, 1.0000, 0.2091]]
bulbB = [[2.3426, 1.0000, 13.9585]]
bulbW = [[1.3050, 1.0000, 0.1526]]
bulbC = [[0.9724, 1.0000, 1.3588]]

target = [[1.4645, 1.0000, 0.1363]]
targetX = targetY =targetZ = 0;

maxR=4.268125
maxG=8.2026
maxB=1.843
maxW=7.243225
maxC=10.95095

kr = 0.170725
kg = 0.328104
kb = 0.07372
kw = 0.289729
kc = 0.438038


def calculate(r):
    if r <= 10:
        R=(r/255.0000)/12.9200
    else:
        R=pow(((r/255.0000)+0.055)/1.055, 2.4)
    return R
    # Use a breakpoint in the code line below to debug your script.

    print("Hi, {0}:r={1}", R, r)

def calcualte_rgb(r,g,b):
    #workbook = xlsxwriter.Workbook('step1.xlsx')
    #worksheet = workbook.add_worksheet()

    #worksheet.write('A1','r')
    #worksheet.write('B1', 'g')
    #worksheet.write('C1', 'b')

   # worksheet.write('D1', 'R')
   # worksheet.write('E1', 'G')
    #worksheet.write('F1', 'B')

   # worksheet.write('G1', 'X')
   # worksheet.write('H1', 'Y')
   # worksheet.write('I1', 'Z')

   # worksheet.write('J1', 'x')
   # worksheet.write('K1', 'y')
   # worksheet.write('L1', 'z')

    row = 1
    #while(r <= i):
     #   g=10
      #  while (g <= i):
      #      b=10
       #     while (b <= i):
                #worksheet.write(row, 0, r)
                #worksheet.write(row, 1, g)
                #worksheet.write(row, 2, b)
    print("r=%d,g=%d,b=%d" % (r, g, b))
    R = calculate(r)
    G = calculate(g)
    B = calculate(b)

    rgb = sRGBColor(r, g, b,True)
    xyz = convert_color(rgb, XYZColor, target_illuminant='d50')
    print("==========================")
    print(xyz)
    print("==========================")
    # worksheet.write(row, 3, R)
    # worksheet.write(row, 4, G)
    # worksheet.write(row, 5, B)
    print("R=%f,G=%f,B=%f" % (R, G, B))
    data = np.mat([R, G, B]);
    m = np.mat([[0.412390799265960,0.357584339383878, 0.180480788401834],
                [0.212639005871510, 0.715168678767756, 0.072192315360734],
                [0.019330818715592, 0.119194779794626, 0.950532152249661]])
    XYZ = data * m * 100

    X = xyz.xyz_x
    Y = xyz.xyz_y
    Z = xyz.xyz_z

    print("X=%f,Y=%d,Z=%d" % (X, Y, Z))


    # worksheet.write(row, 6, X)
    # worksheet.write(row, 7, Y)
    # worksheet.write(row, 8, Z)

    sumxyz = X + Y + Z
    if sumxyz != 0:
        x = X / sumxyz
        y = Y / sumxyz
        z = Z / sumxyz
    else:
        x = 0
        y = 0
        z = 0
    if y == 0:
        X1 = 0
        Y1 = 1
        Z1 = 0
    else:
        X1 = x/y
        Y1 = 1
        Z1 = z/y
    # worksheet.write(row, 9, x)
    # worksheet.write(row, 10, y)
    # worksheet.write(row, 11, z)
    print("x=%f,y=%f,z=%f" % (x, y, z))
    print("X1=%f,Y1=%f,Z1=%f" % (X1, Y1, Z1))
    caculate5ratio(r, g, b, X1, Y1, Z1, [[X1, Y1, Z1]])
         #       b = b + 1
         #       row = row + 1
         #   g = g + 1
       # r = r+1


    #workbook.close()

def caculate5ratio(r,g,b,X,Y,Z,targetXYZ):
    sumLight = r/255*maxR + g/255*maxG + b/255*maxB

    combList = list(combinations("RGBCW", 3))

    sumR = sumG = sumB = sumW = sumC = 0.0000;
    count =0;
    matComb = np.zeros((3, 3))
    resutlistR = []
    resutlistG =[]
    resutlistB =[]
    resutlistW =[]
    resutlistC = []
    for comb in combList:
        i = 0;
        print(comb)
        matComb = np.zeros((3, 3))
        for c in comb:

            if c == 'R':
                matComb[:, [i]] = np.array(bulbR).T
            elif c == 'G':
                matComb[:, [i]] = np.array(bulbG).T
            elif c == 'B':
                matComb[:, [i]] = np.array(bulbB).T
            elif c == 'W':
                matComb[:, [i]] = np.array(bulbW).T
            elif c == 'C':
                matComb[:, [i]] = np.array(bulbC).T
            i = i + 1
        m = np.mat(matComb)
        print('matrix tristimulus value')
        print(matComb)
        print('inverse matrix')
        print(m.I)
        triResult = m.I * np.array(targetXYZ).T
        print('Ratio result')
        print(triResult)

        isNagtive = 0
        for n in triResult:
            if n < 0:
                isNagtive = 1

        if isNagtive == 0:
            i = 0
            count = count + 1
            for c in comb:
                if c == 'R':
                    resutlistR.append(triResult[i, 0])
                    sumR = sumR + triResult[i, 0]
                elif c == 'G':
                    resutlistG.append(triResult[i, 0])
                    sumG = sumG + triResult[i, 0]
                elif c == 'B':
                    resutlistB.append(triResult[i, 0])
                    sumB = sumB + triResult[i, 0]
                elif c == 'W':
                    resutlistW.append(triResult[i, 0])
                    sumW = sumW + triResult[i, 0]
                elif c == 'C':
                    resutlistC.append(triResult[i, 0])
                    sumC = sumC + triResult[i, 0]

                i=i + 1

    cr = sumR / kr
    cg = sumG / kg
    cb = sumB / kb
    cw = sumW / kw
    cc = sumC / kc
    print('sum R current = %f' % sumR)
    print('sum G current = %f' % sumG)
    print('sum B current = %f' % sumB)
    print('sum C current = %f' % sumW)
    print('sum W current = %f' % sumC)

    if count > 0 :
        rp = sumR/count
        rg = sumG/count
        rb = sumB/count
        rw = sumW/count
        rc = sumC/count
    else:
        rp=rg=rb=rw=rc =0
    print('percent R current = %f' % rp)
    print('percent G current = %f' % rg)
    print('percent B current = %f' % rb)
    print('percent C current = %f' % rw)
    print('percent W current = %f' % rc)

    tr = int(sumLight * rp/maxR*255)
    tg = int(sumLight * rg / maxG * 255)
    tb = int(sumLight * rb / maxB * 255)
    tw = int(sumLight * rw / maxW * 255)
    tc = int(sumLight * rc / maxC * 255)

    # print('cr current = %f' % cr)
    # print('cg current = %f' % cg)
    # print('cb current = %f' % cb)
    # print('cw current = %f' % cw)
    # print('cc current = %f' % cc)

    print(resutlistR)
    print(resutlistG)
    print(resutlistB)
    print(resutlistC)
    print(resutlistW)

    db = pymysql.connect(host="rm-wz97h2x290l64sx96fo.mysql.rds.aliyuncs.com",
                         user="zflive",
                         password="zfadmin!",
                         port=3306,
                         database="zflive",
                         charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM ce_color_mapping".format(1000)

    #cr= int(cr/maxR*255)
    #cg = int(cg / maxG * 255)
    #cb = int(cb / maxB * 255)
    #cw = int(cw / maxW * 255)
    #cc = int(cc / maxC * 255)

    # sumrgbcw = cr+cg+cb+cw+cc
    # if sumrgbcw == 0:
    #     sumrgbcw=1
    #
    # cr= cr/sumrgbcw
    # cg = cg / sumrgbcw
    # cb = cb / sumrgbcw
    # cw = cw / sumrgbcw
    # cc = cc / sumrgbcw
    #
    sql = "INSERT INTO ce_color_mapping(OrR,OrG,OrB,X,Y,Z,TR,TG,TB,TW,TC) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7},{8}, {9}, {10})"\
        .format(r,g,b,X,Y,Z,tr, tg, tb, tw, tc)
    try:
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()
    db.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
     calcualte_rgb(200, 100, 180)

     # index = 255
     # x=0
     # while x<index:
     #     y=0
     #     while y<index:
     #         z=0
     #         while z<index:
     #             calcualte_rgb(x, y, z)
     #             z=z+10
     #         y=y+10
     #     x=x+10



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
