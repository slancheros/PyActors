import pykka

class Greeter(pykka.ThreadingActor):
    def __init__(self, greeting='Hi there!'):
        super(Greeter, self).__init__()
        self.greeting = greeting

    def on_receive(self, message):
        print('Hi there!' + str( message))
        return 'Hi there!' + str( message)


actor_ref = Greeter.start(greeting='Hi you!')


actor_ref.tell({'msg': 'Hi! Tell- Will never block' })
# => Returns nothing. Will never block.


answer = actor_ref.ask({'msg': 'Hi? Ask - Blocking'})
# => May block forever waiting for an answer
print('answer ask-blocking:' + str(answer))

answer = actor_ref.ask({'msg': 'Hi? Ask - Raise Exception with Timeout'}, timeout=3)
# => May wait 3s for an answer, then raises exception if no answer.
print('answer Raise Exception with Timeout:' + str(answer))

future = actor_ref.ask({'msg': 'Hi? Future - Non Blocking'}, block=False)
# => Will return a future object immediately.
answer = future.get()
# => May block forever waiting for an answer
print('answer Future - Non Blocking:' + str(answer))

answer = future.get(timeout=0.1)
# => May wait 0.1s for an answer, then raises exception if no answer.
print('answer Future - Non Blocking with timeout:' + str(answer))

actor_ref.stop()