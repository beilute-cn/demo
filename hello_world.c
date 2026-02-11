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

void prepare(void);
void config_pins(void);

#if 0
int scan(char *format, ...);
int print(char *format, ...);
#endif

int main(void)
{
    BOARD_InitHardware();
    prepare();

    PRINTF("MCUX SDK version: %s\r\n", MCUXSDK_VERSION_FULL_STR);
    PRINTF("start, check:%s\n", "sad1398289");
    for (int i = 0; i < 5; ++i)
    {
        printf("test i=%d\n", i);
    }

    config_pins();

    // GPIO2 PIN12 LOW/hight\n

    char buffer[100] = {0};

    while (1)
    {
        memset(buffer, 0, 100);
        scan("%[^\n]\n", buffer);
        print("buffer = %s\n", buffer);
    }
}

void prepare(void)
{
    // 或者让系统自动分配缓冲区
    // setvbuf(stdin, NULL, _IOLBF, 100);
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
            2,                  //
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
#if 0
void f100(void)
{
    PRINTF("test float %6.2f\r\n", 3.1415926);
    int i = -1;
    int j = -1;
    int n = -1;
    int t = -1;
    char buf[100] = "init buffer";
    char b[100] = "hello world";
    PRINTF("i=%d, j=%d, string=%s", i, j, b);
    while (1)
    {
        i = -1;
        j = -1;
        n = -1;
        t = -1;
        t = SCANF("GPIO%d PIN%d%n %s", &i, &j, &n, b);
        PRINTF("1.t=%d, n=%d, i=%d, j=%d, string=%s\r\n", t, n, i, j, b);
        t = SCANF("%s", buf);
        PRINTF("2.t=%d\n", t);
        t = sscanf(buf, "GPIO%d PIN%d%n %s", &i, &j, &n, b);
        PRINTF("3.t=%d, n=%d, i=%d, j=%d, string=%s\r\n", t, n, i, j, b);
    }
}
#endif

#if 0
    while (1)
    {
#if 0
        memset(buf, 0, 100);
        memset(b, 0, 100);
        i = -1;
        j = -1;
        k = 0;
        do
        {
            ch     = GETCHAR();
            buf[k] = ch;
            ++k;
        } while (ch != '\n');
        sscanf(buf, "GPIO%d PIN%d %s", &i, &j, (char *)b);
        if ((i == -1) && (j == -1))
        {
            PRINTF("invalid command: %s\r\n", buf);
            continue;
        }
        if ((i < 0) || (i >= sizeof(pins) / sizeof(pins[0])))
        {
            PRINTF("unsupported gpio<%u>\r\n", i);
            continue;
        }
        bool t = false;
        for (int n = 0, size = sizeof(pins[0]) / sizeof(pins[0][0]); (n < size) && (pins[i][n] != 0xff); ++n)
        {
            if (pins[i][n] == j)
            {
                if (!strcmp("LOW", b))
                {
                    GPIO_PinWrite(gpios[i], pins[i][n], 0);
                    PRINTF("<%d, %d, %s> done\r\n", i, pins[i][n], b);
                }
                else if (!strcmp("HIGH", b))
                {
                    GPIO_PinWrite(gpios[i], pins[i][n], 1);
                    PRINTF("<%d, %d, %s> done\r\n", i, pins[i][n], b);
                }
                else
                {
                    PRINTF("unknown level %s\r\n", b);
                }
                t = true;
            }
        }
        if (!t)
        {
            PRINTF("unsupported pin<%d, %d>\r\n", i, j);
        }
    }
#endif
#if 0
    // int k = 0;
    while (1)
    {
        PRINTF("k=%u\r\n", k);
        for (int i = 0; i < 4; ++i)
        {
            for (int j = 0; j < 32; ++j)
            {
                if (pins[i][j] == 0xff)
                {
                    break;
                }
                PRINTF("gpio toggle <%u, %u>\r\n", i, j);
                // GPIO_PortToggle(gpios[i], 1 << pin[i][j]);
                GPIO_PinWrite(gpios[i], pins[i][j], k % 2);
            }
        }
        ++k;
        if (k == 1000 * 1000)
        {
            k = 0;
        }
    }
#endif

#endif
#endif /* end of run_test_gpio */

#ifdef run_read_gpio

#endif

#include "fsl_lpuart.h"

size_t __write(int handle, const unsigned char *buf, size_t bufSize)
{
    if (buf == NULL)
    {
        return SIZE_MAX - 1;
    }
    if (bufSize == 0)
    {
        return SIZE_MAX - 2;
    }
    status_t status = LPUART_WriteBlocking(LPUART1, buf, bufSize);
    if (status == kStatus_Success)
    {
        return bufSize;
    }
    else
    {
        return SIZE_MAX - 3;
    }
}

size_t __read(int handle, unsigned char *buf, size_t bufSize)
{
    if (buf == NULL)
    {
        return SIZE_MAX - 1;
    }
    if (bufSize == 0)
    {
        return SIZE_MAX - 2;
    }
    status_t status = LPUART_ReadBlocking(LPUART1, buf, bufSize);
    if (status == kStatus_Success)
    {
        return bufSize;
    }
    else
    {
        return SIZE_MAX - 3;
    }
}

#include <stdarg.h>

int scan(char *format, ...)
{
#define size (100)
    static char buffer[size] = {0};
    // static bool has_enter             = false;
    char ch = '\0';
    int i   = 0;
    for (i = 0; i < size; ++i)
    {
        if (LPUART_ReadBlocking(LPUART1, (uint8_t *)&ch, 1) == kStatus_Success)
        {
            buffer[i] = ch;
            if (ch == '\n')
            {
                break;
            }
        }
        else
        {
            return -1;
        }
    }
    buffer[i] = '\0';
    va_list args;
    va_start(args, format);
    int r = vsscanf(buffer, format, args);
    va_end(args);
    return r;
#undef buffer_size
}
int E(int n)
{
    int t = 1;
    while (!(n & t))
    {
        t <<= 1;
    }
    return t;
}
int print(char *format, ...)
{
#define size (100)
    static char buffer[size] = {0};
    va_list args;
    va_start(args, format);
    int r = vsnprintf(buffer, size, format, args);
    va_end(args);
    r = printf("%s", buffer);
    return r;
#undef buffer_size
}