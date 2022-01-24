from bitstring import BitArray
import snow_arrays
import time
import statistics
import random
import RC4
from Crypto.Util.number import long_to_bytes
from Crypto.Hash import SHA
from Crypto.Cipher import ARC4
from Crypto.Cipher import Salsa20


def Trim_32(x):
    temp = BitArray(length=32)
    if len(x) < 32:
        n = 32 - len(x)
        temp[n:] = x
        return temp
    else:
        return x


def MULx(v, c):
    if v.bin[0] == '1':
        return (v << 1) ^ c
    else:
        return v << 1


def MULxPOW(v,i,c):
    if i == 0:
        return v
    else:
        return MULx(MULxPOW(v, i-1, c), c)


def MUL_alpha(c):
    c = c[:8]
    x = BitArray('0xa9')
    return (MULxPOW(c, 23, x))+(MULxPOW(c, 245, x))+(MULxPOW(c, 48, x))+(MULxPOW(c, 239, x))


def DIV_alpha(c):
    c = c[24:]
    x = BitArray('0xa9')
    return (MULxPOW(c, 16, x))+(MULxPOW(c, 39, x))+(MULxPOW(c, 6, x))+(MULxPOW(c, 64, x))


def S(w):
    w = BitArray(w)
    w3 = w[:8].uint
    w2 = w[8:16].uint
    w1 = w[16:24].uint
    w0 = w[24:].uint
    r = Trim_32(BitArray(snow_arrays.snow_T0[w0])) ^ Trim_32(BitArray(snow_arrays.snow_T1[w1])) ^ Trim_32(BitArray(snow_arrays.snow_T2[w2])) ^ Trim_32(BitArray(snow_arrays.snow_T3[w3]))
    return r


def Initialize128(k, IV):
    global LFSR_S0, LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10, LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15, FSM_R1, FSM_R2
    LFSR_S15 = k[3] ^ IV[0]
    LFSR_S14 = k[2]
    LFSR_S13 = k[1]
    LFSR_S12 = k[0] ^ IV[1]
    LFSR_S11 = k[3] ^ BitArray('0xffffffff')
    LFSR_S10 = k[2] ^ BitArray('0xffffffff') ^ IV[2]
    LFSR_S9 = k[1] ^ BitArray('0xffffffff') ^ IV[3]
    LFSR_S8 = k[0] ^ BitArray('0xffffffff')
    LFSR_S7 = k[3]
    LFSR_S6 = k[2]
    LFSR_S5 = k[1]
    LFSR_S4 = k[0]
    LFSR_S3 = k[3] ^ BitArray('0xffffffff')
    LFSR_S2 = k[2] ^ BitArray('0xffffffff')
    LFSR_S1 = k[1] ^ BitArray('0xffffffff')
    LFSR_S0 = k[0] ^ BitArray('0xffffffff')
    FSM_R1 = BitArray('0x00000000')
    FSM_R2 = BitArray('0x00000000')
    for i in range(32):
        F = ClockFSM()
        Clock_init_LFSR(F)

def Initialize256(k, IV):
    global LFSR_S0, LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10, LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15, FSM_R1, FSM_R2
    LFSR_S15 = k[7] ^ IV[0]
    LFSR_S14 = k[6]
    LFSR_S13 = k[5]
    LFSR_S12 = k[4] ^ IV[1]
    LFSR_S11 = k[3]
    LFSR_S10 = k[2] ^ IV[2]
    LFSR_S9 = k[1] ^ IV[3]
    LFSR_S8 = k[0]
    LFSR_S7 = k[7] ^ BitArray('0xffffffff')
    LFSR_S6 = k[6] ^ BitArray('0xffffffff')
    LFSR_S5 = k[5] ^ BitArray('0xffffffff')
    LFSR_S4 = k[4] ^ BitArray('0xffffffff')
    LFSR_S3 = k[3] ^ BitArray('0xffffffff')
    LFSR_S2 = k[2] ^ BitArray('0xffffffff')
    LFSR_S1 = k[1] ^ BitArray('0xffffffff')
    LFSR_S0 = k[0] ^ BitArray('0xffffffff')
    FSM_R1 = BitArray('0x00000000')
    FSM_R2 = BitArray('0x00000000')
    for i in range(32):
        F = ClockFSM()
        Clock_init_LFSR(F)

def GenerateKeystream(n):
    ClockFSM()
    Clock_work_LFSR()
    z = []

    for d in range(n):
        F = ClockFSM()
        z.append(F^LFSR_S0)
        Clock_work_LFSR()
    return z


