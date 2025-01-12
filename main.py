# main.py
from c_compiler import Compiler
from simple_assembler import Assembler
# 假设 Assembler 类已经定义好了
import Machine

# 创建 Assembler 类的实例
assembler = Assembler()

# 定义要编译的汇编代码
assembly_code = """
MOV %R0, $10
MOV %R1, $20
ADD %R2, %R0
ADD %R2, %R1
PUSH %R2
POP %R3
HLT
"""

# 调用 assemble 方法来编译汇编代码
machine_code = assembler.assemble(assembly_code)
#
# # 打印生成的机器码
# #print("Generated machine code:", machine_code)
# vm = M.VirtualMachine()
# vm.load_program(machine_code)
# vm.run()
# vm.dump_memory()
# vm.dump_registers()


memory_program = """
; 内存管理示例
; 分配内存
MOV %R0, $0x1000  ; 分配 4KB 内存
INT $0x01         ; 调用内存分配中断

; 释放内存
MOV %R0, $0x1000  ; 要释放的内存地址
INT $0x02         ; 调用内存释放中断
"""

# control_mem = assembler.assemble(memory_program)
# vm = Machine.VirtualMachine()
# vm.load_program(control_mem)
# vm.run()
# vm.dump_memory()
# vm.dump_registers()


compiler = Compiler()
source = """
int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    int y = 20;
    int z = add(x, y);
    return z;
}
"""
code = compiler.compile(source)
print("Generated code:", code)
vm = Machine.VirtualMachine()
vm.load_program(code)
vm.run()
print("Registers:", vm.registers)