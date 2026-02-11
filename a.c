#define run_test_gpio
// #define run_read_gpio

#ifdef run_test_gpio

#include <stdio.h>

#include "board.h"
#include "app.h"
#include "fsl_port.h"

/*
PRINTF_FLOAT_ENABLE=1
SCANF_FLOAT_ENABLE=1
PRINTF_ADVANCED_ENABLE=1
SCANF_ADVANCED_ENABLE=1
*/
#include "fsl_debug_console.h"

void config_pins(void);

int main(void)
{
    BOARD_InitHardware();
    prepare();

    PRINTF("MCUX SDK version: %s\r\n", MCUXSDK_VERSION_FULL_STR);
    PRINTF("start, check:%s\n", "sad1398289");

    config_pins();

    while (1)
    {
    }
}

void config_pins(void)
{
#ifdef PORT_CLOCKS
    clock_ip_name_t clocks[] = PORT_CLOCKS;

    for (int i = 0, size = sizeof(clocks) / sizeof(clocks[0]); i < size; ++i)
    {
        CLOCK_EnableClock(clocks[i]);
    }
#endif

#ifdef PORT_RSTS
    SYSCON_RSTn_t resets[] = PORT_RSTS;
    for (int i = 0, size = sizeof(resets) / sizeof(resets[0]); i < size; ++i)
    {
        RESET_ReleasePeripheralReset(resets[i]);
    }
#endif

    GPIO_Type *gpios[] = GPIO_BASE_PTRS;
    PORT_Type *ports[] = PORT_BASE_PTRS;

    uint8_t pins[4][33] = {
#if 1 // frdmmcxc353
      // gpio 0
        {0xff, 0, 1, 2, 3, 4, 5, 6, 7, 0xff},
        // gpio 1
        {
            3,                  //
            0xff,               //
            0, 1,               //
            2,                  // pwt0 in0
            3, 8,               //    uart1 tx / i2c1 sda / pwm a2
            9, 10, 11, 12, 0xff //
        },
        // gpio 2
        {
#if 0                                                                    // debug console uart0
            0, 1,
#endif
            0xff, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23, 0xff //
        },
        // gpio 3
        {0xff, 0, 1, 2, 3, 12, 13, 14, 15, 27, 28, 0xff},
#endif
#if 0 // kw47
      // gpio a
        {0xff},
        // gpio b
        {0xff},
        // gpio c
        {1, // blue led
         0xff},
        // gpio d
        {0xff},
#endif
    };

    {
        gpio_pin_config_t config = {.pinDirection = kGPIO_DigitalOutput, .outputLogic = 1U};
        for (int i = 0, size = sizeof(gpios) / sizeof(gpios[0]); i < size; ++i)
        {
            for (int j = 0; j < 33; ++j)
            {
                if (pins[i][j] == 0xff)
                {
                    break;
                }
                PRINTF("gpio init <%u, %u>\r\n", i, j);
                GPIO_PinInit(gpios[i], pins[i][j], &config);
            }
        }
    }
    {
        const port_pin_config_t config = {
            .pullSelect          = kPORT_PullDisable,
            .pullValueSelect     = kPORT_LowPullResistor,
            .slewRate            = kPORT_FastSlewRate,
            .passiveFilterEnable = kPORT_PassiveFilterDisable,
            .openDrainEnable     = kPORT_OpenDrainDisable,
            .driveStrength       = kPORT_LowDriveStrength,
            .driveStrength1      = kPORT_NormalDriveStrength,
            .mux                 = kPORT_MuxAsGpio, // 0/1
#if defined(FSL_FEATURE_PORT_HAS_INPUT_BUFFER) && FSL_FEATURE_PORT_HAS_INPUT_BUFFER
            .inputBuffer = kPORT_InputBufferEnable,
#endif
            .invertInput  = kPORT_InputNormal,
            .lockRegister = kPORT_UnlockRegister
            //
        };
        for (int i = 0, size = sizeof(ports) / sizeof(ports[0]); i < size; ++i)
        {
            for (int j = 0; j < 33; ++j)
            {
                if (pins[i][j] == 0xff)
                {
                    break;
                }
                PRINTF("port set <%u, %u>\r\n", i, j);
                PORT_SetPinConfig(ports[i], pins[i][j], &config);
            }
        }
    }
    PRINTF("have initialized all pins as gpio\r\n");
}

#endif /* end of run_test_gpio */

#ifdef run_read_gpio

#endif
