# NNELS Pipeline Gadget

## The Problem Statement
The problem that was provided was the need to create a script that would rename epub files with their cooresponding unique identifiers from the MarcXML files.

### Generic Approch
Given that there isn't any ideal way of identifing the epubs with their correspinding MarcXML (there is no unified way of nameing the epubs) Consequently, before we can match the entries up there needs to be a corresponding peice of data between the MarcXML entry and the epub file. After somme discussion it was decided that this shared peice of information would be the title. Which meant that I would have to extract the title from the OPF file in the epub. So, in a list form the things that need to get done were:
1. Identify all EPUB files
For Each:
2. Extract the OPF file from each EPUB
3. Extract the title from the OPF file
4. Rename the EPUB file with the corresponding title
5. Identify the entry in the MarcXML file that contains that name
6. Extract the unique identifier from the entry found in the prevous step
7. Rename the EPUB file with the unique identifier found in the prevous step

## Implementation Specifics
While implementing the approach detailed above there were a number of considerations and design decisions that were made unilaterally so that the implementation was scalable, reusable and timely.
### Tools/Utiltiies Used
In thinking through the implementation of the solution I realized that there were a lot of sources of information and lots of different standards. Consequently, my implementation had to be robust enough to compensate for enough human error that it can still work with a vast majority of the files we recieve. For this reason I thought that it would very quickly become out of scope if I tried to do many of these tasks myself.
#### XPath
One such task was parsing XML on my own. Because XML can't be easily or accurately parsed by Regular Expressions I made the decision to go looking for a pre-built solution and found one utility called *xpath* which is named after a "language" or notation that the utility uses to extract information from the XML file. You can get/install the utility on Debian based linux using tha apt package manager by doing something like ```sudo apt-get install libxml-..```. After a little bit of looking around I also found out that you can install it on Macos through the package manager called Homebrew which isn't installed by default but might be a good thing to have with scripts like this one.
#### Unzip
Now this seems to be defaulty installed on my new MacBook so I'm not sure if this comes with all Macs or not but I had to install this utility on Debian based linux using something similar to ```sudo apt insall unizip```. I needed this utility to extract OPF file from the EPUB archieve and felt that it didn't make sesne for me to try to extract it manually if there was already a tool out there to do it for me.
#### zipgrep
This utility seems to come pre-installed on all BASH enabled computers (namely Macos and Linux). This utility allows me to extract data directly from the archieve itself in particular I use it to find and extract information from the OPF file rather than unziping the OPF file because this way I don't have to run the result through a parser.
### Challenges and Decisions
Along the way I realized there were a number of things that happened that I had originally not accounted for.
#### OPF Filename
I will say that this had a more clear cut solution then many of the other solutions underneath the Challenges and Decisions heading. But essentially one of the things that really tripped me up initally is when I went to extract the OPF file they were named differently between archieves which meant that there was no good way to extract them directly consequently after a little bit of searching how EPUBs and archieves worked in general I found out that if I extract the contents file from the META-INF directory and extract the name of the OPF file from there (as it keeps track of what files are in the archieve) I could just feed that into my zipgrep expression so that I could look in the right file. An thus a solution was found.
#### Extraction of EPUB Metadata Scope
So, one of the things I identified fairly early on was there was a bit of an oppopportunity here to extract more than just the title from the EPUB directly so that when we come back to integrate that information into Drupal directly its easy and straight forward  enough to just extract the information with the existing code. While that sounds great it did make sections of the code a bit more complicated. Its pretty reasonable though.
#### Name Issues
So one of the things we forgot to consider was that a name can contain any valid character however a filename can't. Its also inconvient that most titles contain spaces but in file systems you have to escape spaces. This, I think is one of the major issue I'm having right now in that I don't have the fully legitament name becuase of filesystem constraints where the MarcXML uses that full name. One idea might be to transition to a language where I could keep that variable in a HashTable or "Dictionary" but this would certainly take some recoding. 
#### Extracting MarcXML Records
I'll be honest I'm still somewhat figuring this one out which is why the code isn't posted yet. I've tried doing some stuff with grep and some stuff with say XPath but nothing is giving me the exact result that I would like. It seems like its a lot of "hacky" work to try to get the outside of the entry and then find the exact entry I want again. This will probably need a fair bit more work before I can say that it is able to do what we want.
## To Be Worked On
There are lots of things that could an probably should be worked on but for the moment need to get the Minimum Viable Product up and running. My top priorities right now are as follows:
- Get the MarcXML extraction up and running on a consistant basis
- Rename the file with the information from the extractions
Some things that might need to happen along the way or I'd like to get done right after are:
- Transition to a better language I'm thinking Python because you could essentially transition everything into os.system calls and then just remove and replace with native Python as you go.
