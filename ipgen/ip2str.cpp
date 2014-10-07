#include "ip2str.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

std::string 
ip2str(uint32_t ip)
{
  struct in_addr ina;
  ina.s_addr = ip;
  return std::string(inet_ntoa(ina));
}

bool
str2ip(const std::string& s, uint32_t *ip)
{
  return inet_pton(AF_INET, s.c_str(), ip);
}
