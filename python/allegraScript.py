import sys
import counterfactualMethods as cfm
from nltk.tag.perceptron import PerceptronTagger


def main():
    tagger = PerceptronTagger()
    print(cfm.get_cf_form(cfm.get_tagged_message(sys.argv[1], tagger)))

if __name__ == "__main__":
    main()