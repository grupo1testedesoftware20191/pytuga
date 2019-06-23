from tokenize import NEWLINE

from transpyler import token
from transpyler.token import Token


def end_command(idx, match, start, end, iterator, tokens):
    # Finish command
    if match[0] in (NEWLINE, ':'):
        token.displace_tokens(tokens[idx:], 1)
        endtokens = Token.from_strings(start, '+', '1', ')')
        token.insert_tokens_at(tokens, idx, endtokens, end=end)

    # Unexpected token
    else:
        raise SyntaxError(
            'comando malformado na linha %s.\n'
            '    Espera um ":" no fim do bloco' % (start.lineno)
        )
    return tokens


def insert_a_cada(idx, match, start, end, iterator, tokens):
    # Matches "a cada" or the end of the line
    if match == ('a', 'cada'):
        middletokens = Token.from_strings(start, '+', '1', ',')
        del tokens[idx:idx + 2]
        token.insert_tokens_at(tokens, idx, middletokens, end=end)

        # Proceed to the end of the line
        idx, match, start, end = next(iterator)
        if match[0] not in (NEWLINE, ':'):
            raise SyntaxError(
                'comando malformado na linha %s.\n'
                '    Espera um ":" no fim do bloco' % (start.lineno)
            )
        endtok = Token(')', start=start)
        token.displace_tokens(tokens[idx:], 1)
        tokens.insert(idx, endtok)
        return end_command(idx, match, start, end, iterator, tokens)
    return None


def insert_ate(idx, match, start, end, iterator, tokens):
    # Matches the 'até' token and insert a comma separator
        idx, match, start, end = next(iterator)
        if match[0] in ['até', 'ate']:
            token.displace_tokens(tokens[idx:], -3)
            tokens[idx] = Token(',', start=tokens[idx - 1].end)
        else:
            raise SyntaxError(
                'comando para cada malformado na linha %s.\n'
                '    Espera comando do tipo\n\n'
                '        para cada <x> de <a> até <b>:\n'
                '            <BLOCO>\n\n'
                '    Palavra chave "até" está faltando!' % (start.lineno)
            )

        idx, match, start, end = next(iterator)
        return insert_a_cada(idx, match, start, end, iterator, tokens)


def funct_iter(iterator, tokens):
    for idx, match, start, end in iterator:
        # Waits for a 'de' token to start processing
        if match[0] != 'de':
            continue

        # Send tokens for the beginning of the equivalent in range(...)
        # test
        start = tokens[idx].start
        starttokens = Token.from_strings(start, 'in', 'range', '(')
        del tokens[idx]
        token.insert_tokens_at(tokens, idx, starttokens, end=end)
        return insert_ate(idx, match, start, end, iterator)


def convert_command(tokens):
    matches = [('de',), ('ate',), ('a', 'cada',), (NEWLINE,), (':',)]
    iterator = token.token_find(tokens, matches)
    tokens = funct_iter(iterator, tokens)
    return tokens
