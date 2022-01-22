from bitstring import BitArray, BitStream
import tabele
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
    result = (a^tabele.snow_alpha_mul[index])
    return result


def MUL_alpha_iverted(w):
    index = (w & 0xFF)
    a = w>>8
    result = a^tabele.snow_alpha_mul_inv[index]
    return result

def S(w):
    r0,r1,r2,r3 = 0,0,0,0
    #todo naprawa
    srw0=SR[(w[:8]).uint]
    srw1=SR[(w[8:16]).uint]
    srw2=SR[(w[16:24]).uint]
    srw3=SR[(w[24:]).uint]

    srw0_new=BitArray(srw0)
    srw1_new=BitArray(srw1)
    srw2_new=BitArray(srw2)
    srw3_new=BitArray(srw3)

    r0=(MULx(srw0_new,cte)^(srw1_new)^(srw2_new)^(MULx(srw3_new,cte)^(srw3_new)))
    r1=((MULx(srw0_new,cte)^(srw0_new))^MULx(srw1_new,cte)^(srw2_new)^(srw3_new))
    r2=((srw0_new)^(MULx(srw1_new,cte)^(srw1_new))^MULx(srw2_new,cte)^(srw3_new))
    r3=((srw0_new)^(srw1_new)^(MULx(srw2_new,cte)^(srw2_new))^MULx(srw3_new,cte))

    return (r0+r1+r2+r3)

def Initialize():
# todo zrobić
