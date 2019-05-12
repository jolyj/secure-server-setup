# -*- coding: utf-8 -*-

from flask import Response, request, Flask
import certificate

# HTTP server using Flask Framework

app = Flask(__name__)

# GET request endpoint to get the signed Certificate
# Parameters are : country, StateName, organizationName, organizationUnitName,
#                  commonName, locality
@app.route('/generation', methods=['GET'])
def generate_cert():
    # get the parameters to create the certificate
    country = request.args.get('country')
    stateName = request.args.get('stateName')
    organizationName = request.args.get('organizationName')
    organizationUnitName = request.args.get('organizationUnitName')
    commonName = request.args.get('commonName')
    locality = request.args.get('locality')

    # generate the certificate from module certificate
    response = certificate.generate("./generate_certificates", country, stateName, organizationName, organizationUnitName, commonName, locality)

    # response is composed of the signed certificate by the server and a key
    return response

if __name__ == "__main__":
    # Launch server on 127.0.0.1:5000
    app.run()
