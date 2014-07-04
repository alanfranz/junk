#include "bogon_filter.h"
#include "ip2str.h"
#include <fstream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <log4cpp/Category.hh>
#include <log4cpp/convenience.h>

LOG4CPP_LOGGER("stn.bogon_filter");

bool 
BogonFilter::parse_netblock(const std::string& s, 
			    NetBlock* netblock) const
{
  LOG4CPP_DEBUG_SD() << "parsing netblock: " << s;
  size_t slash_pos = s.find('/');
  if(slash_pos == std::string::npos) {
    return false;
  }
  uint32_t network, netmask;
  if(!str2ip(s.substr(0, slash_pos), &network) || 
     !str2ip(s.substr(slash_pos+1), &netmask)) 
  {
    LOG4CPP_ERROR_SD() << "failed to parse: " << s;
    return false;
  }
    
  *netblock = NetBlock(ntohl(network), ntohl(netmask));
    
  LOG4CPP_DEBUG_SD() << "successfully parsed: " <<
    ip2str(network) << "/" << ip2str(netmask);

  return true;
}


bool 
BogonFilter::load(const std::string& file)
{
  std::ifstream f(file.c_str());
  if(!f.is_open()) {
    LOG4CPP_ERROR_SD() << "failed to open: " << file;
    return false;
  }
  std::string line;
  NetBlock net_block;
  while(f.good()) {
    getline(f, line);
    if(line[0] == '#')
      continue;
    if(parse_netblock(line, &net_block)) {
      netblocks_.push_back(net_block);
    }
  }
  LOG4CPP_INFO_SD() << "loaded " << netblocks_.size() << " entries.";
  return true;
}

bool 
BogonFilter::contains(uint32_t ip) const
{
  std::vector<NetBlock>::const_iterator it;
  for(it = netblocks_.begin(); it != netblocks_.end(); ++it) {
    if(it->contains(ip)) {
      // LOG4CPP_DEBUG_SD() << "matched: " << ip2str(ip);
      return true;
    }
  }
  // LOG4CPP_DEBUG_SD() << "did not match: " << ip2str(ip);
  return false;
}
