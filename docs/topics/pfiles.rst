.. topics-pfiles:

======================
Support for GE P-files
======================

Support for GE P-files in Suspect is provided by the GE Orchestra library.
This has the advantage of maximum compatibility with the many P-file revisions
out there, but the disadvantage that Orchestra is not a freely distributable
library: GE's current license prohibits the sharing of even the compiled
library. Therefore, in order to enable P-file support, you must download the
Orchestra library yourself and add it to the OpenMRSLab Docker container. This
is a relatively simple process, and the rest of this page gives a detailed
guide to the necessary steps.

##################################################
Step 1. Register for a GE MR Collaboration account
##################################################
Go to the GE MR Collaboration Community `website
<https://collaborate.mr.gehealthcare.com/welcome>`_ and register for an
account. This account is free, but only available for users of GE scanners,
so there is a manual confirmation step which may take a day or two before your
account is active. As well as letting you download Orchestra, this account will
also give you access to GE's MR forums.

#########################################
Step 2. Download the Orchestra Python SDK
#########################################
On the GE MR Collaboration website, go to
https://collaborate.mr.gehealthcare.com/docs/DOC-1727 to download the Orchestra
SDK for Python (current version tested with Suspect is v1.10 on 01/10/20). This
is a rather large download at around 416MB, this is mostly due to the large
amount of sample data included with the code, the actual code library is only
10% of that, unfortunately there is no way to get only the SDK itself.

#####################################
Step 3. Copy the code into OpenMRSLab
#####################################
After extracting the Orchestra files from the downloaded archive, you will find
that as well as the example processing scripts and datasets, there are several
versions of the code library, covering Windows, MacOS and Linux. The file that
we need is the Linux version called GERecon.so.python35. This is because the
OpenMRSLab Docker container is based on Linux, no matter what the host
operating system for your computer is.

Inside the Docker container, OpenMRSLab is already set up to look for the
Orchestra .so file in a directory at the path: `/home/jovyan/work/orchestra`.
If you have followed the recommended approach of mapping a host directory to
the `/home/jovyan/work` directory then the simplest solution is simply to
create a folder called `orchestra` in that mapped directory and copy the
GERecon.so.python35 file into it. Note that it is important to rename the file
GERecon.so (dropping the .python35 part) to allow Python to recognise and load
it.

If you do not have a mapped directory, or if you are accessing your OpenMRSLab
installation remotely and don't have easy access to the host computer file
system then it is also possible to upload the file through the Jupyter server
itself. The home directory for the Jupyter server is /home/jovyan/work so
using the Jupyter file browser interface you can first select New->Folder (from
the top right hand corner of the interface) and name the resulting folder
`orchestra`, then click Upload (next to the New button) and select the
GERecon.so.python35 file from your local system. Again, note that it is
important to rename the file to GERecon.so.

#############################
Step 4. Test the installation
#############################
To test your installation, simply open a Jupyter notebook and run
`import GERecon`. If you have correctly installed the SDK then this will
complete without an error, and you will then be able to use Suspect to work
with GE P-files.