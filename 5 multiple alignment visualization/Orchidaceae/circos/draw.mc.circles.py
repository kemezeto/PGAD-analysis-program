### draw chromosome homology circles for eudicots with VV as reference, if VV is provided. If no vv chro is involved, it draws circles for other species

from math import *
from pylab import *
import re
from matplotlib.patches import *
from bez import *

##### circle parameters
GAP_RATIO = 4 #gaps between chromosome circle, chr:gap = 4: 1
# r0, r1, r2 = 0.2, 0.0055, 0.004
r0, r1, r2 = 0.2, 0.01, 0.0095
sm_radius=(0.005)/2 #telomere capping
figurefile = "Orchidaceae"# 此处是输出的图片文件名称
figure(1, (8, 8))  ### de
# fine the a square, or other rectangle of the figure, if to produce an oval here
root =axes([0, 0, 1, 1])

fpchrolen = open("Dch.lens")# 此处是参考物种及内圈物种的lens文件，第一列为染色体名称，第二列为染色体包含基因数量

fpmcfit = open("output_new.csv")# 此处是多重比对文件，后期可以优化一下，第二列可以绘染色体图并决定物种内部共线性关系

print ("Usage: python draw.mc.circles.py\n")
# 下方是每圈和左下角图例用到的颜色,外圈每种颜色代表一个染色体
chro2color = {"1": "#d72323", "2": "#b83b5e", "3": "#fa4659", "4": "#f07b3f", "5": "#ff5722", "6": "#ffd460", "7": "#A7FC00","8": "#8f8787","9": "#ebcbae","10": "#dcedc1","11": "#9df3c4", "12": "#1fab89","13": "#086972","14": "#537791","15": "#3fbac2","16": "#163172","17": "#8971d0","18": "#ffd9e8","19": "#fc5c9c","20":"#4a266a", "21":"#393e46", "22":"#993333", "23":"#999933", "24":"#CCCCCC", "25":"#FF33CC", "26":"darkslategray", "27":"mediumorchid", "28":"silver", "29":"moccasin", "30":"mediumseCeseen"}
# chro2color = {"1": "c", "2": "#eb2690", "3": "blue", "4": "orange", "5": "red", "6": "lawngreen", "7": "#009c75","8": "#a6c952","9": "#2f7ec2","10": "#00b5ef", "11": "#FFCC33", "12": "#fc8d62","13": "#CCFF33","14": "#CCCCCC","15": "#CCCC99","16": "#CC99FF","17": "#CC9966","18": "#CC9900","19": "#CC66FF", "20": "#FF1493", "21":"#FFA07A", "22": "#BDB76B", "23": "#FF69B4", "24": "#7B68EE", "25": "#1E90FF"}
#chro2color = {"1": "gray", "2": "lightcoral", "3": "firebrick", "4": "sienna", "5": "chocolate", "6": "darkorange", "7": "goldenrod","8": "yellowgreen","9": "darkseCeseen","10": "seCeseen","11": "springgreen", "12": "darkslategray","13": "darkcyan","14": "skyblue","15": "lightsteelblue","16": "navy","17": "indigo","18": "plum","19": "deeppink","20":"bisque"}
# 下方是内圈每条染色体的颜色,最内圈的共线性的线的颜色
#ancestralchro2color = {"A1": "#fecea8", "A2": "#ff847c", "A3": "#e84a5f", "A4": "#2a363b", "A5": "#ff7e67", "A6": "#fafafa", "A7": "#a2d5f2", "A8": "#07689f", "A9": "#625772"}
ancestralchro2color = {"A1": "#d72323", "A2": "#b83b5e", "A3": "#fa4659", "A4": "#f07b3f", "A5": "#ff5722", "A6": "#ffd460", "A7": "#A7FC00","A8": "#8f8787","A9": "#ebcbae","A10": "#dcedc1","A11": "#9df3c4", "A12": "#1fab89","A13": "#086972","A14": "#537791","A15": "#3fbac2","A16": "#163172","A17": "#8971d0","A18": "#ffd9e8","A19": "#fc5c9c","A20":"#4a266a", "A21":"#393e46", "A22":"#993333", "A23":"#999933", "A24":"#CCCCCC", "A25":"#FF33CC", "A26":"darkslategray", "A27":"mediumorchid", "A28":"silver", "A29":"moccasin"}
# 下方右下角图例用到的颜色
#specieschro2color = {"S1": "black", "S2": "g", "S3": "#BA55D3", "S4": "#DA70D6", "S5": "blue", "S6": "cyan", "S7": "r", "S7": "y", "S8": "m", "S9": "red"}

