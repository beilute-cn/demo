apiSetCb("uart", function(data)
    log.info("uart receive", data)
    sys.publish("UART", data)
end)

sys.taskInit(function()
    for i = 0, 255 do
        local r = apiSend("uart", string.format("readlow_gpio %d\n", i))
        sys.wait(1000)
    end
end)
