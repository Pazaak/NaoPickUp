__author__ = 'maleza'

import spade, almath, solver, sys
from naoqi import ALProxy
from math import atan, pi, sqrt, cos, sin, fabs
from header_classes import Robot, Object

# Posicion del robot relativa al problema
posRelx = 0
posRely = 0
posRelTheta = 0.0

# Suponemos que se sabe donde esta el contenedor
contenedorX = 10
contenedorY = 10

# Suponemos que ya hemos detectado las cajas
cajas = "5 7 5 10 10 5"

# Agente maestro?
iamMaster = True

nombreAgente = "robot1@127.0.0.1"
# Si hubiera mas de un agente esto seria una lista
otroAgente = "robot2@127.0.0.1"

"""
robotIP = "127.0.0.1"
robotPort = 48897
"""
robotIP = "192.168.1.5"
robotPort = 9559


def calculeAngle(souX, souY, tarX, tarY):
    if tarY == souY:
        if tarX-souX < 0:
            return pi+posRelTheta
        return posRelTheta
    if tarX == souX:
        if tarY-souY < 0:
            return -pi/2+posRelTheta
        return pi/2+posRelTheta
    if tarX-souX < 0:
        if tarY-souY < 0:
            return -pi+atan(float(tarY-souY)/(tarX-souX))+posRelTheta
        return pi+atan(float(tarY-souY)/(tarX-souX))+posRelTheta
    return atan(float(tarY-souY)/(tarX-souX))+cos(posRelTheta)*posRelTheta


