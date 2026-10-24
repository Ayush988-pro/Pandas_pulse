from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session

from Databases.db import get_db

from dependencies import get_current_user

from Models.user import User
from Models.dataset import Dataset

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(contents)

    dataset = Dataset(
        filename=file.filename,
        file_path=file_location,
        owner_id=current_user.id
    )

    db.add(dataset)

    db.commit()

    db.refresh(dataset)

    return {
        "message": "Upload successful",
        "dataset_id": dataset.id
    }
@router.get("/datasets")
async def get_datasets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    datasets = db.query(Dataset).filter(
        Dataset.owner_id == current_user.id
    ).all()

    return datasets
@router.delete("/datasets/{dataset_id}")
async def delete_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id,
            Dataset.owner_id == current_user.id
        )
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )
    import os

    if dataset.file_path and os.path.exists(dataset.file_path):
        os.remove(dataset.file_path)
    db.delete(dataset)
    db.commit()

    return {
        "message": "Dataset deleted"
    }