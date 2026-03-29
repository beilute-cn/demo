#include <stdio.h>

#include "fsl_debug_console.h"
#include "fsl_port.h"
#include "fsl_lpuart.h"

#include "board.h"
#include "app.h"

void read_line(void);

#define buffer_size (100)
static char buffer[buffer_size + 1];

#ifdef PORT_CLOCKS
clock_ip_name_t port_clocks[] = PORT_CLOCKS;
#endif
#ifdef GPIO_CLOCKS
clock_ip_name_t gpio_clocks[] = GPIO_CLOCKS;
#endif
#ifdef GPIO_BASE_PTRS
GPIO_Type *gpios[] = GPIO_BASE_PTRS;
#endif
#ifdef PORT_BASE_PTRS
PORT_Type *ports[] = PORT_BASE_PTRS;
#endif

static const port_pin_config_t port_config_as_gpio = {
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
    .lockRegister = kPORT_UnlockRegister //
};

int write_gpio(char *content);
int read_gpio(char *content);
int reset(char *content);

int (*(commands[]))(char *content) = {NULL, write_gpio, NULL, read_gpio, reset};

int main(void)
{
    BOARD_InitHardware();

    printf("MCUX SDK version: %s\r\n", MCUXSDK_VERSION_FULL_STR);
    printf("start, check:%s\n", "set132487");

    bool has_handled = false;
    while (1)
    {
        read_line();
        has_handled = false;
        for (int i = 0, size = sizeof(commands) / sizeof(commands[0]); i < size; ++i)
        {
            if (!commands[i])
            {
                continue;
            }
            if (commands[i]("unused"))
            {
                has_handled = true;
                break;
            }
        }
        if (!has_handled)
        {
            printf("@%u, 未知命令：%s\n", __LINE__, buffer);
        }
    }
}
/*
    返回值
        <0  异常
        0   未处理
        1   正常
*/
#define argument_count (2)
// write_gpio (2<<5)|1 1, blue led
int write_gpio(char *content)
{
    int r     = -1;
    int n     = -1;
    int pin   = -1;
    int value = -1;

    r = sscanf(buffer, " write_gpio %d %d %n", &pin, &value, &n);
    if ((r != argument_count) || (n != strnlen(buffer, buffer_size)))
    {
        return 0;
    }
    // XXX 是否存在
    // XXX 不同格式（241，J1-11，J1 11，J1_11，PTC1）
    // TODO 初始化为输出

    int gpio_index = (pin >> 8) & 0xff;
    int pin_index  = (pin >> 0) & 0xff;

    if (gpio_index < 0 || gpio_index >= 4 || pin_index < 0 || pin_index >= 32)
    {
        printf("索引超出可选范围：gpio_index=%d, pin_index=%d\n", gpio_index, pin_index);
        return -1;
    }

    // XXX -> 0/1
    value = (bool)value;

#ifdef PORT_CLOCKS
    CLOCK_EnableClock(port_clocks[gpio_index]);
#endif
#ifdef GPIO_CLOCKS
    CLOCK_EnableClock(gpio_clocks[gpio_index]);
#endif
#ifdef PORT_RSTS
    RESET_ReleasePeripheralReset(resets[gpio_index]);
#endif

    static const gpio_pin_config_t gpio_config = {.pinDirection = kGPIO_DigitalOutput, .outputLogic = 0U};
    GPIO_PinInit(gpios[gpio_index], pin_index, &gpio_config);
    PORT_SetPinConfig(ports[gpio_index], pin_index, &port_config_as_gpio);

    GPIO_PinWrite(gpios[gpio_index], pin_index, value);
    printf(
        "Running command: %s\n"
        "Write PIN:%d, Value:%d\n"
        "\n"
        "Finish command: %s\n",
        buffer, pin, value, buffer //
    );
    // XXX 设置后读取检查
    if (GPIO_PinRead(gpios[gpio_index], pin_index) != value)
    {
        printf("@%u, 设置失败\n", __LINE__);
        return -2;
    }
    return 1;
}
#undef argument_count

