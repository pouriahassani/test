/opt/riscv/bin/riscv32-unknown-elf-gcc -march=rv32im -c -O0 -o mulsf3.o mulsf3.c
/opt/riscv/bin/riscv32-unknown-elf-gcc -march=rv32im -c -O0 -o muldf3.o muldf3.c
/opt/riscv/bin/riscv32-unknown-elf-gcc -march=rv32im -c -O0 -o divsf3.o divsf3.c
/opt/riscv/bin/riscv32-unknown-elf-gcc -march=rv32im -c -O0 -o divdf3.o divdf3.c
/opt/riscv/bin/riscv32-unknown-elf-gcc -march=rv32im -c -O0 -o addsf3.o addsf3.c
/opt/riscv/bin/riscv32-unknown-elf-gcc -march=rv32im -c -O0 -o adddf3.o adddf3.c
/opt/riscv/bin/riscv32-unknown-elf-gcc -march=rv32im -c -O0 -o subdf3.o subdf3.c
/opt/riscv/bin/riscv32-unknown-elf-gcc -march=rv32im -c -O0 -o subsf3.o subsf3.c
cp ./*.o ../
/opt/riscv/bin/riscv32-unknown-elf-ar rcs libgcc.a ./../*.o

