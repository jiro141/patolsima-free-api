from .local_filesystem import LocalFileSystemAdapter


def get_default_storage_adapter():
    return LocalFileSystemAdapter()


__all__ = [get_default_storage_adapter]
