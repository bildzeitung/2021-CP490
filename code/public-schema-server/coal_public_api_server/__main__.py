from .config import connex_app



def main():
  connex_app.add_api('openapi.yaml', arguments={'title': 'Concurrent Online Adventure Land, or MUD'})
  connex_app.run(host='0.0.0.0', port=8000, debug=True)  
