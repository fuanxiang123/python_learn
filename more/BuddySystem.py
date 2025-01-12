class BuddySystem:
    def __init__(self, total_size):
        self.total_size = total_size
        self.min_size = 1024  # 最小块大小
        self.free_lists = {}
        self.initialize_free_lists()

    def initialize_free_lists(self):
        size = self.total_size
        while size >= self.min_size:
            self.free_lists[size] = []
            size //= 2

    def allocate(self, size):
        # 找到合适的块大小
        block_size = self.min_size
        while block_size < size:
            block_size *= 2
        if block_size > self.total_size:
            raise MemoryError("Not enough memory")

        # 查找可用块
        if self.free_lists[block_size]:
            return self.free_lists[block_size].pop()

        # 分裂更大的块
        larger_block = self.allocate(block_size * 2)
        self.free_lists[block_size].append(larger_block + block_size)
        return larger_block

    def free(self, address, size):
        # 合并伙伴块
        block_size = self.min_size
        while block_size < size:
            block_size *= 2
        self.free_lists[block_size].append(address)
        self.merge_buddies(address, block_size)

    def merge_buddies(self, address, block_size):
        buddy = address ^ block_size
        if buddy in self.free_lists[block_size]:
            self.free_lists[block_size].remove(buddy)
            self.free(address & ~block_size, block_size * 2)