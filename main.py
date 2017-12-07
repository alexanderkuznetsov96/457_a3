# Image compression
#
# You'll need Python 2.7 and must install these packages:
#
#   scipy, numpy
#
# You can run this *only* on PNM images, which the netpbm library is used for.
#
# You can also display a PNM image using the netpbm library as, for example:
#
#   python netpbm.py images/cortex.pnm


import sys, os, math, time, netpbm
import numpy as np


# Text at the beginning of the compressed file, to identify it


headerText = 'my compressed image - v1.0'

# Compress an image

def initializeDictionary(dict_size) :
  d = {}
  for i in xrange(dict_size):
    d[chr(0) + chr(i)] = convert16bitto2char(i)
  return d

def getfirstbyte(v) :
    return (v & (0xFF << 8)) >> 8
    
def getsecondbyte(v) :
    return v & 0xFF
    
def convert16bitto2char(n) :
    return chr(getfirstbyte(n)) + chr(getsecondbyte(n))
    
def convert2charto16bit(s) :
    fb = s[0]
    sb = s[1]
    return (ord(fb) << 8) | ord(sb)
    
def compress( inputFile, outputFile ):

  # Read the input file into a numpy array of 8-bit values
  #
  # The img.shape is a 3-type with rows,columns,channels, where
  # channels is the number of component in each pixel.  The img.dtype
  # is 'uint8', meaning that each component is an 8-bit unsigned
  # integer.

  img = netpbm.imread( inputFile ).astype('uint8')
  
  # Compress the image
  #
  # REPLACE THIS WITH YOUR OWN CODE TO FILL THE 'outputBytes' ARRAY.
  #
  # Note that single-channel images will have a 'shape' with only two
  # components: the y dimensions and the x dimension.  So you will
  # have to detect this and set the number of channels accordingly.
  # Furthermore, single-channel images must be indexed as img[y,x]
  # instead of img[y,x,1].  You'll need two pieces of similar code:
  # one piece for the single-channel case and one piece for the
  # multi-channel case.

  startTime = time.time()
 
  outputBytes = bytearray()
  
  # Initialize dictionary
  maxsize = 65536
  dict_size = 256
  d = initializeDictionary(dict_size)
  s = ''
  # For debugging
  f = open('encoded_bytes.txt', 'w')
  ef = open('encoding_input.txt', 'w')
  
  for y in range(img.shape[0]):
    for x in range(img.shape[1]):
      for c in range(img.shape[2]):
        fp = 0;
        if(x > 0):
            fp = img[y,x-1,c]
        e = img[y,x,c] - fp
        ef.write(str(e) + ' \n')
        if(s + chr(e) in d):
            s += chr(e)
        else:
            #f.write(' s = ' + s + ' d[s]= ' + str(d[s
            #f.write(str(d[s]))
            #f.write(d[s] + '\n')
            f.write(str(ord(d[s][0])) + ',' + str(ord(d[s][1])) + '\n')
            outputBytes.append(d[s][0])
            outputBytes.append(d[s][1])
            d[s + chr(e)] = convert16bitto2char(dict_size)
            dict_size += 1
            if(dict_size > maxsize):
                dict_size = 256
                d = initializeDictionary(dict_size)
            s = chr(e)
  outputBytes.append(d[s][0])
  outputBytes.append(d[s][1])
  #outputBytes.append(getfirstbyte(d[s]))
  #outputBytes.append(getsecondbyte(d[s]))
  endTime = time.time()
  ef.close()
  f.close()
  
  # Output the bytes
  #
  # Include the 'headerText' to identify the type of file.  Include
  # the rows, columns, channels so that the image shape can be
  # reconstructed.

  outputFile.write( '%s\n'       % headerText )
  outputFile.write( '%d %d %d\n' % (img.shape[0], img.shape[1], img.shape[2]) )
  outputFile.write( outputBytes )

  # Print information about the compression
  
  inSize  = img.shape[0] * img.shape[1] * img.shape[2]
  outSize = len(outputBytes)

  sys.stderr.write( 'Input size:         %d bytes\n' % inSize )
  sys.stderr.write( 'Output size:        %d bytes\n' % outSize )
  sys.stderr.write( 'Compression factor: %.2f\n' % (inSize/float(outSize)) )
  sys.stderr.write( 'Compression time:   %.2f seconds\n' % (endTime - startTime) )

# Get next code

def getnextcode( byteIter ) :
    fb = byteIter.next()
    sb = byteIter.next()
    #return (int(fb) << 8) | sb
    return chr(fb) + chr(sb)

# Uncompress an image

