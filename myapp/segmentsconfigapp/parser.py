import re

class ParserSegmentConfig():

    """
    Lexer
    """

    def token_validation(self, mystr):
        list_pretoken = mystr.split('\n')
        for pretoken in list_pretoken:
            if re.match("^@{1}[a-zA-Z_0-9]+$", pretoken):
                self.token_li.append(Token("rulename", pretoken))
            elif pretoken == '':
                self.token_li.append(Token("separator", pretoken))
            else:
                self.token_li.append(Token("rule", pretoken))

    """
    Parser
    """
    
    def parse_tokens(self):
        self.token_iterli = iter(self.token_li)
        try:
            self.getrulename_list()
        except SyntaxError as err:
            self.last_error = err.args[0]
            print(err.args)
            return False
        return True

    def getrulename_list(self):
        for token in self.token_iterli:
            if token.typename == "rulename":
            	rulename_extracted =  re.match("^@{1}([a-zA-Z_0-9]+)$", token.content).group(1);
            	if self.unique_rulename(rulename_extracted) == False:
            		raise SyntaxError('The rulename "' + token.content + '" already exist in the context')
                token_next = next(self.token_iterli, None)
                if token_next != None and token_next.typename == "rule":
                    self.rule_list.append([rulename_extracted, token_next.content])
                else:
                    raise SyntaxError('A rulename "' + token.content + '" had been declared but no rule is associated')
            elif token.typename == "rule":
                raise SyntaxError('A rule "' + token.content + '" had been declared but no rulename is associated')
        return token

    def unique_rulename(self, name):
    	for rule in self.rule_list:
    		if rule[0] == name:
    			return False
    	return True

    """
    Main Calls
    """

    def parse(self, str):
        self.token_validation(str)
        return (self.parse_tokens())

    def debug_print(self):
        print self.rule_list
        print "\n"

    def __init__(self):
        #List of token created after token_validation
        self.token_li = []
        #Use an iterator when parse tokens after token_validation
        self.token_iterli = []
        #Result of the parsing end into a list in which each name is associated with his rule
        self.rule_list = []
        self.last_error = ""

class Token():
    def __init__(self, typename, content):
        self.typename = typename
        self.content = content
