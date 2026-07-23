class LimitsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['limits', 'auth', 'contenttypes', 'sessions', 'admin']:
            return 'sqlite'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['limits', 'auth', 'contenttypes', 'sessions', 'admin']:
            return 'sqlite'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['limits', 'auth', 'contenttypes', 'sessions', 'admin']:
            return db == 'sqlite'
        return db == 'default'