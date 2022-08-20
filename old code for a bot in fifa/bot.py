

import pyautogui
import time
import Xlib
import random

"""""
Main
"""""
def main():

    while 1:
        answer = raw_input("Would you like Start Sniping?(y=yes)")
        if answer == 'y':
            break;
    while 1:
        answer = raw_input("Fast-1\Slow-2")
        if answer == '1':
            snipe()
            break;
        if answer =='2':
            slowSnipe()
            break

    return 0;


def snipe():
    #start up time:
    for i in range(1,6):
        print 6-i
        time.sleep(1)
    print "Snipe!!"

    #snipe loop:
    c=0;
    c2=0;
    lim = random.randint(5, 12)
    lim2=random.randint(50,100)
    slowCounter=0
    while 1:
        #randomness:
        r=random.uniform(0.4,0.6)
        x=random.uniform(0.08,0.20)
        j=random.uniform(0.02,0.07)
        v=random.uniform(0.3,0.52)
        k=random.uniform(0.05,0.09)

        #search and wait a bit
        pyautogui.press("0")
        time.sleep(k)

        # #maybe go down to more offers
        # if(question==1):
        #     u=random.uniform(0.09,0.15)
        #     pyautogui.press("down")
        #     time.sleep(u)



        pyautogui.press('enter')
        time.sleep(x)
        pyautogui.press("9")
        time.sleep(j)
        pyautogui.press("9")
        time.sleep(v)
        pyautogui.press('backspace')
        time.sleep(r)

        #Human wait
        c+=1
        c2+=1
        if c==lim:
            c=0
            lim = random.randint(4, 7)
            wait=random.uniform(0,2.5)
            time.sleep(wait)

        if c2==lim2:
            c2=0;
            slowCounter+=1
            lim2=random.randint(50,100)
            wait2=random.uniform(2,6)
            time.sleep(wait2)
            # if slowCounter==10:
            #     slowSnipe()

    return 0;

def slowSnipe():
    #start up time:
    for i in range(1,6):
        print 6-i
        time.sleep(1)
    print "Snipe!!"

    #snipe loop:
    c=0;
    c2=0;
    lim = random.randint(5, 12)
    lim2=random.randint(50,100)
    while 1:
        #randomness:
		k=random.uniform(0.1,0.3)
		x=random.uniform(0.2,0.4)
		v=random.uniform(1,1.5)
		r=random.uniform(1,1.5)
		question=random.randint(1,2)

		#search and wait a bit
		pyautogui.press("0")
		time.sleep(k)



		pyautogui.press('enter')
		time.sleep(x)
		pyautogui.press("9")
		time.sleep(v)
		pyautogui.press('backspace')
		time.sleep(r)

		#Human wait
		c+=1
		c2+=1
		if c==lim:
			c=0
			lim = random.randint(4, 7)
			wait=random.uniform(0.5,2)
			time.sleep(wait)

		if c2==lim2:
			c2=0;
			lim2=random.randint(50,100)
			wait2=random.uniform(2,5)
			time.sleep(wait2)
	

if __name__ == "__main__":
    main()