def Clock_init_LFSR(F):
    global LFSR_S0, LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10, LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15
    # v = F ^ MUL_alpha(LFSR_S0) ^ LFSR_S2 ^ DIV_alpha(LFSR_S11)
    v = ((LFSR_S0 << 8) ^ MUL_alpha(BitArray(LFSR_S0)) ^ (LFSR_S2) ^ (LFSR_S11 >> 8) ^ DIV_alpha(BitArray(LFSR_S11)) ^ F)
    LFSR_S0 = LFSR_S1
    LFSR_S1 = LFSR_S2
    LFSR_S2 = LFSR_S3
    LFSR_S3 = LFSR_S4
    LFSR_S4 = LFSR_S5
    LFSR_S5 = LFSR_S6
    LFSR_S6 = LFSR_S7
    LFSR_S7 = LFSR_S8
    LFSR_S8 = LFSR_S9
    LFSR_S9 = LFSR_S10
    LFSR_S10 = LFSR_S11
    LFSR_S11 = LFSR_S12
    LFSR_S12 = LFSR_S13
    LFSR_S13 = LFSR_S14
    LFSR_S14 = LFSR_S15
    LFSR_S15 = v


# zegar działaanie
def Clock_work_LFSR():
    global LFSR_S0, LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10,LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15
    # v = MUL_alpha(LFSR_S0) ^ LFSR_S2 ^ DIV_alpha(LFSR_S11)
    v = ((LFSR_S0 << 8) ^ MUL_alpha(BitArray(LFSR_S0)) ^ (LFSR_S2) ^ (LFSR_S11 >> 8) ^ DIV_alpha(BitArray(LFSR_S11)))
    LFSR_S0 = LFSR_S1
    LFSR_S1 = LFSR_S2
    LFSR_S2 = LFSR_S3
    LFSR_S3 = LFSR_S4
    LFSR_S4 = LFSR_S5
    LFSR_S5 = LFSR_S6
    LFSR_S6 = LFSR_S7
    LFSR_S7 = LFSR_S8
    LFSR_S8 = LFSR_S9
    LFSR_S9 = LFSR_S10
    LFSR_S10 = LFSR_S11
    LFSR_S11 = LFSR_S12
    LFSR_S12 = LFSR_S13
    LFSR_S13 = LFSR_S14
    LFSR_S14 = LFSR_S15
    LFSR_S15 = v


# zegar fsm
def ClockFSM():
    global FSM_R1, FSM_R2, LFSR_S5, LFSR_S15
    x = LFSR_S15.uint + FSM_R1.uint
    x %= 4294967296 # 4294967296=2**32
    F = Trim_32(BitArray(hex(x))) ^ FSM_R2 # 4294967296=2**32
    temp = LFSR_S5.uint + FSM_R2.uint
    temp %= 4294967296
    FSM_R2 = S(FSM_R1)
    FSM_R1 = Trim_32(BitArray(hex(temp)))
    return F


LFSR_S0 = BitArray('0x00000000')
LFSR_S1 = BitArray('0x00000000')
LFSR_S2 = BitArray('0x00000000')
LFSR_S3 = BitArray('0x00000000')
LFSR_S4 = BitArray('0x00000000')
LFSR_S5 = BitArray('0x00000000')
LFSR_S6 = BitArray('0x00000000')
LFSR_S7 = BitArray('0x00000000')
LFSR_S8 = BitArray('0x00000000')
LFSR_S9 = BitArray('0x00000000')
LFSR_S10 = BitArray('0x00000000')
LFSR_S11 = BitArray('0x00000000')
LFSR_S12 = BitArray('0x00000000')
LFSR_S13 = BitArray('0x00000000')
LFSR_S14 = BitArray('0x00000000')
LFSR_S15 = BitArray('0x00000000')

# deklaracja 32 bitowego FSM:
FSM_R1 = BitArray('0x00000000')
FSM_R2 = BitArray('0x00000000')
s = BitArray('0xFFFFFFFF') # 4,294,967,295



# ______________________________________________________________________________________________________________________
# Konfiguracja

# wybór trybu testów:
# 1 - sprawdzenie wektorów testowych 128 bitowych,
# 2 - sprawdzenie wektorów testowych 256 bitowych
# 3 - testy średniej szybkości iinicjalizacji
# 4 - testy średniej szybkości generacji keystreamu
# 5 - testy średniej szybkości generacji ciphertextu SNOW 2.0.py
# 6 - testy średniej szybkości generacji ciphertextu RC4.c
# 7 - testy średniej szybkości generacji ciphertextu Salsa20.c
# 8 - testy średniej szybkości generacji ciphertextu RC4.py