class AgRobot(spade.Agent.Agent):
    class Reach(spade.Behaviour.Behaviour):
        def _process(self):
            self.msg = None
            self.msg = self._receive(True)
            print "Descubierto"
            self.myAgent.sendTo("inform", "Position", str(self.myAgent.pos[0])+" "+str(self.myAgent.pos[1]), otroAgente)

    class Position(spade.Behaviour.Behaviour):
        def _process(self):
            self.msg = None
            self.msg = self._receive(True)
            temp1 = self.msg.getSender().getName()
            print "Mensaje de posicionamiento"
            if self.myAgent.others == 1:
                print "Posicionando", temp1
                i = 0
                while temp1 != self.myAgent.robots[i].dir: i += 1
                temp2 = self.msg.getContent()
                temp2 = temp2.split()
                self.myAgent.robots[i].x = int(temp2[0])
                self.myAgent.robots[i].y = int(temp2[1])
                print temp1, int(temp2[0]), int(temp2[1])
                self.myAgent.others -= 1
                self.myAgent.sendTo("inform", "Ack", None, otroAgente)
            else:
                print "Recibidas cajas", temp1
                self.msg = str(self.msg.getContent())
                temp2 = self.msg.split()
                for i in xrange(0, len(temp2), 2):
                    self.myAgent.boxes.append(Object(int(temp2[i]), int(temp2[i+1])))
                X, temp = solver.branchAndBound(self.myAgent.robots, Object(10, 10), self.myAgent.boxes)
                s = ""
                for box in temp[1]:
                    s += box.toMessage()
                self.myAgent.sendTo("inform", "Path", s, self.myAgent.robots[1].dir)
                self.myAgent.schedule = temp[0]

    class Ack(spade.Behaviour.Behaviour):
        def _process(self):
            self.msg = None
            self.msg = self._receive(True)
            print "Mensaje Ack"
            if not iamMaster and self.myAgent.state == 0:
                self.myAgent.state += 1
                print "Enviando cajas"
                self.myAgent.sendTo("inform", "Position", cajas, otroAgente)
            elif iamMaster and self.myAgent.state == 0:
                self.myAgent.state += 4
                print "Caja 0"
                goForBoxes(self.myAgent, self.myAgent.schedule, 0)
                print "Caja 1"
                goForBoxes(self.myAgent, self.myAgent.schedule, 1)
                print "Caja 2"
                goForBoxes(self.myAgent, self.myAgent.schedule, 2)
                self.myAgent.sendTo("inform", "Ack", None, otroAgente)
            elif str(self.msg.getContent()) == "End":
                for i in xrange(self.myAgent.state-1, len(self.myAgent.schedule)):
                    goForBoxes(self.myAgent, self.myAgent.schedule, i)
                print "Trabajo finalizado, volviendo a la posicion inicial... "
                realPos = almath.Pose2D(self.myAgent.locationProxy.getRobotPosition(False))
                self.myAgent.motionProxy.post.moveTo(0,0,0-realPos.theta)
                self.myAgent.motionProxy.waitUntilMoveIsFinished()
                self.myAgent.motionProxy.post.moveTo(0-realPos.x,0-realPos.y,0)
                self.myAgent.motionProxy.waitUntilMoveIsFinished()
                realPos = almath.Pose2D(self.myAgent.locationProxy.getRobotPosition(False))
                print realPos
                print "FIN"
                self.myAgent._kill()
                sys.exit(0)
            elif self.myAgent.state > 0:
                print "Caja", self.myAgent.state-1
                goForBoxes(self.myAgent, self.myAgent.schedule, self.myAgent.state-1)
                self.myAgent.state += 1
                print "Caja", self.myAgent.state-1
                goForBoxes(self.myAgent, self.myAgent.schedule, self.myAgent.state-1)
                self.myAgent.state += 1
                if len(self.myAgent.schedule) == (self.myAgent.state-1)/2:
                    self.myAgent.sendTo("inform", "Ack", "End", otroAgente)
                    print "Trabajo finalizado, volviendo a la posicion inicial... "
                    self.myAgent.locationProxy.goToHome()
                    realPos = almath.Pose2D(self.myAgent.locationProxy.getRobotPosition(False))
                    print realPos
                    print "FIN"
                    self.myAgent._kill()
                    sys.exit(0)
                else:
                    self.myAgent.sendTo("inform", "Ack", None, otroAgente)

    class Path(spade.Behaviour.Behaviour):
        def _process(self):

            self.msg = None
            self.msg = self._receive(True)
            print "Recibido camino", self.msg.getContent()
            msg = self.msg.getContent().split()
            temp = []
            for pos in xrange(0, len(msg), 2):
                temp.append(Object(int(msg[pos]), int(msg[pos+1])))
            self.myAgent.schedule = temp
            self.myAgent.sendTo("inform", "Ack", None, otroAgente)
            print "Caja 0"
            self.myAgent.state += 1
            goForBoxes(self.myAgent, temp, 0)

    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setOntology("NaoTest")

        # Posicionar al esclavo y las cajas
        template.setPerformative( "inform" )
        template.setConversationId("Position")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.Position(), mt)

        # Ack
        template.setPerformative( "inform" )
        template.setConversationId("Ack")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.Ack(), mt)

        # Informar del camino
        template.setPerformative( "inform" )
        template.setConversationId("Path")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.Path(), mt)

        self.motionProxy = ALProxy("ALMotion", robotIP, robotPort)
        self.talkProxy = ALProxy("ALTextToSpeech", robotIP, robotPort)
        self.locationProxy = ALProxy("ALLocalization", robotIP, robotPort)

        self.locationProxy.learnHome()

        realPos = almath.Pose2D(self.locationProxy.getRobotPosition(False))
        print "Posicion inicial:", realPos

        self.others = 1

        if iamMaster:
            print "Explorando agentes..."
            self.sendTo("inform", "Reach", nombreAgente, otroAgente)

        self.robots = []
        self.boxes = []
        if iamMaster:
            self.robots.append(Robot(posRelx+int(round(realPos.x, 1)*10), posRely+int(round(realPos.y, 1)*10), nombreAgente))
            self.robots.append(Robot(0, 0, otroAgente))
            temp = cajas.split()
            for i in xrange(0, len(temp), 2):
                self.boxes.append(Object(int(temp[i]), int(temp[i+1])))

        self.pos = [0]*3
        self.pos[0] = posRelx+int(round(realPos.x, 1)*10)
        self.pos[1] = posRely+int(round(realPos.y, 1)*10)
        self.pos[2] = realPos.theta

        # Descubrimiento del servidor, despues para tener la posicion fisica
        template.setPerformative( "inform" )
        template.setConversationId("Reach")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.Reach(), mt)

        self.state = 0


    def sendTo(self, perf, id, content, receiver):
        msg = spade.ACLMessage.ACLMessage()
        msg.setOntology("NaoTest")
        msg.setPerformative(perf)
        msg.setConversationId(id)
        msg.setContent(content)
        gameManager = spade.AID.aid(name=receiver, addresses=["xmpp://"+receiver])
        msg.addReceiver(gameManager)
        self.send(msg)

