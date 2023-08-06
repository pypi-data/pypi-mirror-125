from django.apps import AppConfig

MODULE_NAME = "location"

DEFAULT_CFG = {
    "location_types": ['R', 'D', 'W', 'V'],
    "gql_query_locations_perms": ["121901"],
    "gql_query_health_facilities_perms": ["121101"],
    "gql_mutation_create_locations_perms": ["121902"],
    "gql_mutation_edit_locations_perms": ["121903"],
    "gql_mutation_delete_locations_perms": ["121904"],
    "gql_mutation_move_location_perms": ["121905"],
    "gql_mutation_create_health_facilities_perms": ["121102"],
    "gql_mutation_edit_health_facilities_perms": ["121103"],
    "gql_mutation_delete_health_facilities_perms": ["121104"],
}


class LocationConfig(AppConfig):
    name = MODULE_NAME

    location_types = []
    gql_query_locations_perms = []
    gql_query_health_facilities_perms = []
    gql_mutation_create_locations_perms = []
    gql_mutation_edit_locations_perms = []
    gql_mutation_delete_locations_perms = []
    gql_mutation_move_location_perms = []
    gql_mutation_create_health_facilities_perms = []
    gql_mutation_edit_health_facilities_perms = []
    gql_mutation_delete_health_facilities_perms = []

    def _configure_permissions(self, cfg):
        LocationConfig.location_types = cfg[
            "location_types"]
        LocationConfig.gql_query_locations_perms = cfg[
            "gql_query_locations_perms"]
        LocationConfig.gql_query_health_facilities_perms = cfg[
            "gql_query_health_facilities_perms"]
        LocationConfig.gql_mutation_create_locations_perms = cfg[
            "gql_mutation_create_locations_perms"
        ]
        LocationConfig.gql_mutation_edit_locations_perms = cfg[
            "gql_mutation_edit_locations_perms"
        ]
        LocationConfig.gql_mutation_delete_locations_perms = cfg[
            "gql_mutation_delete_locations_perms"
        ]
        LocationConfig.gql_mutation_move_location_perms = cfg[
            "gql_mutation_move_location_perms"
        ]
        LocationConfig.gql_mutation_create_health_facilities_perms = cfg[
            "gql_query_health_facilities_perms"
        ]
        LocationConfig.gql_mutation_edit_health_facilities_perms = cfg[
            "gql_query_health_facilities_perms"
        ]
        LocationConfig.gql_mutation_delete_health_facilities_perms = cfg[
            "gql_query_health_facilities_perms"
        ]

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)
