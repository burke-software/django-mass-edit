from django.db import models
        
class RightsSupport(models.Model):
            
    class Meta:
        
        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model. 
                
        default_permissions = () # disable "add", "change", "delete"
                                 # and "view" default permissions

        permissions = ( 
            ('can_mass_edit', 'Can perform mass editing'),  
        )