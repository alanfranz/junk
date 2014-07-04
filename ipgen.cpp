#include "ip_enumerator.h"
#include "ip2str.h"
#include <cstdio>
#include <vector>
#include <arpa/inet.h>
#include <stdint.h>
#include <openssl/evp.h>
#include <log4cpp/Category.hh>
#include <log4cpp/BasicConfigurator.hh>
#include <log4cpp/convenience.h>
#include <boost/program_options.hpp>

LOG4CPP_LOGGER("ipgen");

// Keying params for skip32 encryption
unsigned char salt[] = "The slow green fox";
std::string keystr = "12345";
uint8_t key[10]; 

const char *state_file = "ipgen.state";
int save_state_every = 0;
int stop_after = 0;

namespace po = boost::program_options;

int main(int argc, char **argv)
{
  log4cpp::BasicConfigurator::configure();

  po::options_description desc("options");
  desc.add_options()
    ("help,h", 
         "produce help message")
    ("key,k", po::value<std::string>(), 
         "scan key (string, default \"12345\")")
    ("save,s", po::value<int>(),
         "save state every n ips (int, default 0, don't save)")
    ("num,n", po::value<int>(),
         "stop after n ips (int, default 0, all the ips)")
    ;
  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, desc), vm);
  po::notify(vm);

  if (vm.count("help")) {
    std::cerr << desc << std::endl;
    return 1;
  }
  if (vm.count("save")) {
    save_state_every = (uint32_t) vm["save"].as<int>();
  }
  if (vm.count("key")) {
    keystr = vm["key"].as<std::string>();
  }
  if (vm.count("num")) {
    stop_after = vm["num"].as<int>();
  } 

  // Derive key bytes
  PKCS5_PBKDF2_HMAC_SHA1(
      keystr.c_str(), keystr.length(),
      salt, sizeof(salt),
      1000, // Num rounds
      10, // Key length
      key);

  // Load bogons and state
  IPEnumerator ip_enum(key, "bogons.txt");
  if(!ip_enum.restore_state(state_file)) {
    LOG4CPP_NOTICE_SD() << "no state; starting from scratch";
  } else {
    LOG4CPP_NOTICE_SD() << "resuming from saved state file";
  }
  
  long count = 0;
  while(1) {
    uint32_t ip = ip_enum.next();
    std::cout << ip2str(ip) << std::endl;
    if(ip == ip_enum.end()) {
        break;
    }
    count++;
    if(count % 1000000 == 0) {
        LOG4CPP_NOTICE_SD() << "progress: " << count / 1000000 << " million...";
    }
    if(save_state_every > 0 && count % save_state_every == 0) {
        ip_enum.save_state(state_file);
    }
    if(stop_after > 0 && count == stop_after) {
        if(save_state_every > 0) { // Record that we finished.
            ip_enum.save_state(state_file);
        }
        break;
    }
  }

  LOG4CPP_ALERT_SD() << "Scan complete!";
}

