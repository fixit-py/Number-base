class Numberbase:
    def __init__(self):
        self.base_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.base10 = 10
        self.base2 = 2
        
        
    def decimal_to_base(self,number: float, fin_base: int):
        """ Returns a signed float decimal number in the specified base.
        """
        self.fin_base=fin_base
        # Checks if the input number is negative
        is_negative = False
        if number < 0:
            is_negative = True
            # Make the number positive for processing
            number = abs(number)
        # Separates the integer and fractional parts of the number
        int_part = int(number)
        fraction_part = number - int_part
        final_value = ""  # Initializes an empty string
    
        # Converts integer part to the desired base
        while int_part > 0:
            remainder = int_part % fin_base
            final_value = self.base_digits[remainder] + final_value
            int_part //= fin_base
    
        # Handles the case when the integer part is 0
        if final_value == "":
            final_value = "0"
    
        # Adds a decimal point if there is a fractional part
        if fraction_part > 0:
            final_value += "."
    
        # Converts fractional part to the desired base with a limited number of digits
        max_fraction_digits = 10
        current_fraction_digits = 0
        while fraction_part > 0 and current_fraction_digits < max_fraction_digits:
            fraction_part *= fin_base
            digit = int(fraction_part)
            final_value += self.base_digits[digit]
            fraction_part -= digit
            current_fraction_digits += 1
    
        # Convert the final result back to a float and apply a negative sign if necessary
        if is_negative:
            final_value = "-" + final_value
    
        return final_value
    
    def check(self,number,base):
        for char in number:
                if char.isdigit():
                    if int(char) >= base:
                        raise ValueError("Invalid digit in the input, input digit should not be greater than base")            
                if ord('A') <= ord(char) <= ord('Z'):
                     #Convert the character to a numeric value in base 36
                    numeric_value = int(char, 36)
                    if numeric_value >= base:
                        raise ValueError("Invalid digit in the input, input digit should not be greater than base")
                    
    def base_to_decimal(self,number, base):
        # Check if the base is within the valid range (2 to 36)
        
        number = str(number)
        if base < 2 or base > 36:
            raise ValueError("Base must be between 2 and 36")    
        self.check(number,base)
        is_negative = False
        if number.startswith('-'):
            is_negative = True
            number = number[1:]
    
        # Split the number into integer and fractional parts (if present)
        if '.' in number:
            integer_part, fractional_part = number.split('.')
        else:
            integer_part = number
            fractional_part = "0"
    
        decimal_integer = 0
        power = 0
    
        # Convert the integer part to decimal
        for digit in integer_part[::-1]:
            if digit.isdigit():
                decimal_integer += int(digit) * (base ** power)
            elif 'A' <= digit <= 'Z':
                decimal_integer += (ord(digit) - ord('A') + 10) * (base ** power)
            else:
                raise ValueError("Invalid digit in the input, input digit should not be greater than base")
    
            power += 1
    
        # Convert the fractional part to decimal
        decimal_fractional = 0
        fractional_base = 1 / base
    
        for digit in fractional_part:
            if digit.isdigit():
                decimal_fractional += int(digit) * fractional_base
            elif 'A' <= digit <= 'Z':
                decimal_fractional += (ord(digit) - ord('A') + self.base10) * fractional_base
            else:
                raise ValueError("Invalid digit in the input, input digit should not be greater than base")
    
            fractional_base /= base
    
        # Combine the integer and fractional parts to get the final decimal number
        decimal = decimal_integer + decimal_fractional
    
        # Apply the negative sign if the number was negative
        if is_negative:
            decimal = -decimal
    
        return decimal   
    
    def convert_base_to_base(self,number, from_base, to_base):
        number = str(number)
        self.check(number,from_base)
        # Convert the number from the source base to base 10
        decimal_number = self.base_to_decimal(number, from_base)
        
        # Convert the base 10 number to the target base
        result = self.decimal_to_base(decimal_number, to_base)
        
        return result
    
    def perform_arithmetric_operation(self,number1,number2,operation,from_base):
        if from_base != self.base10:
            base10_number1 = float(self.convert_base_to_base(number1,from_base,self.base10))
            base10_number2 = float(self.convert_base_to_base(number2,from_base,self.base10))
        else:
            base10_number1 = float(number1)
            base10_number2 = float(number2)
        if operation == '+':
            result = base10_number1 + base10_number2
        elif operation == '-':
            result = base10_number1 - base10_number2
        elif operation == '*':
            result = base10_number1 * base10_number2
        elif operation == '/':
            result = base10_number1 / base10_number2
        elif operation == '//':
            result = base10_number1 // base10_number2
        elif operation == '**':
            result = base10_number1 ** base10_number2       
        else:
            raise ValueError("Invalid Operation")
        return self.decimal_to_base(result,from_base)
    
    
    
    def radixcomplement(self,number, from_base):
        # Check if the number is negative
       
        # Convert the number to a string
        number_str = str(number)
    
        # Check if the input number is valid for the given base
        for char in number_str:
            if not ('0' <= char <= '9' or 'A' <= char <= 'Z'):
                raise ValueError("Invalid digit in the input. Digits should be valid for the specified base.")
    
        # Calculate the complement
        complement_str = ""
        carry = 1  # Initialize the carry to 1
        for char in reversed(number_str):
            if '0' <= char <= '9':
                digit = int(char)
            else:
                digit = ord(char) - ord('A') + 10
            complement_digit = (from_base - 1 - digit + carry) % from_base
            carry = 1 if (from_base - 1 - digit + carry) >= from_base else 0
            if 0 <= complement_digit <= 9:
                complement_str = str(complement_digit) + complement_str
            else:
                complement_str = chr(ord('A') + complement_digit - 10) + complement_str
        return complement_str
    
   
    def diminishedradixcomplement(self,number, from_base):
        you = self.radixcomplement(number, from_base)
        dim = self.perform_arithmetric_operation(str(you),1,"-",from_base)
        return dim
    
    #def IEEE(self,number,from_base):
        #number = convert_base_to_base(number,from_base,2)
        #count = 0
        #for char in number:
            #print(char)
            #count = count + 1
        #count = count - 1
        #print(count)
        #mantissa = 127 + count
        #mantissa =  convert_base_to_base(number,from_base,2)
        #return number
    
#print(Numberbase().IEEE(132,10))      
    
print(Numberbase().decimal_to_base(-346.7,36))

print(Numberbase().base_to_decimal("12345", 6))
print(Numberbase().perform_arithmetric_operation("1000.0","10.1","+",2))
print(Numberbase().radixcomplement(34,12))
print(Numberbase().diminishedradixcomplement(34,12))
