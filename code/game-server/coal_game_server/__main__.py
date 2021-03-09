from .config import connex_app



def main():
  connex_app.add_api('openapi.yaml', arguments={'title': 'COAL Game Server'})
  connex_app.run(host='0.0.0.0', port=8100, debug=True)  