### input chromosome length
chro2len = {}
labels = []
for row in fpchrolen:
    chro, length = row.split()
    chro = chro.upper()
    chro2len[chro] = int(length)
    labels.append(chro)
fpchrolen.close()
### full chro list
print ("all chro", labels)

def rad_to_coord(angle, radius):
    return radius*cos(angle), radius*sin(angle)

def to_deg(bp, total):
    # from basepair return as degree
    return bp*360./total

def to_radian(bp, total):
    # from basepair return as radian
#    print "to_radian", bp, total
    return radians(bp*360./total)

def plot_arc(start, stop, radius, clcl):
    # start, stop measured in radian
    print ("In plot_arc ", start, stop)
    t = arange(start, stop, pi/720.)
    x, y = radius*cos(t), radius*sin(t)
    plot(x, y, color=clcl, linestyle = "-", alpha=.5, lw = .5)#circle line color

def plot_cap(angle, clockwise=True, radius=sm_radius):
    # angle measured in radian, clockwise is boolean
    if clockwise: t = arange(angle, angle+pi, pi/30.)
    else: t = arange(angle, angle-pi, -pi/30.)
    x, y = radius*cos(t), radius*sin(t)
    middle_r = (radius_a+radius_b)/2
    x, y = x + middle_r*cos(angle), y + middle_r*sin(angle)
    plot(x, y, "k-", alpha=.5)

def plot_arc_block(start, chain, radius):
    t = arange(start, start+blocklength, pi/720.)
    x,y = radius * cos(t), radius*sin(t)
    x1, y1 = (radius-blockthick) * cos(t), (radius-blockthick) * sin(t)
    plot(x, y, "b-", alpha=0.2)
#    plot(x1, y1, "g-", alpha=0.5)

    x0, y0 = radius*cos(start), radius*sin(start)
    x1,y1  = (radius-blockthick)*cos(start), (radius-blockthick)*sin(start)
#    plot([x0, y0], [x1, y1], "g-", lw=0.2)

    x0, y0 = radius*cos(start+blocklength), radius*sin(start+blocklength)
    x1,y1  = (radius-blockthick)*cos(start+blocklength), (radius-blockthick)*sin(start+blocklength)
#    plot([x0, y0], [x1, y1], "g-", lw=0.2)

fullchrolen = sum(list(chro2len.values()))#此处添加list
chr_number = len(labels) # total number of chromosomes
GAP = fullchrolen/GAP_RATIO/chr_number # gap size in base pair
total_size = fullchrolen + chr_number * GAP # base pairs

start_list = [0]*chr_number
for i in range(1, chr_number):
    start_list[i] = start_list[i-1] + chro2len[labels[i-1]] + GAP
    print ("chr ", i, start_list[i])
stop_list = [(start_list[i] + chro2len[labels[i]]) for i in range(chr_number)]

def transform_deg(ch, pos):
    return to_deg(pos + start_list[ch], total_size)

def transform_pt(ch, pos, r):
    # convert chromosome position to axis coords
#    print "transform", ch, pos, r
#    print "startlist", start_list[ch]
    rad = to_radian(pos + start_list[ch], total_size)
    return r*cos(rad), r*sin(rad)
