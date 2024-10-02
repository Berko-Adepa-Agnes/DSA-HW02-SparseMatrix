import os
from sparse_matrix import SparseMatrix

def main():
    print("Select matrix operation:")
    
    print("1. Addition")
    
    print("2. Subtraction")
    
    print("3. Multiplication")
    
    print("4. Display Sparse Matrix")
    
    choice = input("Enter your choice (1/2/3/4): ").strip()
    
    if choice not in {'1', '2', '3', '4'}:
        return print("Invalid choice. Quitting...")

    matrix_file_1 = input(f"Enter the path of the{' first' if choice != '4' else ''} matrix file: ").strip()
   
    matrix_file_2 = ''
        
    if choice != '4':   
        matrix_file_2 = input("Enter the path of the second matrix file: ").strip()

    try:
        matrix1 = SparseMatrix(matrix_file_path=matrix_file_1)
        
        matrix2 = SparseMatrix(matrix_file_path=matrix_file_2)
                
        if choice == '4':
            return matrix1.display()
        
        output_file = ''

        directory = matrix_file_1.split('sample_input_for_students')[0]
        
        if choice == '1':
            result = matrix1.add(matrix2)

            output_file = f'{directory}/outputs/Addition of {matrix_file_1.split("/")[-1].split(".txt")[0]} and {matrix_file_2.split("/")[-1].split(".txt")[0]}.txt'

        elif choice == '2':
            result = matrix1.subtract(matrix2)
          
            output_file = f'{directory}/outputs/Subtraction of {matrix_file_2.split("/")[-1].split(".txt")[0]} from {matrix_file_1.split("/")[-1].split(".txt")[0]}.txt'

        elif choice == '3':
            result = matrix1.multiply(matrix2)
        
            output_file = f'{directory}/outputs/Multiplication of {matrix_file_1.split("/")[-1].split(".txt")[0]} and {matrix_file_2.split("/")[-1].split(".txt")[0]}.txt'
            
        os.makedirs(f'{directory}/outputs', exist_ok=True)
        
        result.write_to_file(output_file)
        
        print(f"Operation successful! Result written to {output_file}")
    
    except SyntaxError as error:
        print(f"Syntax Error: {error}")
    
    except FileNotFoundError:
        print("File Not Found Error: One or both input files were not found.")
    
    except Exception as error:
        print(f"Unexpected Error: An unexpected error occurred: {error}")

main()