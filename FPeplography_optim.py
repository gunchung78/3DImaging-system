import numpy as np
import cv2
from cv2 import CV_32F
import warnings

def FPE(out, ):
    warnings.filterwarnings(action='ignore')
    # out = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
    [v, h, d] = np.shape(out)
    # print('--- Mask generation stage ---')
    mask = (v + h)*np.ones((v, h))
    mask[0,0] = 2*v*h
    mask[0,1:] = (v*h + v)
    mask[1:,0] = (v*h + h)
    mask1 = mask[0,0]/mask
    # print('--- FFT stage ---')
    fft_out = np.ones([v,h,d],dtype = 'complex_')
    fft_out2 = np.ones([v,h,d])
    fft_out[:,:,0]=np.fft.fft2(out[:,:,0])*mask1
    fft_out[:,:,1]=np.fft.fft2(out[:,:,1])*mask1
    fft_out[:,:,2]=np.fft.fft2(out[:,:,2])*mask1

    # print('--- Restoration stage ---')
    fft_out2[:,:,0]=np.fft.ifft2(fft_out[:,:,0])
    fft_out2[:,:,1]=np.fft.ifft2(fft_out[:,:,1])
    fft_out2[:,:,2]=np.fft.ifft2(fft_out[:,:,2])
    if np.min(fft_out2) < 0:
        fft_out2 = fft_out2 - np.min(fft_out2)

    fft_out2 = (fft_out2/np.max(fft_out2))
    return fft_out2

if __name__ == "__main__":
    img = cv2.imread("F:/_project_/_matlab/_source/fog1.jpg")
    cv2.imshow("original", img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fft_out2 = FPE(img)
    cv2.imshow("fpimg", fft_out2)
    cv2.waitKey()
    cv2.destroyAllWindows()