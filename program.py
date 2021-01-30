import numpy as np
import cv2
import matplotlib.pyplot as plt
import random

def customGreen(contour):
    r=np.power(max(np.power(contour[:,0],2)+np.power(contour[:,1],2)),0.5)/2

    beta=np.arctan(contour[:,1]/contour[:,0])
    gamma=np.arccos(1-((np.power(contour[:,0],2)+np.power(contour[:,1],2))/(2*r*r)))
    alpha=beta-((np.array([np.pi]*len(beta))-gamma)/2)
    a=r*np.cos(alpha)
    b=r*np.sin(alpha)
    c=contour[:,0]-a
    d=contour[:,1]-b

    print("r",r)

    delta=np.diff(contour,axis=0)
    all_ans=list(-d[:-1]*delta[:,0]+c[:-1]*delta[:,1])+[-d[-1]*(contour[0][0]-contour[-1][0])+c[-1]*(contour[0][1]-contour[-1][1])]
    
    return all_ans,a,b

im = cv2.imread("bkk.png")
imgray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray,100,255,1)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

am_contours=[[i] for i in contours]

all_of_area=[]
temp_all_of_area=[]
for contours in am_contours:
    contour=contours[0]
    contour=np.array([i[0] for i in contour])
    all_ans,a,b=customGreen(contour)
    all_ans=np.array([i for i in all_ans if not np.isnan(i)])
    all_of_area.append(abs(sum(all_ans)))
    temp_all_of_area.append(abs(sum(all_ans)))
sorted(temp_all_of_area)
print(temp_all_of_area)

area_calc=(temp_all_of_area[-1]+temp_all_of_area[-2])/2

contours=am_contours[all_of_area.index(temp_all_of_area[-2])]
contour=contours[0]
contour=np.array([i[0] for i in contour])

all_ans,a,b=customGreen(contour)
all_ans=np.array([i for i in all_ans if not np.isnan(i)])

plt.imshow(im)
plt.plot(contour[:,0],contour[:,1],'yo',markersize=1)
rand_idx=np.random.random_integers(0,len(a)-1,10)
for i in rand_idx:
    plt.plot([a[i],contour[i][0]],[b[i],contour[i][1]],'b-')
    plt.plot([0,a[i]],[0,b[i]],'g-')
plt.title("Plot Bangkok")
plt.text(1500,-500,"Custom Green's Theorem {}".format(np.abs(np.round(area_calc,3))))
sum_area=cv2.contourArea(am_contours[all_of_area.index(temp_all_of_area[-2])][0])
sum_area+=cv2.contourArea(am_contours[all_of_area.index(temp_all_of_area[-1])][0])
plt.text(1500,-400,"Built In CV2 {}".format(np.abs(np.round(sum_area/2))))
plt.show()
print("Area From Custom Green's Theorem",sum(all_ans))
for c in contours:
    print("Area From built in is",cv2.contourArea(c))