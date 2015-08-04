#!/usr/bin/env python
# ftpserver.py

#
# Call this script with:
# sudo python ftpserver-cli.py --directory=/tmp/srvtest
#

import sys
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
      default="2121", help="port")
  optargs = optparser.parse_args(sys.argv[1:]) #(sys.argv)
  return optargs


ftp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "user")
optargs = processCmdLineOptions()

print("Using: user: %s pass: %s port: %d dir: %s" % (optargs.username, optargs.password, optargs.port, ftp_dir))

authorizer = DummyAuthorizer()
authorizer.add_user(optargs.username, optargs.password, ftp_dir, perm="elradfmw")
authorizer.add_anonymous(os.path.dirname(os.path.realpath(__file__)))

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", optargs.port), handler)
server.serve_forever()
