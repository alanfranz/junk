
TARGETS = ipgen ipgen_state
CXXFLAGS = -O3 -Wall -I/usr/local/include 
CFLAGS = $(CXXFLAGS)
LDFLAGS = -L/usr/local/lib

all: $(TARGETS)

ipgen: ipgen.o skip32.o bogon_filter.o ip_enumerator.o ip2str.o 
	g++ $(LDFLAGS) -o $@ $^ -llog4cpp -lboost_program_options-mt -lcrypto

ipgen_state: ipgen_state.o
	g++ $(LDFLAGS) -o $@ $^

clean:
	rm -f $(TARGETS) $(TESTS) *.so *.o *~ *.pyc

