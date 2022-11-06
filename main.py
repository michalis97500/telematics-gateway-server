import connection as cn
import message_handler as mh


def main():
  
  # Create a connection object
  connection = cn.connect(default=True,DEBUG=True)
  # Create a message handler object
  _message_handler = mh.MessageHandler(DEBUG=True)
  #Connect to the broker
  if type(connection) == cn.mqtt_client.MQTTClient:
    # Subscribe to the topic
    connection.subscribe(topic='#')
    while True:
      # Get the message and handle it
      handled = _message_handler.message_handle_method(connection.get_message())
      if handled:
        if handled == True:
          print("Message received and handled")
        elif handled == False:
          print("Message not handled")
          
main()