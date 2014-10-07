#ifndef _IP2STR_H
#define _IP2STR_H

#include <string>
#include <stdint.h>

std::string ip2str(uint32_t ip);
bool str2ip(const std::string& s, uint32_t *ip);
// std::string 

#endif /* _IP2STR_H */