def transform_pt2(rad, r):
    return r*cos(rad), r*sin(rad)

# 绘制内圈线的函数
def plot_bez_inner(p1, p2, cl):
    print ("inner")
    a, b, c = p1
    ex1x, ex1y = transform_pt(a, b, c)
    a, b, c = p2
    ex2x, ex2y = transform_pt(a, b, c)
    # Bezier ratio, controls curve, lower ratio => closer to center
    ratio = .5
    x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
    y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
    step = .01
    t = arange(0, 1+step, step)
    xt = Bezier(x, t)
    yt = Bezier(y, t)
    plot(xt, yt, color=cl, linestyle='-', lw=.2)#改内 圈线粗

def plot_bez_outer(p1, p2, cl):
    print ("outer")
    a, b, c = p1
    ex1x, ex1y = transform_pt(a, b, c)
    a, b, c = p2
    ex2x, ex2y = transform_pt(a, b, c)
    # Bezier ratio, controls curve, lower ratio => closer to center
    ratio = 1.1
    x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
    y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
    step = .01
    t = arange(0, 1+step, step)
    xt = Bezier(x, t)
    yt = Bezier(y, t)
    plot(xt, yt, '-', color=cl, lw=.1)#改外圈线粗

def plot_bez_Ks(rad1, r1, rad2, r2, col):
    print ("bez Ks 1")
    ex1x, ex1y = transform_pt2(rad1, r1)
    ex2x, ex2y = transform_pt2(rad2, r2)
    ratio = 0.5
    x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
    y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
    step = .01
    t = arange(0, 1+step, step)
    xt = Bezier(x, t)
    yt = Bezier(y, t)
    plot(xt, yt, '-', color=col, lw=0.1)#改

def plot_bez_Ks2(rad1, r1, rad2, r2, col):
    print ("bez Ks 2")
    ex1x, ex1y = transform_pt2(rad1, r1)
    ex2x, ex2y = transform_pt2(rad2, r2)
    ratio = 0.5
    sita = pi/2
    if ex1x != ex2x:
        sita = atan((ex2y-ex1y)/(ex2x-ex1x))#在此处添加一个缩进
    d = sqrt((ex2x-ex1x)**2+(ex2y-ex1y)**2)
    L = d * ratio
    P1x = ex1x + L*sin(sita)
    P1y = ex1y - L*cos(sita)
    P2x = ex2x + L*sin(sita)
    P2y = ex2y - L*cos(sita)
    step = .01
    t = arange(0, 1+step, step)
    x=[ex1x, P1x, P2x, ex2x]
    y=[ex1y, P1y, P2y, ex2y]
    xt = Bezier(x,t)
    yt = Bezier(y,t)
    plot(xt, yt, '-', color = col, lw = 0.1)

def plot_sector(s):
    # block_id, chr_id, start_bp, stop_bp
    block_id, chr_id, start_bp, stop_bp = s
    theta0, theta1 = transform_deg(chr_id, start_bp), transform_deg(chr_id, stop_bp)
    dtheta = .1
    p1 = Wedge((0, 0), radius_a, theta0, theta1, dtheta=dtheta, fc="w", ec="w")
    p2 = Wedge((0, 0), radius_b, theta0, theta1, dtheta=dtheta, fc=colors[block_id], ec="w")
    root.add_patch(p2)
    root.add_patch(p1)

print ("r0r1r2", r0, r1, r2)
### input mcscan data
row = fpmcfit.readline()
### read in pair file
gene2alignpos = {}
gene2wgdpara = {}
rowno = 0
for row in fpmcfit:
#    print "thisrow", row，对每行数据进行分析
    item = row.split("\t")
    thischro = item[1]
    #print "the ancestor is", thischro
    #color2 = ancestralchro2color[thischro]
    chropos = item[0].split("=")
    (c2, p2, s2) = (-1, -1, -1)

