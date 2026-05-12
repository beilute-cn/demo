// #define origin
#define modify

#ifdef origin
/*
 * Copyright (c) 2015, Freescale Semiconductor, Inc.
 * Copyright 2016-2022 NXP
 * All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "fsl_debug_console.h"
#include "board.h"
#include "app.h"
#include "fsl_pwm.h"

/*******************************************************************************
 * Definitions
 ******************************************************************************/
/* Definition for default PWM frequence in hz. */
#ifndef APP_DEFAULT_PWM_FREQUENCY
#define APP_DEFAULT_PWM_FREQUENCY (1000UL)
#endif

/* DEMO_PWM_DISABLE_MAP_OP: Operator, it can be define as '~') in app.h */
#ifndef DEMO_PWM_DISABLE_MAP_OP
#define DEMO_PWM_DISABLE_MAP_OP
#endif
/*******************************************************************************
 * Prototypes
 ******************************************************************************/

/*******************************************************************************
 * Variables
 ******************************************************************************/

/*******************************************************************************
 * Code
 ******************************************************************************/
static void PWM_DRV_Init3PhPwm(void)
{
    uint16_t deadTimeVal;
    pwm_signal_param_t pwmSignal[2];
    uint32_t pwmSourceClockInHz;
    uint32_t pwmFrequencyInHz = APP_DEFAULT_PWM_FREQUENCY;

    pwmSourceClockInHz = PWM_SRC_CLK_FREQ;

    /* Set deadtime count, we set this to about 650ns */
    deadTimeVal = ((uint64_t)pwmSourceClockInHz * 650) / 1000000000;

    pwmSignal[0].pwmChannel       = kPWM_PwmA;
    pwmSignal[0].level            = kPWM_HighTrue;
    pwmSignal[0].dutyCyclePercent = 50; /* 1 percent dutycycle */
    pwmSignal[0].deadtimeValue    = deadTimeVal;
    pwmSignal[0].faultState       = kPWM_PwmFaultState0;
    pwmSignal[0].pwmchannelenable = true;

    pwmSignal[1].pwmChannel = kPWM_PwmB;
    pwmSignal[1].level      = kPWM_HighTrue;
    /* Dutycycle field of PWM B does not matter as we are running in PWM A complementary mode */
    pwmSignal[1].dutyCyclePercent = 50;
    pwmSignal[1].deadtimeValue    = deadTimeVal;
    pwmSignal[1].faultState       = kPWM_PwmFaultState0;
    pwmSignal[1].pwmchannelenable = true;

    /*********** PWMA_SM0 - phase A, configuration, setup 2 channel as an example ************/
    PWM_SetupPwm(BOARD_PWM_BASEADDR, kPWM_Module_0, pwmSignal, 2, kPWM_SignedCenterAligned, pwmFrequencyInHz,
                 pwmSourceClockInHz);

    /*********** PWMA_SM1 - phase B configuration, setup PWM A channel only ************/
#ifdef DEMO_PWM_CLOCK_DEVIDER
    PWM_SetupPwm(BOARD_PWM_BASEADDR, kPWM_Module_1, pwmSignal, 1, kPWM_SignedCenterAligned, pwmFrequencyInHz,
                 pwmSourceClockInHz / (1 << DEMO_PWM_CLOCK_DEVIDER));
#else
    PWM_SetupPwm(BOARD_PWM_BASEADDR, kPWM_Module_1, pwmSignal, 1, kPWM_SignedCenterAligned, pwmFrequencyInHz,
                 pwmSourceClockInHz);
#endif

    /*********** PWMA_SM2 - phase C configuration, setup PWM A channel only ************/
#ifdef DEMO_PWM_CLOCK_DEVIDER
    PWM_SetupPwm(BOARD_PWM_BASEADDR, kPWM_Module_2, pwmSignal, 1, kPWM_SignedCenterAligned, pwmFrequencyInHz,
                 pwmSourceClockInHz / (1 << DEMO_PWM_CLOCK_DEVIDER));
#else
    PWM_SetupPwm(BOARD_PWM_BASEADDR, kPWM_Module_2, pwmSignal, 1, kPWM_SignedCenterAligned, pwmFrequencyInHz,
                 pwmSourceClockInHz);
#endif
}

