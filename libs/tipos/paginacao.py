from dataclasses import dataclass


@dataclass
class Paginacao:
    page: int = 1
    page_size: int = 10

    def offset(self) -> int:
        return (self.page - 1) * self.page_size
