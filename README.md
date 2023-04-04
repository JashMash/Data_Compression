# Data Compression Algorithm

Here my goal is to create a set of functions that will compress<br/>
and decompress a byte array. This is given the input does contain<br/>
multiple duplicates that follow each other.<br/>

I have implemented the solutions below and provided unit tests <br/>
for both of the compression and decompression functions. <br/>
The reason I have provided both is to show you the thought process<br/>
of how I was able to come up with these solutions.


### Simple duplication compression for range 0-127.
Functions:
   - byte_compress(data)-> bytes
   - byte_decomp(compressed_data)-> bytes <br/>

Unit test file:
   - data_comp_tests.py
<br/><br/>

### More complex duplication storage for values ranging 0-255.<br/>
Functions:
   - byte_compress_complex(data)-> bytes
   - byte_decomp_complex(compressed_data)-> bytes<br/>

Unit test file:
   - data_comp_complex_tests.py

<br/><br/>

## Brain stormed solutions:
1. ### Simple duplication compression for range 0-127.<br/>
   Since the limit of the input is between 0-127, and bytes can <br/>
   store number up to 256. I would use any number above 127 to <br/>
   store the number of additional duplicates there are as in. <br/>
   Examples:<br/>
      1. Input:<br/>
            [1, 1, 1, 4, 5] 
         
         Compressed:<br/> 
            [1, 127+2, 4, 5]

      2. If more than 128 duplicates it would be <br/>
         stored as shown in the example:<br/>
         Input: <br/>
            [1]*200

         Compressed:<br/>
            [1, 127+128, 127+72]

2. ### More complex duplication storage for values ranging 0-255.<br/>
   Using the first compression technique wouldnt be scalable <br/>
   if they were to input a byte array with values ranging <br/>
   from 0-256. <br/>

   Storing codes for patterns when reading the Lempel-Ziv-Welch (LZW) <br/>
   Compression which uses shorter codes to replace frequently occuring <br/>
   sequnces. Gave the idea of creating a code value that will <br/>
   indicate for duplication.<br/>

   Here the format is use a code value of 1 (arbritrary) so when <br/>
   a value is followed by a 1 that means it could potential<br/>
   contain duplicates or it is just trying to use the value 1.<br/>

   Ideally I would use the least frequented number but that will require<br/>
   an additional pass through the Byte array.<br/>

   To check if it is a dupe it will read the following number:
      1. if the following number is 0, means it was trying to use the <br/>
            value 1 as is

      2. if its followed by any other value it indicates how many <br/>
            duplicates of the number before it is trying to store
   
   Examples:<br/>

      1. Input:<br/>
            [2, 2, 2, 2, 2, 2, 3, 1]
      
         Compressed:<br/>
            [2, 1, 4, 3, 1, 0]
      
      2. For many duplicates:<br/>
         Input:<br/>
            [2]*300

         Compressed:<br/>
            [2, 1,255, 1,44]
      
      3. For duplicate code values:
         Input:<br/>
            [2, 1,1,1,1,1,1,1,1]
      
         Compressed:<br/>
            [2, 1,0, 1,7]

   