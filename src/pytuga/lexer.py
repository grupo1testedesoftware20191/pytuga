from tokenize import NEWLINE

from transpyler import token
from transpyler.lexer import Lexer
from transpyler.token import Token

from utils import convert_command

__all__ = ['PytugaLexer']


class PytugaLexer(Lexer):
    """
    Pytuga lexer.

    Defines the "repetir n vezes" and "de X ate Y a cada Z" commands.
    """

    def process_repetir_command(self, tokens):
        """
        Converts command::

            repetir <N> vezes:
                <BLOCO>

        or::

            repita <N> vezes:
                <BLOCO>

        to::

            for ___ in range(<N>):
                <BLOCO>
        """

        matches = [('repetir',), ('repita',), ('vezes',), (NEWLINE,)]
        iterator = token.token_find(tokens, matches)

        for idx, match, start, end in iterator:
            # Send tokens to the beginning of the equivalent "for" loop
            starttokens = Token.from_strings(
                tokens[idx].start, 'for', '___', 'in', 'range', '('
            )
            del tokens[idx]
            token.insert_tokens_at(tokens, idx, starttokens, end=end)

            # Matches the 'vezes' token
            try:
                idx, match, start, end = next(iterator)
            except StopIteration:
                match = [None]

            if match[0] != 'vezes':
                raise SyntaxError(
                    'comando repetir malformado na linha %s.\n'
                    '    Espera comando do tipo\n\n'
                    '        repetir <N> vezes:\n'
                    '            <BLOCO>\n\n'
                    '    Palavra chave "vezes" está faltando!' % (start.lineno)
                )
            else:
                tokens[idx] = Token(')', start=start)
                token.displace_tokens(tokens[idx + 1:], -4)

        return tokens

    def process_de_ate_command(self, tokens):
        """
        Converts command::

            de <X> até <Y> [a cada <Z>]

        to::

            in range(<X>, <Y> + 1[, <Z>])

        """
        tokens = convert_command(tokens)
        return tokens

    def transpile_tokens(self, tokens):
        tokens = super().transpile_tokens(tokens)
        tokens = self.process_repetir_command(tokens)
        tokens = self.process_de_ate_command(tokens)
        return tokens
