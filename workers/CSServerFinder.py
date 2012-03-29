import sqlite3, struct, socket, time, json, traceback
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class CSServerFinder(DatagramProtocol):
    def startProtocol(self):
        try:
            self.dbConnection = sqlite3.connect("../db/csdb.sqlite")
            self.dbCursor = self.dbConnection.cursor()
            self.createDatabase()
            self.dstPort = 27015
            self.magicList = [0xff, 0xff, 0xff, 0xff, 0x54, 0x53, 0x6f, 0x75, 0x72, 0x63, 0x65, 0x20, 0x45, 0x6e, 0x67, 0x69, 0x6e, 0x65, 0x20, 0x51, 0x75, 0x65, 0x72, 0x79, 0x00]
            self.magicString = struct.pack("!" + "B"*len(self.magicList), *self.magicList)
#            self.ipRanges = ["10.1.33.255", "10.1.34.255", "10.1.35.255", "10.1.36.255", "10.1.39.255", "10.1.40.255",
#                             "10.1.65.255", "10.1.66.255", "10.1.98.255", "10.2.12.255", "10.2.16.255", "10.2.20.255",
#                             "10.2.24.255", "10.2.28.255", "10.2.32.255", "10.2.36.255", "10.2.4.255" , "10.2.40.244",
#                             "10.2.44.255", "10.2.8.255" , "10.3.3.255" , "10.3.4.255" , "10.4.3.255" , "10.5.2.255" ,
#                             "172.17.16.255"]
            self.ipRanges = ["10.1.34.%s", "10.1.35.%s", "10.1.36.%s", "10.1.39.%s", "10.1.40.%s", "10.1.65.%s", "10.1.66.%s"]
            self.lastSendTime = None
            self.pingerTask = LoopingCall(self.serverPinger)
            self.pingerTask.start(10.0)
        except Exception as e:
            print (e)
            traceback.print_exc()

    def createDatabase (self):
        try:
            self.dbCursor.execute('drop table if exists cs')
            self.dbCursor.execute('''
               create table cs(
                    serverIP text,
                    serverPort text,
                    serverName text,
                    serverMapName text,
                    serverType text,
                    serverGameName text,
                    serverPlayer int,
                    serverPlayerMax int,
                    serverLatency int)''')
            self.dbConnection.commit()
        except Exception as e:
            print(e)
            traceback.print_exc()

    def serverPinger (self):
        try:
            self.dbCursor.execute('delete from cs')
            self.dbConnection.commit()
            self.jsonString = '[{"serverIP":"Server IP", "serverPort":"Port", "serverName":"Server Name", "serverMapName":"Map", "serverType":"Type", "serverGameName":"Game Name", "serverPlayer":"Players", "serverPlayerMax":"Max Players", "serverLatency":"Latency"}]'
            filePointer = open("../JSON/cs.json", 'w')
            filePointer.write(json.dumps(self.jsonString))
            filePointer.close()
            self.lastSendTime = time.time()
            for self.ipAddr in self.ipRanges:
                for i in xrange(2, 254):
                    self.transport.write(self.magicString, (self.ipAddr % i, self.dstPort))
        except Exception as e:
                print(e)
                traceback.print_exc()

    def datagramReceived (self, serverResponse, (host, port)):
        try:
            serverLatency = int((time.time() - self.lastSendTime)*1000)
            serverResponseList = serverResponse.split("\0")
            if len(serverResponseList) < 6 :
                return
            serverIP, serverPort = serverResponseList[0].split("m")[1].split(":")
            serverName = serverResponseList[1]
            serverMapName = serverResponseList[2]
            serverType = serverResponseList[3]
            serverGameName = serverResponseList[4]
            serverPlayer = ord(serverResponseList[5][0])
            serverPlayerMax = ord(serverResponseList[5][1])

#            print ("Server Found" +
#                   "\n\tServer Name : " + serverName +
#                   "\n\tServer IP : " + serverIP + ":" + serverPort +
#                   "\n\tMap Name : " + serverMapName +
#                   "\n\tType : " + serverType +
#                   "\n\tPlayers : " + str(serverPlayer) + "/" + str(serverPlayerMax) +
#                   "\n\tLatency : " + str(serverLatency) + "\n")

            self.dbCursor.execute("insert into cs values (?,?,?,?,?,?,?,?,?)", (serverIP, serverPort, serverName, serverMapName, serverType, serverGameName, serverPlayer, serverPlayerMax, serverLatency))
            self.dbConnection.commit()
            self.dbCursor.execute("select * from cs")
            self.jsonString = [dict((self.dbCursor.description[i][0], value) for i, value in enumerate(row)) for row in self.dbCursor.fetchall()]
            self.jsonString.insert(0, { 'serverIP':u'Server IP' , 'serverPort':u'Port', 'serverName':u'Server Name', 'serverMapName':u'Map', 'serverType':u'Type', 'serverGameName':u'Game Name', 'serverPlayer':u'Players', 'serverPlayerMax':u'Max Players', 'serverLatency':u'Latency'})
            print self.jsonString
            filePointer = open("../JSON/cs.json", 'w')
            filePointer.write(json.dumps(self.jsonString))
            filePointer.close()
        except Exception as e:
            print(e)
            traceback.print_exc()

if __name__ == "__main__":
    reactor.listenUDP(0, CSServerFinder())
    reactor.run()
