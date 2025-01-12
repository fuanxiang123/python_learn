#simple_assembler.py
class Assembler:
    def __init__(self):
        self.opcodes = {
            "MOV": 0x01,
            "ADD": 0x02,
            "SUB": 0x03,
            "JMP": 0x04,
            "CMP": 0x05,
            "PUSH": 0x06,
            "POP": 0x07,
            "CALL": 0x08,
            "RET": 0x09,
            "INT": 0x0A,
            "HLT": 0x0B,
        }
        self.registers = {f"R{i}": i for i in range(16)}  # R0-R15
        self.labels = {}  # 用于存储标签地址

    def assemble(self, code):
        machine_code = []
        lines = code.strip().split("\n")

        # 第一遍：解析标签
        current_address = 0
        for line in lines:
            # 移除注释和多余的空白字符
            line = line.split(';')[0].strip()  # 只保留分号前的部分，并移除首尾空白
            if not line or line.endswith(":"):  # 忽略空行或标签定义行
                continue
            current_address += 1

        # 重置当前地址以进行第二遍扫描
        current_address = 0
        for line in lines:
            # 再次移除注释和多余的空白字符
            line = line.split(';')[0].strip()
            if not line or line.endswith(":"):
                continue

            tokens = line.split()
            opcode = tokens[0].upper()
            if opcode not in self.opcodes:
                raise ValueError(f"Unknown instruction: {opcode}")
            machine_code.append(self.opcodes[opcode])
            current_address += 1

            # 移除指令后多余的逗号
            tokens = [token.rstrip(',') for token in tokens]

            for operand in tokens[1:]:
                if operand.startswith("%"):
                    # 寄存器
                    reg = operand[1:].upper()
                    print(f"Parsing register: {reg}")  # 调试信息
                    if reg not in self.registers:
                        raise ValueError(f"Unknown register: {reg}")
                    machine_code.append(self.registers[reg])
                elif operand.startswith("$"):
                    # 立即数
                    value = int(operand[1:], 0)
                    machine_code.append(value & 0xFFFFFFFF)  # 32 位立即数
                elif operand in self.labels:
                    # 标签地址
                    machine_code.append(self.labels[operand])
                else:
                    try:
                        # 内存地址或数值
                        machine_code.append(int(operand, 0) & 0xFFFFFFFF)  # 32 位地址
                    except ValueError as e:
                        raise ValueError(f"Invalid operand '{operand}' at address {current_address}: {e}")
                current_address += 1

        return machine_code