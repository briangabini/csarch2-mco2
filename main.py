""" 
IEEE-754 Binary-128 floating point converter (incl. all special cases)

Input/s: 
(1) binary mantissa and base-2 (i.e., 101.01x25) 
(2) Decimal and base-10 (i.e. 65.0x103). Also should support special cases (i.e., NaN).

Output/s:
(1) binary output with space between section 
(2) its hexadecimal equivalent 
(3) with option to output in text file.
"""

import tkinter as tk
from tkinter import filedialog, ttk

import customtkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1525x790")

class Binary128Converter:
    def __init__(self):
        self.sign_bit = '0'                                                                                         # 1 bit | 0 if positive, 1 if negative
        self.exponent_bits = '0' * 15                                                                               # 15 bits | 16383 + base_2_exponent
        self.mantissa_bits = '0' * 112                                                                              # 112 bits | binary mantissa

    def convert_decimal_to_binary128(self, decimal_number, base_2_exponent):
        # Split the decimal number into integer and fractional parts
        integer_part = int(decimal_number)                      
        fractional_part = abs(decimal_number) - abs(integer_part)
        binary_integer_part = format(integer_part, 'b')                                                             # Convert the integer part to binary        
        binary_fractional_part = self.convert_fraction_to_binary(fractional_part)                                   # Convert the fractional part to binary
        binary_number = binary_integer_part + '.' + binary_fractional_part                                          # Combine the binary integer and fractional parts                 
        self.convert_binary_mantissa_to_binary128(binary_number, base_2_exponent)                                   # Convert the binary mantissa to binary128

    def convert_fraction_to_binary(self, fraction):
        binary_fraction = ''                                                                                        # Set the binary fraction to an empty string                             
        while fraction:
            fraction *= 2                                                                                           # Multiply the fraction by 2
            bit = int(fraction)
            
            # If the integer part of the fraction is 1, subtract the whole number part from the fraction and add '1' to the binary fraction
            if bit == 1:                                                                                                                
                fraction -= bit
                binary_fraction += '1'
            # If the integer part of the fraction is 0, add '0' to the binary fraction
            else:
                binary_fraction += '0'
            
            if len(binary_fraction) >= 112:                                                                         # If the binary fraction is greater than 100 bits
                break                                                                                               # Break the loop
            
        return binary_fraction
    
    def normalize_binary_floating_point(self,  binary_mantissa, base_2_exponent):
        
        binary_mantissa = binary_mantissa.replace('-', '')                                                          # Remove the negative sign if any
        original_point_position = binary_mantissa.index('.')                                                        # Find the position of the binary point
        binary_mantissa = binary_mantissa.replace('.', '')                                                          # Remove the binary point
        one_position = binary_mantissa.index('1')                                                                   # Find the position of the first '1'
        bits_before_one = binary_mantissa[:one_position]                                                            # get the values of the bits before the first '1'
        normalized_mantissa_with_leading_zeroes = bits_before_one + '1.' + binary_mantissa[one_position+1:]         # attach the bits before the first '1' to the normalized mantissa (for getting the offset of the binary point after normalization)
        normalized_mantissa = '1.' + binary_mantissa[one_position+1:]                                               # Normalize the mantissa
        new_point_position = normalized_mantissa_with_leading_zeroes.index('.')                                     # Find the position of the binary point after normalization      
        shift = original_point_position - new_point_position                                                        # Calculate the shift                    

        # base_2_exponent += shift                                                                                    # add the shift to the exponent (shift can be negative or positive)
        base_2_exponent = int(base_2_exponent) + shift
        
        return normalized_mantissa, base_2_exponent

    def convert_binary_mantissa_to_binary128(self, binary_mantissa, base_2_exponent):
        # if (is_sNaN(entry1.get()) and is_sNaN(entry2.get())) or (is_sNaN(entry3.get()) and is_sNaN(entry4.get())):
        #     self.sign_bit = 'x'
        #     self.exponent_bits = '1' * 15
        #     self.mantissa_bits = '01' + 'x' * 110
        # elif (is_qNaN(entry1.get()) and is_qNaN(entry2.get())) or (is_qNaN(entry3.get()) and is_qNaN(entry4.get())):
        #     self.sign_bit = 'x'
        #     self.exponent_bits = '1' * 15
        #     self.mantissa_bits = '1' + 'x' * 111

        self.sign_bit = '0' if binary_mantissa[0] != '-' else '1'                                                   # Calculate the sign bit
        
        if '.' not in binary_mantissa:
            binary_mantissa += '.'

        binary_mantissa, base_2_exponent = self.normalize_binary_floating_point(binary_mantissa, base_2_exponent)   # Normalize the binary mantissa
        print(binary_mantissa, base_2_exponent)
        # If the base-2 exponent is less than -16382, then special case denormalized
        if base_2_exponent < -16382:                                                                                # If the base-2 exponent is less than -16382, the number is denormalized
            self.exponent_bits = '0' * 15                                                                           # The exponent bits are all zeros for denormalized numbers
            shift = min(112, -base_2_exponent - 16382)
            shift = abs(shift - 1)
            self.mantissa_bits = binary_mantissa.replace('.', '')
            self.mantissa_bits = '0' * shift + self.mantissa_bits
            self.mantissa_bits = self.mantissa_bits.ljust(112, '0')[:112]
        # If the base-2 exponent is greater than 16383, then special case infinity
        elif base_2_exponent > 16383:
            self.exponent_bits = '1' * 15                                                                           # The exponent bits are all ones for infinity
            self.mantissa_bits = '0' * 112                                                                           # The mantissa bits are all zeros for infinity
        else:
            self.exponent_bits = format(16383 + base_2_exponent, '015b')                                                # Calculate the exponent bits               
            self.mantissa_bits = binary_mantissa.split('.')[1].ljust(112, '0')[:112]                                  # Calculate the mantissa bits      

    def get_binary128(self):
        return self.sign_bit + ' ' + self.exponent_bits + ' ' + self.mantissa_bits                                  # Return the binary128 representation
        
    def get_hexadecimal(self):
        binary128 = self.get_binary128().replace(' ', '')                                                  # Remove the spaces
        hex_value = hex(int(binary128, 2)).upper()                                                                  # Convert binary to hexadecimal
        
        return hex_value
    
