import sys, signal, subprocess
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from time import sleep
import datetime

device = None

startTime = None


def checkMissionComplete(device, count, snapshot):
    # print('Count = %d' %count)
    now = datetime.datetime.now()

    targetImage = snapshot.getSubImage((1550, 900, 5, 5))
    baseImage = MonkeyRunner.loadImageFromFile('./sc/target2.png')

    titleImage = MonkeyRunner.loadImageFromFile('./sc/title.png')
    nowTitleImage = snapshot.getSubImage((755, 885, 1, 1))


    # check SOTANG Dialog
    if not titleImage.sameAs(nowTitleImage, 1):
        # Open Sotang Dialg
        device.touch(455, 200, MonkeyDevice.DOWN_AND_UP)
        sleep(3)
        # Click Sotang Left Menu
        device.touch(650, 450, MonkeyDevice.DOWN_AND_UP)

        nowTitleImage.writeToFile('./sc/nowtitle.png', 'png')
        print('Sotang Dialog closed. OPEN!!. ')
        return

    # Check SOTANG Finished
    if not targetImage.sameAs(baseImage, 1):
        print('[%d] OK!! Finished...' % count)
        print now
        device.touch(1550, 900, MonkeyDevice.DOWN_AND_UP)
    else:
        print('[%d] Not finished' % count)
        device.touch(1400, 500, MonkeyDevice.DOWN_AND_UP)

    # Check Auto mode OFF
    if count % 5 == 0:
        proImage = MonkeyRunner.loadImageFromFile('./sc/ingNo.png')
        newProgresssImage = snapshot.getSubImage((1360, 670, 50, 28))

        if newProgresssImage.sameAs(proImage, 1):
            print('Click! Auto mode')
            autoClick(device)

        saveProgress(device)
        print('Save Progress... ')


def autoClick(device):
    # Click X Btn, Close Dialog.
    device.touch(1882, 112, MonkeyDevice.DOWN_AND_UP)
    sleep(2)

    # Click Auto Btn
    device.touch(2025, 577, MonkeyDevice.DOWN_AND_UP)
    sleep(2)

    # Open Sotang Dialg
    device.touch(455, 200, MonkeyDevice.DOWN_AND_UP)
    sleep(2)

    # Click Sotang Left Menu
    device.touch(650, 450, MonkeyDevice.DOWN_AND_UP)


def saveProgress(device):
    snapshot = device.takeSnapshot()
    titleImage = snapshot.getSubImage((1360, 670, 50, 28))
    titleImage.writeToFile('./sc/ingNo.png', 'png')


def saveTitle(device):
    snapshot = device.takeSnapshot()
    titleImage = snapshot.getSubImage((755, 885, 1, 1))
    titleImage.writeToFile('./sc/title.png', 'png')


def writeFullscreen(device):
    snapshot = device.takeSnapshot()
    snapshot.writeToFile('./sc/shot2.png', 'png')


def writeBaseImage(device):
    snapshot = device.takeSnapshot()
    baseImage = snapshot.getSubImage((1550, 900, 5, 5))
    baseImage.writeToFile('./sc/target2.png', 'png')


def exitGracefully(self, signum, frame):
    print "Exiting Gracefully..."
    subprocess.call(['./killmonkey.sh'])
    sys.exit(1)


def StartGame(device):
    print('StartGame')
    print "TERA Classic Launch!..."
    device.touch(142, 1587, MonkeyDevice.DOWN_AND_UP)

    sleep(10)

    cnt=1

    while True:
        snapshot = device.takeSnapshot()
        startgame = snapshot.getSubImage((1778, 967, 3, 3))
        baseStartgame = MonkeyRunner.loadImageFromFile('./sc/startgame.png')
        dialogImage = MonkeyRunner.loadImageFromFile('./sc/otherUser.png')
        nowdialogImage = snapshot.getSubImage((1185, 790, 10, 10))

        # Check Other User
        if dialogImage.sameAs(nowdialogImage, 1):
            device.touch(1185, 790, MonkeyDevice.DOWN_AND_UP)

        if startgame.sameAs(baseStartgame, 1):
            device.touch(1778, 967, MonkeyDevice.DOWN_AND_UP)
            print "Start!! Game..."
            break

        device.touch(1778, 967, MonkeyDevice.DOWN_AND_UP)
        sleep(1)
        device.touch(1260, 767, MonkeyDevice.DOWN_AND_UP)
        sleep(5)
        cnt = cnt + 1
        if cnt > 30:
            break


    # writeFullscreen(device)
    sleep(5)

    device.touch(400, 977, MonkeyDevice.DOWN_AND_UP)
    sleep(1)
    device.touch(400, 977, MonkeyDevice.DOWN_AND_UP)
    sleep(1)
    device.touch(400, 977, MonkeyDevice.DOWN_AND_UP)
    sleep(1)

    # Open Sotang Dialg
    device.touch(455, 200, MonkeyDevice.DOWN_AND_UP)
    sleep(3)

    # Click Sotang Left Menu
    device.touch(650, 450, MonkeyDevice.DOWN_AND_UP)

    # Start Sotang
    device.touch(1550, 900, MonkeyDevice.DOWN_AND_UP)
    sleep(3)

    # Click Auto Btn
    device.touch(2025, 577, MonkeyDevice.DOWN_AND_UP)
    sleep(10)


def execute(device):

    StartGame(device)

    count = 1
    while True:
        snapshot = device.takeSnapshot()

        checkMissionComplete(device, count, snapshot)
        count = count + 1
        sleep(5)

        dialogImage = MonkeyRunner.loadImageFromFile('./sc/otherUser.png')
        nowdialogImage = snapshot.getSubImage((1185, 790, 5, 5))
        # Check Other User
        if dialogImage.sameAs(nowdialogImage, 1):
            print('Other User Login.. Finish')
            device.touch(1185, 790, MonkeyDevice.DOWN_AND_UP)
            sleep(10)
            StartGame(device)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exitGracefully)

    now = datetime.datetime.now()
    startTime = now

    setTime = now.replace(hour=10, minute=00, second=0, microsecond=0)

    while True:
        sleep(1)
        now = datetime.datetime.now()
        # print setTime
        print now

        if now > setTime:
            break

    print('START Monkey!!!')
    print now
    device = MonkeyRunner.waitForConnection()
    print('Device Connected.')


    execute(device)
