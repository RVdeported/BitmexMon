import bitmex
from close_all import clients, acc_names 
import time
from pprint import pprint
from inspect import getmembers, isfunction
import json
from termcolor import colored

def get_acc_info(a_cli):
    try: 
        return a_cli.Position.Position_get().result()[0]
    except:
        return None

def get_margin(a_cli):
    try:
        return a_cli.User.User_getMargin(currency="USDt").response()[0]
    except Exception as e:
        e = str(e)
        js = e[e.find("["):e.find("]")+1]
        if (js.find("marginLeverage") < 0 ):
            return None
        js = js.replace("'", "\"")
        return json.loads(js)[0]


if __name__ == "__main__":
    for i, cli in enumerate(clients):
        accI    = get_acc_info(cli)
        margI   = get_margin(cli)
        if (accI is None or margI is None):
            continue
        
        print("ACC {} Margin: {:.2f}"\
                .format(acc_names[i], margI["amount"] / 1e6))
        for n in accI:
            if not n["isOpen"]: continue
            qty = n["homeNotional"]
            color = "green" if qty > 0 else "yellow"
            res = "\t{} Qty:{:.4f} Notional:{:.2f} PnL:{:.2f}({:.2f}%)"\
                  .format(n["symbol"], qty, 
                          -n["foreignNotional"], n["unrealisedPnl"] / 1e6, 
                          n["unrealisedPnlPcnt"] * 100)
            print(colored(res, color))
