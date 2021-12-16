from massadmin.massadmin import MassAdmin


class MockRenderMassAdmin(MassAdmin):
    def render_mass_change_form(
            self,
            request,
            context,
            add=False,
            change=False,
            form_url='',
            obj=None):
        return {
            'request': request,
            'context': context,
            'add': add,
            'change': change,
            'form_url': form_url,
            'obj': obj,
        }
