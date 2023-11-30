class Numberbase:
    def __init__(self):
        self.base_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.base10 = 10
        self.base2 = 2

    def decimal_to_base(self, number: float, fin_base: int):
        """
        Converts a float number from base 10 to a float number between base 2 and 16.

        Given the number and the final base, this function computes
        the equivalent number of the decimal.

        Args:
            number (float): The number
            fin_base (int): The final base

        Returns:
            str: The equivalent number of the decimal.

        Example:
            >>> nb = Numberbase()
            >>> nb.decimal_to_base(-346.7, 36)
            '-9M.P777777761'
            >>> nb.decimal_to_base(-3466.9, 5)
            '-102331.4222222222'
            >>> nb.decimal_to_base(-836126, 15)
            '-117B1B'
            >>> nb.decimal_to_base(836126, 16)
            'CC21E'
            >>> nb.decimal_to_base(1.9789298498448, 14)
            '1.D9C27D78DC'
        """

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

    def check(self, number, base):
        """
        Check if the input number is valid for the specified base.

        Raises a ValueError if an invalid digit is found.

        Args:
            number (str): The input number.
            base (int): The specified base.

        Raises:
            ValueError: If an invalid digit is found.
        """
        for char in number:
            if char.isdigit():
                if int(char) >= base:
                    raise ValueError("Invalid digit in the input, input digit should not be greater than base")
            if ord('A') <= ord(char) <= ord('Z'):
                # Convert the character to a numeric value in base 36
                numeric_value = int(char, 36)
                if numeric_value >= base:
                    raise ValueError("Invalid digit in the input, input digit should not be greater than base")

    def base_to_decimal(self, number, base):
        """
        Convert a number from a given base to base 10.

        Args:
            number (str): The number to be converted.
            base (int): The base of the input number.

        Returns:
            float: The equivalent number in base 10.

        Example:
            >>> nb = Numberbase()
            >>> nb.base_to_decimal("1101.001", 2)
            13.125
            >>> nb.base_to_decimal("1A.2", 16)
            26.125
            >>> nb.base_to_decimal("12345", 6)
            5461
        """
        # Convert the number to a string
        number = str(number)
        # Check if the base is within the valid range (2 to 36)
        if base < 2 or base > 36:
            raise ValueError("Base must be between 2 and 36")
        # Check if the digits in the number are valid for the specified base
        self.check(number, base)
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

    def convert_base_to_base(self, number, from_base, to_base):
        """
        Convert a number from one base to another.

        Args:
            number (str): The number to be converted.
            from_base (int): The base of the input number.
            to_base (int): The target base.

        Returns:
            str: The equivalent number in the target base.

        Example:
            >>> nb = Numberbase()
            >>> nb.convert_base_to_base("1101.001", 2, 16)
            'D.2'
            >>> nb.convert_base_to_base("1A.2", 16, 2)
            '11010.001'
            >>> nb.convert_base_to_base("12345", 6, 8)
            '101111'
        """
        # Convert the number to a string
        number = str(number)
        # Check if the digits in the number are valid for the source base


        self.check(number, from_base)
        # Convert the number from the source base to base 10
        decimal_number = self.base_to_decimal(number, from_base)

        # Convert the base 10 number to the target base
        result = self.decimal_to_base(decimal_number, to_base)
        return result

    def perform_arithmetric_operation(self, number1, number2, operation, from_base):
        """
        Perform arithmetic operations on numbers in the specified base.

        Args:
            number1 (str): The first number.
            number2 (str): The second number.
            operation (str): The arithmetic operation ('+', '-', '*', '/', '//', '**').
            from_base (int): The base of the input numbers.

        Returns:
            str: The result of the arithmetic operation in the specified base.

        Example:
            >>> nb = Numberbase()
            >>> nb.perform_arithmetric_operation('1101', '101', '+', 2)
            '10110'
            >>> nb.perform_arithmetric_operation('1A', '2', '*', 16)
            '34'
            >>> nb.perform_arithmetric_operation('1101', '101', '/', 2)
            '10.1'
            >>> nb.perform_arithmetric_operation('ABC', '10', '**', 16)
            '786F08A8B6642B2B3D17370B5ACBF83A11A91C3DCE2293FA2D8E522D1629951A'
        """
        if from_base != self.base10:
            base10_number1 = float(self.convert_base_to_base(number1, from_base, self.base10))
            base10_number2 = float(self.convert_base_to_base(number2, from_base, self.base10))
        else:
            base10_number1 = float(number1)
            base10_number2 = float(number2)

        # Perform the arithmetic operation in base 10
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

        # Convert the result back to the original base
        return self.decimal_to_base(result, from_base)

    def radixcomplement(self, number, from_base):
        """
        Compute the radix complement of a number in the specified base.

        Args:
            number (str): The number.
            from_base (int): The base of the input number.

        Returns:
            str: The radix complement of the input number.

        Example:
            >>> nb = Numberbase()
            >>> nb.radixcomplement('10101', 2)
            '01010'
            >>> nb.radixcomplement('12345', 8)
            '5432'
            >>> nb.radixcomplement('ABC', 16)
            '543'
        """
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

    def diminishedradixcomplement(self, number, from_base):
        """
        Compute the diminished radix complement of a number in the specified base.

        Args:
            number (str): The number.
            from_base (int): The base of the input number.

        Returns:
            str: The diminished radix complement of the input number.

        Example:
            >>> nb = Numberbase()
            >>> nb.diminishedradixcomplement('10101', 2)
            '01011'
            >>> nb.diminishedradixcomplement('12345', 8)
            '5431'
            >>> nb.diminishedradixcomplement('ABC', 16)
            '542'
        """
        # Calculate the radix complement
        you = self.radixcomplement(number, from_base)

        # Perform arithmetic operation to get the diminished radix complement
        dim = self.perform_arithmetric_operation(str(you), 1, "-", from_base)
        return dim
        
    def base_to_binary_float(self, number:float|int) -> list[str]:
    """
    Converts a number to 32 bit binary float
       Args: 
        number (float/int): The number to convert. 

       Returns:
        list[str]: 3 elements, sign(a 1 or 0 representing negative or positive respectively), exponent and mantissa
    """
    output = [] #ouput array
    is_negative = False
    
    #checks if number is negative
    if number < 0:
        number = abs(number)
        is_negative = True

    #Separates the integer and fractional parts of the number
    int_part = number // 1
    frac_part = number - int_part

    #binary representation for the integer and fractional parts of the number
    int_base_2_rep = self.convert_base_to_base(int_part,10, 2)
    frac_base_2_rep = self.convert_base_to_base(frac_part,10, 2)
    exp = len(int_base_2_rep) - 1

    if frac_base_2_rep == '0':
        mantissa = int_base_2_rep

    else:
        point_index = frac_base_2_rep.find('.')
        mantissa = int_base_2_rep[1:] +  frac_base_2_rep[point_index+1:]

    e_b = exp + 127
    decimal_e_b = self.convert_base_to_base(e_b, 10,2)

    #Checks the sign to determine if it's a 1 or 0
    if(is_negative):
        output.append('1')
    else:
        output.append('0')

    output.append(decimal_e_b)

    #Fill out with 0's to make it 32 bit
    if len(mantissa) < 23:
        total = 23 - len(mantissa)
        added_zeroes = '0' * total
        mantissa = mantissa + added_zeroes
        output.append(mantissa)
    return output
    

    
 
