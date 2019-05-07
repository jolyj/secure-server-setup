#!/usr/bin/python

from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join
import rsa
from Crypto.PublicKey import RSA

# This function open and return a certificate written in a file. It is used to load the server certificate.
def load_server_certificate(path):
    try:
        f = open(path, 'rt')
    except:
        print("Certificate file '%s' could not be open" % path)
        return None
    try:
        try:
            return crypto.load_certificate(crypto.FILETYPE_PEM, f.read())
        except crypto.Error, e:
            print("Certificate file '%s' could not be loaded: %s" % (path, str(e)))
            return None
    finally:
        f.close()

# This function open and return a key written in a file. It is used to load the server key.
def load_server_key(path):
    try:
        f = open(path, 'rt')
    except:
        print("Key file '%s' could not be open" % path)
        return None
    try:
        try:
            return crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
        except crypto.Error, e:
            print("Key file '%s' could not be loaded: '%s'" % (path, str(e)))
            return None
    finally:
        f.close()

# This function create a certificate, sign it with the server server key, set the issuer with the server certificate and write it in a file.
def create_signed_cert(cert_dir, country, stateName, organizationName, organizationUnitName, commonName, locality):

    # Generated files name
    cert_file_name = organizationName + "_" + commonName + "_" + country + ".crt"
    key_file_name = organizationName + "_" + commonName + "_" + country + ".key"

    # Load server certificate and key
    self_ca_cert = load_server_certificate("./server_certificate/secure_server.crt")
    self_ca_key = load_server_key("./server_certificate/secure_server.key")
    if (self_ca_cert == None or self_ca_key == None):
        print("Couldn't generate certificate\n")
        return False

    # Generate key for the user
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # Generate cert for the user
    cert = crypto.X509()

    # Set parameters according to the user data
    cert.get_subject().C = country
    cert.get_subject().ST = stateName
    cert.get_subject().L = locality
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName

    cert.set_serial_number(1000)
    # Set available period of the cetificate (10 years in this case)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    # Set issuer with the server certificate
    cert.set_issuer(self_ca_cert.get_subject())
    # Set the key for the user
    cert.set_pubkey(k)
    # Sign the certificate with server private key using sha-256 hash algorithm
    cert.sign(self_ca_key, 'sha256')

    # Dump generated certificate and key into files
    open(join(cert_dir, cert_file_name), "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(join(cert_dir, key_file_name), "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    return True

def generate(path, country, stateName, organizationName, organizationUnitName, commonName, locality):
    # create certificate
    res = create_signed_cert(path, country, stateName, organizationName, organizationUnitName, commonName, locality)

    # if fail return a false success
    if (res == None):
        return ("{" + "success: false" + "}")
    else:
        # open the certificate and key generated
        cert_file = open(path + "/" + organizationName + "_" + commonName + "_" + country + ".crt", "rt")
        key_file = open(path + "/" + organizationName + "_" + commonName + "_" + country + ".key", "rt")
        # get the certificate and the key and dump them in a json response
        cert = cert_file.read()
        key = key_file.read()
        return ("{" + "success: true" + "\ncert:" + cert + "\nkey: " + key + "}")
