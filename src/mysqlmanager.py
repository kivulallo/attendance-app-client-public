import mysql.connector
import printlog as pr

'''
Student attendance logging in MySQL database.
'''

class mysqlManager:
    def __init__(self,host,port,username,password,db,firebasemanager):
        pr.pl("MySQL connecting")
        self.client = mysql.connector.connect(host=host,port=port,user=username,passwd=password,database=db)
        pr.pl("MySQL connected")
        self.fbm = firebasemanager

    def setAttended(self,id:int,attended:bool):
        cursor = self.client.cursor()
        lessonnow = self.getCurrentLessonForStudent(id)
        if lessonnow[-1] == 0 and attended is True:
            sql = "update `attended` set `attended` = %s where `studentid` = "+str(id)+" and `lessonid` = "+str(lessonnow[0])
            val = (1,)
            cursor.execute(sql,val)
            self.client.commit()
            self.fbm.triggerUpdateAsync()

    def getPastUnattendedForStudent(self,id:int):
        cursor = self.client.cursor()
        retval = []
        sql = "select * from `lessons` inner join `attended` on `lessons`.`id` = `attended`.`lessonid` where `fromDate` < DATE(NOW()) and `attended`.`attended` = 0 and `attended`.`studentid` = "+str(id)
        cursor.execute(sql)
        result = cursor.fetchall()
        for lesson in result:
            retval.append(lesson)
        print(str(retval))
        cursor.close()
        return retval

    def getCurrentLessonForStudent(self,studentid:int):
        cursor = self.client.cursor()
        sql = "select * from `lessons` inner join `attended` on `lessons`.`id` = `attended`.`lessonid` where `fromDate` <= DATE(NOW()) and `fromTime` <= TIME(NOW()) and `toDate` >= DATE(NOW()) and `toTime` >= TIME(NOW()) and `attended`.`studentid` = "+str(studentid)
        cursor.execute(sql)
        result = cursor.fetchmany()

        return result[0]
