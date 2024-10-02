class SparseMatrix:
    def __init__(self, matrix_file_path='', row_count=0, column_count=0):
        self.data = {}  # Dictionary to store non-zero elements
        
        self.rows = row_count
        
        self.columns = column_count
        
        if matrix_file_path != '':
            return self.read_from_file(matrix_file_path)
            
        if row_count is not None and column_count is not None:
            self.rows = row_count
            
            self.columns = column_count
            
            return
        
        raise SyntaxError("Could not initialize Sparse Matrix")

    def read_from_file(self, matrix_file_path: str):
        # Reads sparse matrix from file and populates the data dictionary.
        
        file =  open(matrix_file_path, 'r')
        
        self.rows = int(file.readline().split('=')[1].strip())
        
        self.columns = int(file.readline().split('=')[1].strip())
        
        for line in file:
            # Remove all whitespace
            line = line.strip()
            
            # Skip empty lines
            if line == '':
                continue
            
            # Skip if the line does not have proper parentheses
            if not (line.startswith('(') and line.endswith(')')):
                continue
            
            try:
                content = line.strip()[1:-1].split(',')
            
                # Skip if the line does not have all 3 valid components to make up the matrix
                if len(content) != 3:
                    continue

                row, col, value = map(int, content)

                self.set_element(row, col, value)

            except ValueError:
                # Skip lines that throw an error
                continue

    # Sets the value at [row.column]. If value is zero, it removes the entry
    def set_element(self, row, column, value):
        key = f'{row}.{column}'
       
        if value != 0:
            self.data[key] = value
        
        elif key in self.data:
            del self.data[key]

    # Gets the value at [row.column]
    def get_element(self, row, column):
        # It should return 0 if the element does not exist
        return self.data.get(f'{row}.{column}', 0)

    # Adds two sparse matrices
    def add(self, other: 'SparseMatrix') -> 'SparseMatrix':
        if self.rows != other.rows or self.columns != other.columns:
            raise SyntaxError("To add two matrices, they must have the same rows & columns")
        
        result = SparseMatrix(row_count=self.rows, column_count=self.columns)
        
        # Add elements from self
        for key, value in self.data.items():
            row, col = map(int, key.split('.'))
            
            result.set_element(row, col, value + other.get_element(row, col))
        
        # Add elements from other (not already in self)
        for key, value in other.data.items():
            if key not in self.data:
                row, col = map(int, key.split('.'))
                
                result.set_element(row, col, value)
        
        return result

    # Subtracts other sparse matrix from self
    def subtract(self, other: 'SparseMatrix') -> 'SparseMatrix':
        if self.rows != other.rows or self.columns != other.columns:
            raise SyntaxError("To subtract one matrix from another, they must have the same rows & columns")
        
        result = SparseMatrix(row_count=self.rows, column_count=self.columns)
        
        # Subtract elements from self and other
        for key, value in self.data.items():
            row, col = map(int, key.split('.'))
            
            result.set_element(row, col, value - other.get_element(row, col))
        
        # Subtract elements from other (not already in self)
        for key, value in other.data.items():
            if key not in self.data:
                row, col = map(int, key.split('.'))
                
                result.set_element(row, col, -value)
        
        return result

    # Multiplies two sparse matrices
    def multiply(self, other: 'SparseMatrix') -> 'SparseMatrix':
        if self.columns != other.rows:
            raise SyntaxError("To Multiply two matrices, the first matrix's column count must be the same as the other matrix's row count")

        result = SparseMatrix(row_count=self.rows, column_count=other.columns)

        other_non_zero = {}
        
        for key, value in other.data.items():
            row, column = map(int, key.split('.'))

            if column not in other_non_zero:
                other_non_zero[column] = []

            other_non_zero[column].append((row, value))
        
        for key, value in self.data.items():
            row, column = map(int, key.split('.'))
            
            if column in other_non_zero:
                 for other_column, other_value in other_non_zero[column]:
                     result.set_element(row, other_column, result.get_element(row, other_column) + (value * other_value))
                     
        return result

    # Displays all real elements of the sparse matrix
    def display(self):
        print(f'rows={self.rows}')
        
        print(f'cols={self.columns}')
        
        for key, value in sorted(self.data.items()):
            row, column = key.split('.')
            
            print(f"({row}, {column}, {value})")

    # Writes the sparse matrix to an output file path
    def write_to_file(self, output_file_path):
        file = open(output_file_path, 'w')
        
        file.write(f'rows={self.rows}\n')
        
        file.write(f'cols={self.columns}\n')
        
        for key, value in sorted(self.data.items()):
            row, column = key.split('.')
            
            file.write(f'({row}, {column}, {value})\n')