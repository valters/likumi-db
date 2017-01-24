# likumi-db
Latvijas Republikas likumu konsolidētās vēsturiskās versijas teksta formātā

Consolidated historical, plain-text versions of the laws of Republic of Latvia

## Tree structure
* incoming html in 'intake' folder
* cleaned 'text' versions in 'text' folder
* diff comparison reports in 'diff' folder

## Build process

If you are reading this for first time, please read Prerequisites section first.

Here's how we ultimately build the diffs:

1) Retrieve home-page version of law manually, place into intake/ folder

2) Run `python3 write_versions.py <(law file).html>`
This will produce .ver file by extracting the historical-versions information from html.

3) Manually add information about the law to `toc.json`
The important part is _print_id_, which is required to retrieve "formatted for print" cleaner versions of html.

4) Run `python3 write_retrievers.py <(law short id)>`, for example 'python3 write_retrievers.py satversme'.
This loads the toc.json and parses .ver file to write bunch of curl commands for retrieving the print versions of laws -
all available historic versions.
The script will be stored in folder '(law short id)' (ex. 'satversme').

5) Go into this folder, run the retrieval script.
It will store retrieve the historic version .html files.

6) Run `python3 clean_visibility.py <folder>`.
It will process all .html files, and will put cleaned versions in 'clean/' subfolder.

This is necessary because before we can convert .html to raw .txt we must first clean up the .html a bit.
To render .txt we are using text-only browser 'elinks', which currently does not support css 'display:none' instruction, and the supposedly hidden text would get rendered into .txt result. So, to avoid this bug, we must remove such supposedly invisible sections explicitly from source files, producing 'clean' intermediate .html.

7) Go back to intake/ folder, run `./to-txt-do <folder name>` script (ex. `./to-txt-do satversme`) . It will in turn invoke 'elinks' browser (you may need to build it from sources).
The key why we use 'elinks', is because when it dumps the .txt result, it allows to specify very long line size: so that almost all law paragraphs will get rendered as single line: which again helps with diff.

8) Run `python3 clean_leadspaces.py <folder name>`, to remove the leading 3 spaces from all lines of .txt, which would also mess with the diff.

9) To produce diffs, run `java -jar (built location)/LawDiff-app/target/lawdiff-app.jar` in the law <folder>.
It will go through all files in 'txt/' folder, and produce diff .html reports in 'diff/' folder.

## Prerequisites

If you want to build/run some of this yourself,

1) You need to have most recent 'elinks' browser (v0.13), build it from sources. See http://elinks.cz/download.html and http://elinks.cz/documentation/installation.html

2) Clone and build https://github.com/valters/lawdiff

Or: download the app jar directly from
http://repo.maven.apache.org/maven2/io/github/valters/lawdiff-app/1.0.0/lawdiff-app-1.0.0.jar

This is consolidated jar that needs no other dependencies or java classpath gymnastics to run.