# Test with binary mantissa
# binary_mantissa = input("Enter the binary mantissa: ")
# base_2_exponent = int(input("Enter the base-2 exponent: "))

converter = Binary128Converter()
    
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill="both", expand=True)


label = customtkinter.CTkLabel(master=frame, text="Binary-128 Floating Point Converter", font=("Arial", 20))
label.pack(pady=10, padx=10)

# dropdown menu for input type
input_type = tk.StringVar()
combobox = ttk.Combobox(master=frame, textvariable=input_type, values=["Binary", "Decimal"], state="readonly")
combobox.pack(pady=10, padx=10)

# set default value dropdown to "Binary"
input_type.set("Binary")

import re


def is_valid_binary(input_string):
    # The regex pattern for a binary number with or without a decimal point
    pattern = r'^-?[01]+(\.[01]+)?$|^sNaN$|^qNaN$'
    return bool(re.match(pattern, input_string))

def is_valid_decimal(input_string):
    # The regex pattern for a decimal number
    pattern = r'^-?\d+(\.\d+)?$|^sNaN$|^qNaN$'
    return bool(re.match(pattern, input_string))

def is_valid_exponent(input_string):
    # The regex pattern for a base-2 exponent
    pattern = r'^-?\d+$|^sNaN$|^qNaN$'
    return bool(re.match(pattern, input_string))

def is_sNaN(input_string):
    # The regex pattern for a base-2 exponent
    pattern = r'^sNaN$'
    return bool(re.match(pattern, input_string))

def is_qNaN(input_string):
    # The regex pattern for a base-2 exponent
    pattern = r'^qNaN$'
    return bool(re.match(pattern, input_string))

