import argparse
import asyncio
import json
import subprocess
from datetime import datetime

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date_str',type=str)
    parser.add_argument('--email_id',type=str)
    args = parser.parse_args()

    time2send = datetime.fromisoformat(args.date_str)
    email_id = args.email_id

    while True:
        print(datetime.now(),'\t',time2send)
        if time2send <= datetime.now():
            print('paso el tiempo')
            subprocess.Popen(['python3','sendmail.py','--email_id',email_id])
            break
        else:
            fecha1 = datetime.now()
            seconds = (time2send - fecha1).total_seconds()
            seconds = seconds/2
            await asyncio.sleep(seconds)


if __name__ == '__main__':
    asyncio.run(main())
