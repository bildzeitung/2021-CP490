import connexion
from connexion.resolver import RestyResolver


# Create the Connexion application instance
options = {"swagger_ui": False}
connex_app = connexion.App(__name__, specification_dir="./openapi", options=options, resolver=RestyResolver('coal_public_api_server.controllers'))
