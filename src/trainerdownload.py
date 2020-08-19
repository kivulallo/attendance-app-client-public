import urllib.request
import printlog as pr

class Downloader:
    downloaded = 0
    downloadFinished = False
    downloadStarted = False
    def downloadfile(self,path, filename, url):
        pr.pl("Downloading file "+ str(url))
        file = path + "/" + filename
        self.downloadStarted = True
        self.downloadFinished = False
        urllib.request.urlretrieve(url,file,self.show_prorgress)
        self.downloadFinished = True
        pr.pl("Completed download")
        self.downloaded = 0

    def show_prorgress(self, count,block_size,total_size):
        self.downloaded += block_size
        print(str(round(self.downloaded / total_size * 100)) + "%")

