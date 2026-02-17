#include <stdio.h>

#include "fsl_debug_console.h"
#include "fsl_port.h"
#include "fsl_lpuart.h"

#include "board.h"
#include "app.h"

void config(void);
void read_line(void);

#define buffer_size (100)
static char buffer[buffer_size + 1];

static const GPIO_Type *gpios[] = GPIO_BASE_PTRS;
static const PORT_Type *ports[] = PORT_BASE_PTRS;

#ifdef PORT_CLOCKS
static const clock_ip_name_t port_clocks[] = PORT_CLOCKS;
#endif
#ifdef PORT_RSTS
static const SYSCON_RSTn_t resets[] = PORT_RSTS;
#endif

static const gpio_pin_config_t gpio_pin_config_output_0 = {.pinDirection = kGPIO_DigitalOutput, .outputLogic = 0U};
static const gpio_pin_config_t gpio_pin_config_output_1 = {.pinDirection = kGPIO_DigitalOutput, .outputLogic = 1U};
static const gpio_pin_config_t gpio_pin_config_input    = {.pinDirection = kGPIO_DigitalInput};

static const port_pin_config_t port_pin_config_gpio = {
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
#if 0                                                                // debug console uart0
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
        //
        1,   // blue led
        0xff //
    },
    // gpio d
    {0xff},
#endif
};

bool write_gpio(char *content);
bool read_gpio(char *content);
bool reset_gpio(char *content);

bool (*(commands[]))(char *content) = {NULL, write_gpio, NULL, read_gpio, reset_gpio};

int main(void)
{
    BOARD_InitHardware();

    printf("MCUX SDK version: %s\r\n", MCUXSDK_VERSION_FULL_STR);
    printf("start, check:%s\n", "set132487");

    config();

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

#define argument_count (2)
// write_gpio (2<<5)|1 1, blue led
bool write_gpio(char *content)
{
    int r     = -1;
    int n     = -1;
    int pin   = -1;
    int value = -1;

    r = sscanf(buffer, " write_gpio %d %d %n", &pin, &value, &n);
    if ((r != argument_count) || (n != strnlen(buffer, buffer_size)))
    {
        printf("命令参数错误，或格式不完全匹配\n");
        return false;
    }
    // XXX 是否存在
    // XXX 不同格式（241，J1-11，J1 11，J1_11，PTC1）
    // TODO 初始化为输出

    int gpio_index = (pin >> 8) & 0xff;
    int pin_index  = (pin >> 0) & 0xff;

    // XXX -> 0/1
    value = (bool)value;

#ifdef PORT_CLOCKS
    CLOCK_EnableClock(port_clocks[gpio_index]);
#endif
#ifdef PORT_RSTS
    RESET_ReleasePeripheralReset(resets[gpio_index]);
#endif
    GPIO_PinInit(gpios[gpio_index], pin_index, &gpio_pin_config_output_0);
    PORT_SetPinConfig(ports[gpio_index], pin_index, &port_pin_config_gpio);

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
    }

    return true;
}
#undef argument_count

#define argument_count (1)
// read_gpio (2<<5)|1
bool read_gpio(char *content)
{
    int r   = -1;
    int n   = -1;
    int pin = -1;
    r       = sscanf(buffer, " read_gpio %d %n", &pin, &n);
    if ((r != argument_count) || (n != strnlen(buffer, buffer_size)))
    {
        printf("命令参数错误，或格式不完全匹配\n");
        return false;
    }
    // 初始化为输入

    int gpio_index = (pin >> 8) & 0xff;
    int pin_index  = (pin >> 0) & 0xff;

#ifdef PORT_CLOCKS
    CLOCK_EnableClock(port_clocks[gpio_index]);
#endif
#ifdef PORT_RSTS
    RESET_ReleasePeripheralReset(resets[gpio_index]);
#endif
    GPIO_PinInit(gpios[gpio_index], pin_index, &gpio_pin_config_output_0);
    PORT_SetPinConfig(ports[gpio_index], pin_index, &port_pin_config_gpio);

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
bool reset_gpio(char *content)
{
    int r = -1;
    int n = -1;
    r     = sscanf(buffer, " reset_gpio %n", &n);
    if ((r != argument_count) || (n != strnlen(buffer, buffer_size)))
    {
        printf("命令参数错误，或格式不完全匹配\n");
        return false;
    }
    // 初始化为输入
    printf("reset gpio\n");
    return true;
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