"""Exceções do cliente Receita Federal."""

from typing import Optional


class ReceitaFederalError(Exception):
    """Exceção base para erros da API da Receita Federal."""

    def __init__(
        self,
        message: str,
        codigo: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.codigo = codigo
        self.status_code = status_code

    def __str__(self) -> str:
        if self.codigo:
            return f"[{self.codigo}] {self.message}"
        return self.message

    def __repr__(self) -> str:
        return (
            f"ReceitaFederalError(message={self.message!r}, "
            f"codigo={self.codigo!r}, status_code={self.status_code!r})"
        )
