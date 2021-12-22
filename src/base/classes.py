class MixedSerializer:
    
    def get_serializer(self, *args, **kwargs):
        try:
            serializer_class = self.serializer_classes_by_action[self.action]
        except KeyError:
            serializer_class = self.get_serializer_class()
        finally:
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)


class MixedPermissions:

    def get_permissions(self):
        try:
            permission_classes = self.permission_classes_by_action[self.action]
        except KeyError:
            permission_classes = self.permission_classes
        finally:
            return [permission() for permission in permission_classes]
