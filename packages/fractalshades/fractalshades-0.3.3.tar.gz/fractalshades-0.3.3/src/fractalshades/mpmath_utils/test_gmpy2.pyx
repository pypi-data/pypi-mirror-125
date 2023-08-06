"A minimal cython file test_gmpy2.pyx"

from gmpy2 cimport *

cdef extern from "gmp.h":
    void mpz_set_si(mpz_t, long)

import_gmpy2()   # needed to initialize the C-API

cdef mpz z = GMPy_MPZ_New(NULL)
mpz_set_si(MPZ(z), -7)

print(z + 3)
