"""
Módulo central que define os modelos de dados (entidades) da aplicação.

Este módulo é a Fonte Única da Verdade (Single Source of Truth - SSOT) para todas
as estruturas de dados canônicas utilizadas no Fotix. Utiliza Pydantic para
validação, tipagem e serialização, garantindo a integridade dos dados que fluem
pelo sistema.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from pydantic import BaseModel, Field


class ScanConfig(BaseModel):
    """Configurações para uma operação de escaneamento de diretórios."""

    target_paths: list[Path] = Field(
        ...,
        description="Lista de caminhos de diretório ou arquivos para escanear."
    )
    include_zip_files: bool = Field(
        ...,
        description="Se verdadeiro, escaneia o conteúdo de arquivos .zip."
    )
    excluded_folders: list[str] = Field(
        ...,
        description="Lista de nomes de pastas a serem ignoradas durante o escaneamento."
    )


class FileMetadata(BaseModel):
    """Metadados extraídos de um arquivo de mídia."""

    resolution: Optional[Tuple[int, int]] = Field(
        None,
        description="Resolução da imagem ou vídeo (largura, altura)."
    )
    creation_date: Optional[datetime] = Field(
        None,
        description="Data de criação do arquivo de mídia, extraída dos metadados EXIF/etc."
    )


class FileRecord(BaseModel):
    """Representação canônica de um arquivo processado pelo sistema."""

    absolute_path: Path = Field(
        ...,
        description="Caminho absoluto para o arquivo no sistema de arquivos."
    )
    size_bytes: int = Field(
        ...,
        ge=0,
        description="Tamanho do arquivo em bytes."
    )
    file_hash: Optional[str] = Field(
        None,
        description="Hash criptográfico (BLAKE3) do conteúdo do arquivo."
    )
    metadata: FileMetadata = Field(
        ...,
        description="Metadados de mídia extraídos do arquivo."
    )
    source_zip_path: Optional[Path] = Field(
        None,
        description="Se o arquivo foi extraído de um ZIP, este é o caminho para o arquivo ZIP de origem."
    )


class DuplicateSet(BaseModel):
    """Representa um conjunto de arquivos que são cópias idênticas uns dos outros."""

    file_hash: str = Field(
        ...,
        description="O hash compartilhado por todos os arquivos neste conjunto."
    )
    files: list[FileRecord] = Field(
        ...,
        description="A lista de registros de arquivos que são duplicatas."
    )
    keeper: Optional[FileRecord] = Field(
        None,
        description="O arquivo que foi selecionado para ser mantido, com base na estratégia de seleção."
    )
    to_delete: list[FileRecord] = Field(
        default_factory=list,
        description="A lista de arquivos a serem excluídos (todos exceto o 'keeper')."
    )


class ProcessingStats(BaseModel):
    """Estatísticas sobre uma operação de processamento concluída."""

    total_files_scanned: int = Field(
        ...,
        ge=0,
        description="Número total de arquivos analisados no sistema de arquivos."
    )
    total_duplicates_found: int = Field(
        ...,
        ge=0,
        description="Número total de arquivos individuais identificados como duplicatas."
    )
    space_to_be_saved_bytes: int = Field(
        ...,
        ge=0,
        description="Espaço em disco (em bytes) que será liberado após a exclusão das duplicatas."
    )
    processing_time_seconds: float = Field(
        ...,
        ge=0.0,
        description="Tempo total gasto na operação de escaneamento e análise, em segundos."
    )
