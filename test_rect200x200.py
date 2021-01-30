import numpy as np
import cv2
import matplotlib.pyplot as plt

def customGreen(contour):
    r=np.power(max(np.power(contour[:,0],2)+np.power(contour[:,1],2)),0.5)/2

    beta=np.arctan(contour[:,1]/contour[:,0])
    # print("temp",((np.power(contour[:,0],2)+np.power(contour[:,1],2))/(2*r*r)))
    gamma=np.arccos(1-((np.power(contour[:,0],2)+np.power(contour[:,1],2))/(2*r*r)))
    alpha=beta-((np.array([np.pi]*len(beta))-gamma)/2)
    a=r*np.cos(alpha)
    b=r*np.sin(alpha)
    c=contour[:,0]-a
    d=contour[:,1]-b

    print("r",r)
    # print("beta",len(beta),beta)
    # print("gamma",len(gamma),gamma)
    # print("alpha",len(alpha),alpha)
    # print("a",len(a),a)
    # print("b",len(b),b)
    # print("c",len(c),c)
    # print("d",len(d),d)
    # print("x",contour[:,0])
    # print("y",contour[:,1])

    delta=np.diff(contour,axis=0)
    # print("delta",delta)
    all_ans=list(-d[:-1]*delta[:,0]+c[:-1]*delta[:,1])+[-d[-1]*(contour[0][0]-contour[-1][0])+c[-1]*(contour[0][1]-contour[-1][1])]
    
    return all_ans,a,b


im=cv2.rectangle(np.ones((600,600,3),np.uint8),(300,300),(500,500),(255,0,0),2)

imgray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# imgray=im[:,:,2]
ret, thresh = cv2.threshold(imgray,10,255,1)
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
# plt.scatter([i[0] for i in contour],[i[1] for i in contour])
# plt.scatter(contour[:,0],contour[:,1])
# plt.show()

# contour[:,0]-=200
# contour[:,1]+=100

all_ans,a,b=customGreen(contour)
all_ans=np.array([i for i in all_ans if not np.isnan(i)])

# plt.quiver(a,b,contour[:,0],contour[:,1],units='xy',scale=21)
# ax.set_aspect('equal')
# plt.xlim(-20,90)
# plt.ylim(-20,90)
plt.imshow(im)
plt.plot(contour[:,0],contour[:,1],'ro',markersize=1)
rand_idx=np.random.random_integers(0,len(a)-1,10)
for i in rand_idx:
    plt.plot([a[i],contour[i][0]],[b[i],contour[i][1]],'b-')
    plt.plot([0,a[i]],[0,b[i]],'g-')
# plt.axis('equal')
plt.xlim(0,800)
plt.ylim(600,-300)
plt.title("Plot Rectangle 200*200 pixels")
plt.text(50,-250,"Custom Green's Theorem {}".format(np.abs(np.round(area_calc,3))))
sum_area=cv2.contourArea(am_contours[all_of_area.index(temp_all_of_area[-2])][0])
sum_area+=cv2.contourArea(am_contours[all_of_area.index(temp_all_of_area[-1])][0])
plt.text(50,-200,"Built In CV2 {}".format(np.abs(np.round(sum_area/2,3))))
plt.text(50,-150,"Truly Drawing {}".format(200*200))
plt.show()
print("Area From Custom Green's Theorem",sum(all_ans))
for c in contours:
    print("Area From built in is",cv2.contourArea(c))