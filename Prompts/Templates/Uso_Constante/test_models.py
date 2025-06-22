"""
Testes unitários para os modelos de dados em fotix.core.models.
"""

import pytest
from pydantic import ValidationError
from pathlib import Path
from datetime import datetime

from fotix.core.models import (
    ScanConfig,
    FileMetadata,
    FileRecord,
    DuplicateSet,
    ProcessingStats
)

# Testes para ScanConfig
def test_scan_config_creation():
    """Verifica a criação bem-sucedida de ScanConfig com dados válidos."""
    config = ScanConfig(
        target_paths=[Path("/tmp/photos"), Path("/tmp/other_photos")],
        include_zip_files=True,
        excluded_folders=["cache", ".tmp"]
    )
    assert config.target_paths == [Path("/tmp/photos"), Path("/tmp/other_photos")]
    assert config.include_zip_files is True
    assert config.excluded_folders == ["cache", ".tmp"]

def test_scan_config_missing_fields():
    """Verifica se a validação falha quando campos obrigatórios estão ausentes."""
    with pytest.raises(ValidationError):
        ScanConfig(target_paths=[Path("/tmp")])

# Testes para FileMetadata
def test_file_metadata_creation_full():
    """Verifica a criação de FileMetadata com todos os campos preenchidos."""
    now = datetime.now()
    metadata = FileMetadata(
        resolution=(1920, 1080),
        creation_date=now
    )
    assert metadata.resolution == (1920, 1080)
    assert metadata.creation_date == now

def test_file_metadata_creation_partial():
    """Verifica a criação de FileMetadata com campos opcionais ausentes."""
    metadata = FileMetadata()
    assert metadata.resolution is None
    assert metadata.creation_date is None

# Testes para FileRecord
@pytest.fixture
def sample_file_metadata():
    """Fornece uma instância de FileMetadata para os testes."""
    return FileMetadata(resolution=(800, 600))

def test_file_record_creation(sample_file_metadata):
    """Verifica a criação bem-sucedida de FileRecord."""
    record = FileRecord(
        absolute_path=Path("/tmp/image.jpg"),
        size_bytes=1024,
        file_hash="somehash",
        metadata=sample_file_metadata,
        source_zip_path=Path("/tmp/archive.zip")
    )
    assert record.absolute_path == Path("/tmp/image.jpg")
    assert record.size_bytes == 1024
    assert record.file_hash == "somehash"
    assert record.metadata == sample_file_metadata
    assert record.source_zip_path == Path("/tmp/archive.zip")

def test_file_record_optional_fields_null(sample_file_metadata):
    """Verifica a criação de FileRecord com campos opcionais nulos."""
    record = FileRecord(
        absolute_path=Path("/tmp/image.jpg"),
        size_bytes=1024,
        metadata=sample_file_metadata,
    )
    assert record.file_hash is None
    assert record.source_zip_path is None

def test_file_record_invalid_size(sample_file_metadata):
    """Verifica se a validação falha com um tamanho de arquivo negativo."""
    with pytest.raises(ValidationError):
        FileRecord(
            absolute_path=Path("/tmp/image.jpg"),
            size_bytes=-100,
            metadata=sample_file_metadata,
        )

# Testes para DuplicateSet
@pytest.fixture
def sample_file_records(sample_file_metadata):
    """Fornece uma lista de FileRecord para os testes."""
    return [
        FileRecord(absolute_path=Path("/tmp/img1.jpg"), size_bytes=1024, metadata=sample_file_metadata),
        FileRecord(absolute_path=Path("/tmp/img2.jpg"), size_bytes=1024, metadata=sample_file_metadata)
    ]

def test_duplicate_set_creation(sample_file_records):
    """Verifica a criação bem-sucedida de DuplicateSet."""
    keeper_record = sample_file_records[0]
    dup_set = DuplicateSet(
        file_hash="commonhash",
        files=sample_file_records,
        keeper=keeper_record,
        to_delete=[sample_file_records[1]]
    )
    assert dup_set.file_hash == "commonhash"
    assert dup_set.files == sample_file_records
    assert dup_set.keeper == keeper_record
    assert dup_set.to_delete == [sample_file_records[1]]

def test_duplicate_set_default_to_delete(sample_file_records):
    """Verifica se o campo 'to_delete' tem o valor padrão correto (lista vazia)."""
    dup_set = DuplicateSet(
        file_hash="commonhash",
        files=sample_file_records,
    )
    assert dup_set.to_delete == []

# Testes para ProcessingStats
def test_processing_stats_creation():
    """Verifica a criação bem-sucedida de ProcessingStats."""
    stats = ProcessingStats(
        total_files_scanned=1000,
        total_duplicates_found=50,
        space_to_be_saved_bytes=512000,
        processing_time_seconds=123.45
    )
    assert stats.total_files_scanned == 1000
    assert stats.total_duplicates_found == 50
    assert stats.space_to_be_saved_bytes == 512000
    assert stats.processing_time_seconds == 123.45

def test_processing_stats_invalid_values():
    """Verifica se a validação falha com valores numéricos negativos."""
    with pytest.raises(ValidationError):
        ProcessingStats(
            total_files_scanned=-1,
            total_duplicates_found=50,
            space_to_be_saved_bytes=512000,
            processing_time_seconds=123.45
        )
    with pytest.raises(ValidationError):
        ProcessingStats(
            total_files_scanned=1000,
            total_duplicates_found=50,
            space_to_be_saved_bytes=512000,
            processing_time_seconds=-1.0
        )
