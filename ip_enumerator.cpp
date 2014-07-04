#include "ip_enumerator.h"
#include "skip32.h"
#include <cstring>
#include <cstdlib>
#include <cerrno>
#include <unistd.h>
#include <arpa/inet.h>
#include <log4cpp/Category.hh>
#include <log4cpp/convenience.h>

LOG4CPP_LOGGER("stn.ip_enumerator");

IPEnumerator::IPEnumerator(uint8_t *key, std::string bogon_file)
  : idx_(0)
{
  memcpy(key_, key, sizeof(key_));
  if(!filter_.load(bogon_file)) {
    LOG4CPP_ERROR_SD() << "failed to load: " << bogon_file;
    // TODO: should fail here...
  }
  LOG4CPP_NOTICE_SD() << "loaded: " << bogon_file;
}

IPEnumerator::~IPEnumerator()
{}

uint32_t
IPEnumerator::next()
{
  uint32_t x;
  while(!empty()) {
    x = idx_++;
    skip32(key_, (BYTE *) &x, 1);
    if(!filter_.contains(x)) {
      return htonl(x);
    }
  }
  return end();
}

bool
IPEnumerator::empty() const
{
    //return idx_ == end();
    //never end to make producer repeat itself, idx will overflow back to zero -- aj 7/9/11
    return false;
}

void 
IPEnumerator::reset()
{
  idx_ = 0;
  LOG4CPP_NOTICE_SD() << "resetting ip_enumerator";
}

bool
IPEnumerator::save_state(const char *filename)
{
  int fd = open(filename, O_CREAT | O_TRUNC | O_WRONLY, S_IRUSR|S_IWUSR);
  if(fd == -1) {
    LOG4CPP_ERROR_SD() << "failed to save state to file: '" 
		       << filename << "': " 
		       << strerror(errno);
    return false;
  }
  if(write(fd, &idx_, sizeof(idx_)) != sizeof(idx_)) {
    LOG4CPP_ERROR_SD() << "failed to write state to file: '"
		       << filename << "' "
		       << strerror(errno);
    close(fd);
    return false;
  }
  close(fd);  
  LOG4CPP_DEBUG_SD() << "saved state to file: '"
		     << filename << "'";
  return true;
}

bool
IPEnumerator::restore_state(const char *filename)
{
  int fd = open(filename, 0, O_RDONLY);
  if(fd == -1) {
    LOG4CPP_WARN_SD() << "failed to load state from file: '" 
		       << filename << "': " 
		       << strerror(errno);
    return false;
  }
  uint32_t x;
  if(read(fd, &x, sizeof(x)) != sizeof(idx_)) {
    LOG4CPP_ERROR_SD() << "failed to read state from file: '"
		       << filename << "' "
		       << strerror(errno);
    close(fd);
    return false;
  }
  idx_ = x;
  LOG4CPP_NOTICE_SD() << "loaded state from file: '"
		      << filename << "'";
  LOG4CPP_NOTICE_SD() << "was up to ip number " << idx_ << " of 4294967296";
  close(fd);
  return true;
}