/*!
 * @brief Main function
 */
int main(void)
{
    /* Structure of initialize PWM */
    pwm_config_t pwmConfig;
    pwm_fault_param_t faultConfig;
    uint32_t pwmVal = 4;

    /* Board pin, clock, debug console init */
    BOARD_InitHardware();

    PRINTF("MCUX SDK version: %s\r\n", MCUXSDK_VERSION_FULL_STR);

    PRINTF("FlexPWM driver example\n");
    /*
     * pwmConfig.enableDebugMode = false;
     * pwmConfig.enableWait = false;
     * pwmConfig.reloadSelect = kPWM_LocalReload;
     * pwmConfig.clockSource = kPWM_BusClock;
     * pwmConfig.prescale = kPWM_Prescale_Divide_1;
     * pwmConfig.initializationControl = kPWM_Initialize_LocalSync;
     * pwmConfig.forceTrigger = kPWM_Force_Local;
     * pwmConfig.reloadFrequency = kPWM_LoadEveryOportunity;
     * pwmConfig.reloadLogic = kPWM_ReloadImmediate;
     * pwmConfig.pairOperation = kPWM_Independent;
     */
    PWM_GetDefaultConfig(&pwmConfig);

#ifdef DEMO_PWM_CLOCK_DEVIDER
    pwmConfig.prescale = DEMO_PWM_CLOCK_DEVIDER;
#endif

    /* Use full cycle reload */
    pwmConfig.reloadLogic = kPWM_ReloadPwmFullCycle;
    /* PWM A & PWM B form a complementary PWM pair */
    pwmConfig.pairOperation   = kPWM_ComplementaryPwmA;
    pwmConfig.enableDebugMode = true;

    /* Initialize submodule 0 */
    if (PWM_Init(BOARD_PWM_BASEADDR, kPWM_Module_0, &pwmConfig) == kStatus_Fail)
    {
        PRINTF("PWM initialization failed\n");
        return 1;
    }

    /* Initialize submodule 1, make it use same counter clock as submodule 0. */
    pwmConfig.clockSource           = kPWM_Submodule0Clock;
    pwmConfig.prescale              = kPWM_Prescale_Divide_1;
    pwmConfig.initializationControl = kPWM_Initialize_MasterSync;
    if (PWM_Init(BOARD_PWM_BASEADDR, kPWM_Module_1, &pwmConfig) == kStatus_Fail)
    {
        PRINTF("PWM initialization failed\n");
        return 1;
    }

    /* Initialize submodule 2 the same way as submodule 1 */
    if (PWM_Init(BOARD_PWM_BASEADDR, kPWM_Module_2, &pwmConfig) == kStatus_Fail)
    {
        PRINTF("PWM initialization failed\n");
        return 1;
    }

    /*
     *   config->faultClearingMode = kPWM_Automatic;
     *   config->faultLevel = false;
     *   config->enableCombinationalPath = true;
     *   config->recoverMode = kPWM_NoRecovery;
     */
    PWM_FaultDefaultConfig(&faultConfig);

#ifdef DEMO_PWM_FAULT_LEVEL
    faultConfig.faultLevel = DEMO_PWM_FAULT_LEVEL;
#endif
    /* Sets up the PWM fault protection */
    PWM_SetupFaults(BOARD_PWM_BASEADDR, kPWM_Fault_0, &faultConfig);
    PWM_SetupFaults(BOARD_PWM_BASEADDR, kPWM_Fault_1, &faultConfig);
    PWM_SetupFaults(BOARD_PWM_BASEADDR, kPWM_Fault_2, &faultConfig);
    PWM_SetupFaults(BOARD_PWM_BASEADDR, kPWM_Fault_3, &faultConfig);

    /* Set PWM fault disable mapping for submodule 0/1/2 */
    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_0, kPWM_PwmA, kPWM_faultchannel_0,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));
    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_1, kPWM_PwmA, kPWM_faultchannel_0,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));
    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_2, kPWM_PwmA, kPWM_faultchannel_0,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));

