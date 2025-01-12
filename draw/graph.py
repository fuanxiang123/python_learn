from graphviz import Digraph


def visualize_control_flow_graph(code):
    dot = Digraph(comment='Control Flow Graph')
    block_id = 0
    block_start = 0
    labels = {}

    def add_block(dot, start, end, block_id):
        label = f"Block {block_id}\n{code[start:end]}"
        labels[block_id] = label
        dot.node(str(block_id), label)

    for i, opcode in enumerate(code):
        if opcode in [0x08, 0x0A, 0x0B]:  # JMP, JE, JNE
            target = code[i + 1]
            add_block(dot, block_start, i, block_id)
            dot.edge(str(block_id), str(target))
            block_start = i + 2
            block_id += 1
        elif opcode == 0x0E:  # RET
            add_block(dot, block_start, i, block_id)
            dot.edge(str(block_id), 'Return')
            block_start = i + 1
            block_id += 1

    if block_start < len(code):
        add_block(dot, block_start, len(code), block_id)

    return dot


# 示例调用
machine_code = [0x01, 0, 10, 0x01, 1, 20, 0x02, 0, 1, 0x0E]
dot = visualize_control_flow_graph(machine_code)
dot.render('control_flow_graph', format='png', view=True)  # 保存为 PNG 文件并打开查看
