from bitstring import BitArray
import snow_arrays


def Trim_32(x):
    temp = BitArray(length=32)
    if (len(x) < 32):
        n = 32 - len(x)
        temp[n:] = x
        return temp
    else:
        return x


def MULx(v,c):
    if v.bin[0]=='1':
        return ((v<<1)^c)
    else:
        return (v<<1)


def MULxPOW(v,i,c):
    if i==0:
        return v
    else:
        return MULx(MULxPOW(v,i-1,c),c)


def MUL_alpha(c):
    c = c[:8]
    x=BitArray('0xa9')
    return ((MULxPOW(c,23,x))+(MULxPOW(c,245,x))+(MULxPOW(c,48,x))+(MULxPOW(c,239,x)))


def DIV_alpha(c):
    c = c[24:]
    x=BitArray('0xa9')
    return ((MULxPOW(c,16,x))+(MULxPOW(c,39,x))+(MULxPOW(c,6,x))+(MULxPOW(c,64,x)))


def S(w):
    w = BitArray(w)
    w3 = w[:8].uint
    w2 = w[8:16].uint
    w1 = w[16:24].uint
    w0 = w[24:].uint
    r = Trim_32(BitArray(snow_arrays.snow_T0[w0])) ^ Trim_32(BitArray(snow_arrays.snow_T1[w1])) ^ Trim_32(BitArray(snow_arrays.snow_T2[w2])) ^ Trim_32(BitArray(snow_arrays.snow_T3[w3]))
    return r


def Initialize(k,IV):
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

def GenerateKeystream(n):
    #todo tu też sprawdzić
    ClockFSM()
    Clock_work_LFSR()
    z = []

    for d in range(n):
        F = ClockFSM()
        z.append(F^LFSR_S0)
        Clock_work_LFSR()
    return z


def Clock_init_LFSR(F):
    global LFSR_S0,LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10, LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15
    #v = F ^ MUL_alpha(LFSR_S0) ^ LFSR_S2 ^ DIV_alpha(LFSR_S11)
    v = ((LFSR_S0 << 8) ^ MUL_alpha(BitArray(LFSR_S0)) ^ (LFSR_S2) ^ (LFSR_S11 >> 8) ^ DIV_alpha(BitArray(LFSR_S11)) ^ F)
    LFSR_S0=LFSR_S1
    LFSR_S1=LFSR_S2
    LFSR_S2=LFSR_S3
    LFSR_S3=LFSR_S4
    LFSR_S4=LFSR_S5
    LFSR_S5=LFSR_S6
    LFSR_S6=LFSR_S7
    LFSR_S7=LFSR_S8
    LFSR_S8=LFSR_S9
    LFSR_S9=LFSR_S10
    LFSR_S10=LFSR_S11
    LFSR_S11=LFSR_S12
    LFSR_S12=LFSR_S13
    LFSR_S13=LFSR_S14
    LFSR_S14=LFSR_S15
    LFSR_S15=v


# zegar działaanie
def Clock_work_LFSR():
    global LFSR_S0, LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10,LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15
    #v = MUL_alpha(LFSR_S0) ^ LFSR_S2 ^ DIV_alpha(LFSR_S11)
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
LFSR_S1=BitArray('0x00000000')
LFSR_S2=BitArray('0x00000000')
LFSR_S3=BitArray('0x00000000')
LFSR_S4=BitArray('0x00000000')
LFSR_S5=BitArray('0x00000000')
LFSR_S6=BitArray('0x00000000')
LFSR_S7=BitArray('0x00000000')
LFSR_S8=BitArray('0x00000000')
LFSR_S9=BitArray('0x00000000')
LFSR_S10=BitArray('0x00000000')
LFSR_S11=BitArray('0x00000000')
LFSR_S12=BitArray('0x00000000')
LFSR_S13=BitArray('0x00000000')
LFSR_S14=BitArray('0x00000000')
LFSR_S15=BitArray('0x00000000')

# deklaracja 32 bitowego FSM:
FSM_R1=BitArray('0x00000000')
FSM_R2=BitArray('0x00000000')
s = BitArray('0xFFFFFFFF') # 4,294,967,295

# ______________________________________________________________________________________________________________________

# E00982F5, 25F02054, 214992D8, 706F2B20, DA585E5B dla AAAAA,(0,0,0,0)
key = [BitArray('0xAAAAAAAA'),BitArray('0xAAAAAAAA'),BitArray('0xAAAAAAAA'),BitArray('0xAAAAAAAA')]
k = [key[3],key[2],key[1],key[0]] # nie wiem czy trzeba odwrócić kolejność czy nie, sprawdzić później
IV = [BitArray('0x00000000'),BitArray('0x00000000'),BitArray('0x00000000'),BitArray('0x00000000')]
iv = [IV[3],IV[2],IV[1],IV[0]]# nie wiem czy trzeba odwrócić kolejność czy nie, sprawdzić później
Initialize(k,iv)
keystream = GenerateKeystream(5)
print(keystream)

