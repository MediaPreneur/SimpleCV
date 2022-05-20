from SimpleCV import *

def movement_check(x = 0,y = 0,t=1):
    direction = ""
    directionX = ""
    directionY = ""
    if x > t:
        directionX = "Right"
    if x < -1*t:
        directionX = "Left"
    if y < -1*t:
        directionY = "Up"
    if y > t:
        directionY = "Down"

    direction = f"{directionX} {directionY}"
    return direction if direction is not "" else "No Motion"

def main():
    scale_amount = (200,150)
    d = Display(scale_amount)
    cam = Camera(0)
    prev = cam.getImage().scale(scale_amount[0],scale_amount[1])
    time.sleep(0.5)
    t = 0.5
    buffer = 20
    count = 0
    while d.isNotDone():
        current = cam.getImage()
        current = current.scale(scale_amount[0],scale_amount[1])
        if ( count < buffer ):
            count = count + 1
        elif fs := current.findMotion(prev, window=15, method="BM"):
            dx = 0
            dy = 0
            for f in fs:
                dx = dx + f.dx
                dy = dy + f.dy

            lengthOfFs = len(fs)
            dx = (dx / lengthOfFs)
            dy = (dy / lengthOfFs)
            motionStr = movement_check(dx,dy,t)
            current.drawText(motionStr,10,10)

        prev = current
        time.sleep(0.01)
        current.save(d)

if __name__ == '__main__':
    main()
