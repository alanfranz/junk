#include <fcntl.h>
#include <unistd.h>
#include <iostream>
#include <stdint.h>

/* Reads current ip_producer state, ie how far through ipv4 it
   is. Devide the number output by 2^32 for a rough % completed */
int main(int argc, char **argv)
{
  const char *filename = "ip_producer.state";
  int fd = open(filename, 0, O_RDONLY);
  if(fd == -1) {
    std::cerr << "failed to load state from file: " 
	      << filename << std::endl;
    return 1;
  }
  
  uint32_t x;
  int rc = read(fd, &x, sizeof(x)) != sizeof(x);
  close(fd);
  
  if(rc != sizeof(x)) {
    std::cerr << "error reading file: " << filename << std::endl;
    return 1;
  } 

  std::cout << x << std::endl;
  return 0;
}


