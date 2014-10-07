#ifndef _BOGON_FILTER_H
#define _BOGON_FILTER_H

#include "netblock.h"
#include <vector>
#include <string>
#include <stdint.h>

class BogonFilter
{
public:
  BogonFilter() {};
  
  bool load(const std::string& file);
  bool contains(uint32_t ip) const;

private:
  bool parse_netblock(const std::string& s, 
		      NetBlock* netblock) const;

private:
  std::vector<NetBlock> netblocks_;
};

#endif /* _BOGON_FILTER_H */
