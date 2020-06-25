import sys, getopt
from os import path

def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print ('Input file is ', inputfile)

   if (not path.exists(inputfile)):
      print('input does not exist')
      sys.exit()
   f = open("result.txt", "w")
   f.write("This is a test to write an output. The input file was "+inputfile)
   f.close()
   print('Done')

if __name__ == "__main__":
   main(sys.argv[1:])
