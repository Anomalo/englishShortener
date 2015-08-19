#import matplotlib.pyplot as plt
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE",
				  default='table.tsv')
parser.add_option("-w", "--words",
                  dest="wordOutput",
                  help="where to save the shortened word list",
				  default = 'words_left.txt')
parser.add_option("-c", "--cycles_per_checkpoint",
                  dest="cycles",
                  help="how many cycles to do per checkpoint",
				  default=1000)
parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
(options, args) = parser.parse_args()
if options.verbose: print 'starting'
import compress

def lists_to_csv(x,y,fname):
    out = []
    for a,b in zip(x,y):
        out.append('%(a)s\t%(b)s'%locals())
    f = open(fname,'w')
    f.write('\n'.join(out))
    f.close()
		

D = compress.dictionary('gutenberg.txt',brackets=False)


d=D
wordsSizes = []
cycles = []
n = 0
cyclesperturn = options.cycles
while True:
    cycles.append(n)
    wordsSizes.append(d.words())
    if options.verbose: print wordsSizes[-1], cycles[-1]
    d.redundantCycle(cycles = cyclesperturn,v=False)
    n+=cyclesperturn
    if d.isReduced():
        wordsSizes.append(d.words())
        cycles.append(n)
        break
		
if options.verbose: print wordsSizes[-1], cycles[-1]

lists_to_csv(cycles,wordsSizes, options.filename)
f = open(options.wordOutput,'w')
f.write('\n'.join(sorted(d.D.keys())))
f.close()

if options.verbose: print 'DONE'

'''
cycles = cycles[:len(wordsSizes)]
wordsSizes=wordsSizes[:len(cycles)]
plt.plot(cycles,wordsSizes)
plt.ylabel('words')
plt.xlabel('cycles')
clear_output()
plt.show()
'''
