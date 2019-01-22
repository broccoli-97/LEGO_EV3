# a=[]
# b=[]
# with open('test.txt','r') as f:
#     data1=f.readline()
#     dis=line.split()
#     dis_float=map(float,dis)
#     a.append(dis_float)
#     data2=f.readline()
#     dis=line.split()
#     dis_float=map(float,dis)
#     b.append(dis_float)
import numpy 
import matplotlib.pyplot as plt
a=numpy.loadtxt('testt.txt')
#print(a[1])
#用于中文和负号的正常显示
plt.rcParams['font.sans-serif']='Microsoft YaHei'
plt.rcParams['axes.unicode_minus']=False

plt.style.use('ggplot')
N=len(a[0])
a[1]=a[1][::-1]
angles=numpy.linspace(0,2*numpy.pi,N,endpoint=False)
values1=numpy.concatenate((a[0],[a[0][0]]))
values2=numpy.concatenate((a[1],[a[1][0]]))

angles=numpy.concatenate((angles,[angles[0]]))
#绘图
fig=plt.figure()
ax=fig.add_subplot(111,polar=True)
#绘制折线图
ax.plot(angles,values1,'o-',linewidth=2)
#填充颜色
ax.fill(angles,values1,alpha=0.25)

#绘制第二条折线图
ax.plot(angles, values2, 'o-', linewidth=2)
ax.fill(angles, values2, alpha=0.25)

#ax.set_thetagrids(angles*180/numpy.pi)

ax.grid(True)
plt.show()

