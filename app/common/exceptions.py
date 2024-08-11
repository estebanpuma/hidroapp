class InvalidFileDate(Exception):
    """Excepción lanzada cuando la fecha no es válida."""
    def __init__(self, filename, message="Fecha no permitidaa"):
        self.filename = filename
        self.message = f"{message}: {filename}"
        super().__init__(self.message)