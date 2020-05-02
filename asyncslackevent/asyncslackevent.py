from quart import Quart, request, abort, jsonify, make_response
from quart.exceptions import BadRequest
from quart_openapi import Pint, Resource
from swagger_ui import quart_api_doc
from time import time


class SlackEventException(Exception):
    """
    Base exception for all errors raised by the SlackClient library
    """
    def __init__(self, msg=None):
        if msg is None:
            # default error message
            msg = "An error occurred in the SlackEventsApi library"
        Exception.__init__(self, msg)


class AsyncSlackEventServer(Pint):
    def __init__(self, signing_secret, endpoint, emitter, server):
        self.signing_secret = signing_secret
        self.emitter = emitter
        self.endpoint = endpoint

        if server:
            if isinstance(server, Pint) or isinstance(server, Quart):
                self.bind_route(server)
            else:
                raise TypeError("Server must be an instance of Quart or Pint")
        else:
            Pint.__init__(self, __name__, no_openapi=True)
            print("Self assigned Server")

            quart_api_doc(
                self,
                config_url="http://localhost:8080/api/doc/swagger.json",
                url_prefix="/api/doc",
                title="API doc",
            )

            @self.route("/api/doc/swagger.json")
            async def openapi():
                return jsonify(self.__schema__)

            self.bind_route(self)

    def bind_route(self, server):
        @server.route(self.endpoint, methods=['GET', 'POST'])
        async def events():
            if request.method == 'GET':
                # If a GET request is made, return 404.
                print("GET RECEIVED!!!")
                return await make_response(
                    "These are not the slackbots you're looking for.", 404)

            if request.method == 'POST':
                # Each request comes with request timestamp and request
                # signature emit an error if the timestamp is out of range
                req_timestamp = request.headers.get(
                    'X-Slack-Request-Timestamp')
                if abs(time() - int(req_timestamp)) > 60 * 5:
                    slack_exception = SlackEventException(
                        'Invalid request timestamp')
                    self.emitter.emit('error', slack_exception)
                    return await make_response("", 403)

                # Verify the request signature using the app's signing secret
                # emit an error if the signature can't be verified
                req_signature = request.headers.get('X-Slack-Signature')
                # if not self.verify_signature(req_timestamp, req_signature):
                #    slack_exception = SlackEventException(
                #        'Invalid request signature')
                #    self.emitter.emit('error', slack_exception)
                #    return await make_response("", 403)

                # Parse the request payload into JSON
                event_data = await request.get_json()

                # Echo the URL verification challenge code back to Slack
                if "challenge" in event_data:
                    data_response = {"challenge": event_data["challenge"]}
                    return jsonify(data_response)

                # Parse the Event payload and emit the event to the event
                # listener
                if "event" in event_data:
                    event_type = event_data["event"]["type"]
                    self.emitter.emit(event_type, event_data['event'])
                    print("Callback for Event Type: %s" % event_type)
                    response = make_response("", 200)
                    # response.headers['X-Slack-Powered-By'] =self.package_info
                    return await response
