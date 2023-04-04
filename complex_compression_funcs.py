import os, sys
import time
import numpy as np


"""
    Contains compression and decompression functions for ranges of
    0-255 with the use of the following functions:
        - byte_compress_complex(data)-> bytes
        - byte_decomp_complex(compressed_data)-> bytes
    
    The descriptions of the following functions contain more information on
    how and what they perform the compressions and decompressions on to the 
    provided data.
"""



def byte_compress_complex(data)-> bytes:  
    """
        Compression method that of storing duplicates for values ranging from 
        0-256. 
        
        Storing codes for patterns when reading the Lempel-Ziv-Welch (LZW) 
        Compression which uses shorter codes to replace frequently occuring 
        sequnces. Gave the idea of creating a code value that will 
        indicate for duplication.

        Here the format is use a code value of 1 (arbritrary) so when 
        a value is followed by a 1 that means it could potential
        contain dupes or it is just trying to use the value 1.

        Ideally I would use the least frequented number but that will require
        an additional pass through the Byte array.

        To check if it is a dupe it will read the following number:
            1. if the following number is 0, means it was trying to use the 
                value 1 as is

            2. if its followed by any other value it indicates how many 
                duplicates of the number before it is trying to store

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

    dup_code = 1
    its_own_val = 0

    compressed_data=list()
    prev = None
    
    count=0
    for val in data:
        
        if prev is not None:
            if val == prev:
                count += 1
            else:
                
                if count > 0:
                    if prev is dup_code: # Store the actual value represented by code
                        compressed_data.extend([dup_code, its_own_val])
                    else:
                        compressed_data.append(prev)

                    
                    if count >255: # More duplicates than storable in single byte
                        while count >0:
                            dups = (255 if count >255 else count)
                            compressed_data.extend([dup_code, dups])
                            count-=255
                    else:
                        compressed_data.extend([dup_code, count])
                    count = 0
                else:
                    if prev is dup_code: # Store the actual value represented by code
                        compressed_data.extend([dup_code, its_own_val])
                    else:
                        compressed_data.append(prev)
                
        prev = val
    
    # Making sure the last value is appended 
    if count > 0:
        if val is dup_code: # Store the actual value represented by code
            compressed_data.extend([dup_code, its_own_val])
        else:
            compressed_data.append(prev)

        
        if count >255: # More duplicates than storable in single byte
            while count >0:
                dups = (255 if count >255 else count)
                compressed_data.extend([dup_code, dups])
                count-=255

        else:
            compressed_data.extend([dup_code, count])
    else:
        compressed_data.append(prev)

    # Converting the list to a bytes object
    return bytes(compressed_data)


def byte_decomp_complex(compressed_data)-> bytes:
    """
        This function will ONLY works when paired with the 
        compression function 'byte_compress_complex()'.

        Function's purpose is to decompress the compressed
        bytes passed to it.

        Using the 'dup_code' which in this case has been choosen
        to be 1. Any 1 found will be taken as either an indication
        of the previous number containing duplicates or value the
        choosen for the 'dup_code' 


        Input:
            compressed_data : <class 'bytes'> compressed data from 
                                        'byte_compress_complex()'
        Output:
            decomp_data : <class 'bytes'> decompressed data  
    """
    # Checking input type
    if type(compressed_data) is not bytes:
        raise TypeError("The passed type NEEDS to be of type <bytes>")
    
    # Checking if input is empty
    if len(compressed_data) == 0:
        raise ValueError("No Entries found in data.")

    dup_code = 1
    its_own_val = 0

    decomp_data = list()
    prev = None
    dup_code_active = False
    
    for val in compressed_data:
        if dup_code_active:
            if val is its_own_val:
                decomp_data.append(dup_code)
                prev = dup_code
            else:
                count = val
                for repitition in np.arange(count):
                    decomp_data.append(prev)
            dup_code_active=False

        elif val is dup_code:
            dup_code_active = True
        else:
            decomp_data.append(val)
            prev =val

    # Converting the list to a bytes object
    return bytes(decomp_data)

