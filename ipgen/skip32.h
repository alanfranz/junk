#ifndef _SKIP32_H
#define _SKIP32_H

#ifdef __cplusplus
extern "C" {
#endif 

typedef unsigned char	BYTE; /* 8 bits */
typedef unsigned short	WORD; /* 16 bits */

extern void
skip32(BYTE key[10], BYTE buf[4], int encrypt);

#ifdef __cplusplus
}
#endif 

#endif /* _SKIP32_H */

