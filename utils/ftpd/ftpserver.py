#!/usr/bin/env python
# ftpserver.py
# Call this script with:
# sudo python ftpserver-cli.py --directory=/tmp/srvtest

import sys
sys.path.append("/path/to/pyftpdlib-svn") # enter your proper path here
import argparse
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def processCmdLineOptions():
  global optparser
  optparser = argparse.ArgumentParser(description="ftpserver-cli",
              formatter_class=argparse.RawDescriptionHelpFormatter)
  optparser.add_argument('-u', '--username', action='store', type=str,
      default="user", help="username")
  optparser.add_argument('-p', '--password', action='store', type=str,
      default="12345", help="password")
  optparser.add_argument('-t', '--port', action='store', type=int,
      default="21", help="port")
  optparser.add_argument('-d', '--directory', action='store', type=str,
      default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "user"), help="port")
  optargs = optparser.parse_args(sys.argv[1:]) #(sys.argv)
  return optargs


optargs = processCmdLineOptions()

print("Using: user: %s pass: %s port: %d dir: %s" % (optargs.username, optargs.password, optargs.port, optargs.directory))

authorizer = DummyAuthorizer()
authorizer.add_user(optargs.username, optargs.password, optargs.directory, perm="elradfmw")
#authorizer.add_anonymous("/home/nobody")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", optargs.port), handler)
server.serve_forever()
