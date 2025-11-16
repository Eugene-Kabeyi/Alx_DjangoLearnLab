# LibraryProject 📚

# Permission and Group System — advanced_features_and_security

## Custom Permissions

The `Document` model defines the following permissions:

- `can_view` – view documents
- `can_create` – create documents
- `can_edit` – edit documents
- `can_delete` – delete documents

## Groups

Three groups are defined and should be created in Django Admin:

### Viewers

Permissions:

- can_view

### Editors

Permissions:

- can_view
- can_create
- can_edit

### Admins

Permissions:

- ALL permissions (view/create/edit/delete)

## Views

Each view is protected using `@permission_required`.

Example:

```python
@permission_required('secure_app.can_edit', raise_exception=True)
def edit_document(request):
    ...
```
