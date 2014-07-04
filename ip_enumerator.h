#ifndef _IP_ENUMERATOR
#define _IP_ENUMERATOR

#include "ip_generator.h"
#include "bogon_filter.h"

class IPEnumerator : public IPGenerator
{
 public:
  IPEnumerator(uint8_t *key, std::string bogon_file);
  virtual ~IPEnumerator();
  virtual uint32_t next();
  virtual bool empty() const;
  virtual void reset();
  virtual bool save_state(const char *filename);
  virtual bool restore_state(const char *filename);

 private:
  uint32_t idx_;
  uint8_t key_[10];
  BogonFilter filter_;
};

#endif /* _IP_ENUMERATOR */