tryb = 4


# ___________________________________________________________________________________________________________________
# Działanie dla wektorów testowych 128bit:
if tryb == 1:
    key = BitArray('0x80000000000000000000000000000000')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    start_time = time.time()
    Initialize128(k, iv)
    keystream = GenerateKeystream(5)
    end_time = time.time()
    print(keystream)
    print("Powinno wyjść: 8D590AE9, A74A7D05, 6DC9CA74, B72D1A45, 99B0A083")
    print(f'Czas szyfrowania: {end_time-start_time}')

    key = BitArray('0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    start_time = time.time()
    Initialize128(k, iv)
    keystream = GenerateKeystream(5)
    end_time = time.time()
    print(keystream)
    print("Powinno wyjść: E00982F5, 25F02054, 214992D8, 706F2B20, DA585E5B")
    print(f'Czas szyfrowania: {end_time-start_time}')

    key = BitArray('0x80000000000000000000000000000000')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000004'), BitArray('0x00000003'), BitArray('0x00000002'), BitArray('0x00000001')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    start_time = time.time()
    Initialize128(k, iv)
    keystream = GenerateKeystream(5)
    end_time = time.time()
    print(keystream)
    print("Powinno wyjść: D6403358, E0354A69, 57F43FCE, 44B4B13F, F78E24C2")
    print(f'Czas szyfrowania: {end_time-start_time}')

    key = BitArray('0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000004'), BitArray('0x00000003'), BitArray('0x00000002'), BitArray('0x00000001')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    start_time = time.time()
    Initialize128(k, iv)
    keystream = GenerateKeystream(5)
    end_time = time.time()
    print(keystream)
    print("Powinno wyjść: C355385D, B31D6CBD, F774AF53, 66C2E877, 4DEADAC7")
    print(f'Czas szyfrowania: {end_time-start_time}')
# _____________________________________________________________________________________________________________________
# Działanie dla wektorów testowych 256bit:
if tryb == 2:
    key = BitArray('0x8000000000000000000000000000000000000000000000000000000000000000')
    k = [key[224:], key[192:224], key[160:192], key[128:160], key[96:128], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    start_time = time.time()
    Initialize256(k, iv)
    keystream = GenerateKeystream(5)
    end_time = time.time()
    print(keystream)
    print("Powinno wyjść: 0B5BCCE2, 0323E28E, 0FC20380, 9C66AB73, CA35A680")
    print(f'Czas szyfrowania: {end_time-start_time}')

    key = BitArray('0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    k = [key[224:], key[192:224], key[160:192], key[128:160], key[96:128], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    start_time = time.time()
    Initialize256(k, iv)
    keystream = GenerateKeystream(5)
    end_time = time.time()
    print(keystream)
    print("Powinno wyjść: D9CC22FD, 861492D0, AE6F43FB, 0F072012, 078C5AEE")
    print(f'Czas szyfrowania: {end_time-start_time}')

    key = BitArray('0x8000000000000000000000000000000000000000000000000000000000000000')
    k = [key[224:], key[192:224], key[160:192], key[128:160], key[96:128], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000004'), BitArray('0x00000003'), BitArray('0x00000002'), BitArray('0x00000001')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    start_time = time.time()
    Initialize256(k, iv)
    keystream = GenerateKeystream(5)
    end_time = time.time()
    print(keystream)
    print("Powinno wyjść: 7861080D, 5755E90B, 736F1091, 6ED519B1, 2C1A3A42")
    print(f'Czas szyfrowania: {end_time-start_time}')

    key = BitArray('0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    k = [key[224:], key[192:224], key[160:192], key[128:160], key[96:128], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000004'), BitArray('0x00000003'), BitArray('0x00000002'), BitArray('0x00000001')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    start_time = time.time()
    Initialize256(k, iv)
    keystream = GenerateKeystream(5)
    end_time = time.time()
    print(keystream)
    print("Powinno wyjść: 29261FCE, 5ED03820, 1D6AFAF8, B87E74FE, D49ECB10")
    print(f'Czas szyfrowania: {end_time-start_time}')
# _____________________________________________________________________________________________________________________
# Test czasu inicjalizacji
if tryb == 3:
    key = BitArray(long_to_bytes(random.getrandbits(128)))
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    for i in range(100):
        start_time = time.time()
        Initialize128(k, iv)
        time_taken.append(time.time()-start_time)
    mean = statistics.mean(time_taken)
    print("Średni czas inicjalizacji dla klucza 128 bitowego: ")
    print(mean)

    key = BitArray(long_to_bytes(random.getrandbits(128)))
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000004'), BitArray('0x00000003'), BitArray('0x00000002'), BitArray('0x00000001')] # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    for i in range(100):
        start_time = time.time()
        Initialize128(k, iv)
        time_taken.append(time.time()-start_time)
    mean = statistics.mean(time_taken)
    print("Średni czas inicjalizacji dla klucza 128 bitowego: ")
    print(mean)

    key = BitArray(long_to_bytes(random.getrandbits(256)))
    k = [key[224:], key[192:224], key[160:192], key[128:160], key[96:128], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    for i in range(100):
        start_time = time.time()
        Initialize256(k, iv)
        time_taken.append(time.time()-start_time)
    mean = statistics.mean(time_taken)
    print("Średni czas inicjalizacji dla klucza 256 bitowego: ")
    print(mean)

    key = BitArray(long_to_bytes(random.getrandbits(256)))
    k = [key[224:], key[192:224], key[160:192], key[128:160], key[96:128], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000004'), BitArray('0x00000003'), BitArray('0x00000002'), BitArray('0x00000001')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    for i in range(100):
        start_time = time.time()
        Initialize256(k, iv)
        time_taken.append(time.time()-start_time)
    mean = statistics.mean(time_taken)
    print("Średni czas inicjalizacji dla klucza 256 bitowego: ")
    print(mean)
# _____________________________________________________________________________________________________________________
# Test czasu generacji keystreamu
if tryb == 4:
    key = BitArray('0x80000000000000000000000000000000')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    Initialize128(k, iv)
    for i in range(1000):
        start_time = time.time()
        keystream = GenerateKeystream(1)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("32 bity keystreamu generowane średnio co: ")
    print(mean)

    key = BitArray('0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    Initialize128(k, iv)
    for i in range(1000):
        start_time = time.time()
        keystream = GenerateKeystream(1)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("32 bity keystreamu generowane średnio co: " )
    print(mean)

    key = BitArray('0x80000000000000000000000000000000')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    Initialize128(k, iv)
    for i in range(500):
        start_time = time.time()
        keystream = GenerateKeystream(4)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("128 bity keystreamu generowane średnio co: ")
    print(mean)

    key = BitArray('0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    Initialize128(k, iv)
    for i in range(500):
        start_time = time.time()
        keystream = GenerateKeystream(4)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("128 bity keystreamu generowane średnio co: ")
    print(mean)


    key = BitArray('0x80000000000000000000000000000000')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    Initialize128(k, iv)
    for i in range(200):
        start_time = time.time()
        keystream = GenerateKeystream(8)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("256 bity keystreamu generowane średnio co: ")
    print(mean)

    key = BitArray('0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    Initialize128(k, iv)
    for i in range(200):
        start_time = time.time()
        keystream = GenerateKeystream(8)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("256 bity keystreamu generowane średnio co: " )
    print(mean)

    key = BitArray('0x80000000000000000000000000000000')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    Initialize128(k, iv)
    for i in range(100):
        start_time = time.time()
        keystream = GenerateKeystream(32)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("1024 bity keystreamu generowane średnio co: ")
    print(mean)

    key = BitArray('0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'),
          BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    Initialize128(k, iv)
    for i in range(100):
        start_time = time.time()
        keystream = GenerateKeystream(32)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("1024 bity keystreamu generowane średnio co: ")
    print(mean)
# _____________________________________________________________________________________________________________________
# Test czasu generacji ciphertextu SNOW 2.0
if tryb == 5:
    # plaintext 128 znaków - 1024bity
    key = BitArray(long_to_bytes(random.getrandbits(128)))
    k = [key[96:], key[64:96], key[32:64], key[:32]]
    IV = [BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000'), BitArray('0x00000000')]  # (IV3,IV2,IV1,IV0)
    iv = [IV[3], IV[2], IV[1], IV[0]]
    time_taken = []
    for i in range(100):
        plaintext = long_to_bytes(random.getrandbits(1024))
        plaintext = BitArray(plaintext)
        start_time = time.time()
        Initialize128(k,iv)
        stream = GenerateKeystream(32)
        keystream = ''
        for j in stream:
            keystream+=j
        ciphertext = plaintext ^ keystream
        time_taken.append(time.time() - start_time)
    mean=statistics.mean(time_taken)
    print("średni czas wygenerowania 1024 bitowego ciphertextu przez SNOW2: ")
    print(mean)

    time_taken = []
    for i in range(10):
        plaintext = long_to_bytes(random.getrandbits(8192))
        plaintext = BitArray(plaintext)
        start_time = time.time()
        Initialize128(k, iv)
        stream = GenerateKeystream(256)
        keystream = ''
        for j in stream:
            keystream += j
        ciphertext = plaintext ^ keystream
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 8192 bitowego ciphertextu przez SNOW2: ")
    print(mean)

    time_taken = []
    for i in range(5):
        plaintext = long_to_bytes(random.getrandbits(32768))
        plaintext = BitArray(plaintext)
        start_time = time.time()
        Initialize128(k, iv)
        stream = GenerateKeystream(1024)
        keystream = ''
        for j in stream:
            keystream += j
        ciphertext = plaintext ^ keystream
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 32768 bitowego ciphertextu przez SNOW2: ")
    print(mean)
# _____________________________________________________________________________________________________________________
# Test czasu generacji ciphertextu RC4
if tryb == 6:
    key = long_to_bytes(random.getrandbits(128))
    tempkey = SHA.new(key).digest()
    time_taken = []
    for i in range(500):
        plaintext = long_to_bytes(random.getrandbits(1024))
        start_time = time.time()
        cipher = ARC4.new(tempkey)
        ciphertext = cipher.encrypt(plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 1024 bitowego ciphertextu przez RC4: ")
    print(mean)

    key = long_to_bytes(random.getrandbits(128))
    tempkey = SHA.new(key).digest()
    time_taken = []
    for i in range(500):
        plaintext = long_to_bytes(random.getrandbits(8192))
        start_time = time.time()
        cipher = ARC4.new(tempkey)
        ciphertext = cipher.encrypt(plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 8192 bitowego ciphertextu przez RC4: ")
    print(mean)

    key = long_to_bytes(random.getrandbits(128))
    tempkey = SHA.new(key).digest()
    time_taken = []
    for i in range(500):
        plaintext = long_to_bytes(random.getrandbits(32768))
        start_time = time.time()
        cipher = ARC4.new(tempkey)
        ciphertext = cipher.encrypt(plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 32768 bitowego ciphertextu przez RC4: ")
    print(mean)
# _____________________________________________________________________________________________________________________
# Test czasu generacji ciphertextu Salsa20
if tryb == 7:
    key = long_to_bytes(random.getrandbits(256))
    time_taken = []
    for i in range(500):
        plaintext = long_to_bytes(random.getrandbits(1024))
        start_time = time.time()
        cipher = Salsa20.new(key=key)
        ciphertext = cipher.encrypt(plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 1024 bitowego ciphertextu przez Salsa20: ")
    print(mean)

    key = long_to_bytes(random.getrandbits(256))
    time_taken = []
    for i in range(500):
        plaintext = long_to_bytes(random.getrandbits(8192))
        start_time = time.time()
        cipher = Salsa20.new(key=key)
        ciphertext = cipher.encrypt(plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 8192 bitowego ciphertextu przez Salsa20: ")
    print(mean)

    key = long_to_bytes(random.getrandbits(256))
    time_taken = []
    for i in range(500):
        plaintext = long_to_bytes(random.getrandbits(32768))
        start_time = time.time()
        cipher = Salsa20.new(key=key)
        ciphertext = cipher.encrypt(plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 32768 bitowego ciphertextu przez Salsa20: ")
    print(mean)
# _____________________________________________________________________________________________________________________
# Test czasu generacji ciphertextu RC4
if tryb == 8:
    key = str(long_to_bytes(random.getrandbits(128)),'iso-8859-15')
    time_taken = []
    for i in range(500):
        plaintext = long_to_bytes(random.getrandbits(1024))
        plaintext = str(plaintext,'iso-8859-15')
        start_time = time.time()
        ciphertext = RC4.encrypt(key,plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 1024 bitowego ciphertextu przez RC4: ")
    print(mean)

    key = str(long_to_bytes(random.getrandbits(128)),'iso-8859-15')
    time_taken = []
    for i in range(100):
        plaintext = long_to_bytes(random.getrandbits(8192))
        plaintext = str(plaintext, 'iso-8859-15')
        start_time = time.time()
        ciphertext = RC4.encrypt(key,plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 8192 bitowego ciphertextu przez RC4: ")
    print(mean)

    key = str(long_to_bytes(random.getrandbits(128)),'iso-8859-15')
    time_taken = []
    for i in range(100):
        plaintext = long_to_bytes(random.getrandbits(32768))
        plaintext = str(plaintext, 'iso-8859-15')
        start_time = time.time()
        ciphertext = RC4.encrypt(key,plaintext)
        time_taken.append(time.time() - start_time)
    mean = statistics.mean(time_taken)
    print("średni czas wygenerowania 32768 bitowego ciphertextu przez RC4: ")
    print(mean)