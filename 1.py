class FreeBlock:
    def __init__(self, start_address, length):
        self.start_address = start_address  # Endereço inicial da área livre
        self.length = length  # Quantidade de blocos livres contíguos na área


class MemoryHeap:
    def __init__(self, size):
        self.heap = [False] * size  # Vetor inicializado com valores booleanos
        self.free_blocks = [FreeBlock(0, size)]  # Lista de áreas livres inicialmente contendo toda a memória
        self.size = size

    def allocate_memory_first_fit(self, num_blocks):
        for block in self.free_blocks:
            if block.length >= num_blocks:
                # Encontrou um bloco livre que atende aos requisitos de alocação
                allocated_block = FreeBlock(block.start_address, num_blocks)
                # Define os valores correspondentes no heap como ocupados (True)
                for i in range(allocated_block.start_address, allocated_block.start_address + allocated_block.length):
                    self.heap[i] = True
                # Atualiza o bloco livre removendo os blocos alocados
                block.start_address += num_blocks
                block.length -= num_blocks
                if block.length == 0:
                    # Remove o bloco livre se o comprimento for zero
                    self.free_blocks.remove(block)
                return allocated_block
        # Retorna um bloco inválido se não for possível alocar memória
        return FreeBlock(-1, -1)

    def allocate_memory_best_fit(self, num_blocks):
        best_fit_block = None
        for block in self.free_blocks:
            if block.length >= num_blocks:
                if best_fit_block is None or block.length < best_fit_block.length:
                    # Encontrou um novo melhor ajuste
                    best_fit_block = block
        if best_fit_block is not None:
            # Aloca memória no melhor ajuste encontrado
            allocated_block = FreeBlock(best_fit_block.start_address, num_blocks)
            # Define os valores correspondentes no heap como ocupados (True)
            for i in range(allocated_block.start_address, allocated_block.start_address + allocated_block.length):
                self.heap[i] = True
            # Atualiza o bloco livre removendo os blocos alocados
            best_fit_block.start_address += num_blocks
            best_fit_block.length -= num_blocks
            if best_fit_block.length == 0:
                # Remove o bloco livre se o comprimento for zero
                self.free_blocks.remove(best_fit_block)
            return allocated_block
        # Retorna um bloco inválido se não for possível alocar memória
        return FreeBlock(-1, -1)

    def free_memory(self, block):
        start_address = block.start_address
        length = block.length
        # Define os valores correspondentes no heap como livres (False)
        for i in range(start_address, start_address + length):
            self.heap[i] = False

        # Mescla blocos livres adjacentes
        merged_blocks = []
        for free_block in self.free_blocks:
            if start_address + length == free_block.start_address:
                start_address = free_block.start_address
                length += free_block.length
            elif free_block.start_address + free_block.length == start_address:
                length += free_block.length
            else:
                merged_blocks.append(free_block)

        # Adiciona o bloco livre resultante após a mesclagem
        merged_blocks.append(FreeBlock(start_address, length))
        self.free_blocks = merged_blocks

    def print_heap(self):
        print("Heap: ", end="")
        for value in self.heap:
            print("1" if value else "0", end="")
        print()

    def print_free_blocks(self):
        print("Blocos Livres:")
        for block in self.free_blocks:
            print("Endereço Inicial:", block.start_address, "Comprimento:", block.length)
        print()

    def execute_program(self, program):
        for instruction in program:
            if instruction.startswith("ALLOCATE FIRST_FIT"):
                num_blocks = int(instruction.split()[2])
                allocated_block = self.allocate_memory_first_fit(num_blocks)
                if allocated_block.start_address != -1:
                    print("First Fit - Alocados", num_blocks, "blocos a partir do endereço", allocated_block.start_address)
                else:
                    print("First Fit - Falha ao alocar", num_blocks, "blocos")
            elif instruction.startswith("ALLOCATE BEST_FIT"):
                num_blocks = int(instruction.split()[2])
                allocated_block = self.allocate_memory_best_fit(num_blocks)
                if allocated_block.start_address != -1:
                    print("Best Fit - Alocados", num_blocks, "blocos a partir do endereço", allocated_block.start_address)
                else:
                    print("Best Fit - Falha ao alocar", num_blocks, "blocos")
            elif instruction.startswith("FREE"):
                start_address, length = map(int, instruction.split()[1:])
                block_to_free = FreeBlock(start_address, length)
                self.free_memory(block_to_free)
                print("Liberados", length, "blocos a partir do endereço", start_address)

            self.print_heap()
            self.print_free_blocks()
            print()


# Programa de exemplo com lista de comandos no heap
programa = [
    "ALLOCATE FIRST_FIT 4",
    "ALLOCATE BEST_FIT 6",
    "ALLOCATE BEST_FIT 2",
    "ALLOCATE FIRST_FIT 5",
    "FREE 4 4",
    "ALLOCATE FIRST_FIT 3",
    "FREE 6 2",
    "ALLOCATE BEST_FIT 7",
    "ALLOCATE BEST_FIT 3",
    "ALLOCATE FIRST_FIT 2",
    "ALLOCATE FIRST_FIT 3",
    "ALLOCATE BEST_FIT 4",
    "FREE 5 5",
    "FREE 0 6"# limpa 6 espaços da memória começando no endereço 0 do heap
]

heap = MemoryHeap(50)
heap.execute_program(programa)  # Executa o programa
