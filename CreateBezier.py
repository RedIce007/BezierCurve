import tkinter
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure


#绘制贝塞尔曲线时的鼠标单击事件
def xFunc1(event):
    global array
    global l
    m = round(((event.x-75)/4.65), 2)
    n = round(((534-event.y)/4.62), 2)
    m = limit_point(m)
    n = limit_point(n)
    print(f"坐标是:x={m}y={n}")
    a = ([[m, n]])
    array = np.vstack((array, a))
    Draw_point(array)
    if (len(array)) >= 2:
        Draw_line(array)
    updateDraw()
    #如果控制点点击完毕，则绘制贝塞尔曲线
    if len(array) >= c:
        root.unbind("<ButtonRelease-1>")
        l.append(array)
        print(array)
        print(l)
        BezierDraw(array)


#改变控制点时的鼠标单击事件
def xFunc2(event):
    m = round(((event.x-75)/4.65), 2)
    n = round(((534-event.y)/4.62), 2)
    m = limit_point(m)
    n = limit_point(n)
    print(f"x={m}y={n}")
    pd = np.empty((0, 2))
    rd = 0
    wd = 0
    for td in l:
        pd = np.vstack((pd, td))
    print(pd)
    #如果鼠标点击点在控制点上，则进行拖动修改
    for kd in pd:
        if(m <= kd[0] + 1 and m >= kd[0] - 1):
            if(n <= kd[1] + 1 and n >= kd[1] - 1):
                i = 0
                for n in l:
                    h = list(np.where(n == kd))[0]
                    if h != []:
                        rd = i
                        wd = h[0]
                        print(h[0])
                        print(i)
                    i = i + 1
                root.bind("<B1-Motion>", handlerAdaptor(xFunc3, pl=rd, po=wd))
                root.bind("<ButtonRelease-1>", xFunc4)
                updateDraw()


#改变控制点时的鼠标拖动事件
def xFunc3(event, pl, po):
    m = round(((event.x-75)/4.65), 2)
    n = round(((534-event.y)/4.62), 2)
    m = limit_point(m)
    n = limit_point(n)
    print(f"x={m}y={n}")
    (l[pl])[po, 0] = m
    (l[pl])[po, 1] = n
    print((l[pl])[po, 0])
    line1 = A.scatter((l[pl])[:, 0], (l[pl])[:, 1], marker = '.', color='r', 
            linewidth=2)
    line2 = A.plot((l[pl])[:, 0], (l[pl])[:, 1], color='k',
            linewidth=0.5)
    updateDraw()
    line1.remove()
    line2.pop(0).remove()
    

#改变控制点时的鼠标松开事件
def xFunc4(event):
    A.cla()
    A.axis((0, 100, 0, 100))
    if yn == 0:
        i = 0
        for po in l:
            Draw_point((l[i]))
            Draw_line((l[i]))
            BezierDraw(l[i])
            i = i + 1
    else:
        Bezier_spliced()
    root.unbind("<B1-Motion>")
    updateDraw()


#鼠标右键结束事件
def xFunc5(event):
    top_text.destroy()
    root.unbind("<ButtonPress-1>")
    root.unbind("<B1-Motion>")
    root.unbind("<ButtonRelease-1>")
    root.unbind("<ButtonPress-3>")
    

#事件处理函数适配器
def handlerAdaptor(fun, **kwds):
	return lambda event,fun=fun,kwds=kwds: fun(event, **kwds)


#Button绘制贝塞尔曲线
def callback():
    global xls_text
    global top
    print("我被调用了！")
    top = tkinter.Toplevel()
    top.title('贝塞尔曲线')
    top.geometry("300x150+600+300")
    top.wm_attributes('-topmost',1)
    
    l1 = tkinter.Label(top, text="请输入贝塞尔曲线的阶数")
    l1.place(x = 75, y = 35)
    xls_text = tkinter.StringVar()
    xls = tkinter.Entry(top, textvariable = xls_text)
    xls_text.set(" ")
    xls.place(x = 75, y = 60)
    tkinter.Button(top,text = '   确定   ', cursor = 'hand2', 
            command = confirm).place(x = 120, y = 90)
            

#Button改变控制点
def callback1():
    global top_text
    print("我被调用了！")
    if len(l) > 0:
        root.bind("<ButtonPress-1>", xFunc2)
        root.bind("<ButtonPress-3>", xFunc5)
        top_text = tkinter.Label(root, text="当前处于修改模式，退出请按鼠标右键")
        top_text.place(x = 200, y = 50)


