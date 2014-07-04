
TARGETS = ipgen ipgen_state
CXXFLAGS = -O3 -Wall

all: $(TARGETS)

ipgen: ipgen.o skip32.o bogon_filter.o ip_enumerator.o ip2str.o 
	g++ $(CXXFLAGS) -o $@ $^ -llog4cpp -lboost_program_options-mt

ipgen_state: ipgen_state.o
	g++ $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(TARGETS) $(TESTS) *.so *.o *~ *.pyc

