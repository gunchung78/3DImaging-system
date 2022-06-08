import cv2
import numpy as np
import FPeplography_optim
import photon

cap = cv2.VideoCapture(0)
key_val = 0


if cap.isOpened() == False:
    print("Unable to read camera")

else: 
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('data/videos/output.avi',
                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                        10,
                        (frame_width, frame_height) )                      
    while True:
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)
            if cv2.waitKey(1) == 113 or key_val == 113:
                frame = frame
                if key_val != 113:
                    key_val = 113
                    print("original")
            if cv2.waitKey(1) == 97 or key_val == 97:
                frame = FPeplography_optim.FPE(frame)
                if key_val != 97:
                    key_val = 97
                    print("fpe")
            if cv2.waitKey(1) == 98 or key_val == 98:
                frame = photon.photon(frame)
                if key_val != 98:
                    key_val = 98
                    print("photon")
            cv2.imshow('frame out', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break       
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()