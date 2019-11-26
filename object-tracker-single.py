# Import the required modules
import dlib
import cv2
import argparse as ap
import get_points
# import cv2
print(cv2.__version__)
# x markz Box 
# y vstsh 
# width box 
# hight box

def run(source=0, dispLoc=False):


    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)
    # success,image = cam.read()
    cam.set(3,640)
    cam.set(4,480)
    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()
    
    print("Press key `p` to pause the video to start tracking")
    while True:
        # Retrieve an image and Display it.
        retval, img = cam.read()
        if not retval:
            print("Cannot capture frame device")
            exit()
        if(cv2.waitKey(10)==ord('p')):
            break
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
    cv2.destroyWindow("Image")

    # Co-ordinates of objects to be tracked 
    # will be stored in a list named `points`
    points = get_points.run(img) 

    if not points:
        print("ERROR: No object to be tracked.")
        exit()
    
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)

    # Initial co-ordinates of the object to be tracked 
    # Create the tracker object
    tracker = dlib.correlation_tracker()
    # Provide the tracker the initial position of the object
    tracker.start_track(img, dlib.rectangle(*points[0]))

    count = 0

    while True:
        # Read frame from device or file
        retval, img = cam.read()
        if not retval:
            print("Cannot capture frame device | CODE TERMINATING :(")
            exit()
        # Update the tracker  
        tracker.update(img)
        # Get the position of the object, draw a 
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        # pt1new = (int(pt1[0]) + int(pt1[1]))/2
        # pt2new = (int(pt2[0]) + int(pt2[1]))/2
        # new1 = pt1new
        # new2 = pt2new + 20
        # pttupleleel = (int(new1),int(new2))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)

        crop = img[pt1[1]:pt2[1],pt1[0]:pt2[0]]
        height, width, channels = crop.shape 
        print(height/2, width/2)
        # cv2.circle(img, (int(height/2),  int(width/2)),50, (255, 255, 255), 3)

        # todo txt file 
        cv2.imwrite("extracted/frame%d.jpg" % count, crop)     # save frame as JPEG file
        count += 1

        cv2.imshow("croped", crop)
        
        # cv2.circle(img, (pttupleleel), 100, (255,255,255), 3)
        # print("Object tracked at [{}, {}] \r".format(pt1, pt2)),
        if dispLoc:
            loc = (int(rect.left()), int(rect.top()-20))
            txt = "Object tracked at [{}, {}]".format(pt1, pt2)
            cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)

        
     

        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        # Continue until the user presses ESC key
    
        if cv2.waitKey(1) == 27:
                break
    # Relase the VideoCapture object
    cam.release()

if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])
    run(source, args["dispLoc"])
