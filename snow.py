from bitstring import BitArray, BitStream
import snow_arrays
import clock

# deklaracja 32 bitowego  LFSR:
LFSR_S0=BitArray('0x00000000')
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
def MUL_alpha(w):
    index = w>>24 # '>>'  	Shift right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off
    a = 0
    for i in range (0,8):
        a = w<<1
        if(a>>32 == 1):
            a^=s+1
    result = (a ^ snow_arrays.snow_alpha_mul[index])
    return result


def MUL_alpha_iverted(w):
    index = (w & 0xFF)
    a = w>>8
    result = a ^ snow_arrays.snow_alpha_mul_inv[index]
    return result


#def SR(x):
    #return (tabele.Sbox[b] for b in x)

def S(w):
    w0 = w[:8]
    w1 = w[8:16]
    w2 = w[16:24]
    w3 = w[24:]

    r = snow_arrays.snow_T0[w0] ^ snow_arrays.snow_T1[w1] ^ snow_arrays.snow_T2[w2] ^ snow_arrays.snow_T3[w3]
    return r

def Initialize(k,IV):
    global LFSR_S0, LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10, LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15, FSM_R1, FSM_R2
    LFSR_S15 = k[3] ^ IV[0]
    LFSR_S14 = k[2]
    LFSR_S13 = k[1]
    LFSR_S12 = k[0] ^ IV[1]
    LFSR_S11 = k[3] ^ 0xffffffff #
    LFSR_S10 = k[2] ^ 0xffffffff ^ IV[2]
    LFSR_S9 = k[1] ^ BitArray('0xffffffff') ^ IV[3]
    LFSR_S8 = k[0] ^ BitArray('0xffffffff')
    LFSR_S7 = k[3]
    LFSR_S6 = k[2]
    LFSR_S5 = k[1]
    LFSR_S4 = k[0]
    LFSR_S3 = k[3] ^ BitArray('0xffffffff')
    LFSR_S2 = k[2] ^ BitArray('0xffffffff')
    LFSR_S1 = k[1] ^ 0xffffffff
    LFSR_S0 = k[0] ^ 0xffffffff
    FSM_R1 = BitArray('0x00000000')
    FSM_R2 = BitArray('0x00000000')
    for i in range(32):
        F = clock.ClockFSM()
        clock.Clock_init_LFSR(F)

def GenerateKeystream(n):
    clock.ClockFSM()
    clock.Clock_work_LFSR()
    z = []

    for d in range(n):
        F = clock.ClockFSM()
        z.append(F^LFSR_S0)
        clock.Clock_work_LFSR()
	return z