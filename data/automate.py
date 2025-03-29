import schedule
import time
import subprocess

def run_script():
    subprocess.run(["python", "C:\\Yaminis workspace\\work\\rag\\project\\data\\all_news.py"])

schedule.every(1).hour.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(60)