
''' 
McMaster University | UtraHacks 2018  
    
    [1]      Jarvis Wang         
    [2]      ZAch M.        
    [3]      Raghib Quader       
    [4]      Ben Li
'''


import cv2;         
import argparse;

# Arguments Stuffs .............................................................................................

parser = argparse.ArgumentParser(description = 'python main.py [opaque][1]')
parser.add_argument("bgrnd",help="0 => clear bgrnd | 1=>opaque bgrnd", type=int)     # backcground type 
parser.add_argument("cam",help="0 for webcam | 1 for external cam", type=int)       # webcam to use
args = parser.parse_args()


# Computer Vision .............................................................................................

in_count = 0                                            # count the frame-#

# Loading Haar-Cascades 
play_cascade = cv2.CascadeClassifier('palm_right.xml'); #global referential ==> right-hand
pause_cascade = cv2.CascadeClassifier('hand_fist.xml'); #global referential ==> fist

playing = 0;  # TRACK PLAY/PAUSE Status

# Running the Detection Algorithm
def detect(gray, frame):  

    # configure background
    if(args.bgrnd==1):
        cv2.rectangle(frame, (0, 0), (1000, 1000), (0, 0, 0), 10000); 

    # Detect PLAY Gesture
    global playing;
    text = ""
    if(playing): 
        text = "PLAYING!!"
    else:
        text = "PAUSED!!"
    cv2.putText(frame, text, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 5, cv2.LINE_AA); 

    if not(playing):
        # Detect Face Position
        plays = play_cascade.detectMultiScale(gray, 1.1, 2); 
        for(play_x, play_y, _w, _h) in plays:    
            # draw rect around palm
            cv2.rectangle(frame,(play_x,play_y),(play_x + _w + 25, play_y + _h + 25), (255,105,180), 5); 
            # change PAUSE-state to PLAYING 
            cv2.rectangle(frame, (0, 0), (1000, 1000), (0, 0, 0), 10000); 
            playing = 1

    # Detect PAUSE Gesture
    else:
        pauses = pause_cascade.detectMultiScale(gray, 1.1, 2); 
        for(pause_x, pause_y, _w, _h) in pauses: 
            #draw rect around palm
            cv2.rectangle(frame,(pause_x,pause_y),(pause_x + _w + 25, pause_y + _h + 25), (255,105,180), 5); 
            # change PLAYING-state to PAUSED 
            cv2.rectangle(frame, (0, 0), (1000, 1000), (0, 0, 0), 10000); 
            playing = 0
        
    return frame;


# Implementing Continuous Detection .............................................................................................

video_capture = cv2.VideoCapture(args.cam);    #"0" => object of live webcam video

while True:

    # process (detection) frame 
    _, frame = video_capture.read()   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # cascade operates on grayscale
    canvas = detect(gray,frame) 

    # un-invert camera-feed
    canvas = cv2.flip(canvas, 1)

    # resizing webcam window
    cv2.namedWindow('Press Q to Quit',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Press Q to Quit',800,620)
    cv2.imshow('Press Q to Quit',canvas)
    
    # Program Exit Sequence
    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break

video_capture.release()
cv2.destroyAllWindows()     