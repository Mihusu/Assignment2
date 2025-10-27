#!/usr/bin/env python3
"""
This is a virtual Machine Monitor (VMM) Simulator,
Which can trap-and-Emulate model for CPU virtualization
"""

class VMMSimulator:
    def __init__(self):
        self.acc = 0  # accumulator register
        self.running = True
    
    def execute_guest_program(self, filename):
        """Execute the guest program with trap-and-emulate logic"""
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
            
            for line in lines:
                if not self.running:
                    break
                    
                instruction = line.strip()
                if not instruction:
                    continue
                    
                self.execute_instruction(instruction)
                
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {e}")
    
    def execute_instruction(self, instruction):
        """Execute a single instruction with trap-and-emulate"""
        parts = instruction.split()
        opcode = parts[0]
        
        # Check if instruction is privileged
        if opcode in ['scan_disk', 'halt']:
            # Privileged instruction - trap to VMM
            print(f"[VMM] Trapped privileged instruction '{opcode}', emulating...")
            self.emulate_privileged_instruction(opcode)
        else:
            # Non-privileged instruction - execute directly
            print(f"[Guest] Executing: {instruction}")
            self.execute_non_privileged_instruction(opcode, parts[1:] if len(parts) > 1 else [])
    
    def execute_non_privileged_instruction(self, opcode, operands):
        """Execute non-privileged instructions directly"""
        if opcode == 'add':
            if len(operands) == 1:
                try:
                    value = int(operands[0])
                    self.acc += value
                except ValueError:
                    print(f"Error: Invalid value '{operands[0]}' for add instruction")
            else:
                print("Error: add instruction requires one operand")
                
        elif opcode == 'print':
            print(f"Accumulator value: {self.acc}")
            
        else:
            print(f"Error: Unknown instruction '{opcode}'")
    
    def emulate_privileged_instruction(self, opcode):
        """Emulate privileged instructions safely"""
        if opcode == 'scan_disk':
            # Simulate disk I/O operation
            # In a real VMM, this would involve actual disk access with proper isolation
            print("[VMM] Disk scan emulated successfully")
            
        elif opcode == 'halt':
            # Halt the guest program
            self.running = False
            print("[VMM] Trapped privileged instruction 'halt'. Halting guest.")
            
        else:
            print(f"Error: Unknown privileged instruction '{opcode}'")

def main():
    """Main function to run the VMM simulator"""
    simulator = VMMSimulator()
    
    # Execute the guest program
    simulator.execute_guest_program("guest_program.txt")

if __name__ == "__main__":
    main()