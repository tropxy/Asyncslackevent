# Asyncslackevent
Async SlackEvent server handler based on https://github.com/slackapi/python-slack-events-api


The AsyncSlack Events is an Async version of the Python-based solution of python-slack-events-api to receive and parse events
from Slack’s Events API. Therefore, it works in the same manner as python-slack-events-api by using an Async event emitter attaching functions to event listeners.

It can serve your app by creating a Quart server or it can uses your own serer framework. The app uses Pint (openapi for Quart), however I couldnt manage to construct the code in order to use the openapi features and use at the same time the same structure as python-slack-events-api, so, for now, it creates creates routes as usually when using Quart:

.. code:: python
  @app.route("/", methods=['GET', 'POST'])
  async def events():
      if request.method == 'GET':
          # If a GET request is made, return 404.
          print("GET RECEIVED!!!")
          return await make_response(
              "These are not the slackbots you're looking for.", 404)



Installation
----------------
----


Create a Slack Event Adapter for receiving actions via the Events API
-----------------------------------------------------------------------
**Using the built-in Quart server:**

.. code:: python

  from asyncslackevent import AsyncSlackEventAdapter
  
  # Use AsyncSlackEventAdapter to start a Quart/Pint Server and handle the EventsAPI
  app_server = AsyncSlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events")


  # Create an event listener for "reaction_added" events and print the emoji name
  @app_server.on("reaction_added")
  async def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(emoji)


  # Start the server on port 3000
  app_server.run(port=3000)


**Using your existing Flask instance:**


.. code:: python

  from quart import Quart
  from asyncslackevent import AsyncSlackEventAdapter


  # This `app` represents your existing Quart app
  app = Quart(__name__)


  # An example of one of your Quart app's routes
  @app.route("/")
  def hello():
    return "Hello there!"


  # Bind the Events API route to your existing Quart app by passing the server
  # instance as the last param, or with `server=app`.
  slack_event_handler = AsyncSlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)


  # Create an event listener for "reaction_added" events and print the emoji name
  @slack_event_handler.on("reaction_added")
  def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(emoji)


  # Start the server on port 3000
  if __name__ == "__main__":
    app.run(port=3000)

For a comprehensive list of available Slack `Events` and more information on
`Scopes`, see https://api.slack.com/events-api
