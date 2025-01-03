from fastapi import HTTPException, status


class CustomHTTPException:
    @staticmethod
    def credentials_exception():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def permission_exception():
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não possui permissão para acessar este recurso"
        )

    @staticmethod
    def not_found_exception(resource: str):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} não encontrado"
        )