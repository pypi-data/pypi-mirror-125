# Weak POS Tagger Model # 
 This package utilizes two models for labeling parts of speech. 
 The first model uses files containing lists of words of a certain gramatical class. 
 The second model uses rules to break ambiguity when the first model cannot decide on only one class for a word.
 
 The package takes as input sentences in the form of strings and outputs a string with the POS Tags of the words on the sentence.
 
# Installation
The Weak POS Tagger can be installed from PyPi:

```bash 
pip install weak_postagger
```

# Usage

## POS Tag Classes Accepted

This project utilizes portuguese part of speech classes. The accepted classes and their tokens are as follow:

    'verbos': 'VERB',
    'adjetivos': 'ADJ',
    'adverbios': 'ADV',
    'artigos': 'ART',
    'conjuncoes': 'CONJ',
    'interjeicoes': 'INT',
    'substantivos': 'SUBS',
    'pronomes': 'PRON',
    'numeros': 'NUM',
    'preposicoes': 'PREP',
    'participios': 'PART'

## Text Pre Processing

All text used is pre processed by the default utilizing the following operations:

* Case lowering
* Adding space around punctuation
* Removing non-ASCII characters

It can also optionally perform the following tokenizations:
* E-mails
* Urls
* Numbers 
* Codes
 
In order to use the optional pre processing the user needs to pass a list containing `EMAIL`, `URL`, `NUMBER` and/or `CODE`. 
It can be passed in the instatiation of the class as shown bellow:

    tokenization_options = ['EMAIL', 'CODE']
    weak_postag = WeakPOSTagging('directory_path/', tokenization_options)

  
## List Based Model

### Files

In order to label a string using the list based model the user needs to create a directory containing one text file for each part of speech class it wants to use. 
The name of each file needs to contain the name of the part of speech class and the contents of the file must be words that are classified as part of that class.
For example:
We may have a file called `substantivos.txt` and it would contain the following words:

    carro  
    mesa  
    banana  

And also have a second file called ``adjetivos.txt`` and it would contain the words:

    azul  
    lento  
    calmo  

### Weak Labeling

The default weak labeling utilizes two steps:
* The first step is the labeling module `ListWeakModel` created with the files input in the class.
* The second step is the label correction module `RuleBasedDisambiguation`.

In order to use the default pipeline to label a sentence the user needs to first instantiate the class passing the path of the directory where the files are stored.
The user then can use this class to label a sentence: 
 
    weak_postaging = WeakPOSTagging('directory_path/')
    sentence = "Uma banana verde"
    labeled_sentence = weak_postaging.label_sentence(sentences)
       
 And the user should receive back the result:
        
    'ART SUBS ADJ'
 
 The user can also specify which optional text pre processing will be applied on the sentence:
 
    tokenization_options = ['EMAIL', 'CODE']
    weak_postag = WeakPOSTagging('directory_path/', tokenization_options)  
    sentence = "o meu contato é research@email.com"
    labeled_sentence = weak_postaging.label_sentence(sentences)

 And the user should receive back the result:
        
    'ART PRON VERB SUBS'
    
#### Setting a custom pipeline

A custom labeling pipeline can be created by clearing the default pipeline and adding each step to it in the order they need to be executed.

    weak_postaging = WeakPOSTagging('directory_path/')
    weak_postaging.clear()
    
    list_model_1 = ListWeakModel('directory/')
    list_model_2 = ListWeakModel('directory_two/')
    rule_weak_model = RuleBasedDisambiguation()
    
    weak_postaging.add_pipeline_step(list_model_1)
            .add_pipeline_step(rule_weak_model)
            .add_pipeline_step(list_model_2)
            .add_pipeline_step(rule_weak_model)
            
It is important to note that the first step should always be a list based one.
    
    
# Contribute
If this is the first time you are contributing to this project, first create the virtual environment using the following command:
    
    conda env create -f env/environment.yml
   
Then activate the environment:

    conda activate weakpostag_env
    
To test your modifications build the package:

    pip install dist\weak_postagger-0.0.1-py3-none-any.whl --force-reinstall
    
Then run the tests:

    pytest
