# -*- Makefile -*- (for emacs)
# src/Makefile-UserModules.  Generated from Makefile-UserModules.in by configure.
#
# Herwig++ 2.7.1
#
# This Makefile is intended for compiling Herwig++ plugins
# You can find example plugins in the Contrib directory
#
# This Makefile received very little testing, 
# any bug reports are very welcome!
#

#
# C++ flags
# 
CXX = g++

CXXFLAGS = -g -W -Wall -O3


ROOTCFLAGS=`root-config --cflags`                        
ROOTGLIBS=`root-config --glibs`    
ROOTLDFLAGS=`root-config --ldflags`
ROOTLIBS=`root-config --libs`
ROOTEVELIBS=`root-config --evelibs`

ROOT=$(ROOTCFLAGS) $(ROOTGLIBS) $(ROOTLDFLAGS) $(ROOTLIBS) $(ROOTEVELIBS) 


# add additional package header directories here
#CPPFLAGS = -I/home/myskam/raid/Programs/Herwig-7.0.2-MPI/include -I$(ROOTSYS)/include
CPPFLAGS = -I/home/ssd/Programs/Herwig-7.0.2/include -I$(ROOTSYS)/include

# -I/home/mira/local/ThePEG-1.9.2/include -I/home/mira/local/HepMC-2.06.09/include

# add additional libraries here
#LDFLAGS = -L$(ROOTSYS)/lib -lCore -lTree -lRIO -lHist -L/home/myskam/raid/Programs/Herwig-7.0.2-MPI/lib -lfastjet
LDFLAGS = -L$(ROOTSYS)/lib -lCore -lTree -lRIO -lHist -L/home/ssd/Programs/Herwig-7.0.2/lib -lfastjet
#-L/home/mira/local/Herwig-7.0.1-default/lib

ALLCCFILES=$(shell echo *.cc)
all : $(ALLCCFILES:.cc=.so)

%.so : %.cc %.h 
	$(CXX) -shared -fPIC -Wl,--no-as-needed $(CPPFLAGS) $(CXXFLAGS) $(ROOT) $(LDFLAGS) $< -o $@  



clean:
	rm -f $(ALLCCFILES:.cc=.so)






