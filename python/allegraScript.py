import sys
import counterfactualMethods as cfm
from nltk.tag.perceptron import PerceptronTagger

# prints form of each message in args
def main():
    tagger = PerceptronTagger()
    for i in xrange(1, len(sys.argv)):
    	print(cfm.get_cf_form(cfm.get_tagged_message(sys.argv[i], tagger)))

if __name__ == "__main__":
    main()