#    print "position is ", chropos[0], chropos[1]
    sbgene1 = ""
    sbgene2 = ""
    for i in range(2, min(len(item), 28)):############add blocks改
        if len(item[i]) > 6:
            xx1, yy1 = transform_pt(int(chropos[0]), int(chropos[1]), r0+(i-3)*(r1+r2)*1)
            xx2, yy2 = transform_pt(int(chropos[0]), int(chropos[1]), r0+(i-3)*(r1+r2)*1+1.7*r1)

        print ("the ancestor is", item[1])

        if item[i].find("g") == -1:
            continue
        itemN = item[i].split("/")
        for j in range(len(itemN)):
            if itemN[j].find("g") != -1:
                item[i] = itemN[j]
                break
        chro = item[i].split("g")[0]
        chro = re.sub('\D', '', chro)
        chro = re.sub('^0', '', chro)
        color = chro2color[chro]
        color2 = ancestralchro2color[thischro]
        print ("the i is ", i, item[i], color, thischro, color2)
#       在这里画每个圈的颜色
        if i==2:
            plot([xx1, xx2], [yy1, yy2], color=color2, linestyle='-', lw = 0.19)#改
        if i >2 and i<28:
            plot([xx1, xx2], [yy1, yy2], color=color, linestyle='-', lw = 0.2)#改，线的粗细
           
        if i==2:
            (c2, p2, s2) =(int(chropos[0]), int(chropos[1]), r0-r1*6)
            gene2alignpos[item[i]] = (c2, p2, s2)
            sbgene1 = item[i]
#              print "sbgene1 is ", sbgene1

        if i==3 or i==4 or i == 5:
            sbgene2 = item[i]
            print ("sbgene2 is ", sbgene2)
        
#   print "sbgenes ", sbgene1, " ", sbgene2, " ", sbgene3

    if sbgene1 != "" and sbgene2 != "":
        gene2wgdpara[thischro+" "+ sbgene1 + " " + sbgene2] = 1
#       print "genepair", sbgene1, sbgene2
    rowno = rowno + 1
    # if rowno == 300:#改
    #     break

fpmcfit.close()

### draw colinear lines，绘制内圈的线，只有第2、3、4、5列有物种内部发生加倍事件才会出现。
for genepair in gene2wgdpara.keys():
    print ("thisgenepair#########", genepair)
    thischro, gene1, gene2 = genepair.split(' ')
    if gene1 in gene2alignpos and gene2 in gene2alignpos:
        plot_bez_inner(gene2alignpos[gene1], gene2alignpos[gene2], cl=ancestralchro2color[thischro])
#####################################################
#################################################
# specieschro2color = {"S1": "black", "S2": "g", "S3": "#BA55D3", "S4": "#DA70D6", "S5": "blue", "S6": "cyan", "S7": "r", "S7": "y", "S8": "m", "S9": "red"}

# the chromosome layout
j = 0
for start, stop in zip(start_list, stop_list):

    start, stop = to_radian(start, total_size), to_radian(stop, total_size)

    # 每条染色体的起始弧度和终止弧度,以及距离圆心的半径
    print ("chropos ", start, stop, r0-r1)

#   添加每圈的黑色边框,以及内圈的颜色
    plot_arc(start, stop, r0-(r1+r2)-r1*0.5, clcl = "black")#############################will be revise#inner circle line
    # 此处用于修改多重比对的圈数
    for i in range(-1, 6):#############add circle line改
        if i ==-1 or i ==0 or i ==1  or i ==2  or i ==3  or i ==4  or i ==5  or i ==6  or i ==7  or i ==8  or i ==9  or i ==10  or i ==11  or i ==12  or i ==13  or i ==14 or i ==15 or i ==16  or i ==17  or i ==18 or i ==19 or i ==20 or i ==21  or i ==22  or i ==23  or i ==24  or i ==25  or i ==26  or i ==27  or i ==28  or i ==29 or i ==30 or i ==31 or i ==32 or i ==33:
                  plot_arc(start, stop, r0+i*(r1+r2)*1, clcl = "black")###################will be revise        

    # telemere capping
    #plot_cap(start, clockwise=False)
    #plot_cap(stop)
    # chromosome labels 最内圈的染色体序号文字
    label_x, label_y = rad_to_coord(start+0.06, r0-5*r1)
    plot(label_x, label_y, 'yo', markersize=15, lw=0.2)#draw circle for chromosomes number染色体号圈颜色
    text(label_x, label_y, labels[j], horizontalalignment="center", verticalalignment="center", fontsize = 5.5, color = 'black')
    j+=1


