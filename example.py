import time
import download_async

if __name__ == "__main__":

    def post_up(dl):
        print dl, "DONE"

    url = "http://soundcloud.com/hoodinternet/the-hood-internet-gangz-a-make/download"
    download = download_async.Download(url, post_up, target_filename="hot-ish.mp3")
    while not download.finished:
        print download
        time.sleep(1)
