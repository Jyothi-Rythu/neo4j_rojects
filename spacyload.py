!pip install -U pip setuptools wheel
!python -m spacy project clone tutorials/rel_component
!pip install -U spacy-nightly --pre
!!pip install -U spacy transformers
import spacy
#restart the runtime after installation of deps
nlp = spacy.load("[PATH_TO_THE_MODEL]/model-best")
