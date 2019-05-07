# Dependancies

- python 2+
- module python Flask
- module python openssl

-----------------

# Certificate generation server

The aim of this project is to create a server in python that deliver free signed certificate.
To launch the server run the launch script:

>./launch

The default host and port is 127.0.0.1:5000

The server_certificate folder contains the server's certificate and key.
The generate_certificates contains certificates generated and signed by the server.


# Server protocole

1. Generate Certificate

    Description : Generate a certificate signed by the server  
    EndPoint : `/generation`  
    Method : `GET`

    **Parameters** :    

    __Query strings__ :   

    | Parameter | Description | Data Type |
    | :-------: | :--------: | :--------: |
    | country | Contains the country's name | string |
    | stateName | Contains the state's name | string |
    | organizationName | Contains organization's name | string |
    | organizationUnitName | Contains the organization's unit name | string |
    | commonName | Contains the common name | string |
    | locality | Contains the locality name | string |

    **Response messages** :  

    | HTTP Status Code | Reason | Response Model |
    | :-----------------: | :------: | :-------------: |
    | 201 | Document created | { "success": true, "cert": "", "key":""}|
    | 4XX | Error in request | { "success": false}  |