error_message = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 16))
error_message.pack(pady=10, padx=10)

def calculate():
    error_message.configure(text="")
    # put input into calculations
    if input_type.get() == "Binary":  # If the binary mantissa and base-2 exponent fields are not empty
        if not entry1.get() or not entry2.get():
            error_message.configure(text="Please enter a binary mantissa and a base-2 exponent.")
            return
        elif not is_valid_binary(entry1.get()):
            error_message.configure(text="Invalid binary input. Please enter a binary number (with or without a decimal point).")
            return
        elif not is_valid_exponent(entry2.get()):
            error_message.configure(text="Invalid base 2 exponent input. Please enter a whole number exponent, either positive or negative.")
            return
        converter.convert_binary_mantissa_to_binary128(entry1.get(), entry2.get())
    elif input_type.get() == "Decimal":  # If the decimal number and base-10 exponent fields are not empty
        if not entry3.get() or not entry4.get():  # If the decimal number or base-10 exponent field is empty
            error_message.configure(text="Please enter a decimal number and a base-10 exponent.")
            return
        elif not is_valid_decimal(entry3.get()):
            error_message.configure(text="Invalid decimal input. Please enter a number (with or without a decimal point).")
            return
        elif not is_valid_exponent(entry4.get()):
            error_message.configure(text="Invalid base 10 exponent input. Please enter a whole number exponent, either positive or negative.")
            return
        converter.convert_decimal_to_binary128(float(entry3.get()), int(entry4.get()))
    
    # print final results
    result1.configure(text=f'BINARY RESULT = {converter.get_binary128()}')
    result11.configure(text=f'Sign bit: {converter.sign_bit}')
    result12.configure(text=f'Exponent: {converter.exponent_bits}')
    result13.configure(text=f'Mantissa: {converter.mantissa_bits}')
    resultdiv.configure(text=f'--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    result2.configure(text=f'HEXADECIMAL RESULT = {converter.get_hexadecimal()}')
    save_button.pack(pady=10, padx=10)

def clear():
    entry1.delete(0, "end")
    entry2.delete(0, "end")
    entry3.delete(0, "end")
    entry4.delete(0, "end")

# 143 - 173 are what I edited - Carl
binary_frame = customtkinter.CTkFrame(master=frame)
binary_frame.pack(pady=10, padx=10, fill="both")
decimal_frame = customtkinter.CTkFrame(master=frame)

result_frame = customtkinter.CTkFrame(master=frame)

convert_button = customtkinter.CTkButton(master=frame, text="Convert", command=calculate, font=("Arial", 14)) # calculates the result based on the given input
clear_button = customtkinter.CTkButton(master=frame, text="Clear", command=clear, font=("Arial", 14)) # clears all text input

convert_button.pack(pady=10, padx=10)
clear_button.pack(pady=10, padx=10)
result_frame.pack(pady=10, padx=10, fill="both")

i = 0
# update displayed input fields based on selected input type
def update_inputs(event):
    global i
    error_message.configure(text="")
    result1.configure(text="")
    result11.configure(text="")
    result12.configure(text="")
    result13.configure(text="")
    resultdiv.configure(text="")
    result2.configure(text="")
    save_button.pack_forget()
    
    if i > 0:
        convert_button.pack_forget()
        clear_button.pack_forget()
    if input_type.get() == "Binary":
        # reset frame
        decimal_frame.pack_forget()
        convert_button.pack_forget()
        clear_button.pack_forget()
        result_frame.pack_forget()
        
        # append (or pack) new frames
        binary_frame.pack(pady=10, padx=10, fill="both")
        convert_button.pack(pady=10, padx=10)
        clear_button.pack(pady=10, padx=10)
        result_frame.pack(pady=10, padx=10, fill="both")
        
        
    else:
        # reset frame
        binary_frame.pack_forget()
        convert_button.pack_forget()
        clear_button.pack_forget()
        result_frame.pack_forget()
        
        # append (or pack) new frames
        decimal_frame.pack(pady=10, padx=10, fill="both")
        convert_button.pack(pady=10, padx=10)
        clear_button.pack(pady=10, padx=10)
        result_frame.pack(pady=10, padx=10, fill="both")
        
    i += 1
    print(i)
    
def save_to_file():
    # Open a save file dialog
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    
    # If a file path is provided
    if file_path:
        # Write the result to the file
        with open(file_path, "w") as file:
            file.write(f'BINARY RESULT = {converter.get_binary128()}\n')
            file.write(f'Sign bit: {converter.sign_bit}\n')
            file.write(f'Exponent: {converter.exponent_bits}\n')
            file.write(f'Mantissa: {converter.mantissa_bits}\n')
            file.write(f'--------------------------------------------------------------------------------------------------------------------------\n')
            file.write(f'HEXADECIMAL RESULT = {converter.get_hexadecimal()}\n')
            
combobox.bind("<<ComboboxSelected>>", update_inputs)

entryBinaryIntro = customtkinter.CTkLabel(master=binary_frame, text="Please input your binary values:", font=("Arial", 14))
entryBinaryIntro.pack(pady=10, padx=10)

entry1 = customtkinter.CTkEntry(master=binary_frame, 
                                placeholder_text="Binary mantissa", 
                                font=("Arial", 14),
                                height=40,
                                width=200,
                                corner_radius = 40
                                )
entry1.pack(pady=10, padx=10)

entry2 = customtkinter.CTkEntry(master=binary_frame, 
                                placeholder_text="Base-2 exponent", 
                                font=("Arial", 14),
                                height=40,
                                width=200,
                                corner_radius = 40
                                )
entry2.pack(pady=10, padx=10)

entryDecimalIntro = customtkinter.CTkLabel(master=decimal_frame, text="Please input your decimal values:", font=("Arial", 14))
entryDecimalIntro.pack(pady=10, padx=10)

entry3 = customtkinter.CTkEntry(master=decimal_frame, 
                                placeholder_text="Decimal number", 
                                font=("Arial", 14),
                                height=40,
                                width=200,
                                corner_radius = 40
                                )
entry3.pack(pady=10, padx=10)

entry4 = customtkinter.CTkEntry(master=decimal_frame, 
                                placeholder_text="Base-10 exponent", 
                                font=("Arial", 14),
                                height=40,
                                width=200,
                                corner_radius = 40
                                )
entry4.pack(pady=10, padx=10)

# result1 is for the binary format of the result
result1 = customtkinter.CTkLabel(master=result_frame, text="", font=("Arial", 18))
result1.pack(anchor="w", pady=14, padx=10)

# result11 is for the SIGN BIT of the binary format of the result
result11 = customtkinter.CTkLabel(master=result_frame, text="", font=("Arial", 16))
result11.pack(anchor="w", pady=3, padx=10)

# result12 is for the EXPONENT of the binary format of the result
result12 = customtkinter.CTkLabel(master=result_frame, text="", font=("Arial", 16))
result12.pack(anchor="w", pady=3, padx=10)

# result13 is for the MANTISSA of the binary format of the result
result13 = customtkinter.CTkLabel(master=result_frame, text="", font=("Arial", 16))
result13.pack(anchor="w", pady=3, padx=10)

# resultdiv is for separating the binary and hexadecimal results
resultdiv = customtkinter.CTkLabel(master=result_frame, text="", font=("Arial", 18))
resultdiv.pack(anchor="w", pady=10, padx=10)

# result2 is for the hexadecimal format of the result
result2 = customtkinter.CTkLabel(master=result_frame, text="", font=("Arial", 18))
result2.pack(anchor="w", pady=14, padx=10)

# save_button is for saving the results to a text file; Should only show up when the result is calculated
save_button = customtkinter.CTkButton(master=frame, text="Save to File", command=save_to_file, font=("Arial", 14))

root.mainloop()