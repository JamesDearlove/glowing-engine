import glowbit

LENGTH = 24
stick = glowbit.stick(brightness=16, rateLimitFPS=15, numLEDs=LENGTH)

def demo():
    stick.demo()


def pulse(colors: list[int], reverse: bool):
    num_colors = len(colors)
    speed = -100 if reverse else 100
    index = LENGTH if reverse else 0

    frame = 0
    stick.addPulse(colour=colors, index=index, speed=speed)
    while frame < LENGTH + num_colors:
        stick.pixelsFill(stick.black())
        stick.updatePulses()
        stick.pixelsShow()

        frame = frame + 1

def chaos():
    stick.chaos()

def fill(color):
    stick.pixelsFill(stick.white())
    stick.pixelsShow()
