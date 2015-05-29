__author__ = 'maleza'

import spade
from header_classes import Robot, Object
import solver

servidor="127.0.0.1"

nombreAgente = "Controller"


class Controller(spade.Agent.Agent):

    class register(spade.Behaviour.Behaviour):
        def _process(self):
            self.msg = None
            self.msg = self._receive(True)
            temp = self.msg.getSender().getName()
            print "New robot registered: "
            print temp
            self.myAgent.robots.append(Robot(0, 0, temp))
            self.myAgent.sendTo("inform", "Report", None, temp)

    class robotPos(spade.Behaviour.Behaviour):
        def _process(self):
            self.msg = None
            self.msg = self._receive(True)
            temp1 = self.msg.getSender().getName()
            i = 0
            while temp1 != self.myAgent.robots[i].dir: i += 1
            temp2 = self.msg.getContent()
            temp2 = temp2.split()
            self.myAgent.robots[i].x = int(temp2[0])
            self.myAgent.robots[i].y = int(temp2[1])
            print temp1, int(temp2[0]), int(temp2[1])
            self.myAgent.sendTo("inform", "Report", None, temp1)

    class boxPos(spade.Behaviour.Behaviour):
        def _process(self):
            self.msg = None
            self.msg = self._receive(True)
            temp1 = self.msg.getSender().getName()
            temp2 = self.msg.getContent()
            temp2 = temp2.split()
            for i in xrange(0, len(temp2), 2):
                self.myAgent.boxes.append(Object(int(temp2[i]), int(temp2[i+1])))
            self.myAgent.sendTo("inform", "Report", None, temp1)
            self.myAgent.reportedBoxes += 1
            if self.myAgent.reportedBoxes == 2:
                """
                for rob in self.myAgent.robots:
                    print rob
                X, schedule = solver.branchAndBound(self.myAgent.robots, Object(10, 10), self.myAgent.boxes)
                for rob in xrange(len(self.myAgent.robots)):
                    s = ""
                    for box in schedule[rob]:
                        s += box.toMessage()
                    self.myAgent.sendTo("inform", "Schedule", s, self.myAgent.robots[rob].dir)
                    self.myAgent._kill()
                """
                X, self.myAgent.schedule = solver.branchAndBound(self.myAgent.robots, Object(10, 10), self.myAgent.boxes)
                print self.myAgent.robots[0]
                s = ""
                for box in self.myAgent.schedule[0]:
                    s += box.toMessage()
                self.myAgent.sendTo("inform", "Schedule", s, self.myAgent.robots[0].dir)
                self.myAgent.schedule.pop(0)
                self.myAgent.robots.pop(0)

    class nextTurn(spade.Behaviour.Behaviour):
        def _process(self):
            self.msg = None
            self.msg = self._receive(True)
            if self.myAgent.robots:
                print self.myAgent.robots[0]
                s = ""
                for box in self.myAgent.schedule[0]:
                    s += box.toMessage()
                self.myAgent.sendTo("inform", "Schedule", s, self.myAgent.robots[0].dir)
                self.myAgent.schedule.pop(0)
                self.myAgent.robots.pop(0)
            else:
                self.myAgent._kill()

    def _setup(self):
        self.robots = []
        self.boxes = []
        self.reportedBoxes = 0
        template = spade.Behaviour.ACLTemplate()
        template.setOntology("NaoTest")
        template.setPerformative("request")
        template.setConversationId("Register")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.register(), mt)

        template.setPerformative("inform")
        template.setConversationId("RobotPos")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.robotPos(), mt)

        template.setPerformative("inform")
        template.setConversationId("BoxPos")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.boxPos(), mt)

        # Nuevo, turnos parados
        template.setPerformative("inform")
        template.setConversationId("End")
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.nextTurn(), mt)

        print nombreAgente+": Listening to robots..."

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

        ag = Controller("controller@"+servidor, "secret")
        ag.start()