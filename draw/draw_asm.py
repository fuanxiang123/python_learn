def print_control_flow_graph(code):
    print("Control Flow Graph:")
    block_start = 0
    for i, opcode in enumerate(code):
        if opcode == 0x08:  # JMP
            target = code[i + 1]
            print(f"Block [{block_start}:{i}] -> Block [{target}:]")
            block_start = i + 2
        elif opcode == 0x0A:  # JE
            target = code[i + 1]
            print(f"Block [{block_start}:{i}] -> [JE] Block [{target}:]")
            block_start = i + 2
        elif opcode == 0x0B:  # JNE
            target = code[i + 1]
            print(f"Block [{block_start}:{i}] -> [JNE] Block [{target}:]")
            block_start = i + 2
        elif opcode == 0x0E:  # RET
            print(f"Block [{block_start}:{i}] -> Return")
            block_start = i + 1
    print(f"Block [{block_start}:] -> End")


# 示例调用
print_control_flow_graph([0x01, 0, 10, 0x01, 1, 20, 0x02, 0, 1, 0x0E])
