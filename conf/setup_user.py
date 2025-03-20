def setup_project_user(user):
    """
    Configure les permissions des utilisateurs Django via YunoHost SSO.
    Seuls les admins YunoHost auront les droits super-utilisateur.
    """

    # Vérifier si l'utilisateur appartient au groupe 'admins' de YunoHost
    from django_yunohost_integration.sso_auth import is_admin

    if is_admin(user.username):
        user.is_staff = True
        user.is_superuser = True  # Donne tous les droits si utilisateur YunoHost Admin
    else:
        user.is_staff = True  # Permet d'accéder à l'interface Django Admin sans être superuser
        user.is_superuser = False

    user.save()
    return user