if __name__ == "__main__":

        ag = AgRobot(nombreAgente, "secret")
        ag.start()


def goForBoxes(controller, msg, counter):
    if len(controller.schedule) <= counter/2: return
    if counter % 2 == 0:
        alpha = calculeAngle(controller.pos[0], controller.pos[1], msg[counter/2].x, msg[counter/2].y)-controller.pos[2]
        if alpha > pi+0.0001:
            alpha -= 2*pi
        if alpha < -pi-0.0001:
            alpha += 2*pi
        controller.motionProxy.post.moveTo(0, 0, alpha)
        controller.motionProxy.waitUntilMoveIsFinished()
        x = (msg[counter/2].x-controller.pos[0])/10.0
        y = (msg[counter/2].y-controller.pos[1])/10.0
        controller.motionProxy.post.moveTo(sqrt(x*x+y*y), 0, 0)
        controller.motionProxy.waitUntilMoveIsFinished()
        realPos = almath.Pose2D(controller.locationProxy.getRobotPosition(False))
        objX = (posRelx+cos(posRelTheta)*msg[counter/2].x)/10.0
        objY = (posRely+cos(posRelTheta)*msg[counter/2].y)/10.0
        while fabs(objX-realPos.x) > 0.09 or fabs(objY-realPos.y) > 0.09:
            print objX-realPos.x, objY-realPos.y, realPos
            x = objX-realPos.x
            y = objY-realPos.y
            theta = -realPos.theta
            controller.motionProxy.post.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), 0)
            controller.motionProxy.waitUntilMoveIsFinished()
            realPos = almath.Pose2D(controller.locationProxy.getRobotPosition(False))
        print "Recogida->", (posRelx+cos(posRelTheta)*msg[counter/2].x)/10.0, (posRely+cos(posRelTheta)*msg[counter/2].y)/10.0, realPos
        controller.pos[0] = int(cos(posRelTheta)*round(realPos.x, 1)*10) + posRelx
        controller.pos[1] = int(cos(posRelTheta)*round(realPos.y, 1)*10) + posRely
        controller.pos[2] = realPos.theta
        controller.talkProxy.say("Recogida")

    else:
        alpha = calculeAngle(controller.pos[0], controller.pos[1], contenedorX, contenedorY) - controller.pos[2]
        if alpha > pi+0.0001:
            alpha -= 2*pi
        if alpha < -pi-0.0001:
            alpha += 2*pi
        controller.motionProxy.post.moveTo(0, 0, alpha)
        controller.motionProxy.waitUntilMoveIsFinished()
        x = (contenedorX-controller.pos[0])/10.0
        y = (contenedorY-controller.pos[1])/10.0
        controller.motionProxy.post.moveTo(sqrt(x*x+y*y), 0, 0)
        controller.motionProxy.waitUntilMoveIsFinished()
        realPos = almath.Pose2D(controller.locationProxy.getRobotPosition(False))
        objX = (posRelx+cos(posRelTheta)*contenedorX)/10.0
        objY = (posRely+cos(posRelTheta)*contenedorY)/10.0
        while fabs(objX-realPos.x) > 0.09 or fabs(objY-realPos.y) > 0.09:
            print objX-realPos.x, objY-realPos.y, realPos
            x = objX-realPos.x
            y = objY-realPos.y
            theta = -realPos.theta
            controller.motionProxy.post.moveTo(x*cos(theta)-y*sin(theta), y*cos(theta)+x*sin(theta), 0)
            controller.motionProxy.waitUntilMoveIsFinished()
            realPos = almath.Pose2D(controller.locationProxy.getRobotPosition(False))
        realPos = almath.Pose2D(controller.locationProxy.getRobotPosition(False))
        print "Dejada->", (posRelx+cos(posRelTheta)*contenedorX)/10.0, (posRely+cos(posRelTheta)*contenedorY)/10.0, realPos
        controller.pos[0] = int(cos(posRelTheta)*round(realPos.x, 1)*10) + posRelx
        controller.pos[1] = int(cos(posRelTheta)*round(realPos.y, 1)*10) + posRely
        controller.pos[2] = realPos.theta
        controller.talkProxy.say("Entregada")