### draw the circle marker text
label_x, label_y = rad_to_coord(0, r0)
text(label_x-0.02, label_y-0.009, "Dch Gel Dno Dth Pzi Pgu", verticalalignment="center", fontsize = 5 )#改
# for i in range(-1, 21):
		# label_x, label_y = rad_to_coord(0.3, r0+(i+1)*(r1+r2)*1.4)
		# if i == -1 or i==6 or i==13:
				# text(label_x-0.01, label_y-0.01, "V",  fontsize = 8)
		# if i == 0 or i == 3 or i==7 or i==10 or i==14 or i==17:
				# text(label_x-0.01, label_y-0.01, "M",  fontsize = 8)
		# if i==1 or i==4 or i==8 or i==11 or i==15 or i==18:
				# text(label_x-0.01, label_y-0.01, "G",  fontsize = 8)
		# if i==2 or i==5 or i==9 or i==12 or i==16 or i==19:
				# text(label_x-0.01, label_y-0.01, "G",  fontsize = 8)

#### draw tick showing scale of chromosomes 刻度线
for i in range(chr_number):
    pos = 0
    while pos < chro2len[labels[i]]:
        xx1, yy1 = transform_pt(i, int(pos), r0-(r1+r2)-r1*1.0)
        xx2, yy2 = transform_pt(i, int(pos), r0-(r1+r2)-r1*0.5)
        plot([xx1, xx2], [yy1, yy2], "k-", lw = .2)
        pos = pos + 200

#

