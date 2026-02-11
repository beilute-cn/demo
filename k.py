class Example:
    def __getattr__(self, name):
        """当属性不存在时才调用"""
        print(f"__getattr__: {name}")
        return f"{name} 不存在"
    
    def __getattribute__(self, name):
        """访问任何属性都会调用（包括存在的）"""
        print(f"__getattribute__: {name}")
        return object.__getattribute__(self, name)
    
    def __setattr__(self, name, value):
        """设置任何属性时调用"""
        print(f"__setattr__: {name} = {value}")
        object.__setattr__(self, name, value)
    
    def __delattr__(self, name):
        """删除属性时调用"""
        print(f"__delattr__: {name}")
        object.__delattr__(self, name)

obj = Example()
obj.x = 10        # 调用 __setattr__
print(obj.x)      # 调用 __getattribute__
print(obj.y)      # 先调用 __getattribute__，失败后调用 __getattr__
del obj.x         # 调用 __delattr__
