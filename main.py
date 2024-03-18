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

import customtkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1400x450")

class Binary128Converter:
    def __init__(self):
        self.sign_bit = '0'                                                                                         # 1 bit | 0 if positive, 1 if negative
        self.exponent_bits = '0' * 15                                                                               # 15 bits | 16383 + base_2_exponent
        self.mantissa_bits = '0' * 112                                                                              # 112 bits | binary mantissa

    def convert_decimal_to_binary128(self, decimal_number, base_2_exponent):
        # Split the decimal number into integer and fractional parts
        integer_part = int(decimal_number)                      
        fractional_part = decimal_number - integer_part

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
        self.sign_bit = '0' if binary_mantissa[0] != '-' else '1'                                                   # Calculate the sign bit
        
        binary_mantissa, base_2_exponent = self.normalize_binary_floating_point(binary_mantissa, base_2_exponent)   # Normalize the binary mantissa
        print(binary_mantissa, base_2_exponent)
        # If the base-2 exponent is less than -16382, then special case denormalized
        if base_2_exponent < -16382:                                                                                # If the base-2 exponent is less than -16382, the number is denormalized
            self.exponent_bits = '0' * 15                                                                           # The exponent bits are all zeros for denormalized numbers
            shift = min(112, -base_2_exponent - 16382) 
            shift = abs(shift)
            self.mantissa_bits = binary_mantissa.replace('.', '')
            self.mantissa_bits = '0' * shift + self.mantissa_bits
            self.mantissa_bits = self.mantissa_bits.ljust(112, '0')
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

def calculate():
    # put input into calculations
    if entry1.get() and entry2.get():  # If the binary mantissa and base-2 exponent fields are not empty
        converter.convert_binary_mantissa_to_binary128(entry1.get(), entry2.get())
    elif entry3.get() and entry4.get():  # If the decimal number and base-10 exponent fields are not empty
        converter.convert_decimal_to_binary128(float(entry3.get()), int(entry4.get()))
    
    # print final result/s
    result0.configure(text=f'----- RESULT -----')
    result1.configure(text=f'Binary format: {converter.get_binary128()}')
    result2.configure(text=f'Hexadecimal format: {converter.get_hexadecimal()}')

def clear():
    entry1.delete(0, "end")
    entry2.delete(0, "end")

label = customtkinter.CTkLabel(master=frame, text="Binary-128 Floating Point Converter", font=("Arial", 20))
label.pack(pady=10, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, 
                                placeholder_text="Binary mantissa", 
                                font=("Arial", 14),
                                height=40,
                                width=200,
                                corner_radius = 40
                                )
entry1.pack(pady=10, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, 
                                placeholder_text="Base-2 exponent", 
                                font=("Arial", 14),
                                height=40,
                                width=200,
                                corner_radius = 40
                                )
entry2.pack(pady=10, padx=10)

entry3 = customtkinter.CTkEntry(master=frame, 
                                placeholder_text="Decimal number", 
                                font=("Arial", 14),
                                height=40,
                                width=200,
                                corner_radius = 40
                                )
entry3.pack(pady=10, padx=10)

entry4 = customtkinter.CTkEntry(master=frame, 
                                placeholder_text="Base-10 exponent", 
                                font=("Arial", 14),
                                height=40,
                                width=200,
                                corner_radius = 40
                                )
entry4.pack(pady=10, padx=10)

button = customtkinter.CTkButton(master=frame, text="Convert", command=calculate, font=("Arial", 14))
button.pack(pady=10, padx=10)

button = customtkinter.CTkButton(master=frame, text="Clear", command=clear, font=("Arial", 14))
button.pack(pady=10, padx=10)

result0 = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 18))
result0.pack(pady=10, padx=10)

result1 = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 16))
result1.pack(pady=10, padx=10)

result2 = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 16))
result2.pack(pady=10, padx=10)

root.mainloop()
