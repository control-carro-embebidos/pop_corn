from tkinter import Tk, Checkbutton, IntVar, Button, Label, Frame
#import tkinter as tk
#from ..matrix import Matrix

class Out_Tkinter:
    def __init__(self,num_bits,**props):
        self.num_bits=num_bits
        root=props['tk_master']
        # Create a Frame to hold the Checkbuttons and their labels
        frame = Frame(root)
        frame.pack()

        # Create a list to hold IntVars for each bit
        self.bits = [IntVar() for _ in range(num_bits)]

        # Create Checkbuttons and labels for each bit
        for i in range(num_bits):
            # Label for the bit (above the Checkbutton)
            Label(frame, text=f"index{i}").grid(row=0, column=i, padx=5)
            Label(frame, text=f"Out_bit{num_bits - i - 1}").grid(row=1, column=i, padx=5)
            
            # Checkbutton for the bit
            Checkbutton(frame, variable=self.bits[i], state="disabled").grid(row=2, column=i, padx=5)

    def value(self, val):
        """Update the checkboxes based on the entered integer value."""
        if val!=None:
            # Get the integer value from the Entry widget
            #value = int(entry.get())
            if val < 0 or val >= 2**self.num_bits:
                raise ValueError
            
            # Update each Checkbutton to reflect the binary representation
            binary = f"{val:0{self.num_bits}b}"  # Format as n-bit binary string
            for i in range(self.num_bits):
                self.bits[i].set(int(binary[i]))  # Update each bit's state
        else:

            # Get the binary representation
            binary = "".join(str(bit.get()) for bit in self.bits)
            #print(f"Binary Input: {binary},{int(binary,2)}")
            return int(binary,2)
        #except ValueError:
            #print('ValueError:Out_Tkinter')
            # Handle invalid input
            #error_label.config(text=f"Enter a number between 0 and {2**n - 1}")
    def value_bin(self, val):
        """Update the checkboxes based on the entered integer value."""
        if val!=None:
            # Get the integer value from the Entry widget
            #value = int(entry.get())
#             if val < 0 or val >= 2**self.num_bits:
#                 raise ValueError
#             
            # Update each Checkbutton to reflect the binary representation
            #binary = f"{val:0{self.num_bits}b}"  # Format as n-bit binary string
            for i in range(self.num_bits):
                self.bits[i].set(int(val[i]))  # Update each bit's state
        else:

            # Get the binary representation
            binary = "".join(str(bit.get()) for bit in self.bits[::-1])
            #print(f"Binary Input: {binary},{int(binary,2)}")
            return binary
        #except ValueError:
            #print('ValueError:Out_Tkinter')
            # Handle invalid input
            #error_label.config(text=f"Enter a number between 0 and {2**n - 1}")

#     def reset():
#         """Reset the checkboxes to all 0."""
#         #entry.delete(0, 'end')
#         #entry.insert(0, '0')
#         for bit in self.bits:
#             bit.set(0)
#         #error_label.config(text="")

    def update_bin(self, dicci):
        for key, valu in dicci.items():
            self.bits[key].set(int(valu))
            #bin_out[key]=valu
  