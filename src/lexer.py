"""
CAT Compiler — Bootstrap Lexer (Python)
Tokenizes CAT source code into a stream of Token objects.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Any


# ─── Token Kinds ──────────────────────────────────────────────────────────────

class TokenKind(Enum):
    # Keywords
    FN = auto()
    TYPE = auto()
    CONST = auto()
    GLOBAL = auto()
    LOCAL = auto()
    IMPORT = auto()
    EXPORT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    BREAK = auto()
    CONTINUE = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    ENUM = auto()

    # Built-in types
    TY_I8 = auto()
    TY_I16 = auto()
    TY_I32 = auto()
    TY_I64 = auto()
    TY_I128 = auto()
    TY_U8 = auto()
    TY_U16 = auto()
    TY_U32 = auto()
    TY_U64 = auto()
    TY_U128 = auto()
    TY_F32 = auto()
    TY_F64 = auto()
    TY_BOOL = auto()
    TY_VOID = auto()
    TY_PTR = auto()

    # Instructions
    MOV = auto()
    LEA = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    NEG = auto()
    AND = auto()
    ORR = auto()
    XOR = auto()
    NOT = auto()
    SHL = auto()
    SHR = auto()
    SAR = auto()
    ROL = auto()
    ROR = auto()
    CMP = auto()
    CEQ = auto()
    CNE = auto()
    CLT = auto()
    CLE = auto()
    CGT = auto()
    CGE = auto()
    JMP = auto()
    JE = auto()
    JNE = auto()
    JL = auto()
    JLE = auto()
    JG = auto()
    JGE = auto()
    JZ = auto()
    JNZ = auto()
    CALL = auto()
    RET = auto()
    SEL = auto()

    # Special
    DIRECTIVE = auto()
    FLAG = auto()

    # Symbols
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COLON = auto()
    SEMI = auto()
    COMMA = auto()
    DOT = auto()
    ARROW = auto()
    WALRUS = auto()
    ASSIGN = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    SHIFT_L = auto()
    SHIFT_R = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    AMP = auto()
    PIPE = auto()
    CARET = auto()
    TILDE = auto()
    BANG = auto()
    LG_AND = auto()
    LG_OR = auto()
    PLUS_EQ = auto()
    MINUS_EQ = auto()
    STAR_EQ = auto()
    SLASH_EQ = auto()

    # Literals
    IDENT = auto()
    INT_LIT = auto()
    FLOAT_LIT = auto()
    STRING_LIT = auto()
    CHAR_LIT = auto()

    # Meta
    COMMENT = auto()
    LABEL = auto()
    EOF = auto()
    ERROR = auto()


# ─── Keyword lookup ──────────────────────────────────────────────────────────

KEYWORDS = {
    "fn": TokenKind.FN,
    "type": TokenKind.TYPE,
    "const": TokenKind.CONST,
    "global": TokenKind.GLOBAL,
    "local": TokenKind.LOCAL,
    "import": TokenKind.IMPORT,
    "export": TokenKind.EXPORT,
    "if": TokenKind.IF,
    "else": TokenKind.ELSE,
    "while": TokenKind.WHILE,
    "for": TokenKind.FOR,
    "return": TokenKind.RETURN,
    "break": TokenKind.BREAK,
    "continue": TokenKind.CONTINUE,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
    "null": TokenKind.NULL,
    "enum": TokenKind.ENUM,
    # Built-in types
    "i8": TokenKind.TY_I8,
    "i16": TokenKind.TY_I16,
    "i32": TokenKind.TY_I32,
    "i64": TokenKind.TY_I64,
    "i128": TokenKind.TY_I128,
    "u8": TokenKind.TY_U8,
    "u16": TokenKind.TY_U16,
    "u32": TokenKind.TY_U32,
    "u64": TokenKind.TY_U64,
    "u128": TokenKind.TY_U128,
    "f32": TokenKind.TY_F32,
    "f64": TokenKind.TY_F64,
    "bool": TokenKind.TY_BOOL,
    "void": TokenKind.TY_VOID,
    "ptr": TokenKind.TY_PTR,
    # Instructions
    "mov": TokenKind.MOV,
    "lea": TokenKind.LEA,
    "add": TokenKind.ADD,
    "sub": TokenKind.SUB,
    "mul": TokenKind.MUL,
    "div": TokenKind.DIV,
    "mod": TokenKind.MOD,
    "neg": TokenKind.NEG,
    "and": TokenKind.AND,
    "orr": TokenKind.ORR,
    "xor": TokenKind.XOR,
    "not": TokenKind.NOT,
    "shl": TokenKind.SHL,
    "shr": TokenKind.SHR,
    "sar": TokenKind.SAR,
    "rol": TokenKind.ROL,
    "ror": TokenKind.ROR,
    "cmp": TokenKind.CMP,
    "ceq": TokenKind.CEQ,
    "cne": TokenKind.CNE,
    "clt": TokenKind.CLT,
    "cle": TokenKind.CLE,
    "cgt": TokenKind.CGT,
    "cge": TokenKind.CGE,
    "jmp": TokenKind.JMP,
    "je": TokenKind.JE,
    "jne": TokenKind.JNE,
    "jl": TokenKind.JL,
    "jle": TokenKind.JLE,
    "jg": TokenKind.JG,
    "jge": TokenKind.JGE,
    "jz": TokenKind.JZ,
    "jnz": TokenKind.JNZ,
    "call": TokenKind.CALL,
    "ret": TokenKind.RET,
    "sel": TokenKind.SEL,
}


# ─── Token ────────────────────────────────────────────────────────────────────

@dataclass
class Token:
    kind: TokenKind
    lexeme: str
    line: int
    column: int
    literal: Any = None  # int, float, str, or None

    def __repr__(self):
        if self.literal is not None:
            return f"Token({self.kind.name}, {self.lexeme!r}, {self.line}:{self.column}, lit={self.literal!r})"
        return f"Token({self.kind.name}, {self.lexeme!r}, {self.line}:{self.column})"


# ─── Diagnostic ───────────────────────────────────────────────────────────────

@dataclass
class Diagnostic:
    code: str
    message: str
    line: int
    column: int

    def __str__(self):
        return f"[{self.code}] {self.message} at {self.line}:{self.column}"


# ─── Lexer ────────────────────────────────────────────────────────────────────

class Lexer:
    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
        self.diagnostics: List[Diagnostic] = []

    # ── Helpers ───────────────────────────────────────────────────────────

    def _at_end(self) -> bool:
        return self.pos >= len(self.source)

    def _peek(self) -> str:
        if self._at_end():
            return "\0"
        return self.source[self.pos]

    def _peek2(self) -> str:
        if self.pos + 1 >= len(self.source):
            return "\0"
        return self.source[self.pos + 1]

    def _advance(self) -> str:
        if self._at_end():
            return "\0"
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False

    def _emit(self, kind: TokenKind, lexeme: str, line: int, col: int, literal=None):
        self.tokens.append(Token(kind, lexeme, line, col, literal))

    def _error(self, code: str, msg: str, line: int, col: int):
        self.diagnostics.append(Diagnostic(code, msg, line, col))

    # ── Main tokenize loop ────────────────────────────────────────────────

    def tokenize(self) -> List[Token]:
        while not self._at_end():
            self._skip_whitespace()
            if self._at_end():
                break
            self._scan_token()

        self._emit(TokenKind.EOF, "", self.line, self.col)
        return self.tokens

    def _skip_whitespace(self):
        while not self._at_end() and self._peek() in " \t\r\n":
            self._advance()

    # ── Scan one token ────────────────────────────────────────────────────

    def _scan_token(self):
        line = self.line
        col = self.col
        start = self.pos
        ch = self._advance()

        # Single-line comment
        if ch == "#":
            self._scan_line_comment(start, line, col)
            return

        # Block comment
        if ch == "/" and self._peek() == "*":
            self._advance()
            self._scan_block_comment(start, line, col)
            return

        # String literal
        if ch == '"':
            self._scan_string(start, line, col)
            return

        # Character literal
        if ch == "'":
            self._scan_char(start, line, col)
            return

        # Numbers
        if ch.isdigit():
            self._scan_number(start, line, col, ch)
            return

        # Identifier / keyword / instruction
        if ch.isalpha() or ch == "_":
            self._scan_ident(start, line, col, ch)
            return

        # Directive (@name)
        if ch == "@":
            self._scan_directive(start, line, col)
            return

        # Label (.name:) or just Dot
        if ch == ".":
            if self._peek().isalpha() or self._peek() == "_":
                self._scan_label(start, line, col)
                return
            self._emit(TokenKind.DOT, ".", line, col)
            return

        # Flag &c4
        if ch == "&":
            if self._peek() == "c" and self._peek2() == "4":
                self._advance()
                self._advance()
                self._emit(TokenKind.FLAG, "&c4", line, col)
                return
            if self._peek() == "&":
                self._advance()
                self._emit(TokenKind.LG_AND, "&&", line, col)
                return
            self._emit(TokenKind.AMP, "&", line, col)
            return

        # Two-char symbols
        if ch == ":":
            if self._match("="):
                self._emit(TokenKind.WALRUS, ":=", line, col)
            else:
                self._emit(TokenKind.COLON, ":", line, col)
            return

        if ch == "-":
            if self._match(">"):
                self._emit(TokenKind.ARROW, "->", line, col)
            elif self._match("="):
                self._emit(TokenKind.MINUS_EQ, "-=", line, col)
            else:
                self._emit(TokenKind.MINUS, "-", line, col)
            return

        if ch == "=":
            if self._match("="):
                self._emit(TokenKind.EQ, "==", line, col)
            else:
                self._emit(TokenKind.ASSIGN, "=", line, col)
            return

        if ch == "!":
            if self._match("="):
                self._emit(TokenKind.NE, "!=", line, col)
            else:
                self._emit(TokenKind.BANG, "!", line, col)
            return

        if ch == "<":
            if self._match("="):
                self._emit(TokenKind.LE, "<=", line, col)
            elif self._match("<"):
                self._emit(TokenKind.SHIFT_L, "<<", line, col)
            else:
                self._emit(TokenKind.LT, "<", line, col)
            return

        if ch == ">":
            if self._match("="):
                self._emit(TokenKind.GE, ">=", line, col)
            elif self._match(">"):
                self._emit(TokenKind.SHIFT_R, ">>", line, col)
            else:
                self._emit(TokenKind.GT, ">", line, col)
            return

        if ch == "|":
            if self._match("|"):
                self._emit(TokenKind.LG_OR, "||", line, col)
            else:
                self._emit(TokenKind.PIPE, "|", line, col)
            return

        if ch == "+":
            if self._match("="):
                self._emit(TokenKind.PLUS_EQ, "+=", line, col)
            else:
                self._emit(TokenKind.PLUS, "+", line, col)
            return

        if ch == "*":
            if self._match("="):
                self._emit(TokenKind.STAR_EQ, "*=", line, col)
            else:
                self._emit(TokenKind.STAR, "*", line, col)
            return

        if ch == "/":
            if self._match("="):
                self._emit(TokenKind.SLASH_EQ, "/=", line, col)
            else:
                self._emit(TokenKind.SLASH, "/", line, col)
            return

        # Single-char symbols
        SIMPLE = {
            "(": TokenKind.LPAREN,
            ")": TokenKind.RPAREN,
            "{": TokenKind.LBRACE,
            "}": TokenKind.RBRACE,
            "[": TokenKind.LBRACKET,
            "]": TokenKind.RBRACKET,
            ";": TokenKind.SEMI,
            ",": TokenKind.COMMA,
            "%": TokenKind.PERCENT,
            "^": TokenKind.CARET,
            "~": TokenKind.TILDE,
        }
        if ch in SIMPLE:
            self._emit(SIMPLE[ch], ch, line, col)
            return

        # Unknown character
        self._error("E001", f"Unexpected character {ch!r}", line, col)
        self._emit(TokenKind.ERROR, ch, line, col)

    # ── Sub-scanners ──────────────────────────────────────────────────────

    def _scan_line_comment(self, start, line, col):
        text = "#"
        while not self._at_end() and self._peek() != "\n":
            text += self._advance()
        # Comments are discarded (not emitted as tokens)

    def _scan_block_comment(self, start, line, col):
        depth = 1
        while not self._at_end() and depth > 0:
            if self._peek() == "/" and self._peek2() == "*":
                self._advance()
                self._advance()
                depth += 1
            elif self._peek() == "*" and self._peek2() == "/":
                self._advance()
                self._advance()
                depth -= 1
            else:
                self._advance()
        if depth > 0:
            self._error("E003", "Unterminated block comment", line, col)

    def _scan_string(self, start, line, col):
        value = ""
        while not self._at_end():
            ch = self._peek()
            if ch == '"':
                self._advance()
                raw = self.source[start:self.pos]
                self._emit(TokenKind.STRING_LIT, raw, line, col, value)
                return
            if ch == "\n":
                self._error("E002", "Unterminated string literal (newline before closing quote)", line, col)
                raw = self.source[start:self.pos]
                self._emit(TokenKind.ERROR, raw, line, col)
                return
            if ch == "\\":
                self._advance()
                esc = self._parse_escape(line, col)
                if esc is not None:
                    value += esc
            else:
                value += self._advance()

        self._error("E002", "Unterminated string literal", line, col)
        self._emit(TokenKind.ERROR, self.source[start:self.pos], line, col)

    def _scan_char(self, start, line, col):
        if self._at_end():
            self._error("E008", "Empty character literal", line, col)
            self._emit(TokenKind.ERROR, "'", line, col)
            return

        if self._peek() == "'":
            self._advance()
            self._error("E008", "Empty character literal", line, col)
            self._emit(TokenKind.ERROR, "''", line, col)
            return

        if self._peek() == "\\":
            self._advance()
            ch_val = self._parse_escape(line, col)
        else:
            ch_val = self._advance()

        if not self._at_end() and self._peek() == "'":
            self._advance()
        else:
            self._error("E009", "Unterminated or multi-character character literal", line, col)

        raw = self.source[start:self.pos]
        cp = ord(ch_val) if ch_val else 0
        self._emit(TokenKind.CHAR_LIT, raw, line, col, cp)

    def _parse_escape(self, line, col) -> Optional[str]:
        if self._at_end():
            self._error("E006", "Unexpected end of file in escape sequence", line, col)
            return None
        ch = self._advance()
        simple = {"n": "\n", "r": "\r", "t": "\t", "\\": "\\", '"': '"', "'": "'", "0": "\0"}
        if ch in simple:
            return simple[ch]
        if ch == "x":
            h1 = self._advance() if not self._at_end() else "\0"
            h2 = self._advance() if not self._at_end() else "\0"
            try:
                val = int(h1 + h2, 16)
                return chr(val)
            except ValueError:
                self._error("E006", f"Invalid \\x escape: \\x{h1}{h2}", line, col)
                return None
        if ch == "u":
            if self._at_end() or self._peek() != "{":
                self._error("E006", "Expected '{' after \\u", line, col)
                return None
            self._advance()  # consume '{'
            digits = ""
            while not self._at_end() and self._peek() != "}":
                digits += self._advance()
                if len(digits) > 6:
                    self._error("E006", "Too many digits in \\u{} escape", line, col)
                    # consume until '}'
                    while not self._at_end() and self._peek() != "}":
                        self._advance()
                    if not self._at_end():
                        self._advance()
                    return None
            if not self._at_end():
                self._advance()  # consume '}'
            try:
                cp = int(digits, 16)
                if cp > 0x10FFFF:
                    self._error("E007", f"Unicode codepoint U+{cp:X} out of range", line, col)
                    return None
                return chr(cp)
            except ValueError:
                self._error("E006", f"Invalid \\u{{}} escape", line, col)
                return None

        self._error("E006", f"Invalid escape sequence: \\{ch}", line, col)
        return None

    def _scan_number(self, start, line, col, first):
        # Check for hex / binary / octal prefix
        if first == "0" and not self._at_end():
            p = self._peek()
            if p in ("x", "X"):
                self._advance()
                return self._scan_hex(start, line, col)
            if p in ("b", "B"):
                self._advance()
                return self._scan_bin(start, line, col)
            if p in ("o", "O"):
                self._advance()
                return self._scan_oct(start, line, col)

        # Decimal
        while not self._at_end() and (self._peek().isdigit() or self._peek() == "_"):
            self._advance()

        is_float = False

        # Float: '.' followed by digit
        if not self._at_end() and self._peek() == "." and not self._at_end():
            # Check if next char after dot is digit (not identifier like .label)
            if self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit():
                is_float = True
                self._advance()  # consume '.'
                while not self._at_end() and (self._peek().isdigit() or self._peek() == "_"):
                    self._advance()

        # Exponent
        if not self._at_end() and self._peek() in ("e", "E"):
            is_float = True
            self._advance()
            if not self._at_end() and self._peek() in ("+", "-"):
                self._advance()
            while not self._at_end() and self._peek().isdigit():
                self._advance()

        # Type suffix
        suffix = self._try_number_suffix()

        raw = self.source[start:self.pos]
        clean = raw.replace("_", "")
        # Remove suffix from clean for parsing
        if suffix:
            clean = clean[:-len(suffix)]

        if is_float or (suffix and suffix.startswith("f")):
            try:
                val = float(clean)
            except ValueError:
                self._error("E004", f"Invalid float literal: {raw}", line, col)
                self._emit(TokenKind.ERROR, raw, line, col)
                return
            self._emit(TokenKind.FLOAT_LIT, raw, line, col, val)
        else:
            try:
                val = int(clean)
            except ValueError:
                self._error("E004", f"Invalid integer literal: {raw}", line, col)
                self._emit(TokenKind.ERROR, raw, line, col)
                return
            self._emit(TokenKind.INT_LIT, raw, line, col, val)

    def _scan_hex(self, start, line, col):
        if self._at_end() or not self._is_hex(self._peek()):
            self._error("E004", "Expected hex digits after 0x", line, col)
            self._emit(TokenKind.ERROR, self.source[start:self.pos], line, col)
            return
        while not self._at_end() and (self._is_hex(self._peek()) or self._peek() == "_"):
            self._advance()
        suffix = self._try_number_suffix()
        raw = self.source[start:self.pos]
        clean = raw.replace("_", "")
        if suffix:
            clean = clean[:-len(suffix)]
        try:
            val = int(clean, 16)
        except ValueError:
            self._error("E004", f"Invalid hex literal: {raw}", line, col)
            self._emit(TokenKind.ERROR, raw, line, col)
            return
        self._emit(TokenKind.INT_LIT, raw, line, col, val)

    def _scan_bin(self, start, line, col):
        if self._at_end() or self._peek() not in ("0", "1"):
            self._error("E004", "Expected binary digits after 0b", line, col)
            self._emit(TokenKind.ERROR, self.source[start:self.pos], line, col)
            return
        while not self._at_end() and (self._peek() in ("0", "1") or self._peek() == "_"):
            self._advance()
        suffix = self._try_number_suffix()
        raw = self.source[start:self.pos]
        clean = raw.replace("_", "")
        if suffix:
            clean = clean[:-len(suffix)]
        try:
            val = int(clean, 2)
        except ValueError:
            self._error("E004", f"Invalid binary literal: {raw}", line, col)
            self._emit(TokenKind.ERROR, raw, line, col)
            return
        self._emit(TokenKind.INT_LIT, raw, line, col, val)

    def _scan_oct(self, start, line, col):
        if self._at_end() or self._peek() not in "01234567":
            self._error("E004", "Expected octal digits after 0o", line, col)
            self._emit(TokenKind.ERROR, self.source[start:self.pos], line, col)
            return
        while not self._at_end() and (self._peek() in "01234567" or self._peek() == "_"):
            self._advance()
        suffix = self._try_number_suffix()
        raw = self.source[start:self.pos]
        clean = raw.replace("_", "")
        if suffix:
            clean = clean[:-len(suffix)]
        try:
            val = int(clean, 8)
        except ValueError:
            self._error("E004", f"Invalid octal literal: {raw}", line, col)
            self._emit(TokenKind.ERROR, raw, line, col)
            return
        self._emit(TokenKind.INT_LIT, raw, line, col, val)

    def _try_number_suffix(self) -> Optional[str]:
        """Try to consume a type suffix like i32, u64, f32, f64."""
        if self._at_end():
            return None
        p = self._peek()
        if p not in ("i", "u", "f"):
            return None
        # Save position in case we need to backtrack
        save_pos = self.pos
        save_line = self.line
        save_col = self.col
        self._advance()  # consume i/u/f
        digits = ""
        while not self._at_end() and self._peek().isdigit():
            digits += self._advance()
        suffix = p + digits
        valid_suffixes = {"i8", "i16", "i32", "i64", "i128", "u8", "u16", "u32", "u64", "u128", "f32", "f64"}
        if suffix in valid_suffixes:
            return suffix
        # Backtrack — wasn't a valid suffix
        self.pos = save_pos
        self.line = save_line
        self.col = save_col
        return None

    def _is_hex(self, ch: str) -> bool:
        return ch in "0123456789abcdefABCDEF"

    def _scan_ident(self, start, line, col, first):
        while not self._at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        raw = self.source[start:self.pos]
        kind = KEYWORDS.get(raw, TokenKind.IDENT)
        self._emit(kind, raw, line, col)

    def _scan_directive(self, start, line, col):
        if self._at_end() or not (self._peek().isalpha() or self._peek() == "_"):
            self._error("E001", "Expected identifier after @", line, col)
            self._emit(TokenKind.ERROR, "@", line, col)
            return
        while not self._at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        raw = self.source[start:self.pos]
        self._emit(TokenKind.DIRECTIVE, raw, line, col)

    def _scan_label(self, start, line, col):
        while not self._at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        # Consume optional trailing colon
        if not self._at_end() and self._peek() == ":":
            self._advance()
        raw = self.source[start:self.pos]
        self._emit(TokenKind.LABEL, raw, line, col)


# ─── Public API ───────────────────────────────────────────────────────────────

def lex(source: str, filename: str = "<stdin>") -> tuple:
    """Tokenize source code. Returns (tokens, diagnostics)."""
    lexer = Lexer(source, filename)
    tokens = lexer.tokenize()
    return tokens, lexer.diagnostics


# ─── Self-test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    test_source = r'''
fn main() -> i32 {
    msg := "Hello, CAT!\n"
    port := 0x3F8
    count := 1_000_000

    i := 0
    .loop:
        ch := msg[i]
        if ch == 0 { jmp .done }
        @outb(port, ch)
        i = i + 1
        jmp .loop

    .done:
        ret 0
}

# A comment
/* block comment /* nested */ end */

type page_entry {
    present:    u1
    writable:   u1
    frame:      u40
}

&c4
fn fast_hook() {
    local x: i32 = 42i32
    local y: f64 = 3.14f64
    local c: u8 = 'A'
}
'''

    tokens, diags = lex(test_source, "test.cat")

    print(f"=== Lexer Output ({len(tokens)} tokens) ===")
    for t in tokens:
        print(f"  {t}")

    if diags:
        print(f"\n=== Diagnostics ({len(diags)}) ===")
        for d in diags:
            print(f"  {d}")
    else:
        print("\n=== No errors ===")

    # Verify critical tokens
    kinds = [t.kind for t in tokens]
    assert TokenKind.FN in kinds, "Missing FN token"
    assert TokenKind.IDENT in kinds, "Missing IDENT token"
    assert TokenKind.STRING_LIT in kinds, "Missing STRING_LIT token"
    assert TokenKind.INT_LIT in kinds, "Missing INT_LIT token"
    assert TokenKind.LABEL in kinds, "Missing LABEL token"
    assert TokenKind.DIRECTIVE in kinds, "Missing DIRECTIVE token"
    assert TokenKind.FLAG in kinds, "Missing FLAG token"
    assert TokenKind.FLOAT_LIT in kinds, "Missing FLOAT_LIT token"
    assert TokenKind.CHAR_LIT in kinds, "Missing CHAR_LIT token"
    assert TokenKind.ARROW in kinds, "Missing ARROW token"
    assert TokenKind.WALRUS in kinds, "Missing WALRUS token"
    assert TokenKind.EOF in kinds, "Missing EOF token"
    assert len(diags) == 0, f"Unexpected diagnostics: {diags}"

    print("\n=== All lexer assertions passed ===")
