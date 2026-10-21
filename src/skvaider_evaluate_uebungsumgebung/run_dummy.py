import urllib.request
import os

url = "https://raw.githubusercontent.com/studentischerCoder/skvaide_evaluate_uebungsumgebung/main/src/skvaider_evaluate_uebungsumgebung/__init__.py"

urllib.request.urlretrieve(url, "eval_dummy.py")
os.system("python eval_dummy.py")