align = dict(horizontalalignment="center", fontsize=7)
startx, starty = -.45, -.46
square = .011
# 圈的颜色
root.text(startx-square*.1-0.01, starty, "Chr#", align)
root.add_patch(Rectangle((startx+square, starty), 2*square, square, fc=chro2color["1"]))
root.text(startx+2*square, starty-1.4*square, "$1$", align)
root.add_patch(Rectangle((startx+3*square, starty), 2*square, square, fc=chro2color["2"]))
root.text(startx+4*square, starty-1.4*square, "$2$", align)
root.add_patch(Rectangle((startx+5*square, starty), 2*square, square, fc=chro2color["3"]))
root.text(startx+6*square, starty-1.4*square, "$3$", align)
root.add_patch(Rectangle((startx+7*square, starty), 2*square, square, fc=chro2color["4"]))
root.text(startx+8*square, starty-1.4*square, "$4$", align)
root.add_patch(Rectangle((startx+9*square, starty), 2*square, square, fc=chro2color["5"]))
root.text(startx+10*square, starty-1.4*square, "$5$", align)
root.add_patch(Rectangle((startx+11*square, starty), 2*square, square, fc=chro2color["6"]))
root.text(startx+12*square, starty-1.4*square, "$6$", align)
root.add_patch(Rectangle((startx+13*square, starty), 2*square, square, fc=chro2color["7"]))
root.text(startx+14*square, starty-1.4*square, "$7$", align)
root.add_patch(Rectangle((startx+15*square, starty), 2*square, square, fc=chro2color["8"]))
root.text(startx+16*square, starty-1.4*square, "$8$", align)
root.add_patch(Rectangle((startx+17*square, starty), 2*square, square, fc=chro2color["9"]))
root.text(startx+18*square, starty-1.4*square, "$9$", align)
root.add_patch(Rectangle((startx+19*square, starty), 2*square, square, fc=chro2color["10"]))
root.text(startx+20*square, starty-1.4*square, "$10$", align)
root.add_patch(Rectangle((startx+21*square, starty), 2*square, square, fc=chro2color["11"]))
root.text(startx+22*square, starty-1.4*square, "$11$", align)
root.add_patch(Rectangle((startx+23*square, starty), 2*square, square, fc=chro2color["12"]))
root.text(startx+24*square, starty-1.4*square, "$12$", align)
root.add_patch(Rectangle((startx+25*square, starty), 2*square, square, fc=chro2color["13"]))
root.text(startx+26*square, starty-1.4*square, "$13$", align)
root.add_patch(Rectangle((startx+27*square, starty), 2*square, square, fc=chro2color["14"]))
root.text(startx+28*square, starty-1.4*square, "$14$", align)
root.add_patch(Rectangle((startx+29*square, starty), 2*square, square, fc=chro2color["15"]))
root.text(startx+30*square, starty-1.4*square, "$15$", align)
root.add_patch(Rectangle((startx+31*square, starty), 2*square, square, fc=chro2color["16"]))
root.text(startx+32*square, starty-1.4*square, "$16$", align)
root.add_patch(Rectangle((startx+33*square, starty), 2*square, square, fc=chro2color["17"]))
root.text(startx+34*square, starty-1.4*square, "$17$", align)
root.add_patch(Rectangle((startx+35*square, starty), 2*square, square, fc=chro2color["18"]))
root.text(startx+36*square, starty-1.4*square, "$18$", align)
root.add_patch(Rectangle((startx+37*square, starty), 2*square, square, fc=chro2color["19"]))
root.text(startx+38*square, starty-1.4*square, "$19$", align)
root.add_patch(Rectangle((startx+39*square, starty), 2*square, square, fc=chro2color["20"]))
root.text(startx+40*square, starty-1.4*square, "$20$", align)
root.add_patch(Rectangle((startx+41*square, starty), 2*square, square, fc=chro2color["21"]))
root.text(startx+42*square, starty-1.4*square, "$21$", align)
# root.add_patch(Rectangle((startx+43*square, starty), 2*square, square, fc=chro2color["22"]))
# root.text(startx+44*square, starty-1.4*square, "$22$", align)
# root.add_patch(Rectangle((startx+45*square, starty), 2*square, square, fc=chro2color["23"]))
# root.text(startx+46*square, starty-1.4*square, "$23$", align)
# root.add_patch(Rectangle((startx+47*square, starty), 2*square, square, fc=chro2color["24"]))
# root.text(startx+48*square, starty-1.4*square, "$24$", align)
# root.add_patch(Rectangle((startx+49*square, starty), 2*square, square, fc=chro2color["25"]))
# root.text(startx+50*square, starty-1.4*square, "$25$", align)
# root.add_patch(Rectangle((startx+51*square, starty), 2*square, square, fc=chro2color["26"]))
# root.text(startx+52*square, starty-1.4*square, "$26$", align)
# root.add_patch(Rectangle((startx+53*square, starty), 2*square, square, fc=chro2color["27"]))
# root.text(startx+54*square, starty-1.4*square, "$27$", align)
# root.add_patch(Rectangle((startx+55*square, starty), 2*square, square, fc=chro2color["28"]))
# root.text(startx+56*square, starty-1.4*square, "$28$", align)
# root.add_patch(Rectangle((startx+57*square, starty), 2*square, square, fc=chro2color["29"]))
# root.text(startx+58*square, starty-1.4*square, "$29$", align)
###################################
#ancestral chro
align = dict(horizontalalignment="center", fontsize=7)
startx, starty = -.45, -.42
square = .011

