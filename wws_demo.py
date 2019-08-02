import websocket,time
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message,'on_message')

def on_error(ws, error):
    print(error,'on_error')

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send('{sub: "trade_ticker", trade_id: "3", type: "add"}')
        #print('send:','{sub: "trade_ticker", trade_id: "3", type: "add"}')
        time.sleep(30)
        #ws.send('{sub: trade_ticker", trade_id: "3", type: "add"}')
        #ws.send('{ping:{}}'.format(time.time()))
        #time.sleep(30)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

def on_ping():
    print('on_ping')

headers = {
        'Host': 's.btckan.com:8080',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': 'https://bitkan.pro',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        }


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://s.btckan.com:8080/shift",header = headers,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              on_ping= on_ping)
    ws.on_open = on_open
    ws.run_forever()