
from google.oauth2 import service_account
from google.cloud import firestore
import firebase_admin
from firebase_admin import db
import time
import threading
import printlog as pr

'''
Getting student names to display next to faces. This data is coming from firebase.
'''
class firebasemanager:
    JSONPATH = "path/to/firebasekey.json"
    cred = service_account.Credentials.from_service_account_file(JSONPATH)
    lastid = -1
    lastFullname = ""
    def __init__(self):
        pr.pl("Firestore connecting")
        self.db = firestore.Client("projectname",self.cred)
        self.fb = firebase_admin.initialize_app(firebase_admin.credentials.Certificate(self.JSONPATH),options={'databaseURL': 'firestoredb.url'})
        pr.pl("Firestore connected")

    def getNameForUserId(self, id):
        if not self.lastid == id:
            students = self.db.collection(u'students')
            student = students.document(str(id)).get().to_dict()
            if student is not None:
                self.lastFullname = student['firstName'] + " " +student['lastName']
                self.lastid = id
            return self.lastFullname
        return self.lastFullname

    def lastTimeout(self):
        while True:
            time.sleep(10)
            self.lastid = -1

    def updatefirebase(self):
        ref = db.reference("/Update",self.fb)
        ref.set(True)
        time.sleep(1)
        ref.set(False)

    def triggerUpdateAsync(self):
        t = threading.Thread(target=self.updatefirebase())
        t.setDaemon(True)
        t.start()
if __name__ == "__main__":
    f = firebasemanager()
