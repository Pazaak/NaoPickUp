__author__ = 'maleza'
#!/usr/bin/env python


import spade

servidor="127.0.0.1"

nombreAgente = "Robot1"


class Robot(spade.Agent.Agent):
    class Report(spade.Behaviour.Behaviour):
        def _process(self):

            self.msg = None
            self.msg = self._receive(True)
            if self.myAgent.state == 0:
                print "I'm registered."
                self.myAgent.sendController("inform", "RobotPos", "0 0")
            elif self.myAgent.state == 1:
                print "I'm positioned"
                self.myAgent.sendController("inform", "BoxPos", "5 7 5 10 10 5")
            elif self.myAgent.state == 2:
                print "Boxes sent"
            self.myAgent.state += 1

    class Scheduler(spade.Behaviour.Behaviour):
        def _process(self):

            self.msg = None
            self.msg = self._receive(True)
            print self.msg.getContent()
            self.myAgent.sendController("inform", "End", None)
            self.myAgent._kill()

    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setOntology("NaoTest")
        template.setPerformative( "inform" )
        template.setConversationId("Report")
        mt = spade.Behaviour.MessageTemplate(template)
        # Comportamiento de actualizar la tirada en la mesa
        self.addBehaviour(self.Report(), mt)

        template.setPerformative( "inform" )
        template.setConversationId("Schedule")
        mt = spade.Behaviour.MessageTemplate(template)
        # Comportamiento de actualizar la tirada en la mesa
        self.addBehaviour(self.Scheduler(), mt)

        print nombreAgente+": I'm going to register..."
        self.sendController("request", "Register", None)

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