#if defined(FSL_FEATURE_PWM_FAULT_CH_COUNT) && (FSL_FEATURE_PWM_FAULT_CH_COUNT > 1)
    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_0, kPWM_PwmA, kPWM_faultchannel_1,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));
    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_1, kPWM_PwmA, kPWM_faultchannel_1,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));
    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_2, kPWM_PwmA, kPWM_faultchannel_1,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));

    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_0, kPWM_PwmB, kPWM_faultchannel_1,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));
    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_1, kPWM_PwmB, kPWM_faultchannel_1,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));
    PWM_SetupFaultDisableMap(
        BOARD_PWM_BASEADDR, kPWM_Module_2, kPWM_PwmB, kPWM_faultchannel_1,
        DEMO_PWM_DISABLE_MAP_OP(kPWM_FaultDisable_0 | kPWM_FaultDisable_1 | kPWM_FaultDisable_2 | kPWM_FaultDisable_3));
#endif

    /*
     * Call the init function with demo configuration.
     * Recommend to invoke API PWM_SetupPwm after PWM and fault configuration, because reference manual advises to
     * set OUTEN register after other PWM configurations. But set OUTEN register before MCTRL register is okay.
     */
    PWM_DRV_Init3PhPwm();

    /* Set the load okay bit for all submodules to load registers from their buffer */
    PWM_SetPwmLdok(BOARD_PWM_BASEADDR, kPWM_Control_Module_0 | kPWM_Control_Module_1 | kPWM_Control_Module_2, true);

    /* Start the PWM generation from Submodules 0, 1 and 2 */
    PWM_StartTimer(BOARD_PWM_BASEADDR, kPWM_Control_Module_0 | kPWM_Control_Module_1 | kPWM_Control_Module_2);

    while (1U)
    {
        /* Delay at least 100 PWM periods. */
        SDK_DelayAtLeastUs((1000000U / APP_DEFAULT_PWM_FREQUENCY) * 100, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);

        pwmVal = pwmVal + 4;
        pwmVal = 33;

        /* Reset the duty cycle percentage */
        if (pwmVal > 100)
        {
            pwmVal = 4;
        }

        /* Update duty cycles for all 3 PWM signals */
        PWM_UpdatePwmDutycycle(BOARD_PWM_BASEADDR, kPWM_Module_0, kPWM_PwmA, kPWM_SignedCenterAligned, pwmVal);
        PWM_UpdatePwmDutycycle(BOARD_PWM_BASEADDR, kPWM_Module_1, kPWM_PwmA, kPWM_SignedCenterAligned, (pwmVal >> 1));
        PWM_UpdatePwmDutycycle(BOARD_PWM_BASEADDR, kPWM_Module_2, kPWM_PwmA, kPWM_SignedCenterAligned, (pwmVal >> 2));

        /* Set the load okay bit for all submodules to load registers from their buffer */
        PWM_SetPwmLdok(BOARD_PWM_BASEADDR, kPWM_Control_Module_0 | kPWM_Control_Module_1 | kPWM_Control_Module_2, true);
    }
}
#endif

#ifdef modify
#include <stdio.h>

#include "app.h"
#include "board.h"
#include "fsl_debug_console.h"

