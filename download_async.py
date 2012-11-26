import threading
import os
import requests
import urlparse


class Download(object):
    def __init__(self, url, finished_callback, target_directory=".", target_filename=None):
        self._stop_download = False
        self.finished = False
        self.total_size = 0
        self.bytes_read = 0
        self.url = url
        self.finished_callback = finished_callback
        filename = target_filename or urlparse.urlparse(url).path.split("/")[-1]
        self.filepath = os.path.abspath(os.path.join(target_directory, filename))
        # Run the download in a separate thread
        self.dl_thread = threading.Thread(target=self.download_file, args=(url, self.filepath))
        self.dl_thread.start()
        
    def download_file(self, file_url, filename):
        self.bytes_read = 0
        # One minute timeout for the response
        response = requests.get(file_url, timeout=60, prefetch=False)
        self.total_size = response.headers["content-length"]
        handle = response.raw
        with open(filename, "wb") as local_file:
            while handle and not self._stop_download:
                # Download in chunks and update the download count
                data = handle.read(10 * 1024)
                if data == "":
                    break
                self.bytes_read += len(data)
                local_file.write(data)
        self.finished = True
        self.finished_callback(self)

    def stop(self):
        self._stop_download = True

    def __repr__(self):
        return "%s => %s (%s of %s bytes downloaded)" % (self.url, self.filepath, self.bytes_read, self.total_size)

    def __str__(self):
        return self.__repr__()
