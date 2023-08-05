def user(app):
  @app.before_request
  def load_user():
    from flask import request
    import requests
    if len(dict(request.headers)["X-Replit-User-Name"]) != 0:
      request.user = requests.get("https://replit-user-info-api.epiccodewizard.repl.co/@" + dict(request.headers)["X-Replit-User-Name"], params={"count": "false"}).json()
    else:
      request.user = None