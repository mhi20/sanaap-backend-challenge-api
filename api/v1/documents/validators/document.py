from django.core.exceptions import ValidationError

def validate_document_file_size(file):
    limit_mb = 10

    if file.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"File size cannot exceed {limit_mb} MB.")