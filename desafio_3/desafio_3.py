def cached_property(*dependencies):
    def decorator(func):
        attr_name = f"_cached_{func.__name__}"

        def wrapper(self):
            # Verificar se o cache existe
            if hasattr(self, attr_name):
                cached_value, cached_dependencies = getattr(self, attr_name)
                # Obter valores atuais das dependências
                try:
                    current_dependencies = tuple(getattr(self, dep) for dep in dependencies)
                except AttributeError:
                    # Atributo dependente não existe mais
                    current_dependencies = None
                if cached_dependencies == current_dependencies:
                    return cached_value

            # Computar e armazenar em cache o valor junto com as dependências atuais
            value = func(self)
            try:
                current_dependencies = tuple(getattr(self, dep) for dep in dependencies)
            except AttributeError:
                current_dependencies = None
            setattr(self, attr_name, (value, current_dependencies))
            return value

        return property(wrapper)
    return decorator

class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    @cached_property('x', 'y', 'z')
    def magnitude(self):
        print('computando magnitude')
        return (self.x**2 + self.y**2 + self.z**2)**0.5

