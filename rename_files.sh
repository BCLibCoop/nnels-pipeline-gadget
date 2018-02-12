#!/bin/bash

function installXPathDebian() {
    sudo apt install libxml-xpath-perl
}
function installXPathMac() {
    brew tap concept-not-found/tap  
    brew install xpath  
    mv /usr/local/bin/xpath /usr/local/bin/osx.xpath  
    sudo ln -s /usr/local/Cellar/xpath/1.13-7/bin/xpath /usr/local/bin/xpath
}

function getEPUBInfo() {
    ret=-1
    
    echo "Provided $# arguments to getEPUBInfo function"
    
    if [ $# -lt 1 ]; then
        echo
        echo "Usage: getEPUBInfo <epub-file> <meta-tags>..."
        echo
        ret=1
    else
        epubName="$1"
        fileloc=`unzip -l "$epubName" | grep -Po '\b[^\s-]*\.opf\b'`
        echo "Detected Metadata file to be in $fileloc"
        if [ $# -eq 1 ]; then
        #    shift
        #    wantedElements=("$@")
        #    echo "Looking at $epubName for $wantedElements"
        #    for element in $wantedElements; do
        #        extractFromOPF "$element" "$epubName" "$fileloc"
        #    done
        #else
            title=$(extractFromOPF "title" "$epubName" "$fileloc")
            title=${title##*=}
            title=${title%%\?*}
            data=$(extractFromOPF "*" "$epubName" "$fileloc")
            if [ -f "${title}-metadata.ini" ]; then
                echo -e "[$title - $(date +%Y-%m-%d-%T)]" >> "${title}-metadata.ini"
                echo -e "$data" >> "${title}-metadata.ini"
            else
                : > "${title}-metadata.ini"
                echo -e "[$title]" >> "${title}-metadata.ini"
                echo -e "$data" >> "${title}-metadata.ini"
            fi
        fi
    fi
}

# $1 - element being looked for
# $2 - EPUB file
# $3 - OPF file
function extractFromOPF() {
    # Get the Metadata from the OPF file
    zipgrep "<dc:${1/\*/.*}>(.*)</dc:${1/\*/.*}>" "$2" $3 > opf-parse-temp.txt
    
    # Loop over the file line by line to do futher extraction of the metadata
    while IFS="\n" read -r line; do
        # Get the value of the metadata field
        value=$(echo ${line#*:} | xpath -e "/*/text()")
        
        # Get the title of the metadata field
        key=$(echo ${line#*:} | xpath -e "name(/*)")
        key=${key##*:}
        
        # "Print" the results
        echo "$key=$value"
    done < opf-parse-temp.txt
    
    # Remove the file we looped over as it is no longer needed
    rm opf-parse-temp.txt
}


#----------------------------------------------------#
# Purpose: To read a PROPERLY formated XML Document  #
#          Object Model (DOM) and create a           #
#          standardized easily tokenizable string    #
#          for further processing                    #
# Parameters: N/A                                    #
# Return Code: 0 - Success                           #
#              Not 0 - Failure                       #
# Return (Echo): A single tag entry in the format    #
#                [Tag Name]([Attributes])=[value]    #
#----------------------------------------------------#
function read_dom() {
    # Read in the next peice of the file deliminated 
    # by < and > and assign them to the ENTITY and 
    # CONTENT variables respectively
    local IFS=\>
    read -d \< ENTITY CONTENT
    
    # Set this functions return/exit code as that of 
    # the read (previous command)
    local RET=$?
    
    # Further process the text between the < and > to account for attributes
    local TAG_NAME=${ENTITY%% *}
    local ATTRIBUTES=${ENTITY#* }
    
    # "Print" the properly formated string
    echo "$TAG_NAME($ATTRIBUTES)=$CONTENT"
    
    # Return the exit code (0 for success, non-zero otherwise)
    return $RET
}

function parse() {
    if [[ $1 == *"("* ]]; then
        echo "TAG: ${1%%(*}"
        echo "VALUE: ${1##*=}"
    fi
}

#----------------------------------------------------#
# Purpose: Main function of the script (the entry    #
#          point)                                    #
# Parameters: $@ - Program arguments provided on the #
#                  command line at runtime           #
# Return (echo): N/A                                 #
# Exit Code: 0 - Success                             #
#            > 0 - Error                             #
#----------------------------------------------------#
function main() {
    # Find and parse metadata from the epubs
    find . -name '*.epub' -print0 | while read  -d $'\0' file; do
        echo "Looking at file $file"
        getEPUBInfo "$file"
    done
    
    # loop over MarcXML files
    find . -name '*.xml' -print0 | while read -d $'\0' file; do
        echo $file
    done
}

main $@
