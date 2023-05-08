from .local_filesystem import LocalFileSystemStorageAdapter


def get_default_storage_adapter():
    return LocalFileSystemStorageAdapter()


__all__ = [get_default_storage_adapter]
