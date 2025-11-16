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

# Security hardening — notes

This document lists applied security settings and how to test them.

## Key settings (in settings.py)

- DEBUG controlled by `DJANGO_DEBUG` env var (default False)
- SECURE_BROWSER_XSS_FILTER = True
- X_FRAME_OPTIONS = "DENY"
- SECURE_CONTENT_TYPE_NOSNIFF = True
- CSRF_COOKIE_SECURE = True
- SESSION_COOKIE_SECURE = True
- SECURE_SSL_REDIRECT = True
- django-csp is used to provide CSP headers. See settings for `CSP_*` configuration.

## Templates / Forms

All POST forms must include `{% csrf_token %}`.

## Views / DB

- Use Django Form / ModelForm to validate inputs.
- Use ORM filters (e.g., `filter(title__icontains=q)`) — avoid raw SQL.

## CSP

- Using django-csp. Config in `settings.py`.

## Testing

1. Validate 403 on missing CSRF token.
2. Inspect headers for X-Frame-Options, X-Content-Type-Options, Content-Security-Policy.
3. Test group/permission restricted pages while logged in as different user roles.
