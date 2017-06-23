import os
from shutil import copyfile
from subprocess import call
from itertools import repeat

# Replace content in file
# source https://stackoverflow.com/questions/4128144/replace-string-within-file-contents
def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        s = s.replace(old_string, new_string)
        f.write(s)

# Counting the "string" occurrence in a file
# source https://stackoverflow.com/questions/14758463/python-2-7-3-search-count-txt-file-for-string-return-full-line-with-final-occu
def count_string_occurrence(filename,string):
    f = open(filename)
    contents = f.read()
    f.close()
    return contents.count(string)





#has style being copied
copied = False

#number of 100% to count
hundredPercentCount = 3

#iterate on spec.ts file
for root, dirs, files in os.walk("src/app"):
    for file in files:
        if file.endswith(".spec.ts"):
             completePath = os.path.join(root, file)
             completePathBackup = completePath+'copy'
             coverageFilePath = 'coverage/'+completePath[:-7]+'ts.html'

             print('-----------------------------------------')
             print(completePath)

             #check if file already contains fdescribe, fit, xdescribe or xit
             #we ignore the file
             if 'fdescribe(' in open(completePath).read():
                  print "fdescribe() already present, ignoring file"
                  break

             if 'fit(' in open(completePath).read():
                  print "fit() already present, ignoring file"
                  break

             if 'xdescribe(' in open(completePath).read():
                  print "xdescribe() already present, ignoring file"
                  break

             if 'xit(' in open(completePath).read():
                  print "xit() already present, ignoring file"
                  break

             #backup each file
             print("   backuping file")
             copyfile(completePath, (completePath+'copy'))

             #replace describe and it by fdescribe and fit
             inplace_change(completePath, 'describe(', 'fdescribe(')

             #start coverage
             print("   starting coverage")
             os.popen("ng test --code-coverage --single-run").read()

             #check if coverage is 100% for 4 areas
             countHundredPercent = count_string_occurrence(coverageFilePath,'<span class="strong">100% </span>')
             if countHundredPercent < hundredPercentCount:

                 #extract result
                 print("   extracting result")
                 copyfile(coverageFilePath, '../results/'+file[:-7]+'ts.html')

                 #fix style reference to remove ../../ n times to link to prettify.css and base.css
                 #located in the root folder
                 for i in repeat(None, 10):
                     inplace_change('../results/'+file[:-7]+'ts.html', '../prettify.css', 'prettify.css')
                     inplace_change('../results/'+file[:-7]+'ts.html', '../base.css', 'base.css')

                 #replace file by old one
                 print("   rollbacking on file")
                 copyfile(completePathBackup,completePath)
                 os.remove(completePathBackup)

                 #copy style files
                 if not copied:
                      print('-----------------------------------------')
                      print("Copying styles once")
                      copyfile('coverage/base.css', '../results/base.css')
                      copyfile('coverage/base.css', '../results/prettify.css')
                 copied = True

             else:
                 print("   file already covered at 100%")
