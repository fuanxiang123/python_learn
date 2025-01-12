#c_compiler.py
class Compiler:
    def __init__(self):
        self.variables = {}  # 全局变量表
        self.functions = {}  # 函数表
        self.code = []  # 生成的虚拟机指令
        self.label_count = 0  # 标签计数器
        self.stack_frame_size = 0  # 当前栈帧大小
        self.local_variables = {}  # 局部变量表

    def compile(self, source):
        lines = source.strip().split("\n")
        for line in lines:
            self.compile_line(line)
        return self.code

    def compile_line(self, line):
        line = line.strip()

        if line.startswith("int"):
            # 变量声明
            if "(" in line and "{" in line:
                # 函数声明
                func_decl = line[4:line.index("{")].strip()
                func_name = func_decl[:func_decl.index("(")].strip()
                params = func_decl[func_decl.index("(") + 1:func_decl.index(")")].split(',')
                params = [p.strip() for p in params]
                self.functions[func_name] = len(self.code)
                self.local_variables = {param.split()[1]: i for i, param in enumerate(params)}
                self.compile_block(line[line.index("{") + 1:line.rindex("}")])
                self.local_variables = {}
            elif "=" in line:
                var_decl = line[3:].strip()
                var_name, value = var_decl.split("=", 1)
                var_name = var_name.strip()
                value = int(value.strip().strip(";"))
                self.variables[var_name] = len(self.variables)
                self.code.extend([0x01, self.variables[var_name], value])
            else:
                var_name = line[4:].strip().strip(";")
                self.variables[var_name] = len(self.variables)
                self.code.extend([0x01, self.variables[var_name], 0])  # 默认初始化为0

        elif "=" in line:
            # 赋值语句
            var_name, expr = line.split("=", 1)
            var_name = var_name.strip()
            expr = expr.strip().strip(";")
            self.compile_expression(expr)
            if var_name in self.local_variables:
                self.code.extend([0x01, self.local_variables[var_name] + len(self.variables), 0])
            else:
                self.code.extend([0x01, self.variables[var_name], 0])

        elif line.startswith("if"):
            # 条件语句
            condition = line[3:line.index(")")].strip()
            self.compile_condition(condition)
            self.code.append(0x0A)  # JE
            jump_pos = len(self.code)
            self.code.append(0)  # 占位符
            self.compile_block(line[line.index("{") + 1:line.rindex("}")])
            self.code[jump_pos] = len(self.code)

        elif line.startswith("while"):
            # 循环语句
            condition = line[6:line.index(")")].strip()
            start_pos = len(self.code)
            self.compile_condition(condition)
            self.code.append(0x0B)  # JNE
            jump_pos = len(self.code)
            self.compile_block(line[line.index("{") + 1:line.rindex("}")])
            self.code.extend([0x08, start_pos])  # JMP
            self.code[jump_pos] = len(self.code)

        elif line.startswith("return"):
            # 返回语句
            expr = line[7:].strip().strip(";")
            self.compile_expression(expr)
            self.code.append(0x0E)  # RET

        elif "(" in line and ")" in line:
            # 函数调用
            func_call = line[:line.index(")") + 1]
            func_name = func_call[:func_call.index("(")].strip()
            args = func_call[func_call.index("(") + 1:func_call.index(")")].split(',')
            args = [arg.strip() for arg in args]
            for arg in reversed(args):  # 压栈需要反向处理参数
                self.compile_expression(arg)
                self.code.extend([0x06, 0])  # PUSH
            self.code.extend([0x0D, self.functions[func_name]])  # CALL

        else:
            raise ValueError(f"Unsupported statement: {line}")

    def compile_expression(self, expr):
        if "+" in expr:
            left, right = expr.split("+", 1)
            self.compile_expression(left.strip())
            self.compile_expression(right.strip())
            self.code.append(0x02)  # ADD
        elif "-" in expr:
            left, right = expr.split("-", 1)
            self.compile_expression(left.strip())
            self.compile_expression(right.strip())
            self.code.append(0x03)  # SUB
        elif "*" in expr:
            left, right = expr.split("*", 1)
            self.compile_expression(left.strip())
            self.compile_expression(right.strip())
            self.code.append(0x04)  # MUL
        elif "/" in expr:
            left, right = expr.split("/", 1)
            self.compile_expression(left.strip())
            self.compile_expression(right.strip())
            self.code.append(0x05)  # DIV
        elif expr.isdigit():
            self.code.extend([0x01, 0, int(expr)])  # MOV R0, value
        else:
            if expr in self.local_variables:
                self.code.extend([0x01, self.local_variables[expr] + len(self.variables), 0])  # MOV R0, local_var
            elif expr in self.variables:
                self.code.extend([0x01, self.variables[expr], 0])  # MOV R0, global_var
            else:
                raise KeyError(f"Undefined variable or function: {expr}")

    def compile_condition(self, condition):
        if "==" in condition:
            left, right = condition.split("==", 1)
            self.compile_expression(left.strip())
            self.compile_expression(right.strip())
            self.code.append(0x09)  # CMP
        elif "<" in condition:
            left, right = condition.split("<", 1)
            self.compile_expression(left.strip())
            self.compile_expression(right.strip())
            self.code.append(0x09)  # CMP
        else:
            raise ValueError(f"Unsupported condition: {condition}")

    def compile_block(self, block):
        lines = block.strip().split("\n")
        for line in lines:
            self.compile_line(line.strip())