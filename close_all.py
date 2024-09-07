import bitmex
import configparser as cf
import time
import os

cp = cf.ConfigParser()
cp.read("config_info.ini")
if (len(cp.sections()) == 0):
    raise Exception("Could not read the config Path!")
confPath = cp["Main"]["ConfigP"]

configs = [confPath + n for n in os.listdir(confPath) if n[-4:] == ".ini"]
clients = []
instrs  = []
acc_names = []
for c in configs:
    cp.read(c)
    if (len(cp.sections()) == 0):
        raise Exception("Could not read ini file!")
    clients.append(bitmex.bitmex(test=False,
        api_key=cp["OMC"]["H2APIKey"], 
        api_secret=cp["OMC"]["H2APISecret"]))
    instrs.append(cp["Main"]["Instr"])
    instrs[-1] = instrs[-1][:instrs[-1].find("|")]
    acc_names.append(cp["MDC"]["AccountPfx"])

if __name__ == "__main__":
    for s in ["Buy", "Sell"]:
        i = 0
        for c in clients:
            try:
                print(c.Order.Order_new(symbol=instrs[i], side=s, 
                    execInst="Close", ordType="Market").result())
            except Exception as e:
                print("Error on closing orders: " + str(e))

            i+=1


