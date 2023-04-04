import os, sys
import time
import numpy as np


"""
    Contains compression and decompression functions for ranges of 0-127
    with the use of the following functions:
        - byte_compress(data: bytes)-> bytes
        - byte_decomp(compressed_data: bytes)-> bytes
    
    The descriptions of the following functions contain more information on
    how and what they perform the compressions and decompressions on to the 
    provided data.
"""




def byte_compress(data)-> bytes: 
    """
        Compression function that will take a byte array containing
        values ranging from 0-127 and compress consecutive duplicates.

        This function will read through all the values appending them to 
        the compressed output until theres a
        duplicate/s. Once a duplicate is found it will create a 
        counter that updates till a different value is found. 
        Then takes the count adds it to 127 and appends it to the 
        compressed output. Allowing the decompression function to know
        when there are duplicates of the previouc value.

        If more than 128 duplicates it will append another 
        127 + (remain count) until the counter is 0.

        Input:
            data : <class 'bytes'> data to be compressed
        Output:
            compressed_data : <class 'bytes'> input data that has been compressed 
    """
    # Checking input type
    if type(data) is not bytes:
        raise TypeError("The passed type NEEDS to be of type <bytes>")
    
    # Checking if input is empty
    if len(data) == 0:
        raise ValueError("No Entries found in data.")

    compressed_data=list()
    prev = None
    
    count=127
    for val in data:
        if val >127:
            raise ValueError('This array contains value outside range of 0-127,'\
                             'this compression function can only handle values 0-127')

        if prev is not None:
            if val == prev:
                count += 1
            else:
                if count > 127:
                    if count >255:
                        dup_array = []
                        while count >127:
                            dups = (255 if count >255 else count)
                            dup_array.append(dups)
                            count-=128
                        compressed_data.append(prev)
                        compressed_data.extend(dup_array)
                    else:
                        compressed_data.extend([prev,count])
                    count = 127
                else:
                    compressed_data.append(prev)
                
        prev = val


    # Making sure the last value is appended 
    if count > 127:
        if count >255:
            dup_array = []
            while count >127:
                dups = (255 if count >255 else count)
                dup_array.append(dups)
                count-=128
            compressed_data.append(prev)
            compressed_data.extend(dup_array)
        else:
            compressed_data.extend([prev,count])
        count = 127
    else:
        compressed_data.append(prev)

    # Converting the list to a bytes object
    return bytes(compressed_data)

def byte_decomp(compressed_data)-> bytes:
    """
        This function will ONLY works when paired with the 
        compression function 'byte_compress()'.

        Function's purpose is to decompress the compressed
        bytes passed to it.

        Reads through all values in byte array, when a value
        greater than 127 is found. It will create 'x' number of
        duplicates for most recent value that wasnt greater than 
        127, where x = value - 127. 
        
        If followed by another number greater than 127 it will 
        repeat the process for most recent value that wasnt 
        greater than 127.

        Input:
            compressed_data : <class 'bytes'> data to be decompressed
        Output:
            decomp_data : <class 'bytes'> decompressed data     
    """
    # Checking input type
    if type(compressed_data) is not bytes:
        raise TypeError("The passed type NEEDS to be of type <bytes>")
    
    # Checking if input is empty
    if len(compressed_data) == 0:
        raise ValueError("No Entries found in data.")

    decomp_data = list()
    prev = None
    for val in compressed_data:
        if val >127:
            count = val -127
            for repitition in np.arange(count):
                decomp_data.append(prev)
        else:
            decomp_data.append(val)
            prev =val

    # Converting the list to a bytes object
    return bytes(decomp_data)

