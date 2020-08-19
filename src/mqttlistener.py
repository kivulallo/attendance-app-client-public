import paho.mqtt.client as mqtt
from trainerdownload import Downloader
import ssl
import printlog as pr

class Listener:

    client = mqtt.Client()
    run = True
    downloader = Downloader()
    context = ssl.create_default_context()
    subed = False

    def on_connect(self, client,userdata,flags,rc):
        pr.pl("MQTT Connected. Code: "+str(rc))
        pr.pl("MQTT Subscribing")
        self.client.subscribe("cv/training")
        pr.pl("MQTT Subscribed")

    def on_message(self,client,userdata,msg):
        pr.pl("MQTT Received message: "+str(msg.topic)+" "+str(msg.payload))
        if not self.downloader.downloadStarted:
            self.downloader.downloadfile("../trainer","trainer.yml","url.to.trainer.file.generated.by.server")

    def on_subscribe(self):
        pr.pl("Successful subscribe")

    def __init__(self):
        pr.pl("MQTT Listener init")
        self.client = mqtt.Client()
        self.client.username_pw_set("username","password")
        self.client.tls_set_context(self.context)
        self.client.on_subscribe = self.on_subscribe
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


    def start(self):
        pr.pl("MQTT Connecting to MQTT server")
        self.client.connect("MQTT server host", 8883)
        self.client.loop_start()

    def stop(self):
        pr.pl("Stopping MQTT")
        self.client.loop_stop()

if __name__ == "__main__":
    listener = Listener()
    listener.start()
