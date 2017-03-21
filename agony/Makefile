SRCS = graph.cpp agony.cpp read.cpp
OBJS = $(SRCS:.cpp=.o)


CC = g++
LDFLAGS= -lm -O3 -lgsl -lblas -L/opt/local/lib
CFLAGS= -g -O3 -Wall -Wextra -I/opt/local/include/ #-Werror

all : agony 

agony: $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS)


%.o : %.cpp
	 $(CC) $(CFLAGS) -c $*.cpp

clean:
	-rm *.o agony

zip:
	zip agony.zip *.cpp *.h Makefile

depend:
	makedepend -Y -- $(CFLAGS) -- $(SRCS)
# DO NOT DELETE

graph.o: graph.h queue.h
agony.o: graph.h queue.h