# 下方是最内圈的共线性的线的颜色,右下角图例用到的颜色
root.text(startx-square*.1-0.008, starty, "Dch#", align)
root.add_patch(Rectangle((startx+square, starty), 2*square, square, fc=ancestralchro2color["A1"]))
root.text(startx+2*square, starty-1.4*square, "$1$", align)
root.add_patch(Rectangle((startx+3*square, starty), 2*square, square, fc=ancestralchro2color["A2"]))
root.text(startx+4*square, starty-1.4*square, "$2$", align)
root.add_patch(Rectangle((startx+5*square, starty), 2*square, square, fc=ancestralchro2color["A3"]))
root.text(startx+6*square, starty-1.4*square, "$3$", align)
root.add_patch(Rectangle((startx+7*square, starty), 2*square, square, fc=ancestralchro2color["A4"]))
root.text(startx+8*square, starty-1.4*square, "$4$", align)
root.add_patch(Rectangle((startx+9*square, starty), 2*square, square, fc=ancestralchro2color["A5"]))
root.text(startx+10*square, starty-1.4*square, "$5$", align)
root.add_patch(Rectangle((startx+11*square, starty), 2*square, square, fc=ancestralchro2color["A6"]))
root.text(startx+12*square, starty-1.4*square, "$6$", align)
root.add_patch(Rectangle((startx+13*square, starty), 2*square, square, fc=ancestralchro2color["A7"]))
root.text(startx+14*square, starty-1.4*square, "$7$", align)
root.add_patch(Rectangle((startx+15*square, starty), 2*square, square, fc=ancestralchro2color["A8"]))
root.text(startx+16*square, starty-1.4*square, "$8$", align)
root.add_patch(Rectangle((startx+17*square, starty), 2*square, square, fc=ancestralchro2color["A9"]))
root.text(startx+18*square, starty-1.4*square, "$9$", align)
root.add_patch(Rectangle((startx+19*square, starty), 2*square, square, fc=ancestralchro2color["A10"]))
root.text(startx+20*square, starty-1.4*square, "$10$", align)
root.add_patch(Rectangle((startx+21*square, starty), 2*square, square, fc=ancestralchro2color["A11"]))
root.text(startx+22*square, starty-1.4*square, "$11$", align)
root.add_patch(Rectangle((startx+23*square, starty), 2*square, square, fc=ancestralchro2color["A12"]))
root.text(startx+24*square, starty-1.4*square, "$12$", align)
root.add_patch(Rectangle((startx+25*square, starty), 2*square, square, fc=ancestralchro2color["A13"]))
root.text(startx+26*square, starty-1.4*square, "$13$", align)
root.add_patch(Rectangle((startx+27*square, starty), 2*square, square, fc=ancestralchro2color["A14"]))
root.text(startx+28*square, starty-1.4*square, "$14$", align)
root.add_patch(Rectangle((startx+29*square, starty), 2*square, square, fc=ancestralchro2color["A15"]))
root.text(startx+30*square, starty-1.4*square, "$15$", align)
root.add_patch(Rectangle((startx+31*square, starty), 2*square, square, fc=ancestralchro2color["A16"]))
root.text(startx+32*square, starty-1.4*square, "$16$", align)
root.add_patch(Rectangle((startx+33*square, starty), 2*square, square, fc=ancestralchro2color["A17"]))
root.text(startx+34*square, starty-1.4*square, "$17$", align)
root.add_patch(Rectangle((startx+35*square, starty), 2*square, square, fc=ancestralchro2color["A18"]))
root.text(startx+36*square, starty-1.4*square, "$18$", align)
root.add_patch(Rectangle((startx+37*square, starty), 2*square, square, fc=ancestralchro2color["A19"]))
root.text(startx+38*square, starty-1.4*square, "$19$", align)

plt.rcParams["font.family"] = "Arial"


root.set_xlim(-.58, .58)  # 
root.set_ylim(-.6, .58)
root.set_axis_off()
savefig(figurefile + ".svg", dpi=300)
savefig(figurefile + ".png", dpi=300)
#savefig(figurefile + ".svg", dpi=300)

