import uuid
from pathlib import Path

from beanie import PydanticObjectId
from fastapi import File, UploadFile

from src.config.config import config
from src.model.document import DocumentStatus, UploadedDocument


class DocumentService:
    @staticmethod
    async def validate_pdf(file: UploadFile):

        # 1. Validate filename and extension
        if not file.filename:
            raise ValueError("Filename is missing")

        if Path(file.filename).suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are allowed")

        # 2. Validate PDF signature
        try:
            header = await file.read(5)

            if header != b"%PDF-":
                raise ValueError("Invalid PDF file")

            # 3. Validate file size
            total_size = len(header)

            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)

                if total_size > config.MAX_FILE_SIZE:
                    raise ValueError("File size exceeds 10 MB")

            if total_size == 5:
                raise ValueError("Uploaded file is empty")

        finally:
            # Reset file pointer for subsequent operations
            await file.seek(0)

    @staticmethod
    async def save_pdf(file: UploadFile) -> tuple[Path, int]:

        # 1. Validate the uploaded PDF
        file_size = await DocumentService.validate_pdf(file)

        # 2. Create upload directory
        upload_dir = Path("storage/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)

        # 3. Generate unique filename
        stored_filename = f"{uuid.uuid4().hex}.pdf"

        file_path = upload_dir / stored_filename
        temp_path = upload_dir / f".{stored_filename}.tmp"

        try:
            # 4. Write PDF to temporary file
            with temp_path.open("wb") as destination:
                while chunk := await file.read(1024 * 1024):
                    destination.write(chunk)

            # 5. Move to final destination
            temp_path.replace(file_path)

        except Exception:
            temp_path.unlink(missing_ok=True)
            raise

        finally:
            await file.seek(0)

        return file_path, file_size

    @staticmethod
    async def create_document_record(
        user_id: PydanticObjectId, filename: str, file_path: str
    ):
        document = UploadedDocument(
            user_id=user_id,
            filename=filename,
            file_path=str(file_path),
            status=DocumentStatus.UPLOADED,
        )

        await document.insert()

        return document

    from pathlib import Path

    @staticmethod
    async def upload_document(file: UploadFile, user_id: PydanticObjectId):
        file_path: Path | None = None

        try:
            # 1. Save and validate the PDF
            file_path, file_size = await DocumentService.save_pdf(file)

            # 2. Validate filename type
            filename = file.filename

            if filename is None:
                raise ValueError("Filename is missing")

            # 3. Create MongoDB record
            document = await DocumentService.create_document_record(
                user_id=user_id, filename=filename, file_path=str(file_path)
            )

            return document

        except Exception:
            # 4. Cleanup if something fails
            if file_path and file_path.exists():
                file_path.unlink()

            raise
