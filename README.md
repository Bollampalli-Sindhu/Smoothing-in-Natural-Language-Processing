# Smoothing-in-Natural-Language-Processing
## Execution 
#### kneyserNey
> python3 language_models.py k < corpus-file-path >  
#### WrittenBell
> python3 language_models.py w < corpus-file-path >

## Project
1. **Tokenization**  
 A Simple Tokenizer is built using regex which handles following cases:
   - Word Tokenizer
   - Punctuation
   - URLs
   - Hashtags (#manchesterisred)
   - Mentions (@john)    
     
   For the following cases, the tokens have been replced with appropriate placeholders: 
    - URLs: <URL>
    - Hashtags: <HASHTAG>
    - Mentions: <MENTION>  
    
 2. **Smoothing**  
  Language models have been created for Europarl corpus using two different smoothing techniques:
    - KneyserNey Smoothing
    - WrittenBell Smoothing
  
