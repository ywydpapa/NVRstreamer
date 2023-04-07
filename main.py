from threading import Thread
from time import sleep
import signal

import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstRtsp", "1.0")
gi.require_version("GstRtspServer", "1.0")
from gi.repository import GLib, GObject, Gst, GstRtsp, GstRtspServer

PIPELINE = (
    "( rtspsrc location=rtsp://coredjk:core2020@192.168.108.133:554/Streaming/Channels/202 latency=0 ! rtph264depay ! h264parse ! rtph264pay name=pay0 pt=96)")


def main():
#    GObject.threads_init()
    Gst.init(None)

    server = GstRtspServer.RTSPServer.new()
    server.props.service = "3000"

    server.attach(None)

    loop = GLib.MainLoop.new(None, False)

    def on_sigint(_sig, _frame):
        print("Got a SIGINT, closing...")
        loop.quit()
    signal.signal(signal.SIGINT, on_sigint)

    def run_main_loop():
        loop.run()

    main_loop_thread = Thread(target=run_main_loop)

    main_loop_thread.start()

    media_factory = GstRtspServer.RTSPMediaFactory.new()
    media_factory.set_launch(PIPELINE)
    media_factory.set_shared(True)
    server.get_mount_points().add_factory("/test", media_factory)
    print("Stream ready at rtsp://127.0.0.1:3000/test")


    while loop.is_running():
        sleep(0.1)


if __name__ == "__main__":
    main()