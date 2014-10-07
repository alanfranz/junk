#ifndef _NETBLOCK_H
#define _NETBLOCK_H

#include <stdint.h>

class NetBlock 
{
public:
  NetBlock(uint32_t address, uint32_t netmask)
    : address_(address), netmask_(netmask) {}

  NetBlock()
    : address_(0), netmask_(0) {}

  inline bool contains(uint32_t ip) const
  { return (ip & netmask_) == address_; }

  uint32_t address_;
  uint32_t netmask_;
};

#endif /* _NETBLOCK_H */

