#### Install Packages

##### Install Packages (ubuntu)

```
sudo apt-get install libgsl2 libgsl2:i386
sudo apt-get install libblas3gf libblas-doc libblas-dev
sudo apt-get install libgsl0-dev
```

##### Install Packages (OSC)

note:

Before you build, run 'module load mkl'. 

In the makefile change the -I path in CFLAGS to
 
-I/opt/intel/compilers_and_libraries_2016.3.210/linux/mkl/include
 
and the -L path to
 
-L${MKLROOT}/lib/intel64
 
and for the rest of the LDFLAGS use
 
-Wl,--no-as-needed -lgsl -lmkl_intel_ilp64 -lmkl_sequential -lmkl_core -lpthread -lm -ldl
 
**You should also load the mkl module in batch scripts before you run the code.**

#### Compile

```
make
```

#### Run

```
./agony sample.edges result.txt
```

* input: sample.edges 
* output: result.txt
