import cv2
import time
from FPeplography_optim import FPE
from Night_Vision import photon
import numpy as np

def draw_text(img, text, x, y):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_color=(255, 0, 0)
    text_color_bg=(0, 0, 0)
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    offset = 5
    cv2.rectangle(img, (x - offset, y - offset), (x + text_w + offset, y + text_h + offset), text_color_bg, -1)
    cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
print('fps', fps)

if fps == 0.0:
    fps = 30.0

time_per_frame_video = 1/fps
last_time = time.perf_counter()

flag_FPE = 0
flag_PH = 0
NV_n = input()
NV_np = input()
while True:
    ret,Video_Img = cap.read()
    if ret == False:
        print('웹캠에서 영상을 읽을 수 없습니다.')
        break
    time_per_frame = time.perf_counter() - last_time
    time_sleep_frame = max(0, time_per_frame_video - time_per_frame)
    time.sleep(time_sleep_frame)
    real_fps = 1/(time.perf_counter()-last_time)
    last_time = time.perf_counter()
    x = 30
    y = 50
    text = '%.2f fps' % real_fps
    draw_text(Video_Img, text, x, y)        
    if flag_FPE == 1:
       Video_Img = FPE(Video_Img)
       cv2.imshow("ubuntu",Video_Img)
    if flag_PH == 1:
        Video_Img = cv2.cvtColor(Video_Img, cv2.COLOR_BGR2GRAY)
        Video_Img = photon(Video_Img, int(NV_n), int(NV_np), 0)
        cv2.imshow("ubuntu",Video_Img)
    else:
        cv2.imshow("ubuntu",Video_Img)

    if cv2.waitKey(1)&0xFF == 113:
        flag_FPE = 1 - flag_FPE
        if flag_FPE and flag_PH == 1: flag_PH = 0
        time.sleep(1)

    elif cv2.waitKey(1)&0xFF == 119:
        flag_PH = 1 - flag_PH 
        if flag_FPE and flag_PH == 1: flag_FPE = 0
        time.sleep(1)

    if cv2.waitKey(1)&0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()