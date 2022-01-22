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
    index = (w and 0xFF)
    a = w>>8
    result = a^tabele.snow_alpha_mul_inv[index]
    return result

  

def Initialize():
# todo zrobić
