import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class TestingresourceschemaPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'testingresourceschema')
    
    # IDatasetForm
    # Adds custom metadata to resources
    def _modify_package_schema(self, schema):
        schema['resources'].update({
            'testing_custom_field': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ],
        })

        return schema
 
    def create_package_schema(self):
        schema = super(TestingresourceschemaPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(TestingresourceschemaPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(TestingresourceschemaPlugin, self).show_package_schema()

        schema['resources'].update({
            'testing_custom_field': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_from_extras')
            ]
        })

        return schema

    # necessary for schema modification
    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    # necessary for schema modification
    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
