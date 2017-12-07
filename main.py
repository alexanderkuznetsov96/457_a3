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
  d = dict((chr(i), i) for i in xrange(dict_size))
  return d

def getfirstbyte(v) :
    return (v & (0xFF << 8)) >> 8
    
def getsecondbyte(v) :
    return v & 0xFF
    
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
  f = open('debug_encoding.txt', 'w')
  
  for y in range(img.shape[0]):
    for x in range(img.shape[1]):
      for c in range(img.shape[2]):
        fp = 0;
        if(x > 0):
            fp = img[y,x-1,c]
        e = img[y,x,c] - fp
        #f.write(str(e))
        if(s + chr(e) in d):
            s += chr(e)
        else:
            #f.write(' s = ' + s + ' d[s]= ' + str(d[s]))
            outputBytes.append(getfirstbyte(d[s]))
            outputBytes.append(getsecondbyte(d[s]))
            d[s + chr(e)] = dict_size
            dict_size += 1
            if(dict_size > maxsize):
                dict_size = 256
                d = initializeDictionary(dict_size)
            s = chr(e)
  outputBytes.append(getfirstbyte(d[s]))
  outputBytes.append(getsecondbyte(d[s]))
  endTime = time.time()
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
    if(fb != 0):
        return chr(fb) + chr(sb)
    return chr(sb)
    
def convertchar2num( s ):
    if(len(s) > 1) :
        fc = s[0]
        sc = s[1]
        if(ord(fc) != 0):
            return ord(fc)*256 + ord(sc)
    
    return ord(s)
    
def convertnum2char( n ):
    s = ""
    fc = getfirstbyte( n )
    sc = getsecondbyte( n )
    if(fc != 0):
        s += chr(fc)
    s += chr(sc)
    return s

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
  f = open('debug_decoding.txt', 'w')
  
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

  while(True):
        k = getnextcode(byteIter) # this is string
        #f.write(str(k))
        #print(k)
        #if( convertchar2num(k) > dict_size ) :
        #  return
        #if ( k == convertnum2char(dict_size) ) : # special case
        #  d[convertnum2char(dict_size)] = convertchar2num(s + s[0])
        #  dict_size += 1
        #elif ( s != "") :
        #  d[convertnum2char(dict_size)] = convertchar2num(s + convertnum2char(d[k])[0])
        #  dict_size += 1

        # write dictionary[k] to DF
        #sq = str(d[k])
        #f.write(sq + '\n')
        #f.write(' s = ' + s + ' k=' + str(k) + ' d[k] = ' + str(d[str(k)]))
        # S = dictionary[k]
        #s = convertnum2char(d[k])
        #if(dict_size > maxsize):
        #  dict_size = 256
        #  d = initializeDictionary(dict_size)
 
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
