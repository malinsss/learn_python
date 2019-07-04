"""
This program is for generating wafer map with .csv file input

4: try to just more pin value with Low_limit < pin < up_limit
5 : try to use sub plot
"""
PATH="SWSST012-A21079#25_low_temp.csv"
import numpy as np
#import numpy
#from matplotlib import *
from pylab import *
    
def generate_wafer_map(path,axis=None,status ="untest",x_col = 0,y_col =0,sysdut_col = 0 ,title="",
                       pin_col= [],background_RGB=(255,255,255),map_RGB = (255,255,0),pass_RGB=(0,255,0),fail_RGB=(255,0,0),low_limit = 0,up_limit=0):
     




        csv_data_str = np.loadtxt(open(path,"rb"),delimiter=",",skiprows=1, dtype="str")
       

        # x axis for array col, y axis value for array row
        row_of_wafer=max(np.array(csv_data_str[:,y_col], np.int32))
        col_of_wafer=max(np.array(csv_data_str[:,x_col], np.int32))
        #  at least +1 , +2 for beauty
        row = row_of_wafer +2
        col = col_of_wafer + 2
        img =np.array(np.zeros(row*col*3).reshape((row, col,3)),np.int32)
        # set background color
        for r in range(row):
            for c in range(col):
                img[r,c] = background_RGB
        #img.fill(255)
         # every rows represent a dut, array loop according to rows
         
        text =[]
        
        for dut in csv_data_str:
                img[int(dut[y_col]), int(dut[x_col])]= map_RGB
                #save sysdut and its pos
                text.append([int(dut[x_col]), int(dut[y_col]),dut[sysdut_col]])
        if status == "tested":
            for dut in csv_data_str:
                #first set to pass 
                img[int(dut[y_col]), int(dut[x_col])]= pass_RGB
                
                #mark fail
                for c in pin_col:
                    #if pass , go on to test , if fail , not , with a.any() to judge np.array
                    if (img[int(dut[y_col]), int(dut[x_col])]== pass_RGB).any():
                        if low_limit<= float(dut[c])<= up_limit:
                           pass 
                        else:
                            img[int(dut[y_col]), int(dut[x_col])]= fail_RGB
                    else:
                        pass
        else:
            pass
        
        ax.invert_yaxis()                                 
        ax.set_title(title)
        #ax.set_xticks(range(col)) #设置刻度值 list为[] 表示没有
        ax.set_xticks([])
        ax.set_yticks([])
        #ax.set_xticklabels(range(col))
        #ax.set_xticklabels([])
        #ax.set_yticklabels([]) #设置显示的刻度值                                
                                
        ax.yaxis.set_ticks_position('left') 
        ax.xaxis.set_ticks_position('top')
                               
        #ax.yaxis.set_label_text("Y")
                                #ax.xaxis.set_label_text("X")
        ax.yaxis.set_label_position("left")
        ax.xaxis.set_label_position("top")
         #设置显示的Dut number 和 属性 position fontsize alignment .l.. 
       # for t in Text:
       #     #ax.text(int(t[0]), int(t[1]),t[2],fontsize=8,verticalalignment='center', horizontalalignment='center')
       #     ax.text(t[0], t[1],t[2],fontsize=8,verticalalignment='center', horizontalalignment='center')
        
   
        for t in text:
            ax.text(t[0], t[1],t[2],fontsize=8,verticalalignment='center', horizontalalignment='center')
        
           
        ax.imshow(img)
        return 0
       
# 画图过程 类似于 matlab, 创建figure, axis, 在坐标系中画图
plt.figure()
plt.subplot(221) # such as in matlab
ax= plt.gca()
generate_wafer_map(path="SWSST012-A21079#25_low_temp.csv",axis = ax,x_col = 4,y_col=5,sysdut_col = 3,
                   pin_col = [6,7,8],background_RGB=(155,155,155),status = "tested",low_limit=180,up_limit=220,title = "813 DUT")

plt.subplot(222) # such as in matlab
ax= plt.gca()
wafermap2 = generate_wafer_map(path="SWST20--high-temp-silicon-A20998-06-.csv",axis = ax,sysdut_col = 3,x_col = 4,y_col=5,pin_col = [6,7,8],status = "untest",low_limit=180,up_limit=200)

#最后一起show()
show()