#Button拼接贝塞尔曲线回调函数
def callback2():
    global yn
    yn = 1
    print("我被调用了！")
    if len(l) >= 2:
        Bezier_spliced()
        updateDraw()
    

#Button清空坐标系
def callback3():
    global h
    global l
    global yn
    print("我被调用了！")
    yn = 0
    l = list()
    A.cla()
    h = 0
    A.axis((0, 100, 0, 100))
    updateDraw()


#Button结束绘图
def callback4():
    root.destroy()


def limit_point(x):
    if x > 100:
        x = 100
    if x < 0:
        x = 0
    return x


#Bernstein基函数
def Bernstein(i, n, t):
    J = np.math.factorial(n) * t**i * (1 - t)**(n - i) /(np.math.factorial(i) *
        np.math.factorial(n - i))
    return J


#贝塞尔曲线
def Bezier(a, t):
    i = 0
    P = 0
    l = len(a)
    while i <= l - 1:
        P = P + a[i] * Bernstein(i, l - 1, t)
        i = i + 1
    return P


#拼接贝塞尔曲线
def Bezier_spliced():
    A.cla()
    A.axis((0, 100, 0, 100))
    I = l[:]
    i1 = 0
    while i1 < len(I) - 1:
        mi = ((I[i1+1])[0] + (I[i1])[-1]) / 2
        I[i1+1] = np.insert(I[i1+1], 0, values=mi, axis=0)
        I[i1] = np.vstack((I[i1],mi))
        i1 = i1 + 1
    for i2 in I:
        Draw_point(i2)
        Draw_line(i2)
        BezierDraw(i2)


#调用绘制
def confirm():
    global c
    print ('确定')
    c = int(xls_text.get())
    root.bind("<ButtonRelease-1>", xFunc1)
    top.destroy()


#绘制贝塞尔曲线
def BezierDraw(a):
    global array
    T = 0
    z = np.empty((0, 2))
    while T <= 1:
        z = np.vstack((z, (Bezier(a, T))))
        T = T + 0.001
    # 在前面得到的子图上绘图
    x = z[:, 0]
    y = z[:, 1]
    A.plot(x, y)
    updateDraw()
    array = np.empty((0, 2))


#绘制散点
def Draw_point(x):
    A.scatter(x[:, 0], x[:, 1], marker = '.', color='r', linewidth=2)
    

#绘制直线
def Draw_line(x):
    A.plot(x[:, 0], x[:, 1], color='k',linewidth=0.5)


#更新图像
def updateDraw():
    canvas.draw()  
    canvas.get_tk_widget().place(x=20, y=80)


root = tkinter.Tk()  # 创建tkinter的主窗口
root.title("贝塞尔曲线")
root.geometry("1000x750+250+20")

array = np.empty((0, 2))    #当前贝塞尔曲线控制点二维矩阵
global c    #当前贝塞尔曲线的阶数
c = 0
global h    #当前坐标系上点的个数
h = 0
global l    #所有贝塞尔曲线控制点列表
l = list()
global yn    #是否调用过拼接函数
yn = 0

f = Figure(figsize=(5, 5), dpi=120)
global A
A = f.add_subplot(111)  # 添加子图:1行1列第1个
A.axis((0, 100, 0, 100))
tkinter.Button(root,text = '\n\t   绘制贝塞尔曲线   \t\t\n', cursor = 'hand2',
        command = callback).place(x = 700, y = 150)
tkinter.Button(root,text = '\n\t     改变控制点   \t\t\n', cursor = 'hand2',
        command = callback1).place(x = 700, y = 250)
tkinter.Button(root,text = '\n\t  拼接贝塞尔曲线        \t\n', cursor = 'hand2',
        command = callback2).place(x = 700, y = 350)
tkinter.Button(root,text = '\n\t     清空坐标系   \t\t\n', cursor = 'hand2',
        command = callback3).place(x = 700, y = 450)
tkinter.Button(root,text = '\n\t     结束绘图    \t\t\n', cursor = 'hand2',
        command = callback4).place(x = 700, y = 550)

# 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
global canvas
canvas = FigureCanvasTkAgg(f, master=root)
updateDraw()
# matplotlib的导航工具栏显示上来
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.place(x=20, y=80)

root.mainloop()




