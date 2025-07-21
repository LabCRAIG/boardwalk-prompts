# Prompting Schemes

The models were prompted differently depending on the desired mode of implementation. For the purposes of this document, `$DOC` refers to the API's documentation in Markdown, `$RULES` refers to the entire description of that game's rules, and `$CODE` refers to the code implemented for that game as a result of the independent test.

The rules descriptions used for each game are available as text files in this repository.

## API
Message 1: 
> In the next two messages, I will present you first with the documentation for a Python API for implementing board games, and then with the rules for the board game I want you to implement. Your final output must simply be Python code in the expected output code format presented in the documentation, with your code using the informed API.

Message 2:
> `$DOC`

Message 3:
> `$RULES`

## Independent
Message 1: 
> In the next message, I will present you with the rules for a board game. I want you to implement code in Python to play this board game, in exact accordance to the rules.

Message 2:
> `$RULES`

## Adapted
Message 1: 
> In the next three messages, I will present you first with the documentation for a Python API for implementing board games, then with the rules for a board game, then finally with an existing Python implementation of that board game. I want you to adapt that Python code to use the given API, and correct any parts of the code’s logic that don’t correctly implement the given rules.

Message 2:
> `$DOC`

Message 3:
> `$RULES`

Message 3:
> `$CODE`