int main(void)
{
    BOARD_InitHardware();
    PRINTF("test printf start\r\n");
    printf("[%u]> %u\n", __LINE__, 12u);
    printf("[%u]> %d\n", __LINE__, 12);
    printf("[%u]> %d\n", __LINE__, -12);
    printf("[%u]> %f\n", __LINE__, 3.14);
    printf("[%u]> %g\n", __LINE__, 3.14);
    PRINTF("test printf end\r\n");

    CLOCK_EnableClock(kCLOCK_Pwm1);
    RESET_ReleasePeripheralReset(kPWM1_RST_SHIFT_RSTn);

#if 0
    volatile uint8_t *p = (volatile uint8_t *)PWM1;

    for (int i = 0, size = sizeof(PWM_Type); i < size; i += 2)
    {
        printf("[0x%3x] = 0x%04x\n", i, *(volatile uint16_t *)(p + i));
    }
#endif

    PWM_Type *pwm = PWM1;

    // TODO if half/full are both 0, will it reload?
    pwm->SM[0].CTRL = PWM_CTRL_FULL_MASK;

    // 33%
#if 0
    uint16_t _3_3 = 30000;
    uint16_t _1_3 = _3_3 / 3;
    uint16_t _2_3 = _1_3 << 1;

    pwm->SM[0].VAL1 = _3_3;
    pwm->SM[0].VAL3 = _2_3;
    pwm->SM[0].VAL5 = _1_3;
    pwm->SM[0].VAL0 = 0;
    pwm->SM[0].VAL4 = (uint16_t)-_1_3;
    pwm->SM[0].VAL2 = (uint16_t)-_2_3;
    pwm->SM[0].INIT = (uint16_t)-_3_3;
#endif
    // 50%
#if 1
    uint16_t _2_2 = 30000;
    uint16_t _1_2 = _2_2 >> 1;

    pwm->SM[0].VAL1 = _2_2;
    pwm->SM[0].VAL3 = _1_2;
    pwm->SM[0].VAL5 = _1_2;
    pwm->SM[0].VAL0 = 0;
    pwm->SM[0].VAL4 = (uint16_t)-_1_2;
    pwm->SM[0].VAL2 = (uint16_t)-_1_2;
    pwm->SM[0].INIT = (uint16_t)-_2_2;
#endif
    printf(
        "VAL1=%d\n"
        "VAL3=%d\n"
        "VAL5=%d\n"
        "VAL0=%d\n"
        "VAL4=%d\n"
        "VAL2=%d\n"
        "INIT=%d\n",
        (int16_t)pwm->SM[0].VAL1, //
        (int16_t)pwm->SM[0].VAL3, //
        (int16_t)pwm->SM[0].VAL5, //
        (int16_t)pwm->SM[0].VAL0, //
        (int16_t)pwm->SM[0].VAL4, //
        (int16_t)pwm->SM[0].VAL2, //
        (int16_t)pwm->SM[0].INIT  //
    );

    pwm->SM[0].CTRL2 |= PWM_CTRL2_DBGEN_MASK;

    /*
        150M -> 1/150 us
        1us -> 150
    */
    pwm->SM[0].DTCNT0 = 150;
    pwm->SM[0].DTCNT1 = 150;
    // ----------------

    pwm->OUTEN |= 0x710;
    // pwm->OUTEN |= PWM_OUTEN_PWMA_EN(1);

    // pwm->FCTRL = 0xff00;
    pwm->FCTRL = 0xf000;
    pwm->FSTS  = 0xf;

    uint32_t cnt = 0;
    do
    {
        pwm->MCTRL = 7;
        ++cnt;
    } while (pwm->MCTRL != 7);
    printf("assign MCTRL count = %u\n", cnt);

    pwm->MCTRL |= PWM_MCTRL_RUN(1);

    int max         = _2_2;
    pwm->SM[0].VAL1 = max;
    pwm->SM[0].VAL0 = 0;
    pwm->SM[0].INIT = (uint16_t)-_2_2;
    int percent     = 0;

    int t1 = 0;
    int t2 = 0;

    while (1)
    {
        t1 = percent * max / 100;
        t2 = max - t2;
        //
        pwm->SM[0].VAL3 = t1;
        pwm->SM[0].VAL5 = t2;
        //
        pwm->SM[0].VAL4 = (uint16_t)-t2;
        pwm->SM[0].VAL2 = (uint16_t)-t1;
        //

        // must load buffer
        pwm->SM[0].CTRL |= PWM_CTRL_LDMOD_MASK;
        pwm->MCTRL |= PWM_MCTRL_LDOK_MASK;

        ++percent;
        percent %= 100;
        SDK_DelayAtLeastUs(10 * 1000, CLOCK_GetCoreSysClkFreq());
        // printf("precent = %d\n", percent);
    }
}
#endif

#if defined(__GNUC__)
int _write(int file, char *ptr, int len)
{
    PRINTF("%s", ptr);
    return len;
}
#elif defined(__ICCARM__)
size_t __write(int handle, const unsigned char *buf, size_t bufSize)
{
    // bufSize == 1
    PRINTF("%c", *buf);
    return bufSize;
}
#endif