def uncompress( inputFile, outputFile ):

  # Check that it's a known file

  if inputFile.readline() != headerText + '\n':
    sys.stderr.write( "Input is not in the '%s' format.\n" % headerText )
    sys.exit(1)
    
  # Read the rows, columns, and channels.  

  rows, columns, channels = [ int(x) for x in inputFile.readline().split() ]

  # Read the raw bytes.

  inputBytes = bytearray(inputFile.read())

  # Build the image
  #
  # REPLACE THIS WITH YOUR OWN CODE TO CONVERT THE 'inputBytes' ARRAY INTO AN IMAGE IN 'img'.

  startTime = time.time()

  img = np.empty( [rows,columns,channels], dtype=np.uint8 )
  
  byteIter = iter(inputBytes)
   
  # For debugging
  f = open('decoding_bytes.txt', 'w')
  df = open('decoding_output.txt', 'w')
  
  # Initialize dictionary
  maxsize = 65536
  dict_size = 256
  d = initializeDictionary(dict_size)
  s = ''
  
  # oldcode = str(getnextcode(byteIter))
  # f.write(oldcode)
  # ch = oldcode
  # while(True):
    # newcode = str(getnextcode(byteIter))
    # if(newcode not in d):
        # s = str(d[oldcode])
        # s += ch
    # else :
        # s = str(d[newcode])
    # f.write(s)
    # ch = s[0]
    # d[oldcode + ch] = str(dict_size)
    # dict_size += 1
    # oldcode = newcode
  oldcode = getnextcode(byteIter)
  ch = oldcode
  while(True):
    print(d)
    newcode = getnextcode(byteIter) 
    if(newcode not in d):
        s = d[oldcode]
        s += ch
    else:
        s = d[newcode]
    for c in s:
        df.write(str(ord(c)) + '\n')
    ch = s[:2]
    d[oldcode + ch] = convert16bitto2char(dict_size)
    oldcode = newcode
    dict_size += 1
    if(dict_size > maxsize):
        dict_size = 256
        d = initializeDictionary(dict_size)
        #print(str(ord(k[0])) + ',' + str(ord(k[1])) + '\n')
        #k = chr(a) + chr(b)
        #f.write(k + '\n')
        # f.write(str(ord(k[0])) + ',' + str(ord(k[1])) + '\n')
        # if k in d:
            # entry = d[k]
        # elif convert2charto16bit(k) == dict_size:
            # entry = s + s[:2]
        
        # df.write('k = ' + str(ord(k[0])) + ',' + str(ord(k[1])) + ' s = ' + s + '\n')
        # for c in entry:
            # df.write(str(ord(c)) + '\n')
        # d[dict_size] = s + entry[:2]
        # dict_size += 1
        # if(dict_size > maxsize):
            # dict_size = 256
            # d = initializeDictionary(dict_size)
        # #f.write(str(k))
        # if( k > dict_size ) :
          # return
        # if ( k == dict_size ) : # special case
          # d[chr(dict_size)] = s + s[0]
          # dict_size += 1
        # elif ( s != "") :
          # d[chr(dict_size)] = s + chr(d[chr(k)])[0]
          # dict_size += 1

        # # write dictionary[k] to DF
        # f.write(chr(d[chr(k)]))
        # #f.write(str(d[str(k)]))
        # #f.write(' s = ' + s + ' k=' + str(k) + ' d[k] = ' + str(d[str(k)]))
        # # S = dictionary[k]
        # s = chr(d[chr(k)])
        # if(dict_size > maxsize):
          # dict_size = 256
          # d = initializeDictionary(dict_size)
 
  # for y in range(rows):
    # for x in range(columns):
      # for c in range(channels):
        # k = getnextcode(byteIter)  
        # #f.write(str(k))
        # if( k > dict_size ) :
          # return
        # if ( k == dict_size ) : # special case
          # d[str(dict_size)] = s + s[0]
          # dict_size += 1
        # elif ( s != "") :
          # d[str(dict_size)] = s + str(d[str(k)])[0]
          # dict_size += 1

        # # write dictionary[k] to DF
        # f.write(str(d[str(k)]))
        # # S = dictionary[k]
        # s = str(d[str(k)])
        # if(dict_size > maxsize):
          # dict_size = 256
          # d = initializeDictionary(dict_size)
        #fp = 0;
        #if(x > 0) :
        #    fp = img[y,x-1,c]
        #img[y,x,c] = fp + e

  endTime = time.time()
  f.close()
  # Output the image

  netpbm.imsave( outputFile, img )

  sys.stderr.write( 'Uncompression time: %.2f seconds\n' % (endTime - startTime) )

  

  
# The command line is 
#
#   main.py {flag} {input image filename} {output image filename}
#
# where {flag} is one of 'c' or 'u' for compress or uncompress and
# either filename can be '-' for standard input or standard output.


if len(sys.argv) < 4:
  sys.stderr.write( 'Usage: main.py c|u {input image filename} {output image filename}\n' )
  sys.exit(1)

# Get input file
 
if sys.argv[2] == '-':
  inputFile = sys.stdin
else:
  try:
    inputFile = open( sys.argv[2], 'rb' )
  except:
    sys.stderr.write( "Could not open input file '%s'.\n" % sys.argv[2] )
    sys.exit(1)

# Get output file

if sys.argv[3] == '-':
  outputFile = sys.stdout
else:
  try:
    outputFile = open( sys.argv[3], 'wb' )
  except:
    sys.stderr.write( "Could not open output file '%s'.\n" % sys.argv[3] )
    sys.exit(1)

# Run the algorithm

if sys.argv[1] == 'c':
  compress( inputFile, outputFile )
elif sys.argv[1] == 'u':
  uncompress( inputFile, outputFile )
else:
  sys.stderr.write( 'Usage: main.py c|u {input image filename} {output image filename}\n' )
  sys.exit(1)
