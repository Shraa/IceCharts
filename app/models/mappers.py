# -*- coding: utf-8 -*-

grid_mapper = {
    'settings': {
        'number_of_shards': 3,
        'number_of_replicas': 2,
        'analysis': {
            'filter': {
                'autocomplete_filter': {
                    'type': 'edge_ngram',
                    'min_gram': 1,
                    'max_gram': 20
                }
            },
            'analyzer': {
                'autocomplete': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'autocomplete_filter'
                    ]
                }
            }
        }
    },
    'mappings': {
        'grid': {
            'properties': {
                'id': {
                    'type': 'string',
                    'analyzer': 'autocomplete',
                    'search_analyzer': 'standard'
                },
                'name': {
                    'type': 'string',
                    'analyzer': 'autocomplete',
                    'search_analyzer': 'standard'
                },
                'description': {
                    'type': 'text',
                    'index': 'no'
                }
            }
        }
    }
}


cell_mapper = {
    'settings': {
        'number_of_shards': 3,
        'number_of_replicas': 2,
        'analysis': {
            'filter': {
                'autocomplete_filter': {
                    'type': 'edge_ngram',
                    'min_gram': 1,
                    'max_gram': 20
                }
            },
            'analyzer': {
                'autocomplete': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'autocomplete_filter'
                    ]
                }
            }
        }
    },
    'mappings': {
        'cell': {
            'properties': {
                'id': {
                    'type': 'string',
                    'analyzer': 'autocomplete',
                    'search_analyzer': 'standard'
                },
                'grid_id': {
                    'type': 'string',
                    'analyzer': 'autocomplete',
                    'search_analyzer': 'standard'
                },
                'name': {
                    'type': 'string',
                    'analyzer': 'autocomplete',
                    'search_analyzer': 'standard'
                },
                'description': {
                    'type': 'text',
                    'index': 'no'
                }
            }
        }
    }
}
