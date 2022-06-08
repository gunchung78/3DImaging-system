import numpy as np
import cv2

def photon(img):
    out = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX) 
    [v, h, d] = np.shape(out)
    num_p = 100000
    n = 10
    out2 = np.ones([v,h,d])
    ck = np.ones([v,h,d])
    MLE = np.ones([v,h,d])
    temp = 0
    out2[:,:,0]=out[:,:,0]/np.sum(np.sum(out[:,:,0]))
    out2[:,:,1]=out[:,:,1]/np.sum(np.sum(out[:,:,1]))
    out2[:,:,2]=out[:,:,2]/np.sum(np.sum(out[:,:,2]))
    out2 = num_p*out2
    for x in range(n):
        print(x)
        ck[:,:,0] = np.random.poisson(out2[:,:,0])
        ck[:,:,1] = np.random.poisson(out2[:,:,1]) 
        ck[:,:,2] = np.random.poisson(out2[:,:,2]) 
        temp = temp + ck
    MLE = temp/(n*num_p) 
    MLE = MLE/np.max(MLE)
    return MLE

if __name__ == "__main__":
    img = cv2.imread("F:/_project_/_matlab/_source/out6.jpg")
    cv2.imshow("original", img)
    out2 = photon(img)
    cv2.imshow("photon", out2)
    cv2.waitKey()
    cv2.destroyAllWindows()