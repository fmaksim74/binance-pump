#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from requests import PreparedRequest
from requests.sessions import Session
from time import time, sleep

def req1(n=10):
    s = Session()
    smt = 0
    for _ in range(n+1):
        st = time()
        r = s.get('http://api.binance.com/api/v1/ticker/price')
        et = time()
        smt += et -st
    print('Session.get(): Avg time spend {time}'.format(time=smt/n))
    s.close()

def req2(n=10):
    s = Session()
    smt = 0
    for _ in range(n+1):
        st = time()
        r = s.get('http://api.binance.com/api/v1/ticker/price').text
        et = time()
        smt += et -st
    print('Session.get().text: Avg time spend {time}'.format(time=smt/n))
    s.close()

def req3(n=10):
    s = Session()
    smt = 0
    for _ in range(n+1):
        st = time()
        r = s.get('http://api.binance.com/api/v1/ticker/price').json()
        et = time()
        smt += et -st
    print('Session.get().json(): Avg time spend {time}'.format(time=smt/n))
    s.close()

def req4(n=10):
    s = Session()
    req = PreparedRequest()
    req.prepare(method='GET',url='http://api.binance.com/api/v1/ticker/price')
    smt = 0
    for _ in range(n+1):
        st = time()
        r = s.send(req)
        et = time()
        smt += et -st
    print('Session.send(PreparedRequest): Avg time spend {time}'.format(time=smt/n))
    s.close()

def main():
    n = 50
    req1(n)
    req2(n)
    req3(n)
    req4(n)

if __name__ == "__main__":
    main()
