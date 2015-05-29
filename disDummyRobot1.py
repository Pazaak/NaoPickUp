__author__ = 'maleza'

import spade, solver, sys, time
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
iamMaster = False

nombreAgente = "robot1@127.0.0.1"
# Si hubiera mas de un agente esto seria una lista
otroAgente = "robot2@127.0.0.1"


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
                self.myAgent.state += 3
                print "Caja 0"
                time.sleep(10)
                print "Caja 1"
                time.sleep(10)
                self.myAgent.sendTo("inform", "Ack", None, otroAgente)
            elif str(self.msg.getContent()) == "End":
                for i in xrange(self.myAgent.state-1, len(self.myAgent.schedule)):
                    time.sleep(10)
                print "FIN"
                self.myAgent._kill()
                sys.exit(0)
            elif self.myAgent.state > 0:
                print "Caja", self.myAgent.state-1
                time.sleep(10)
                self.myAgent.state += 1
                if len(self.myAgent.schedule) == (self.myAgent.state-1)/2:
                    self.myAgent.sendTo("inform", "Ack", "End", otroAgente)
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
            time.sleep(10)

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

        self.others = 1

        if iamMaster:
            print "Explorando agentes..."
            self.sendTo("inform", "Reach", nombreAgente, otroAgente)


        self.robots = []
        self.boxes = []
        if iamMaster:
            self.robots.append(Robot(posRelx, posRely, nombreAgente))
            self.robots.append(Robot(0, 0, otroAgente))
            temp = cajas.split()
            for i in xrange(0, len(temp), 2):
                self.boxes.append(Object(int(temp[i]), int(temp[i+1])))

        self.pos = [0]*3
        self.pos[0] = posRelx
        self.pos[1] = posRely
        self.pos[2] = posRelTheta

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