# CV2 Threaded Video Capture

Not much to say here, it enables you to read an entire video or a number of frames from a video in an extra thread with some nice syntax.

This project was initially part of my video synopsis project, wich is why the config dict() is required.

### Full video


    from VideoReader import VideoReader
    import os

    fileName = "out.mp4"
    dirName = os.path.join(os.path.dirname(__file__), "generate test footage")

    config = {}
    config["inputPath"] = os.path.join(dirName, fileName)
    config["videoBufferLength"] = 100

    with VideoReader(config) as reader:
        while not reader.videoEnded():
            framenumber, frame = reader.pop()
            print(framenumber)


### Selection of Frames


    from VideoReader import VideoReader
    import os

    fileName = "out.mp4"
    dirName = os.path.join(os.path.dirname(__file__), "generate test footage")

    config = {}
    config["inputPath"] = os.path.join(dirName, fileName)
    config["videoBufferLength"] = 100

    frameList = list(range(100, 500))

    with VideoReader(config, frameList) as reader:
        while not reader.videoEnded():
            framenumber, frame = reader.pop()
            print(framenumber)

