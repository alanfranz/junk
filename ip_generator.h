#ifndef _IP_GENERATOR_H
#define _IP_GENERATOR_H

#include <string>
#include <stdint.h>

class IPGenerator
{
 public:
  virtual ~IPGenerator() {};
  virtual uint32_t next() = 0;
  virtual bool empty() const = 0;
  virtual uint32_t end() const 
  { return 0xffffffff; }
  virtual void reset() = 0;
  virtual bool save_state(const char *filename) = 0;
  virtual bool restore_state(const char *filename) = 0;
};

#endif /* _IP_GENERATOR_H */
