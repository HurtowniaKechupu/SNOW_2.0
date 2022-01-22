import snow
# zegar inicjalizacja
def Clock_init_LFSR():
    # todo nwm
    global LFSR_S0,LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10, LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15
    # todo coś tu dać
    new = 0

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
    LFSR_S15=new


# zegar działaanie
def Clock_work_LFSR():
        # todo zrobić żeby działało
    global LFSR_S0, LFSR_S1, LFSR_S2, LFSR_S3, LFSR_S4, LFSR_S5, LFSR_S6, LFSR_S7, LFSR_S8, LFSR_S9, LFSR_S10,LFSR_S11, LFSR_S12, LFSR_S13, LFSR_S14, LFSR_S15
# todo coś tu dać
    new = 0

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
    LFSR_S15 = new

# zegar fsm
def ClockFSM():
    global FSM_R1, FSM_R2, LFSR_S5, LFSR_S15
    #todo coś tutaj zrobić