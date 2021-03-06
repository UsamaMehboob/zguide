#!/usr/bin/env python

"""
synopsis:
    Hello World client in Python.
    Implemented with ioloop and coroutines.
    Connects REQ socket to Url.
    Sends "Hello" to server; expects reply back.
    Modified for async/ioloop: Dave Kuhlman <dkuhlman(at)davekuhlman(dot)org>
usage:
    python hwclient.py <ident>
notes:
    <ident> is a string used to identify this client and to determine
        whether the right requests are returned to the correct client.
    Before starting this client, start either hwserver.py or mtserver.py.
"""


import sys
import zmq
from zmq.asyncio import Context, Poller, ZMQEventLoop
import asyncio


Url = 'tcp://127.0.0.1:5555'
Ctx = Context()


@asyncio.coroutine
def run(ident):
    #  Socket to talk to server
    print("Connecting to hello world server.  Ctrl-C to exit early.\n")
    socket = Ctx.socket(zmq.REQ)
    socket.connect(Url)
    poller = Poller()
    poller.register(socket, zmq.POLLOUT)
    #  Do multiple requests, waiting each time for a response
    for request in range(10):
        message = '{} Hello {}'.format(ident, request)
        message = message.encode('utf-8')
        print("Sending message: {}".format(message))
        yield from socket.send(message)
        #  Get the reply.
        message = yield from socket.recv()
        print("Received reply: {}".format(message))
    print('exiting')
    return 'nothing'


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit(__doc__)
    ident = args[0]
    try:
        loop = ZMQEventLoop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run(ident))
    except KeyboardInterrupt:
        print('\nFinished (interrupted)')


if __name__ == '__main__':
    main()
