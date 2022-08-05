a.out: main.o threadPool.o osqueue.o
	gcc -o a.out main.o threadPool.o osqueue.o -pthread

main.o: main.c threadPool.h
	gcc -c -o main.o main.c -pthread

threadPool.o: threadPool.c threadPool.h
	gcc -c -o threadPool.o threadPool.c -pthread

osqueue.o: osqueue.c osqueue.h
	gcc -c -o osqueue.o osqueue.c
