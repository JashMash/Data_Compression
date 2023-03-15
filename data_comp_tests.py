#Testing libraries
import sys
import time
import unittest
import numpy as np

# Function imports
from compression_functions import byte_compress
from compression_functions import byte_decomp



# Debugger 
# self.assertEqual(input_output_debugger(data), data)
def input_output_debugger(data:bytes) -> bytes:
    """
        Function used to:
            1. Amount of time taken for compression and decompression 
            2. Size of orignal and compressed objects
            3. Find point of failure by presenting a predefined range
                of points before and after it in both the input and 
                decompressed data  
        
        Input:
            data : <class 'bytes'> data to be compressed
        Output:
            decomp : <class 'bytes'> input data that has been compressed 
                            and decompressed
    """
    print(f"Original size: {sys.getsizeof(data)}\n")

    start = time.process_time()
    compressed_bytes = byte_compress(data) 
    end = time.process_time()
    print(f"COMPRESSED INFO:")
    print(f"Time: {end-start} seconds")
    print(f"    Size: {sys.getsizeof(compressed_bytes)}\n")


    start = time.process_time()
    decomp_data = byte_decomp(compressed_bytes)
    end = time.process_time()
    print(f"DECOMPRESS INFO: \n Time: {end-start} seconds")

    index = 0
    range = 10 # Printing range from the point of error 
    for i, j in zip(decomp_data, data):
        if i is not j:
            print("Found Failure:")
            start = (0 if index-range <0 else index-range)
            end = (len(data) if index+range>len(data) else index+range)
      
            for i in data[start:end]:
                print(i, end=" ")
            print('')

            for i in decomp_data[start:end]:
                print(i, end=" ")
            print('')
            return decomp_data
        index+=1
    return decomp_data

 




class DataCompressionTests(unittest.TestCase):
    """
        Multiple tests for the functions:
            - byte_compress()
            - byte_decomp()
        To ensure their success.

        Tests:
            - Compress input datatype check
            - Decompress input datatype check
            - Compress no data
            - Decompress no data

            - Base case (last index is dupe)
            - Last index not being a dupe
            - More than 128 duplicates
            - Values greater than 127

            - Functional for 2500 Data points
            - Functional for 5000 Data points
            - Functional for 20000 Data points
    """
    def test_wrong_input_compress(self):
        """
            TEST: Compress input datatype check
        """
        data = [0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64, 
                0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09]
        

        with self.assertRaises(TypeError):
            byte_compress(data)
    
    def test_wrong_input_decompress(self):
        """
            TEST: Decompress input datatype check
        """
        data = [0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64, 
                0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09]
        

        with self.assertRaises(TypeError):
            byte_decomp(data)

    def test_no_data_compress(self):
        """
            TEST: Compressing no data
        """
        data = bytes([])
        
        with self.assertRaises(ValueError):
            byte_compress(data)
    
    def test_no_data_decompress(self):
        """
            TEST: Decompressing no data
        """
        data = bytes([])
        
        with self.assertRaises(ValueError):
            byte_decomp(data)


    def test_base_example(self):
        """
            TEST: both compression and decompression 
                    works on base case
        """
        data = bytes([0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64, 
                0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09,0x02])
        

        self.assertEqual(byte_decomp(byte_compress(data)), data)

    def test_last_not_dupe(self):
        """
            TEST: both compression and decompression 
                    works on base case
        """
        data = bytes([0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64, 
                0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09,0x02])
        

        self.assertEqual(byte_decomp(byte_compress(data)), data)

    def test_many_dups(self):
        """
            TEST: if the functions can hold more than 127
                    duplicates
        """

        randNums = np.random.randint(0,127, 50)

        duplicates = [randNums[3]]*200

        data = np.append(randNums, duplicates, axis=0)

        data = bytes(list(data))
        
        self.assertEqual(byte_decomp(byte_compress(data)), data)

    def test_data_out_of_scope(self):
        """
            TEST: If a ValueError is thrown if input contains 
                    values greater than 127
        """

        data = np.random.randint(0,255, 50)

        data = bytes(list(data))
        
        with self.assertRaises(ValueError):
            byte_decomp(byte_compress(data))


    def test_large_data_2500(self):
        """
            TEST: compression and decompression is useful
                    for 2500 Data points
        """

        data = np.random.randint(0,127, 2500)

        data = bytes(list(data))

        self.assertEqual(byte_decomp(byte_compress(data)), data)
        
    def test_large_data_5000(self):
        """
            TEST: compression and decompression is useful
                    for 5000 Data points
        """

        data = np.random.randint(0,127, 5000)

        data = bytes(list(data))

        self.assertEqual(byte_decomp(byte_compress(data)), data)
        
    def test_large_data_20000(self):
        """
            TEST: compression and decompression is useful
                    for 20000 Data points
        """

        data = np.random.randint(0,127, 200000)

        data = bytes(list(data))

        self.assertEqual(byte_decomp(byte_compress(data)), data)



if __name__ == '__main__':
    unittest.main()