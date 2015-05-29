__author__ = 'maleza'

import spade
import almath
from naoqi import ALProxy
from math import atan, pi, sqrt, cos

# Posicion del robot relativa al problema
posRelx = 0
posRely = 0
posRelTheta = 0

# Suponemos que se sabe donde esta el contenedor
contenedorX = 10
contenedorY = 10

# Suponemos que ya hemos detectado las cajas
cajas = "5 7 5 10 10 5"

servidor="127.0.0.1"
nombreAgente = "Robot1"

"""
robotIP = "127.0.0.1"
robotPort = 36567
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


class Robot(spade.Agent.Agent):
    class Report(spade.Behaviour.Behaviour):
        def _process(self):

            self.msg = None
            self.msg = self._receive(True)
            if self.myAgent.state == 0:
                print "I'm registered."
                position = str(posRelx)+" "+str(posRely)
                print position
                self.myAgent.sendController("inform", "RobotPos", position)
            elif self.myAgent.state == 1:
                print "I'm positioned"
                self.myAgent.sendController("inform", "BoxPos", cajas)
            elif self.myAgent.state == 2:
                print "Boxes sent"
            self.myAgent.state += 1

    class Scheduler(spade.Behaviour.Behaviour):
        def _process(self):

            self.msg = None
            self.msg = self._receive(True)
            print self.msg.getContent()
            goForBoxes(self.myAgent, self.msg.getContent())
            self.myAgent.sendController("inform", "End", None)
            self.myAgent._kill()

    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setOntology("NaoTest")
        template.setPerformative( "inform" )
        template.setConversationId("Report")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.Report(), mt)

        template.setPerformative( "inform" )
        template.setConversationId("Schedule")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.Scheduler(), mt)

        print nombreAgente+": I'm going to register..."
        self.sendController("request", "Register", None)

        self.motionProxy = ALProxy("ALMotion", robotIP, robotPort)
        self.talkProxy = ALProxy("ALTextToSpeech", robotIP, robotPort)
        self.locationProxy = ALProxy("ALLocalization", robotIP, robotPort)

        print "Aprendiendo la posicion inicial..."

        self.locationProxy.learnHome()

        realPos = almath.Pose2D(self.locationProxy.getRobotPosition(False))
        print "Posicion inicial:", realPos

        self.pos = [0]*2
        self.pos[0] = posRelx+int(round(realPos.x, 1)*10)
        self.pos[1] = posRely+int(round(realPos.y, 1)*10)

        self.state = 0


    def sendController(self, perf, id, content):
         # Creamos el mensaje
         msg = spade.ACLMessage.ACLMessage()
         # Lo rellenamos
         msg.setOntology( "NaoTest" )
         msg.setPerformative( perf )
         msg.setConversationId( id )
         msg.setContent( content )
         gameManager = spade.AID.aid(name="controller@"+servidor, addresses=["xmpp://controller@"+servidor])
         msg.addReceiver( gameManager )
         self.send(msg)

if __name__ == "__main__":

        ag = Robot("robot1@"+servidor, "secret")
        ag.start()


def goForBoxes(controller, msg):
    msg = msg.split()

    print "Comienza la recogida de cajas, datos relativos al robot"

    # Recoger
    alpha = calculeAngle(controller.pos[0], controller.pos[1], int(msg[0]), int(msg[1]))
    controller.motionProxy.post.moveTo(0, 0, alpha)
    controller.motionProxy.waitUntilMoveIsFinished()
    x = (int(msg[0])-controller.pos[0])/10.0
    y = (int(msg[1])-controller.pos[1])/10.0
    controller.motionProxy.post.moveTo(sqrt(x*x+y*y), 0, 0)
    controller.motionProxy.waitUntilMoveIsFinished()
    realPos = almath.Pose2D(controller.locationProxy.getRobotPosition(False))
    print "Recogida->", (posRelx-int(msg[0]))/10.0, (posRely-int(msg[1]))/10.0, realPos
    controller.pos[0] = int(cos(posRelTheta)*round(realPos.x, 1)*10) + posRelx # Se redondea para no truncar
    controller.pos[1] = int(cos(posRelTheta)*round(realPos.y, 1)*10) + posRely
    controller.talkProxy.say("Recogida")

    # Entregar
    alpha = calculeAngle(controller.pos[0], controller.pos[1], contenedorX, contenedorY) - realPos.theta
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
    print "Dejada->", (posRelx-contenedorX)/10.0, (posRely-contenedorY)/10.0, realPos
    controller.pos[0] = int(cos(posRelTheta)*round(realPos.x, 1)*10) + posRelx
    controller.pos[1] = int(cos(posRelTheta)*round(realPos.y, 1)*10) + posRely
    controller.talkProxy.say("Entregada")

    for i in xrange(2, len(msg), 2):
        # Recoger
        alpha = calculeAngle(controller.pos[0], controller.pos[1], int(msg[i]), int(msg[i+1])) - realPos.theta
        if alpha > pi+0.0001:
            alpha -= 2*pi
        if alpha < -pi-0.0001:
            alpha += 2*pi
        controller.motionProxy.post.moveTo(0, 0, alpha)
        controller.motionProxy.waitUntilMoveIsFinished()
        x = (int(msg[i])-controller.pos[0])/10.0
        y = (int(msg[i+1])-controller.pos[1])/10.0
        controller.motionProxy.post.moveTo(sqrt(x*x+y*y), 0, 0)
        controller.motionProxy.waitUntilMoveIsFinished()
        realPos = almath.Pose2D(controller.locationProxy.getRobotPosition(False))
        print "Recogida->", (posRelx-int(msg[i]))/10.0, (posRely-int(msg[i+1]))/10.0, realPos
        controller.pos[0] = int(cos(posRelTheta)*round(realPos.x, 1)*10) + posRelx
        controller.pos[1] = int(cos(posRelTheta)*round(realPos.y, 1)*10) + posRely
        controller.talkProxy.say("Recogida")


        # Entregar
        alpha = calculeAngle(controller.pos[0], controller.pos[1], contenedorX, contenedorY) - realPos.theta
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
        print "Dejada->", (posRelx-contenedorX)/10.0, (posRely-contenedorY)/10.0, realPos
        controller.pos[0] = int(cos(posRelTheta)*round(realPos.x, 1)*10) + posRelx
        controller.pos[1] = int(cos(posRelTheta)*round(realPos.y, 1)*10) + posRely
        controller.talkProxy.say("Entregada")

    print "Trabajo finalizado, volviendo a la posicion inicial... "
    controller.locationProxy.goToHome()
    """
    controller.motionProxy.post.moveTo(0, 0, 0-realPos.theta)
    controller.motionProxy.waitUntilMoveIsFinished()
    controller.motionProxy.post.moveTo(-realPos.x, -realPos.y, 0)
    controller.motionProxy.waitUntilMoveIsFinished()
    """
    realPos = almath.Pose2D(controller.locationProxy.getRobotPosition(False))
    print realPos
    print "FIN"