#define argument_count (1)
// read_gpio (2<<5)|1
int read_gpio(char *content)
{
    int r   = -1;
    int n   = -1;
    int pin = -1;
    r       = sscanf(buffer, " read_gpio %d %n", &pin, &n);
    if ((r != argument_count) || (n != strnlen(buffer, buffer_size)))
    {
        return 0;
    }
    // 初始化为输入

    int gpio_index = (pin >> 8) & 0xff;
    int pin_index  = (pin >> 0) & 0xff;

    if (gpio_index < 0 || gpio_index >= 4 || pin_index < 0 || pin_index >= 32)
    {
        printf("索引超出可选范围：gpio_index=%d, pin_index=%d\n", gpio_index, pin_index);
        return -1;
    }

#ifdef PORT_CLOCKS
    CLOCK_EnableClock(port_clocks[gpio_index]);
#endif
#ifdef PORT_RSTS
    RESET_ReleasePeripheralReset(resets[gpio_index]);
#endif
    static const gpio_pin_config_t config = {.pinDirection = kGPIO_DigitalInput};
    GPIO_PinInit(gpios[gpio_index], pin_index, &config);
    PORT_SetPinConfig(ports[gpio_index], pin_index, &port_config_as_gpio);

    uint32_t value = GPIO_PinRead(gpios[gpio_index], pin_index);
    printf(
        "Running command: %s\n"
        "Read PIN:%d\n"
        "%s   PIN %s\n"
        "\n"
        "Finish command: %s\n",                  //
        buffer,                                  //
        pin_index,
        (value) ? "LOW_LED_ON" : "HIGH_LED_OFF", //
        (value) ? "HIGH" : "LOW",                //
        buffer                                   //
    );
    return true;
}
#undef argument_count

#define argument_count (0)
int reset(char *content)
{
    int r = -1;
    int n = -1;
    r     = sscanf(buffer, " reset %n", &n);
    if ((r != argument_count) || (n != strnlen(buffer, buffer_size)))
    {
        return 0;
    }
    port_pin_config_t config = port_config_as_gpio;
    config.mux               = kPORT_MuxAlt0;

    int pins[4][32] = {
        {0xff},
        {0xff},
        {0xff},
        {0xff},
    };
    for (int i = 0, max_i = 4; i < max_i; ++i)
    {
        for (int j = 0, max_j = 32; j < max_j; ++j)
        {
            if (pins[i][j] == 0xff)
            {
                break;
            }
            PORT_SetPinConfig(ports[i], j, &config);
        }
    }
    // 初始化为输入
    printf("reset\n");
    return 1;
}
#undef argument_count

void read_line(void)
{
    memset(buffer, 0, buffer_size + 1);
    char ch   = '\0';
    int index = 0;
    while ('\n' != (ch = GETCHAR()))
    {
        if (ch >= 'A' && ch <= 'Z')
        {
            ch += 'a' - 'A';
        }
        buffer[index] = ch;
        ++index;
        if (index == 100)
        {
            printf("@%u, full\r\n", __LINE__);
            break;
        }
    }
    buffer[index] = '\0';
}

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

#if 0
static uint8_t pins[4][33] = {
#if 1 // frdmmcxc353
      // gpio 0
    {
        //
        6,                           // i2c1 scl
        7,                           // i2c1 sda
        0xff,                        //
        0, 1, 2, 3, 4, 5, 6, 7, 0xff //
    },
    // gpio 1
    {
        //
        0,                                 // spi0 sck
        1,                                 // spi0 sdi
        2,                                 // spi0 sdo / pwt0 in0
        3,                                 // spi0 pcs2 / pwm0 a0
        0xff,                              //
        0, 1, 2, 3, 8, 9, 10, 11, 12, 0xff //
    },
    // gpio 2
    {
#if 0 // debug console uart0
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
    {
<<<<<<< HEAD
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
=======
        //
        1,   // blue led
        0xff //
    },
    // gpio d
    {0xff},
#endif
};
#endif
>>>>>>> e17db0f (serial)
