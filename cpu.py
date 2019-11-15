import sys

"""CPU functionality."""

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8

        self.instructions = {}

        self.address = 0
        self.sp = 0
        self.pc = 0

        self.equalFlag = False
        self.halted = False

    def init_sp(self):
        self.sp = 0

    def init_pc(self):
        self.pc = 0
        
    def add_instructions(self):
        
        self.instructions['LDI'] = 0b10000010
        self.instructions['PRN'] = 0b01000111
        self.instructions['HLT'] = 0b00000001
        self.instructions['MUL'] = 0b10100010
        self.instructions['PUSH'] = 0b01000101
        self.instructions['POP'] = 0b01000110
        self.instructions['JEQ'] = 0b01010101
        self.instructions['CMP'] = 0b10100111
        self.instructions['JNE'] = 0b01010110
        self.instructions['JMP'] = 0b01010100
        
    def ram_read(self):
        print(self.ram)

    def ram_write(self, value):
        self.ram[self.sp] = value
        self.sp +=1

    def load(self):
        """Load a program into memory."""
        
        progname = sys.argv[1]
        
        with open(progname) as f:
            for line in f:
                line = line.split('#')[0]
                line = line.strip() # Lose whitespace
                
                if line == '':
                    continue
                
                val = int(line, base=2)
                
                self.ram[self.address] = val
                self.address +=1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        
        else:
            raise Exception("Unsupported ALU operation")

    """
    def trace(self):
 
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.

        print(f"TRACE: %02X | %02X %02X %02X |" % )
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
        """
    def run(self):
        """Run the CPU."""       
        self.init_sp()
        self.init_pc()

        
        print('Running program...')
        while not self.halted:
            instruction = self.ram[self.pc]
            
            if instruction == self.instructions['LDI']:
                #print("LOADING....")
                reg_num = self.ram[self.pc+1]
                value = self.ram[self.pc+2]
                #print("THIS VALUE:", value,"INTO REGISTER:",reg_num)
                
                #print(reg_num)
                #print(value)
                self.reg[reg_num] = value

                #print(self.reg)
                #print(self.ram)


                self.pc += 3

            if instruction == self.instructions['CMP']:
                val1 = self.ram[self.pc+1]
                reg_val1 = self.reg[val1]
                val2 = self.ram[self.pc+2]
                reg_val2 = self.reg[val2]
                #print('CURRENT TRUTH STATUS', self.equalFlag)
                #print("DOES",val1,"EQUAL",val2,'?')
                if reg_val1 == reg_val2:
                    self.equalFlag = True

                #print("NEW TRUTH STATUS", self.equalFlag)

                self.pc +=3


            if instruction == self.instructions['JEQ']:
                reg_num = self.ram[self.pc+1]
                #print("Ram:", self.ram)
                #print("Reg:",self.reg)
                #print("Stack Pointer:", self.sp)
                #print("Memory Pointer:",self.pc)
                if self.equalFlag == True:
                    self.pc = self.reg[reg_num]
                    #print("The POINTER",self.pc)

                else:
                    self.pc +=2

            if instruction == self.instructions['JNE']:
                #print("Ram:", self.ram)
                #print("Reg:",self.reg)
                #print("Stack Pointer:", self.sp)
                #print("Memory Pointer:",self.pc)
                reg_num = self.ram[self.pc+1]
                if self.equalFlag == False:
                    self.pc = self.reg[reg_num]
                    #print("The POINTER",self.pc)

                else:
                    self.pc+=2

            if instruction == self.instructions['JMP']:
                reg_num = self.ram[self.pc+1]
                self.pc = reg_num


                self.pc +=2

            if instruction == self.instructions['PUSH']:
                self.reg[self.sp] -=1  # Decrement the stack pointer
                reg_num = self.ram[self.pc+1]
                reg_val = self.reg[reg_num]

                self.ram[self.reg[self.sp]] = reg_val # Copy reg value into memory at address address

                self.pc +=2

            if instruction == self.instructions['POP']:
                val = self.ram[self.reg[self.sp]]
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = val # Copy val from memory at address into register

                self.reg[self.sp] += 1 # Increment SP

                self.pc += 2
                
            if instruction == self.instructions['PRN']:
                reg_num = self.ram[self.pc+1]
                print("RETURNS:",self.reg[reg_num])
                
                self.pc += 2

            if instruction == self.instructions['MUL']:
                reg_num1 = self.reg[self.ram[self.pc+1]]
                reg_num2 = self.reg[self.ram[self.pc+2]]

                self.reg[self.ram[self.pc+1]] = reg_num1 * reg_num2

                self.pc += 3
                
            if instruction == self.instructions['HLT']:
                self.halted= True
                self.pc+=1
