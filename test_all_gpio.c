
#if 1

    uint32_t pins[4][32] = {
        {6, 7, 0xff},
        {0, 1, 2, 3, 0xff},
        {0xff},
        {0xff},
    };

    GPIO_Type *gpios[] = GPIO_BASE_PTRS;
    PORT_Type *ports[] = PORT_BASE_PTRS;

    const gpio_pin_config_t gpio_config = {.pinDirection = kGPIO_DigitalOutput, .outputLogic = 0U};
    const port_pin_config_t port_config = {
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
    for (int i = 0, max_i = 4; i < max_i; ++i)
    {
        for (int j = 0, max_j = 32; j < max_j; ++j)
        {
            if (pins[i][j] == 0xff)
            {
                continue;
            }
            GPIO_PinInit(gpios[i], pins[i][j], &gpio_config);
            PORT_SetPinConfig(ports[i], pins[i][j], &port_config);
        }
    }

    int i = 0;
    int j = 0;
    int k = 0;
    int t = 0;

    while (1)
    {
        ++k;
        t = GPIO_PinRead(gpios[i], j);
        PRINTF("read <%d, %d> :: %d\r\n", i, j, t);
        GPIO_PortToggle(gpios[i], j);
        t = GPIO_PinRead(gpios[i], j);
        PRINTF("read <%d, %d> :: %d\r\n", i, j, t);
        GPIO_PortToggle(gpios[i], j);
        k *= k;
    }
#endif