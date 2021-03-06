from pyee import AsyncIOEventEmitter
from .asyncslackevent import AsyncSlackEventServer


class AsyncSlackEventAdapter(AsyncIOEventEmitter):
    # Initialize the Slack event server
    # If no endpoint is provided, default to listening on '/slack/events'
    def __init__(self, signing_secret, endpoint="/slack/events", server=None,
                 **kwargs):
        AsyncIOEventEmitter.__init__(self)
        self.signing_secret = signing_secret
        self.server = AsyncSlackEventServer(signing_secret, endpoint, self,
                                            server, **kwargs)

    def run(self, host='0.0.0.0', port=8080, debug=False, **kwargs):
        """
        Start the built in webserver, bound to the host and port you'd like.
        Default host is `0.0.0.0` and port 8080.
        :param host: The host you want to bind the build in webserver to
        :param port: The port number you want the webserver to run on
        :param debug: Set to `True` to enable debug level logging
        :param kwargs: Additional arguments you'd like to pass to Flask
        """
        self.server.run(host=host, port=port, debug=debug, **kwargs)
