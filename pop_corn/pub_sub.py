class PubSub:
    def __init__(self):
        self.topics = {}

    def subscribe(self, topics, who, callback_name):
        self.log("subscribe:"+str(topics)+" "+str( who)+" "+str( callback_name))
        for  topic in topics.split():
            if topic not in self.topics:
                self.topics[topic] = []
            self.topics[topic].append({"who":who,"callback_name":callback_name})

#     def unsubscribe(self, topic, who, callback_name):
#         if topic in self.topics:
#             try:
#                 self.topics[topic].remove(callback)
#                 if not self.topics[topic]:
#                     del self.topics[topic]
#             except ValueError:
#                 pass  # Callback not found

    def publish(self, topics, data=None):
        self.log("publish:"+str(topics)+" "+str( data))
        for  topic in topics.split():
            if topic in self.topics:
                for info in self.topics[topic]:
                    info["who"].published(info|{"data":data,"topic":topic, "who":self.get_name()})
            
    def log(self, string):
        print(string)
        
    def ger_name():
        return "PubSub"
        
        
class Who:
    def __init__(self,name):
        self.name=name
        
    def published(self, data=None):
        print("Who published",self.name,data)

if __name__ == "__main__":


    # Create PubSub instance
    pubsub = PubSub()

###############################################
    who1=Who(1)
#     In who1 ->
#     def temperature_handler(data):
#         print("Temperature update:", data)
    pubsub.subscribe("temperature cool", who1, "temperature_handler")
###############################################
    who2=Who(2)
#     In who2 ->
#     def humidity_handler(data):
#         print("Humidity update:", data)
    pubsub.subscribe("humidity rain",who2 , "humidity_handler")
###############################################
    
    # Publish some data
    pubsub.publish("temperature cool", 25.6)
    pubsub.publish("rain", 65)
    pubsub.publish("humidity", 60)
