import numpy as np
import cv2

def photon(out,n,num_p,color):
    if color == 0:
        [v, h] = np.shape(out)
        out2 = np.ones([v,h])
        ck = np.ones([v,h])
        MLE = np.ones([v,h])
        temp = 0
        out2=out/np.sum(np.sum(out))
        out2 = num_p*out2
        for x in range(n):
            ck = np.random.poisson(out2) 
            temp = temp + ck
        MLE = temp/(n*num_p) 
        MLE = MLE/np.max(MLE)    
    else:
        [v, h, d] = np.shape(out)
        out2 = np.ones([v,h,d])
        ck = np.ones([v,h,d])
        MLE = np.ones([v,h,d])
        temp = 0
        out2[:,:,0]=out[:,:,0]/np.sum(np.sum(out[:,:,0]))
        out2[:,:,1]=out[:,:,1]/np.sum(np.sum(out[:,:,1]))
        out2[:,:,2]=out[:,:,2]/np.sum(np.sum(out[:,:,2]))
        out2 = num_p*out2
        for x in range(n):
            ck[:,:,0] = np.random.poisson(out2[:,:,0])
            ck[:,:,1] = np.random.poisson(out2[:,:,1]) 
            ck[:,:,2] = np.random.poisson(out2[:,:,2]) 
            temp = temp + ck
        MLE = temp/(n*num_p) 
        MLE = MLE/np.max(MLE)
    return MLE

if __name__ == "__main__":
    img = cv2.imread("F:/_project_/_matlab/_source/out6.jpg", 0)
    print(img.shape)
    cv2.imshow("original", img)
    out2 = photon(img, 20, 100000, 0)
    cv2.imshow("photon", out2)
    cv2.waitKey()
    cv2.destroyAllWindows()