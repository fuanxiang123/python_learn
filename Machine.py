class VirtualMachine:
    def __init__(self):
        self.memory = [0] * (1024 * 1024)  # 1MB 内存
        self.registers = [0] * 16  # R0-R15
        self.eip = 0  # 指令指针
        self.esp = len(self.memory) - 4  # 栈指针
        self.eflags = 0  # 状态寄存器
        self.stack_frames = []  # 栈帧

    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def run(self):
        while True:
            opcode = self.memory[self.eip]
            self.eip += 1

            if opcode == 0x01:  # MOV
                self.mov()
            elif opcode == 0x02:  # ADD
                self.add()
            elif opcode == 0x03:  # SUB
                self.sub()
            elif opcode == 0x04:  # MUL
                self.mul()
            elif opcode == 0x05:  # DIV
                self.div()
            elif opcode == 0x06:  # PUSH
                self.push()
            elif opcode == 0x07:  # POP
                self.pop()
            elif opcode == 0x08:  # JMP
                self.jmp()
            elif opcode == 0x09:  # CMP
                self.cmp()
            elif opcode == 0x0A:  # JE
                self.je()
            elif opcode == 0x0B:  # JNE
                self.jne()
            elif opcode == 0x0C:  # HLT
                break
            elif opcode == 0x0D:  # CALL
                self.call()
            elif opcode == 0x0E:  # RET
                self.ret()
            elif opcode == 0x0F:  # LOAD
                self.load()
            elif opcode == 0x10:  # STORE
                self.store()
            elif opcode == 0x11:  # LEA
                self.lea()
            else:
                raise ValueError(f"Unknown opcode: {opcode}")

    def mov(self):
        dest = self.memory[self.eip]
        src = self.memory[self.eip + 1]
        self.eip += 2
        if isinstance(src, int):
            self.registers[dest] = src
        else:
            self.registers[dest] = self.registers[src]

    def add(self):
        dest = self.memory[self.eip]
        src = self.memory[self.eip + 1]
        self.eip += 2
        self.registers[dest] = (self.registers[dest] + self.registers[src]) & 0xFFFFFFFF

    def sub(self):
        dest = self.memory[self.eip]
        src = self.memory[self.eip + 1]
        self.eip += 2
        self.registers[dest] = (self.registers[dest] - self.registers[src]) & 0xFFFFFFFF

    def mul(self):
        dest = self.memory[self.eip]
        src = self.memory[self.eip + 1]
        self.eip += 2
        self.registers[dest] = (self.registers[dest] * self.registers[src]) & 0xFFFFFFFF

    def div(self):
        dest = self.memory[self.eip]
        src = self.memory[self.eip + 1]
        self.eip += 2
        self.registers[dest] = (self.registers[dest] // self.registers[src]) & 0xFFFFFFFF

    def push(self):
        src = self.memory[self.eip]
        self.eip += 1
        self.memory[self.esp] = self.registers[src]
        self.esp -= 4

    def pop(self):
        dest = self.memory[self.eip]
        self.eip += 1
        self.esp += 4
        self.registers[dest] = self.memory[self.esp]

    def jmp(self):
        addr = self.memory[self.eip]
        self.eip = addr

    def cmp(self):
        src1 = self.memory[self.eip]
        src2 = self.memory[self.eip + 1]
        self.eip += 2
        self.eflags = 1 if self.registers[src1] == self.registers[src2] else 0

    def je(self):
        addr = self.memory[self.eip]
        self.eip += 1
        if self.eflags == 1:
            self.eip = addr

    def jne(self):
        addr = self.memory[self.eip]
        self.eip += 1
        if self.eflags == 0:
            self.eip = addr

    def call(self):
        func_addr = self.memory[self.eip]
        self.eip += 1
        self.stack_frames.append((self.eip, self.esp))
        self.eip = func_addr

    def ret(self):
        if not self.stack_frames:
            raise RuntimeError("No stack frame to return to")
        self.eip, self.esp = self.stack_frames.pop()

    def load(self):
        dest = self.memory[self.eip]
        src = self.memory[self.eip + 1]
        self.eip += 2
        self.registers[dest] = self.memory[self.registers[src]]

    def store(self):
        dest = self.memory[self.eip]
        src = self.memory[self.eip + 1]
        self.eip += 2
        self.memory[self.registers[dest]] = self.registers[src]

    def lea(self):
        dest = self.memory[self.eip]
        src = self.memory[self.eip + 1]
        self.eip += 2
        self.registers[dest] = src