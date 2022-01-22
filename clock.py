from bitstring import BitArray, BitStream
from snow import *

# zegar inicjalizacja
def Clock_init_LFSR(F):
    global LFSR_S0,LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10, LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15
    v = F ^ MUL_alpha(LFSR_S0) ^ LFSR_S2 ^ MUL_alpha_iverted(LFSR_S11) # todo naprawić

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
    v = MUL_alpha(LFSR_S0) ^ LFSR_S2 ^ MUL_alpha_iverted(LFSR_S11) # todo naprawić

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
    F = ((LFSR_S15 + FSM_R1)%4294967296) ^ FSM_R2 # 4294967296=2**32
    temp = (LFSR_S5 + FSM_R2)%4294967296
    FSM_R2 = S(FSM_R1)
    FSM_R1 = temp
    return F